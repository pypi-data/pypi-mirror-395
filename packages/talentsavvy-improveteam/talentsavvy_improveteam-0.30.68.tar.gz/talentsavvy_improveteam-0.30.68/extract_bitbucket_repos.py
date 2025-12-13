#!/usr/bin/env python3
"""
Bitbucket Repos Data Extraction Script

This script extracts code events from Bitbucket repositories and saves them to the database.

Usage:
    python extract_bitbucket_repos.py -p <product_name> [-s <start_date>]

Arguments:
    -p, --product: Product name (if provided, saves to database; otherwise saves to CSV)
    -s, --start-date: Start date for extraction in YYYY-MM-DD format (optional)

Modes (automatically determined):
    Fast mode (when -s is provided OR when no last_modified exists):
        - Used for initial bulk extraction with explicit start date
        - Extracts basic events from standard APIs
        - Pull Request Created/Approved/Merged from /pullrequests/activity
        - Code Committed events from /commits (without target_branch)
        - Tag Created events from refs/tags
        - Early termination when possible (sorted by date descending)
        - Faster extraction with optimized pagination

    Enriched mode (when -s is NOT provided AND last_modified exists):
        - Used for incremental updates with enriched data
        - Code Committed events fetched from /pullrequests/{pr_id}/commits
        - Commits include accurate target_branch (PR source branch)
        - Merge commits are excluded
        - More complete and accurate commit information

Events extracted:
    - Pull Request Created
    - Pull Request Approved
    - Pull Request Merged
    - Code Committed (with parent_ids in extended_attributes)
    - Tag Created

Extended Attributes:
    - Pull Request events: pull_request_number, pull_request_title
    - Code Committed: parent_ids (list of parent commit SHAs)

Optimization Features:
    - Pull Requests: Sorted by -created_on with early termination
    - Commits: Early termination when all commits are older than start_date
    - Activity filtering: Skips old activities during processing
    - Tags: Sorted by -name for recent versions first
"""

import argparse
import json
import logging
import os
import re
import sys
import time
from datetime import datetime, timezone
from typing import List, Dict, Optional
from urllib.parse import quote

base_dir = os.path.dirname(os.path.abspath(__file__))
common_dir = os.path.join(base_dir, "common")
if not os.path.isdir(common_dir):
    # go up one level to find "common" (for installed package structure)
    base_dir = os.path.dirname(base_dir)
    common_dir = os.path.join(base_dir, "common")

if os.path.isdir(common_dir) and base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import requests

from common.code_commit_event import CodeCommitEvent
from common.utils import Utils

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('extract_bitbucket_repos')

# Set logger for CodeCommitEvent
CodeCommitEvent.LOGGER = logger

class BitbucketReposExtractor:
    """Extracts code events from Bitbucket repositories with extended_attributes support."""
    
    def __init__(self):
        # Track extracted commits in memory (for enriched mode)
        self.extracted_commits = set()
        
        # Statistics
        self.stats = {
            'pr_created': 0,
            'pr_approved': 0,
            'pr_merged': 0,
            'code_committed': 0,
            'tag_created': 0,
            'total_inserted': 0,
            'total_duplicates': 0
        }
        
    def get_config_from_database(self, cursor) -> Dict:
        """Get Bitbucket configuration from data_source_config table."""
        query = """
        SELECT config_item, config_value
        FROM data_source_config
        WHERE data_source = 'source_code_revision_control'
        AND config_item IN ('Workspace', 'Repos', 'Personal Access Token')
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        config = {}
        for config_item, config_value in results:
            if config_item == 'Repos':
                try:
                    repos = json.loads(config_value) if config_value else []
                    config['repos'] = repos if repos else []
                except (json.JSONDecodeError, TypeError):
                    # Fall back to comma-separated string
                    config['repos'] = [r.strip() for r in config_value.split(',') if r.strip()] if config_value else []
            elif config_item == 'Workspace':
                config['workspace'] = config_value
            elif config_item == 'Personal Access Token':
                config['api_token'] = config_value
                
        return config
    
    def get_last_modified_date(self, cursor) -> Optional[datetime]:
        """Get the last modified date from the database."""
        last_modified = CodeCommitEvent.get_last_event(cursor)
        if last_modified:
            # Convert to naive datetime if timezone-aware
            if last_modified.tzinfo is not None:
                last_modified = last_modified.replace(tzinfo=None)
        return last_modified
    
    def _make_api_request(self, url: str, headers: Dict, params: Dict = None) -> Optional[Dict]:
        """
        Make an API request to Bitbucket with retry logic.
        
        Args:
            url: Full API URL
            headers: Request headers
            params: Query parameters
            
        Returns:
            Response JSON as dict, or None if request fails
        """
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers, params=params, timeout=30)
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 429:
                    # Rate limit exceeded
                    retry_after = response.headers.get('Retry-After', '60')
                    wait_time = int(retry_after) + 10
                    logger.warning(f"Rate limit exceeded. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.warning(f"API request failed: {response.status_code} - {response.text}")
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay * (2 ** attempt))
                        continue
                    break
                    
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request failed (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (2 ** attempt))
                    continue
                break
        
        return None
    
    def _is_merge_commit(self, commit_message: str) -> bool:
        """
        Check if a commit message indicates a merge commit.
        
        Args:
            commit_message: Commit message
            
        Returns:
            True if this is a merge commit, False otherwise
        """
        if not commit_message:
            return False
        
        # Bitbucket merge patterns
        merge_patterns = [
            r"^[Mm]erged in .+ from .+",
            r"^[Mm]erge pull request #\d+",
            r"^[Mm]erge branch .+ into .+",
        ]
        
        for pattern in merge_patterns:
            if re.match(pattern, commit_message):
                return True
        
        return False
    
    # ============================================================================
    # EXTRACTION METHODS (FAST MODE)
    # ============================================================================
    
    def process_repositories(
        self, 
        workspace: str, 
        repos: List[str], 
        headers: Dict, 
        start_date: datetime,
        is_enriched_mode: bool = False
    ) -> List[Dict]:
        """
        Process all repositories using fast or enriched mode extraction logic.
        
        Args:
            workspace: Bitbucket workspace ID
            repos: List of repository names
            headers: Request headers with auth token
            start_date: Start date for extraction
            is_enriched_mode: Whether to use enriched mode
            
        Returns:
            List of all extracted events
        """
        all_events = []
        
        for repo_name in repos:
            logger.info(f"Processing repository: {repo_name}")
            
            try:
                # 1. Pull Request Created events (from /pullrequests API)
                pr_created_events = self.fetch_pull_requests(workspace, repo_name, headers, start_date)
                all_events.extend(pr_created_events)
                
                # 2. Pull Request Approved/Merged events (from /pullrequests/activity API)
                pr_activity_events = self.fetch_pull_request_activity(workspace, repo_name, headers, start_date)
                all_events.extend(pr_activity_events)
                
                # 3. Code Committed events
                if is_enriched_mode:
                    # Enriched mode: Get commits from PRs with target_branch
                    logger.info(f"[Enriched Mode] Fetching commits from PRs for '{repo_name}'")
                    # First, fetch PR details for enrichment (only needed in enriched mode)
                    pr_details = self._fetch_pull_request_details_for_enrichment(workspace, repo_name, headers, start_date)
                    enriched_commits = self.enrich_pr_with_commits(workspace, repo_name, headers, pr_details)
                    if enriched_commits:
                        logger.info(f"[Enriched Mode] Added {len(enriched_commits)} enriched commits for '{repo_name}'")
                        all_events.extend(enriched_commits)
                else:
                    # Fast mode: Get commits from commits endpoint (no target_branch)
                    commit_events = self.fetch_commits(workspace, repo_name, headers, start_date)
                    all_events.extend(commit_events)
                
                # 4. Tag Created events
                tag_events = self.fetch_tags(workspace, repo_name, headers)
                all_events.extend(tag_events)
                    
            except Exception as e:
                logger.error(f"Error processing repository {repo_name}: {e}")
                continue
                
        return all_events
    
    def fetch_pull_request_activity(
        self, 
        workspace: str, 
        repo_name: str, 
        headers: Dict, 
        start_date: datetime
    ) -> List[Dict]:
        """
        Fetch pull request activity and extract PR Approved/Merged events from activity API.
        
        Extracts:
        - Pull Request Approved (with PR number only - details filled by update_code_commit_event.py)
        - Pull Request Merged (with all details from update.source/destination)
        
        Note: PR Created events are extracted from /pullrequests API instead.
        
        API: /repositories/{workspace}/{repo_slug}/pullrequests/activity
        """
        url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{quote(repo_name)}/pullrequests/activity"
        params = {
            'pagelen': 50
            # Note: Activity endpoint doesn't support sorting, so we process all pages
        }
        
        events = []
        page = 1
        start_date_naive = start_date if not start_date.tzinfo else start_date.replace(tzinfo=None)
        
        while True:
            logger.info(f"[PR Activity] Fetching page {page} for repo '{repo_name}'...")
            
            data = self._make_api_request(url, headers, params)
            if not data or not isinstance(data, dict):
                break
            
            activities = data.get('values', [])
            if not activities:
                break
            
            for activity in activities:
                # Check activity timestamp before processing
                timestamp = None
                if 'update' in activity:
                    timestamp = Utils.convert_to_utc(activity.get('update', {}).get('date'))
                elif 'approval' in activity:
                    timestamp = Utils.convert_to_utc(activity.get('approval', {}).get('date'))
                
                if timestamp and timestamp >= start_date_naive:
                    activity_events = self._extract_pr_activity_events(activity, repo_name, start_date)
                    events.extend(activity_events)
            
            logger.info(f"[PR Activity] Page {page}: Processed {len(activities)} activities")
            
            # Check for next page
            next_url = data.get('next')
            if not next_url:
                break
            
            url = next_url
            params = None  # Next URL already has params
            page += 1
        
        logger.info(f"[PR Activity] Fetched {len(events)} PR events for '{repo_name}'")
        logger.info(f"[PR Activity] Completed processing pull request activity for repo '{repo_name}'")
        return events
    
    def _fetch_pull_request_details_for_enrichment(
        self, 
        workspace: str, 
        repo_name: str, 
        headers: Dict, 
        start_date: datetime
    ) -> Dict[int, Dict]:
        """
        Fetch pull request details for enriched mode commit extraction.
        Only called in enriched mode to get PR details for /pullrequests/{pr_id}/commits API.
        Uses descending sort order with early termination for efficiency.
        
        Returns:
            Dictionary mapping PR ID to PR details
        """
        url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{quote(repo_name)}/pullrequests"
        params = {
            'state': 'MERGED,OPEN,DECLINED,SUPERSEDED',
            'pagelen': 50,
            'sort': '-created_on'  # Sort by creation date descending
        }
        
        pr_details = {}
        page = 1
        start_date_naive = start_date if not start_date.tzinfo else start_date.replace(tzinfo=None)
        
        while True:
            logger.info(f"[PR Details for Enrichment] Fetching page {page} for repo '{repo_name}'...")
            
            data = self._make_api_request(url, headers, params)
            if not data or not isinstance(data, dict):
                break
            
            prs = data.get('values', [])
            if not prs:
                break
            
            # Track if any PRs on this page are recent enough
            has_recent_pr = False
            
            for pr in prs:
                pr_id = pr.get('id')
                if pr_id:
                    # Check if PR is recent enough
                    created_on = Utils.convert_to_utc(pr.get('created_on'))
                    if created_on and created_on >= start_date_naive:
                        pr_details[pr_id] = pr
                        has_recent_pr = True
                    elif not created_on:
                        # If no created_on, include it to be safe
                        pr_details[pr_id] = pr
                        has_recent_pr = True
            
            logger.info(f"[PR Details for Enrichment] Page {page}: Fetched {len(prs)} pull requests ({len([p for p in prs if Utils.convert_to_utc(p.get('created_on', '')) and Utils.convert_to_utc(p.get('created_on', '')) >= start_date_naive])} recent)")
            
            # Early termination: if no recent PRs on this page, stop
            if not has_recent_pr:
                logger.info(f"[PR Details for Enrichment] Stopping at page {page} - all PRs are older than start_date")
                break
            
            # Check for next page
            next_url = data.get('next')
            if not next_url:
                break
            
            url = next_url
            params = None
            page += 1
        
        logger.info(f"[PR Details for Enrichment] Fetched details for {len(pr_details)} pull requests")
        return pr_details
    
    def fetch_pull_requests(
        self, 
        workspace: str, 
        repo_name: str, 
        headers: Dict, 
        start_date: datetime
    ) -> List[Dict]:
        """
        Fetch pull requests and create PR Created events.
        
        API: /repositories/{workspace}/{repo_slug}/pullrequests
        
        This extracts PR Created events with full details.
        """
        url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{quote(repo_name)}/pullrequests"
        params = {
            'state': 'MERGED,OPEN,DECLINED,SUPERSEDED',
            'pagelen': 50,
            'sort': '-created_on'  # Sort by creation date descending
        }
        
        events = []
        page = 1
        start_date_naive = start_date if not start_date.tzinfo else start_date.replace(tzinfo=None)
        
        while True:
            logger.info(f"[Pull Requests] Fetching page {page} for repo '{repo_name}'...")
            
            data = self._make_api_request(url, headers, params)
            if not data or not isinstance(data, dict):
                break
            
            prs = data.get('values', [])
            if not prs:
                break
            
            # Track if any PRs on this page are recent enough
            has_recent_pr = False
            
            for pr in prs:
                pr_id = pr.get('id')
                if not pr_id:
                    continue
                
                # Get PR details
                created_on = Utils.convert_to_utc(pr.get('created_on'))
                if not created_on:
                    continue
                
                # Check if PR is recent enough
                if created_on < start_date_naive:
                    continue
                
                has_recent_pr = True
                
                # Extract PR details
                title = pr.get('title', '')
                description = pr.get('description', '')
                author_info = pr.get('author', {})
                author = author_info.get('display_name', author_info.get('nickname', ''))
                
                # Extract source and destination
                source = pr.get('source', {})
                destination = pr.get('destination', {})
                
                source_branch = source.get('branch', {}).get('name', '')
                source_commit = source.get('commit', {}).get('hash', '')
                target_branch = destination.get('branch', {}).get('name', '')
                
                # Extended attributes
                extended_attrs = {
                    'pull_request_number': pr_id,
                    'pull_request_title': title
                }
                
                # Create PR Created event
                events.append(CodeCommitEvent.create_event(
                    timestamp_utc=created_on,
                    repo_name=repo_name,
                    event_type='Pull Request Created',
                    source_branch=source_branch,
                    target_branch=target_branch,
                    revision=source_commit,
                    author=author,
                    comment=description if description else title,
                    extended_attributes=extended_attrs
                ))
                self.stats['pr_created'] += 1
            
            logger.info(f"[Pull Requests] Page {page}: Fetched {len(prs)} pull requests ({len([e for e in events if e])} PR Created events)")
            
            # Early termination: if no recent PRs on this page, stop
            if not has_recent_pr:
                logger.info(f"[Pull Requests] Stopping at page {page} - all PRs are older than start_date")
                break
            
            # Check for next page
            next_url = data.get('next')
            if not next_url:
                break
            
            url = next_url
            params = None
            page += 1
        
        logger.info(f"[Pull Requests] Fetched {len(events)} PR Created events for '{repo_name}'")
        return events
    
    def _extract_pr_activity_events(
        self, 
        activity: Dict, 
        repo_name: str,
        start_date: datetime
    ) -> List[Dict]:
        """
        Extract PR events from a pull request activity entry.
        All data extracted directly from the activity object.
        
        Activity types:
        - approval: PR Approved (has PR number only, details filled later by update_code_commit_event.py)
        - update with state MERGED: PR Merged (has source/destination)
        
        Note: PR Created events are now extracted from /pullrequests API instead.
        """
        events = []
        start_date_naive = start_date if not start_date.tzinfo else start_date.replace(tzinfo=None)
        
        # Get PR ID and title from pull_request object (present in all activities)
        pr = activity.get('pull_request', {})
        if not pr:
            return events
        
        pr_id = pr.get('id')
        pr_title = pr.get('title', '')
        
        if not pr_id:
            return events
        
        # Extended attributes for PR events
        extended_attrs = {
            'pull_request_number': pr_id,
            'pull_request_title': pr_title
        }
        
        # Handle UPDATE activities (PR Created / PR Merged)
        if 'update' in activity:
            update = activity.get('update', {})
            activity_type = update.get('state')
            timestamp = Utils.convert_to_utc(update.get('date'))
            
            if not timestamp or timestamp < start_date_naive:
                return events
            
            # Extract details from update object
            title = update.get('title', pr_title)
            description = update.get('description', '')
            author_info = update.get('author', {})
            author = author_info.get('display_name', author_info.get('nickname', ''))
            
            # Extract source and destination details
            source = update.get('source', {})
            destination = update.get('destination', {})
            
            source_branch = source.get('branch', {}).get('name', '')
            source_commit = source.get('commit', {}).get('hash', '')
            target_branch = destination.get('branch', {}).get('name', '')
            destination_commit = destination.get('commit', {}).get('hash', '')
            
            # PR Merged event (when state is MERGED)
            if activity_type == 'MERGED':
                # For merged PR, use destination commit (the merge result on target branch)
                events.append(CodeCommitEvent.create_event(
                    timestamp_utc=timestamp,
                    repo_name=repo_name,
                    event_type='Pull Request Merged',
                    source_branch=source_branch,
                    target_branch=target_branch,
                    revision=destination_commit,
                    author=author,
                    comment=title,
                    extended_attributes=extended_attrs
                ))
                self.stats['pr_merged'] += 1
        
        # Handle APPROVAL activities (PR Approved)
        if 'approval' in activity:
            approval = activity.get('approval', {})
            timestamp = Utils.convert_to_utc(approval.get('date'))
            
            if not timestamp or timestamp < start_date_naive:
                return events
            
            approver_info = approval.get('user', {})
            approver = approver_info.get('display_name', approver_info.get('nickname', ''))
            
            # PR Approved: Only store PR number and title
            # source_branch, target_branch, and revision will be filled by update_code_commit_event.py
            events.append(CodeCommitEvent.create_event(
                timestamp_utc=timestamp,
                repo_name=repo_name,
                event_type='Pull Request Approved',
                source_branch='',  # Will be filled by update_code_commit_event.py
                target_branch='',  # Will be filled by update_code_commit_event.py
                revision='',       # Will be filled by update_code_commit_event.py
                author=approver,
                comment=pr_title,
                extended_attributes=extended_attrs
            ))
            self.stats['pr_approved'] += 1
        
        return events
    
    def fetch_commits(
        self, 
        workspace: str, 
        repo_name: str, 
        headers: Dict, 
        start_date: datetime
    ) -> List[Dict]:
        """
        Fetch commits with parent_ids in extended_attributes.
        Uses descending sort order with early termination for efficiency.
        
        API: /repositories/{workspace}/{repo_slug}/commits
        
        Excludes merge commits and stores parent commit SHAs.
        """
        url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{quote(repo_name)}/commits"
        params = {
            'pagelen': 50
            # Note: Commits endpoint doesn't reliably support date sorting
            # Will need to fetch all commits and filter
        }
        
        events = []
        page = 1
        start_date_naive = start_date if not start_date.tzinfo else start_date.replace(tzinfo=None)
        
        while True:
            logger.info(f"[Commit] Fetching page {page} for repo '{repo_name}'...")
            
            data = self._make_api_request(url, headers, params)
            if not data or not isinstance(data, dict):
                break
            
            commits = data.get('values', [])
            if not commits:
                break
            
            # Track if any commits on this page are recent enough
            has_recent_commits = False
            page_processed = 0
            
            for commit in commits:
                commit_id = commit.get('hash', '')
                message = commit.get('message', '')
                author_info = commit.get('author', {})
                author = author_info.get('user', {}).get('display_name', 
                        author_info.get('user', {}).get('nickname', 
                        author_info.get('raw', '')))
                
                # Get parent commit IDs
                parents = commit.get('parents', [])
                parent_ids = [p.get('hash', '') for p in parents if p.get('hash')]
                
                commit_dt = Utils.convert_to_utc(commit.get('date'))
                if not commit_dt:
                    continue
                
                # Check if commit is recent enough
                if commit_dt < start_date_naive:
                    # Skip old commits but continue processing page
                    continue
                
                has_recent_commits = True
                
                # Skip merge commits (commits with multiple parents)
                if self._is_merge_commit(message) or len(parent_ids) > 1:
                    continue
                
                # Extended attributes for commits: store parent_ids
                extended_attrs = {'parent_ids': parent_ids}
                
                events.append(CodeCommitEvent.create_event(
                    timestamp_utc=commit_dt,
                    repo_name=repo_name,
                    event_type='Code Committed',
                    source_branch='',
                    target_branch='',  # Leave empty in fast mode
                    revision=commit_id,
                    author=author,
                    comment=message,
                    extended_attributes=extended_attrs
                ))
                self.stats['code_committed'] += 1
                page_processed += 1
                
                # Track extracted commit in memory
                self.extracted_commits.add((repo_name, commit_id))
            
            logger.info(f"[Commit] Page {page}: Processed {page_processed} commits from {len(commits)} total")
            
            # Early termination: if no recent commits on this page, likely no more recent commits ahead
            # Note: Bitbucket commits may not be strictly ordered, but in practice they usually are
            if not has_recent_commits and page > 1:
                logger.info(f"[Commit] Stopping at page {page} - all commits are older than start_date")
                break
            
            # Check for next page
            next_url = data.get('next')
            if not next_url:
                break
            
            url = next_url
            params = None
            page += 1
        
        logger.info(f"[Commit] Fetched {len(events)} commit events for '{repo_name}'")
        logger.info(f"[Commit] Completed processing commits for repo '{repo_name}'")
        return events
    
    def fetch_tags(
        self, 
        workspace: str, 
        repo_name: str, 
        headers: Dict
    ) -> List[Dict]:
        """
        Fetch tags and create Tag Created events.
        
        API: /repositories/{workspace}/{repo_slug}/refs/tags
        
        Note: Tags are typically fetched in full as they are usually fewer in number.
        No date filtering applied for tags.
        """
        url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{quote(repo_name)}/refs/tags"
        params = {
            'pagelen': 50,
            'sort': '-name'  # Sort by name descending (most recent versions first)
        }
        
        events = []
        page = 1
        
        while True:
            logger.info(f"[Tags] Fetching page {page} for repo '{repo_name}'...")
            
            data = self._make_api_request(url, headers, params)
            if not data or not isinstance(data, dict):
                break
            
            tags = data.get('values', [])
            if not tags:
                break
            
            for tag in tags:
                tag_name = tag.get('name', '')
                if not tag_name:
                    continue
                
                # Get target commit
                target = tag.get('target', {})
                commit_date = Utils.convert_to_utc(target.get('date'))
                author_info = target.get('author', {})
                author = author_info.get('user', {}).get('display_name',
                        author_info.get('user', {}).get('nickname',
                        author_info.get('raw', '')))
                
                if not commit_date:
                    continue
                
                # Get the first parent commit instead of the tag commit
                # Tags point to commits, and we want the parent of that commit
                parents = target.get('parents', [])
                if parents and len(parents) > 0:
                    commit_id = parents[0].get('hash', '')
                else:
                    # Fallback to tag's commit if no parent exists
                    commit_id = target.get('hash', '')
                
                events.append(CodeCommitEvent.create_event(
                    timestamp_utc=commit_date,
                    repo_name=repo_name,
                    event_type='Tag Created',
                    source_branch='',
                    target_branch=tag_name,
                    revision=commit_id,
                    author=author,
                    comment=''
                ))
                self.stats['tag_created'] += 1
            
            logger.info(f"[Tags] Page {page}: Fetched {len(tags)} tags")
            
            # Check for next page
            next_url = data.get('next')
            if not next_url:
                break
            
            url = next_url
            params = None
            page += 1
        
        logger.info(f"[Tags] Fetched {len(events)} tag events for '{repo_name}'")
        logger.info(f"[Tags] Completed processing tags for repo '{repo_name}'")
        return events
    
    # ============================================================================
    # ENRICHED MODE
    # ============================================================================
    
    def fetch_pr_commits(
        self, 
        workspace: str, 
        repo_name: str, 
        pr_id: int, 
        headers: Dict
    ) -> List[Dict]:
        """
        Fetch commits for a specific pull request.
        
        API: /repositories/{workspace}/{repo_slug}/pullrequests/{pr_id}/commits
        
        Args:
            workspace: Bitbucket workspace ID
            repo_name: Repository name
            pr_id: Pull request ID
            headers: Request headers
            
        Returns:
            List of commit dictionaries
        """
        url = f"https://api.bitbucket.org/2.0/repositories/{workspace}/{quote(repo_name)}/pullrequests/{pr_id}/commits"
        params = {'pagelen': 50}
        
        all_commits = []
        
        while True:
            data = self._make_api_request(url, headers, params)
            if not data or not isinstance(data, dict):
                break
            
            commits = data.get('values', [])
            if not commits:
                break
            
            all_commits.extend(commits)
            
            # Check for next page
            next_url = data.get('next')
            if not next_url:
                break
            
            url = next_url
            params = None
        
        return all_commits
    
    def enrich_pr_with_commits(
        self,
        workspace: str,
        repo_name: str,
        headers: Dict,
        pr_details: Dict[int, Dict]
    ) -> List[Dict]:
        """
        Enrich Code Committed events by fetching commits from pull requests.
        
        For each PR, fetches commits using /pullrequests/{pr_id}/commits API
        and creates Code Committed events with target_branch from PR source branch.
        
        Args:
            workspace: Bitbucket workspace ID
            repo_name: Repository name
            headers: Request headers
            pr_details: Dictionary of PR details indexed by PR ID
            
        Returns:
            List of enriched Code Committed events
        """
        enriched_events = []
        
        for pr_id, pr in pr_details.items():
            try:
                # Get PR source branch (this will be the target_branch for commits)
                source_branch = pr.get('source', {}).get('branch', {}).get('name', '')
                if not source_branch:
                    continue
                
                logger.info(f"[Enrichment] Fetching commits for PR #{pr_id} (branch: {source_branch})")
                
                # Fetch commits for this PR
                commits = self.fetch_pr_commits(workspace, repo_name, pr_id, headers)
                
                if not commits:
                    continue
                
                logger.debug(f"[Enrichment] Found {len(commits)} commits in PR #{pr_id}")
                
                # Create Code Committed events for each commit
                for commit in commits:
                    commit_id = commit.get('hash', '')
                    message = commit.get('message', '')
                    
                    # Skip if already extracted (to avoid duplicates)
                    if (repo_name, commit_id) in self.extracted_commits:
                        logger.debug(f"[Enrichment] Skipping already extracted commit {commit_id[:8]}")
                        continue
                    
                    # Get author information
                    author_info = commit.get('author', {})
                    author = author_info.get('user', {}).get('display_name',
                            author_info.get('user', {}).get('nickname',
                            author_info.get('raw', '')))
                    
                    # Get parent commit IDs
                    parents = commit.get('parents', [])
                    parent_ids = [p.get('hash', '') for p in parents if p.get('hash')]
                    
                    # Get commit date
                    commit_dt = Utils.convert_to_utc(commit.get('date'))
                    if not commit_dt:
                        continue
                    
                    # Skip merge commits (commits with multiple parents)
                    if self._is_merge_commit(message) or len(parent_ids) > 1:
                        logger.debug(f"[Enrichment] Skipping merge commit {commit_id[:8]}")
                        continue
                    
                    # Extended attributes for commits: store parent_ids
                    extended_attrs = {'parent_ids': parent_ids}
                    
                    enriched_events.append(CodeCommitEvent.create_event(
                        timestamp_utc=commit_dt,
                        repo_name=repo_name,
                        event_type='Code Committed',
                        source_branch='',
                        target_branch=source_branch,  # Use PR source branch
                        revision=commit_id,
                        author=author,
                        comment=message,
                        extended_attributes=extended_attrs
                    ))
                    self.stats['code_committed'] += 1
                    
                    # Track extracted commit in memory
                    self.extracted_commits.add((repo_name, commit_id))
                
                logger.info(f"[Enrichment] PR #{pr_id}: Added {len([e for e in enriched_events if e.get('revision') in [c.get('hash') for c in commits]])} commits")
                
            except Exception as e:
                logger.error(f"[Enrichment] Error processing PR #{pr_id}: {e}")
                continue
        
        return enriched_events
    
    # ============================================================================
    # MAIN ORCHESTRATION
    # ============================================================================
    
    def run_extraction(
        self, 
        cursor, 
        config: Dict, 
        start_date: Optional[str], 
        last_modified: Optional[datetime], 
        export_path: str = None
    ):
        """
        Run extraction: fetch and save data.
        
        Args:
            cursor: Database cursor (None for CSV mode)
            config: Configuration dictionary
            start_date: Start date from command line (optional)
            last_modified: Last modified datetime from database or checkpoint
            export_path: Export path for CSV mode
        """
        # Track maximum timestamp for checkpoint saving
        max_timestamp = None
        
        if not config.get('workspace'):
            logger.error("Missing required configuration: Workspace")
            sys.exit(1)
        
        if not config.get('api_token'):
            logger.error("Missing required configuration: Personal Access Token")
            sys.exit(1)
        
        if not config.get('repos'):
            logger.error("No repositories configured")
            sys.exit(1)
        
        workspace = config['workspace']
        api_token = config['api_token']
        repos = config['repos']
        
        # Set up headers
        headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }
        
        # Determine start date and mode
        is_enriched_mode = False
        if start_date:
            start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
            # Convert to naive UTC datetime
            if start_date_dt.tzinfo is not None:
                start_date_dt = start_date_dt.astimezone(timezone.utc).replace(tzinfo=None)
            else:
                start_date_dt = start_date_dt.replace(tzinfo=None)
        else:
            if last_modified:
                # Convert to naive datetime if timezone-aware
                if last_modified.tzinfo is not None:
                    last_modified = last_modified.replace(tzinfo=None)
                start_date_dt = last_modified
                is_enriched_mode = True  # PLACEHOLDER: Enriched mode when doing incremental extraction
            else:
                start_date_dt = datetime(2024, 1, 1)
        
        # Set up save function
        if cursor:
            # Database mode
            def save_output_fn(events):
                if events:
                    total, inserted, duplicates = CodeCommitEvent.save_events_to_database(events, cursor, cursor.connection)
                    self.stats['total_inserted'] += inserted
                    self.stats['total_duplicates'] += duplicates
                    return total, inserted, duplicates
                return 0, 0, 0
        else:
            # CSV mode - create CSV file at the start
            csv_file = Utils.create_csv_file("bitbucket_repos_events", export_path, logger)
            
            def save_output_fn(events):
                if events:
                    result = Utils.save_events_to_csv(events, csv_file, logger)
                    # Track maximum timestamp for checkpoint
                    if len(result) == 4 and result[3]:  # result[3] is max_ts
                        nonlocal max_timestamp
                        if not max_timestamp or result[3] > max_timestamp:
                            max_timestamp = result[3]
                    
                    inserted = result[0] if len(result) > 0 else len(events)
                    duplicates = result[1] if len(result) > 1 else 0
                    self.stats['total_inserted'] += inserted
                    self.stats['total_duplicates'] += duplicates
                    return len(events), inserted, duplicates
                return 0, 0, 0
        
        # Log the fetch information
        mode_str = "ENRICHED" if is_enriched_mode else "FAST"
        logger.info(f"Starting {mode_str} extraction from {start_date_dt}")
        logger.info(f"Workspace: {workspace}")
        logger.info(f"Repositories: {', '.join(repos)}")
        
        # Process repositories
        all_events = self.process_repositories(workspace, repos, headers, start_date_dt, is_enriched_mode)
        logger.info(f"Processed {len(all_events)} total events")
        
        # Save events
        if not all_events:
            logger.info("No events to save")
            total_events, inserted_count, duplicate_count = 0, 0, 0
        else:
            # Filter events by start_date and save
            filtered_events = []
            for event in all_events:
                event_dt = event.get('timestamp_utc')
                if event_dt:
                    # Convert to naive if timezone-aware
                    if event_dt.tzinfo is not None:
                        event_dt = event_dt.astimezone(timezone.utc).replace(tzinfo=None)
                    if event_dt > start_date_dt:
                        event['timestamp_utc'] = event_dt
                        filtered_events.append(event)
            
            if filtered_events:
                total_events, inserted_count, duplicate_count = save_output_fn(filtered_events)
            else:
                total_events, inserted_count, duplicate_count = 0, 0, 0
        
        # Save checkpoint in CSV mode
        if not cursor and max_timestamp:
            if Utils.save_checkpoint(prefix="bitbucket_repos", last_dt=max_timestamp, export_path=export_path):
                logger.info(f"Checkpoint saved successfully: {max_timestamp}")
            else:
                logger.warning("Failed to save checkpoint")
        
        # Print summary
        self._print_summary(total_events, inserted_count, duplicate_count)
    
    def _print_summary(self, total_events: int, inserted_count: int, duplicate_count: int):
        """Print extraction summary statistics."""
        logger.info(f"Pull Request Created:      {self.stats['pr_created']:>6}")
        logger.info(f"Pull Request Approved:     {self.stats['pr_approved']:>6}")
        logger.info(f"Pull Request Merged:       {self.stats['pr_merged']:>6}")
        logger.info(f"Code Committed:            {self.stats['code_committed']:>6}")
        logger.info(f"Tag Created:               {self.stats['tag_created']:>6}")
        logger.info(f"Total Events:              {total_events:>6}")
        logger.info(f"Inserted to DB:            {inserted_count:>6}")
        logger.info(f"Duplicates Skipped:        {duplicate_count:>6}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Extract Bitbucket Repos data")
    parser.add_argument('-p', '--product', help='Product name (if provided, saves to database; otherwise saves to CSV)')
    parser.add_argument('-s', '--start-date', help='Start date (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    extractor = BitbucketReposExtractor()
    
    if args.product is None:
        # CSV Mode: Load configuration from config.json
        config = json.load(open(os.path.join(common_dir, "config.json")))
        
        # Build config dictionary
        repos_str = config.get("BITBUCKET_REPOS", '')
        repos_list = [repo.strip() for repo in repos_str.split(",") if repo.strip()]
        
        config = {
            'workspace': config.get('BITBUCKET_WORKSPACE_ID'),
            'api_token': config.get('BITBUCKET_API_TOKEN'),
            'repos': repos_list
        }
        
        # Use checkpoint file for last modified date
        last_modified = Utils.load_checkpoint("bitbucket_repos")
        
        extractor.run_extraction(None, config, args.start_date, last_modified)
    
    else:
        # Database Mode: Connect to the database
        from database import DatabaseConnection
        db = DatabaseConnection()
        try:
            with db.product_scope(args.product) as conn:
                with conn.cursor() as cursor:
                    config = extractor.get_config_from_database(cursor)
                    last_modified = extractor.get_last_modified_date(cursor)
                    extractor.run_extraction(cursor, config, args.start_date, last_modified)
        except Exception as e:
            logger.error(f"Error during extraction: {str(e)}")
            return 1
    
    return 0

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)


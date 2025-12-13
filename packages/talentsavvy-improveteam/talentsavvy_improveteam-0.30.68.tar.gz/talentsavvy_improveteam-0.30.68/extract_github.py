#!/usr/bin/env python3
"""
GitHub Data Extraction Script

This script extracts code events from GitHub repositories and saves them to the database.
Supports both fast and enriched extraction modes.

Usage:
    python extract_github.py -p <product_name> [-s <start_date>]

Modes:
    - Fast Mode: Used for initial extraction or when start_date is specified
      * Pull Request Created/Merged/Closed from /pulls API
      * Code Pushed, Initial Push, and Branch Deleted from /activity API
      * Code Committed from /commits API (without target_branch)
      * Tag Created from /tags API
      * Faster extraction with optimized pagination
    
    - Enriched Mode: Automatically used for incremental extraction (no start_date)
      * Pull Request Approved events with actual timestamps from /pulls/{pr_id}/reviews API
      * Code Committed events from /pulls/{pr_id}/commits API (with target_branch from PR source branch)
      * More accurate commit information with branch associations

Events extracted:
    Fast Mode:
    - Pull Request Created
    - Pull Request Merged
    - Pull Request Closed
    - Code Pushed (activity_type: "push")
    - Initial Push (activity_type: "branch_creation")
    - Branch Deleted (activity_type: "branch_deletion")
    - Code Committed (from /commits API, without target_branch)
    - Tag Created
    
    Enriched Mode (additional events extracted):
    - Pull Request Approved (with actual approval timestamps from /reviews API)
    - Pull Request Cherry-picked (from release branches)
    - Code Committed (from /pulls/{pr_id}/commits API, WITH target_branch from PR source branch)
    - Note: In enriched mode, commits are fetched from PRs instead of /commits endpoint
    - Merge commits are excluded from Code Committed events
    - Only commits from PRs are extracted (more accurate branch associations)

Extended Attributes:
    - Pull Request events (Created/Merged/Closed/Approved): pull_request_number, pull_request_title
    - Pull Request Cherry-picked: pull_request_number
    - Code Committed: parent_ids (list of parent commit SHAs)
    
Note:
    - Fast Mode: Code Committed events have empty target_branch, cherry-picks not extracted, merge commits excluded
    - Enriched Mode: Code Committed events have target_branch set to PR source branch, cherry-picks extracted from release branches, merge commits excluded
"""

import argparse
import json
import logging
import os
import re
import sys
import time
from datetime import datetime, timezone, timedelta
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
logger = logging.getLogger('extract_github')

# Set logger for CodeCommitEvent
CodeCommitEvent.LOGGER = logger

class GitHubExtractor:
    """Extracts code events from GitHub repositories with extended_attributes support."""
    
    def __init__(self):
        self.db_connection = None
        
        # Track extracted commits in memory (repo, commit_id)
        self.extracted_commits = set()
        
        # Statistics
        self.stats = {
            'Pull Request Created': 0,
            'Pull Request Merged': 0,
            'Pull Request Closed': 0,
            'Pull Request Approved': 0,
            'Pull Request Cherry-picked': 0,
            'Code Committed': 0,
            'Code Pushed': 0,
            'Initial Push': 0,
            'Branch Deleted': 0,
            'Tag Created': 0,
            'total_inserted': 0,
            'total_duplicates': 0
        }
        
    def get_config_from_database(self, cursor):
        """Get GitHub configuration from data_source_config table."""
        query = """
        SELECT config_item, config_value 
        FROM data_source_config 
        WHERE data_source = 'source_code_revision_control' 
        AND config_item IN ('Organization', 'Personal Access Token', 'Repos')
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
                    config['repos'] = []
            elif config_item == 'Organization':
                config['owner'] = config_value
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

    def _make_api_request(self, url: str, api_token: str, params: Dict = None, return_headers: bool = False):
        """
        Make an API request to GitHub with retry logic.

        Args:
            url: Full API URL
            api_token: GitHub Personal Access Token
            params: Query parameters
            return_headers: If True, return tuple of (data, headers)

        Returns:
            Response JSON as dict or list, or None if request fails
            If return_headers=True, returns tuple of (data, headers)
        """
        headers = {
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }
        if api_token and api_token.strip():
            headers['Authorization'] = f'Bearer {api_token}'
        
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers, params=params, timeout=30)
                
                if response.status_code == 200:
                    data = response.json()
                    if return_headers:
                        return data, response.headers
                    return data
                elif response.status_code == 403:
                    # Rate limit exceeded
                    reset_time = response.headers.get('X-RateLimit-Reset')
                    if reset_time:
                        wait_time = int(reset_time) - int(time.time()) + 10
                        logger.warning(f"Rate limit exceeded. Waiting {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        logger.warning(f"Rate limit exceeded, no reset time provided")
                        break
                elif response.status_code == 404:
                    logger.warning(f"Resource not found: {url}")
                    break
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

        if return_headers:
            return None, None
        return None
    
    def _is_merge_commit(self, commit_message: str) -> bool:
        """
        Check if a commit message indicates a merge commit from a pull request.
        
        Returns:
            True if this is a merge commit, False otherwise
        """
        if not commit_message:
            return False
        
        merge_patterns = [
            r"^[Mm]erge pull request #\d+",
            r"^[Mm]erge branch .+ into .+",
            r"^[Mm]erged in .+ from .+",
        ]
        
        for pattern in merge_patterns:
            if re.match(pattern, commit_message):
                return True
        
        return False
    
    def _parse_link_header(self, link_header: str) -> Dict[str, str]:
        """
        Parse GitHub's Link header to extract pagination URLs.
        
        Args:
            link_header: Link header value from GitHub API response
            
        Returns:
            Dictionary mapping rel types (next, prev, first, last) to URLs
        """
        links = {}
        if not link_header:
            return links
        
        # Link header format: <url1>; rel="next", <url2>; rel="last"
        for link in link_header.split(','):
            parts = link.split(';')
            if len(parts) == 2:
                url = parts[0].strip().strip('<>')
                rel = parts[1].strip()
                # Extract rel value: rel="next" -> next
                if 'rel=' in rel:
                    rel_value = rel.split('=')[1].strip('"')
                    links[rel_value] = url
        
        return links
    
    def _extract_pr_from_commit_message(self, commit_message: str) -> Optional[int]:
        """
        Extract pull request number from commit message.
        
        Pattern: 'Merge pull request #<pull_request_number> from <head_branch_prefix>/<work_item_id>'
        
        Args:
            commit_message: Commit message to parse
            
        Returns:
            Pull request number if found, None otherwise
        """
        if not commit_message:
            return None
        
        # Match pattern: Merge pull request #<number> from ...
        match = re.search(r'Merge pull request #(\d+) from .*/(\d+)', commit_message)
        if match:
            return int(match.group(1))
        
        return None

    # ============================================================================
    # HELPER METHODS FOR CHERRY-PICK EXTRACTION
    # ============================================================================
    
    def get_release_branches(self, owner: str, repo_name: str, api_token: str) -> List[str]:
        """
        Get the list of release branches in the repository.
        
        Release branches are identified by the 'release/' prefix.
        
        Args:
            owner: Repository owner
            repo_name: Repository name
            api_token: GitHub API token
            
        Returns:
            List of release branch names
        """
        url = f"https://api.github.com/repos/{owner}/{repo_name}/branches"
        params = {'per_page': 100, 'page': 1}
        
        all_branches = []
        page = 1
        
        while True:
            params['page'] = page
            
            data = self._make_api_request(url, api_token, params)
            if not data or not isinstance(data, list):
                break
            
            branches = data
            if not branches:
                break
            
            all_branches.extend(branches)
            
            if len(branches) < 100:
                break
            page += 1
        
        # Filter for release branches
        release_branches = [branch['name'] for branch in all_branches if branch['name'].startswith('release/')]
        
        return release_branches
    
    def get_commits_for_branch(self, owner: str, repo_name: str, branch: str, api_token: str, since: datetime, until: Optional[datetime] = None) -> List[Dict]:
        """
        Get commits from a specific branch with date filtering.
        
        Args:
            owner: Repository owner
            repo_name: Repository name
            branch: Branch name
            api_token: GitHub API token
            since: Only commits after this date
            until: Only commits before this date (optional)
            
        Returns:
            List of commit dictionaries
        """
        url = f"https://api.github.com/repos/{owner}/{repo_name}/commits"
        params = {
            'sha': branch,
            'per_page': 100,
            'page': 1
        }
        
        # Add date filters (GitHub API expects ISO 8601 format)
        # Convert to naive datetime if timezone-aware
        since_naive = since if not since.tzinfo else since.replace(tzinfo=None)
        params['since'] = since_naive.isoformat() + 'Z'
        
        if until:
            # Convert to naive datetime if timezone-aware
            until_naive = until if not until.tzinfo else until.replace(tzinfo=None)
            params['until'] = until_naive.isoformat() + 'Z'
        
        all_commits = []
        page = 1
        
        while True:
            params['page'] = page
            
            data = self._make_api_request(url, api_token, params)
            if not data or not isinstance(data, list):
                break
            
            commits = data
            if not commits:
                break
            
            all_commits.extend(commits)
            
            if len(commits) < 100:
                break
            page += 1
        
        return all_commits

    # ============================================================================
    # EXTRACTION METHODS (FAST MODE)
    # ============================================================================

    def process_repositories(self, owner: str, repos: List[str], api_token: str, start_date: datetime, is_enriched_mode: bool = False) -> List[Dict]:
        """Process all repositories using fast or enriched mode extraction logic."""
        all_events = []
        
        for repo_name in repos:
            logger.info(f"Processing repository: {repo_name}")
            
            try:
                # 1. Pull Requests (PR Created/Merged/Closed)
                # Store PR details for enrichment
                pr_details = []
                pr_events = self.fetch_pull_requests(owner, repo_name, api_token, start_date, store_details=is_enriched_mode, pr_details_out=pr_details if is_enriched_mode else None)
                all_events.extend(pr_events)
                
                # 1.5. Enriched Mode: Fetch PR Approved events with actual timestamps
                if is_enriched_mode and pr_details:
                    logger.info(f"[Enriched Mode] Fetching PR approvals for '{repo_name}'")
                    approval_events = self.enrich_pull_requests_with_approvals(
                        owner, repo_name, api_token, pr_details, start_date
                    )
                    all_events.extend(approval_events)
                    self.stats['Pull Request Approved'] += len(approval_events)
                
                # 2. Activity Events (Code Pushed, Initial Push, Branch Deleted)
                activity_events = self.fetch_activity_events(owner, repo_name, api_token, start_date)
                all_events.extend(activity_events)
                
                # 3. Commits (Code Committed with parent_ids in extended_attributes)
                if is_enriched_mode:
                    # Enriched mode: Get commits from PRs with target_branch
                    if pr_details:
                        logger.info(f"[Enriched Mode] Fetching commits from PRs for '{repo_name}'")
                        commit_events = self.enrich_pull_requests_with_commits(
                            owner, repo_name, api_token, pr_details
                        )
                        all_events.extend(commit_events)
                else:
                    # Fast mode: Get commits from commits endpoint (no target_branch)
                    commit_events = self.fetch_commits(owner, repo_name, api_token, start_date)
                    all_events.extend(commit_events)
                
                # 4. Tags
                tag_events = self.fetch_tags(owner, repo_name, api_token, start_date)
                all_events.extend(tag_events)
                
                # 5. Cherry-picks (enriched mode only)
                if is_enriched_mode:
                    logger.info(f"[Enriched Mode] Fetching cherry-picks for '{repo_name}'")
                    cherry_pick_events = self.fetch_cherry_picks(owner, repo_name, api_token, start_date)
                    all_events.extend(cherry_pick_events)
                    
            except Exception as e:
                logger.error(f"Error processing repository {repo_name}: {e}")
                continue
                
        return all_events

    def fetch_pull_requests(self, owner: str, repo_name: str, api_token: str, start_date: datetime, store_details: bool = False, pr_details_out: List = None) -> List[Dict]:
        """
        Fetch pull requests and extract PR events with extended_attributes.
        
        Args:
            owner: Repository owner
            repo_name: Repository name
            api_token: GitHub API token
            start_date: Start date for filtering
            store_details: If True, store PR details in pr_details_out for enrichment
            pr_details_out: List to store PR details (required if store_details=True)
            
        Returns:
            List of PR events (Created/Merged/Closed)
        """
        url = f"https://api.github.com/repos/{owner}/{repo_name}/pulls"
        params = {
            'state': 'all',
            'sort': 'created',
            'direction': 'desc',
            'per_page': 100,
            'page': 1
        }
        
        events = []
        page = 1
        start_date_naive = start_date if not start_date.tzinfo else start_date.replace(tzinfo=None)
        
        while True:
            params['page'] = page
            logger.info(f"[PR] Fetching page {page} for repo '{repo_name}' from {url}?page={page}")

            data = self._make_api_request(url, api_token, params)
            if not data or not isinstance(data, list):
                break

            prs = data
            if not prs:
                break
            
            # Track if any PRs on this page are recent enough
            has_recent_pr = False
                
            for pr in prs:
                pr_number = pr.get('number')
                title = pr.get('title', '')
                body = pr.get('body', '')
                state = pr.get('state', '')
                author = pr.get('user', {}).get('login', '')
                
                # Get branch information
                head = pr.get('head', {})
                base = pr.get('base', {})
                source_branch = head.get('ref', '')
                target_branch = base.get('ref', '')
                sha = head.get('sha', '')
                
                created_at = Utils.convert_to_utc(pr.get('created_at'))
                if not created_at:
                    continue
                
                # Check if PR is recent enough
                if created_at < start_date_naive:
                    continue
                
                has_recent_pr = True
                
                # Store PR details for enrichment if requested
                if store_details and pr_details_out is not None:
                    pr_details_out.append(pr)
                
                merged_at = Utils.convert_to_utc(pr.get('merged_at')) if pr.get('merged_at') else None
                closed_at = Utils.convert_to_utc(pr.get('closed_at')) if pr.get('closed_at') else None

                # Extended attributes for PR events
                extended_attrs = {
                    'pull_request_number': pr_number,
                    'pull_request_title': title
                }

                # PR Created event
                events.append(CodeCommitEvent.create_event(
                    timestamp_utc=created_at,
                    repo_name=repo_name,
                    event_type='Pull Request Created',
                    source_branch=source_branch,
                    target_branch=target_branch,
                    revision=sha,
                    author=author,
                    comment=body if body else title,
                    extended_attributes=extended_attrs
                ))
                self.stats['Pull Request Created'] += 1

                # PR Merged event
                if merged_at:
                    merge_commit_sha = pr.get('merge_commit_sha', '')
                    events.append(CodeCommitEvent.create_event(
                        timestamp_utc=merged_at,
                        repo_name=repo_name,
                        event_type='Pull Request Merged',
                        source_branch=source_branch,
                        target_branch=target_branch,
                        revision=merge_commit_sha,
                        author=author,
                        comment=title,
                        extended_attributes=extended_attrs
                    ))
                    self.stats['Pull Request Merged'] += 1
                
                # PR Closed event (only if closed but not merged)
                elif closed_at and not merged_at:
                    events.append(CodeCommitEvent.create_event(
                        timestamp_utc=closed_at,
                        repo_name=repo_name,
                        event_type='Pull Request Closed',
                        source_branch=source_branch,
                        target_branch=target_branch,
                        revision=sha,
                        author=author,
                        comment=title,
                        extended_attributes=extended_attrs
                    ))
                    self.stats['Pull Request Closed'] += 1

            logger.info(f"[PR] Page {page}: Fetched {len(prs)} pull requests ({len([e for e in events if e])} events)")
            
            # Early termination: if no recent PRs on this page, stop
            if not has_recent_pr:
                logger.info(f"[PR] Stopping at page {page} - all PRs are older than start_date")
                break
            
            if len(prs) < 100:
                break
            page += 1
            
        logger.info(f"[PR] Fetched {len(events)} PR events for '{repo_name}'")
        logger.info(f"[PR] Completed processing pull requests for repo '{repo_name}'")
        return events

    def fetch_activity_events(self, owner: str, repo_name: str, api_token: str, start_date: datetime) -> List[Dict]:
        """
        Fetch repository activity events from activity API.
        
        Extracts:
        - Code Pushed (activity_type: "push")
        - Initial Push (activity_type: "branch_creation")
        - Branch Deleted (activity_type: "branch_deletion")
        
        Note: GitHub activity API uses Link header pagination, not query parameters.
        Activities are sorted by timestamp descending.
        """
        url = f"https://api.github.com/repos/{owner}/{repo_name}/activity"
        params = {
            'per_page': 100
        }
        
        events = []
        iteration = 1
        start_date_naive = start_date if not start_date.tzinfo else start_date.replace(tzinfo=None)
        
        while url:
            logger.info(f"[Activity] Fetching iteration {iteration} for repo '{repo_name}' from {url}")

            result = self._make_api_request(url, api_token, params if iteration == 1 else None, return_headers=True)
            if not result or result[0] is None:
                break
            
            data, response_headers = result
            if not isinstance(data, list):
                break

            activities = data
            if not activities:
                break
            
            # Track the earliest timestamp for early termination
            earliest_timestamp = None
                
            for activity in activities:
                timestamp = Utils.convert_to_utc(activity.get('timestamp'))
                if timestamp:
                    # Track earliest timestamp for early termination
                    if not earliest_timestamp or timestamp < earliest_timestamp:
                        earliest_timestamp = timestamp
                
                activity_type = activity.get('activity_type', '')
                
                # Process push, branch_creation, and branch_deletion activities
                if activity_type not in ('push', 'branch_creation', 'branch_deletion'):
                    continue
                
                if not timestamp:
                    continue
                
                # Skip if older than start_date
                if timestamp < start_date_naive:
                    continue
                
                actor = activity.get('actor', {}).get('login', '')
                ref = activity.get('ref', '')
                
                # Determine branch name
                if ref and ref.startswith('refs/heads/'):
                    branch_name = ref.replace('refs/heads/', '')
                else:
                    continue
                
                # Get before and after commits
                before_sha = activity.get('before', '')
                after_sha = activity.get('after', '')
                
                # Determine event type based on activity_type
                if activity_type == 'branch_creation':
                    event_type = 'Initial Push'
                    revision = after_sha
                    self.stats['Initial Push'] += 1
                elif activity_type == 'branch_deletion':
                    event_type = 'Branch Deleted'
                    revision = before_sha
                    self.stats['Branch Deleted'] += 1
                else:  # activity_type == 'push'
                    event_type = 'Code Pushed'
                    revision = after_sha
                    self.stats['Code Pushed'] += 1
                
                events.append(CodeCommitEvent.create_event(
                    timestamp_utc=timestamp,
                    repo_name=repo_name,
                    event_type=event_type,
                    source_branch='',
                    target_branch=branch_name,
                    revision=revision,
                    author=actor,
                    comment=''
                ))

            logger.info(f"[Activity] Iteration {iteration}: Fetched {len(activities)} activities")
            
            # Early termination: if earliest timestamp is older than start_date, stop
            if earliest_timestamp and earliest_timestamp < start_date_naive:
                logger.info(f"[Activity] Stopping at iteration {iteration} - earliest activity ({earliest_timestamp}) is older than start_date ({start_date_naive})")
                break
            
            # Parse Link header for next page URL
            link_header = response_headers.get('Link', '')
            links = self._parse_link_header(link_header)
            
            # Get next page URL
            url = links.get('next')
            if not url:
                logger.info(f"[Activity] No more pages available")
                break
            
            iteration += 1
            
        logger.info(f"[Activity] Fetched {len(events)} activity events for '{repo_name}'")
        logger.info(f"[Activity] Completed processing activity for repo '{repo_name}'")
        return events

    def fetch_commits(self, owner: str, repo_name: str, api_token: str, start_date: datetime) -> List[Dict]:
        """Fetch commits with parent_ids in extended_attributes and track them in memory."""
        url = f"https://api.github.com/repos/{owner}/{repo_name}/commits"
        params = {
            'since': start_date.isoformat(),
            'per_page': 100,
            'page': 1
        }

        events = []
        page = 1

        while True:
            params['page'] = page
            logger.info(f"[Commit] Fetching page {page} for repo '{repo_name}' from {url}?page={page}")

            data = self._make_api_request(url, api_token, params)
            if not data or not isinstance(data, list):
                break

            commits = data
            if not commits:
                break

            for commit in commits:
                commit_sha = commit.get('sha', '')
                commit_data = commit.get('commit', {})
                message = commit_data.get('message', '')
                author_data = commit_data.get('author', {})
                author = author_data.get('name', '')
                
                # Get parent commit SHAs
                parents = commit.get('parents', [])
                parent_ids = [p.get('sha', '') for p in parents if p.get('sha')]

                commit_dt = Utils.convert_to_utc(author_data.get('date'))
                if not commit_dt:
                    continue
                
                # Skip merge commits
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
                    revision=commit_sha,
                    author=author,
                    comment=message,
                    extended_attributes=extended_attrs
                ))
                self.stats['Code Committed'] += 1
                
                # Track extracted commit in memory
                self.extracted_commits.add((repo_name, commit_sha))

            logger.info(f"[Commit] Page {page}: Fetched {len(commits)} commits")
            
            if len(commits) < 100:
                break
            page += 1

        logger.info(f"[Commit] Fetched {len(events)} commit events for '{repo_name}'")
        logger.info(f"[Commit] Completed processing commits for repo '{repo_name}'")
        return events

    def fetch_tags(self, owner: str, repo_name: str, api_token: str, start_date: datetime) -> List[Dict]:
        """Fetch tags."""
        url = f"https://api.github.com/repos/{owner}/{repo_name}/tags"
        params = {'per_page': 100, 'page': 1}

        events = []
        page = 1

        while True:
            params['page'] = page
            logger.info(f"[Tags] Fetching page {page} for repo '{repo_name}' from {url}?page={page}")

            data = self._make_api_request(url, api_token, params)
            if not data or not isinstance(data, list):
                break

            tags = data
            if not tags:
                break
                
            for tag in tags:
                tag_name = tag.get('name', '')
                if not tag_name:
                    continue

                commit = tag.get('commit', {})
                commit_sha = commit.get('sha', '')
                
                # Fetch commit details to get timestamp and author
                if commit_sha:
                    commit_url = commit.get('url', '')
                    if commit_url:
                        commit_detail = self._make_api_request(commit_url, api_token)
                        if commit_detail:
                            commit_data = commit_detail.get('commit', {})
                            author_data = commit_data.get('author', {})
                            author = author_data.get('name', '')
                            created_dt = Utils.convert_to_utc(author_data.get('date'))
                            
                            if created_dt:
                                events.append(CodeCommitEvent.create_event(
                                    timestamp_utc=created_dt,
                                    repo_name=repo_name,
                                    event_type='Tag Created',
                                    source_branch='',
                                    target_branch=tag_name,
                                    revision=commit_sha,
                                    author=author,
                                    comment=''
                                ))
                                self.stats['Tag Created'] += 1

            logger.info(f"[Tags] Page {page}: Fetched {len(tags)} tags")
            
            if len(tags) < 100:
                break
            page += 1

        logger.info(f"[Tags] Fetched {len(events)} tag events for '{repo_name}'")
        logger.info(f"[Tags] Completed processing tags for repo '{repo_name}'")
        return events
    
    def fetch_cherry_picks(self, owner: str, repo_name: str, api_token: str, start_date: datetime) -> List[Dict]:
        """
        Fetch cherry-pick events from release branches.
        
        This method:
        1. Gets all release branches (branches starting with 'release/')
        2. For each release branch, gets commits filtered by date
        3. Extracts PR number from commit message
        4. Creates Pull Request Cherry-picked events
        
        Args:
            owner: Repository owner
            repo_name: Repository name
            api_token: GitHub API token
            start_date: Only fetch commits after this date
            
        Returns:
            List of Pull Request Cherry-picked events
        """
        events = []
        
        # Get release branches
        branches_url = f"https://api.github.com/repos/{owner}/{repo_name}/branches"
        logger.info(f"[Cherry-pick] Fetching release branches for repo '{repo_name}' from {branches_url}")
        release_branches = self.get_release_branches(owner, repo_name, api_token)
        
        if not release_branches:
            logger.info(f"[Cherry-pick] No release branches found for repo '{repo_name}'")
            return events
        
        # Process each release branch
        for release_branch in release_branches:
            logger.info(f"[Cherry-pick] Fetching commits for branch '{release_branch}' since {start_date}")
            
            commits = self.get_commits_for_branch(owner, repo_name, release_branch, api_token, since=start_date)
            
            if not commits:
                continue
            
            for commit in commits:
                commit_sha = commit.get('sha', '')
                commit_data = commit.get('commit', {})
                commit_message = commit_data.get('message', '')
                commit_timestamp = commit_data.get('committer', {}).get('date', '')
                author_name = commit_data.get('committer', {}).get('name', '')
                
                # Extract pull request number from commit message
                pr_number = self._extract_pr_from_commit_message(commit_message)
                
                if pr_number:
                    # Convert commit timestamp to UTC datetime
                    timestamp_dt = Utils.convert_to_utc(commit_timestamp)
                    if not timestamp_dt:
                        continue
                    
                    # Extended attributes
                    extended_attrs = {
                        'pull_request_number': pr_number
                    }
                    
                    events.append(CodeCommitEvent.create_event(
                        timestamp_utc=timestamp_dt,
                        repo_name=repo_name,
                        event_type='Pull Request Cherry-picked',
                        source_branch='',
                        target_branch=release_branch,
                        revision=commit_sha,
                        author=author_name,
                        comment=commit_message,
                        extended_attributes=extended_attrs
                    ))
                    self.stats['Pull Request Cherry-picked'] += 1
        
        logger.info(f"[Cherry-pick] Fetched {len(events)} cherry-pick events for '{repo_name}'")
        logger.info(f"[Cherry-pick] Completed processing cherry-picks for repo '{repo_name}'")
        return events

    # ============================================================================
    # ENRICHED MODE
    # ============================================================================
    
    def fetch_pr_reviews(self, owner: str, repo_name: str, pr_number: int, api_token: str) -> List[Dict]:
        """
        Fetch reviews for a specific pull request.
        
        API: /repos/{owner}/{repo}/pulls/{pr_number}/reviews
        
        Args:
            owner: Repository owner
            repo_name: Repository name
            pr_number: Pull request number
            api_token: GitHub API token
            
        Returns:
            List of review dictionaries
        """
        url = f"https://api.github.com/repos/{owner}/{repo_name}/pulls/{pr_number}/reviews"
        params = {
            'per_page': 100,
            'page': 1
        }
        
        all_reviews = []
        page = 1
        
        while True:
            params['page'] = page
            
            data = self._make_api_request(url, api_token, params)
            if not data or not isinstance(data, list):
                break
            
            reviews = data
            if not reviews:
                break
            
            all_reviews.extend(reviews)
            
            if len(reviews) < 100:
                break
            page += 1
        
        return all_reviews
    
    def fetch_pr_commits(self, owner: str, repo_name: str, pr_number: int, api_token: str) -> List[Dict]:
        """
        Fetch commits for a specific pull request.
        
        API: /repos/{owner}/{repo}/pulls/{pr_number}/commits
        
        Args:
            owner: Repository owner
            repo_name: Repository name
            pr_number: Pull request number
            api_token: GitHub API token
            
        Returns:
            List of commit dictionaries
        """
        url = f"https://api.github.com/repos/{owner}/{repo_name}/pulls/{pr_number}/commits"
        params = {
            'per_page': 100,
            'page': 1
        }
        
        all_commits = []
        page = 1
        
        while True:
            params['page'] = page
            
            data = self._make_api_request(url, api_token, params)
            if not data or not isinstance(data, list):
                break
            
            commits = data
            if not commits:
                break
            
            all_commits.extend(commits)
            
            if len(commits) < 100:
                break
            page += 1
        
        return all_commits
    
    def enrich_pull_requests_with_approvals(
        self,
        owner: str,
        repo_name: str,
        api_token: str,
        pr_details: List[Dict],
        start_date: datetime
    ) -> List[Dict]:
        """
        Enrich pull requests with approval events.
        
        For each PR, fetches reviews using /pulls/{pr_number}/reviews API
        and creates Pull Request Approved events with actual approval timestamps.
        
        Args:
            owner: Repository owner
            repo_name: Repository name
            api_token: GitHub API token
            pr_details: List of PR details from fetch_pull_requests
            start_date: Start date for filtering
            
        Returns:
            List of Pull Request Approved events
        """
        enriched_events = []
        start_date_naive = start_date if not start_date.tzinfo else start_date.replace(tzinfo=None)
        
        for pr in pr_details:
            try:
                pr_number = pr.get('number')
                if not pr_number:
                    continue
                
                title = pr.get('title', '')
                head = pr.get('head', {})
                base = pr.get('base', {})
                source_branch = head.get('ref', '')
                target_branch = base.get('ref', '')
                sha = head.get('sha', '')
                
                reviews_url = f"https://api.github.com/repos/{owner}/{repo_name}/pulls/{pr_number}/reviews"
                logger.info(f"[Enrichment] Fetching reviews for PR #{pr_number} from {reviews_url}")
                
                # Fetch reviews for this PR
                reviews = self.fetch_pr_reviews(owner, repo_name, pr_number, api_token)
                
                if not reviews:
                    continue
                
                # Extended attributes for PR events
                extended_attrs = {
                    'pull_request_number': pr_number,
                    'pull_request_title': title
                }
                
                # Create Pull Request Approved events for each approval
                for review in reviews:
                    state = review.get('state', '')
                    
                    # Only process APPROVED reviews
                    if state != 'APPROVED':
                        continue
                    
                    submitted_at = Utils.convert_to_utc(review.get('submitted_at'))
                    if not submitted_at:
                        continue
                    
                    # Skip if older than start_date
                    if submitted_at < start_date_naive:
                        continue
                    
                    reviewer = review.get('user', {}).get('login', '')
                    if not reviewer:
                        continue
                    
                    enriched_events.append(CodeCommitEvent.create_event(
                        timestamp_utc=submitted_at,
                        repo_name=repo_name,
                        event_type='Pull Request Approved',
                        source_branch=source_branch,
                        target_branch=target_branch,
                        revision=sha,
                        author=reviewer,
                        comment=title,
                        extended_attributes=extended_attrs
                    ))
                
            except Exception as e:
                logger.error(f"[Enrichment] Error processing PR #{pr_number}: {e}")
                continue
        
        return enriched_events
    
    def enrich_pull_requests_with_commits(
        self,
        owner: str,
        repo_name: str,
        api_token: str,
        pr_details: List[Dict]
    ) -> List[Dict]:
        """
        Enrich Code Committed events by fetching commits from pull requests.
        
        For each PR, fetches commits using /pulls/{pr_number}/commits API
        and creates Code Committed events with target_branch from PR source branch.
        
        Args:
            owner: Repository owner
            repo_name: Repository name
            api_token: GitHub API token
            pr_details: List of PR details from fetch_pull_requests
            
        Returns:
            List of enriched Code Committed events
        """
        enriched_events = []
        
        for pr in pr_details:
            try:
                pr_number = pr.get('number')
                if not pr_number:
                    continue
                
                # Get PR source branch (this will be the target_branch for commits)
                head = pr.get('head', {})
                source_branch = head.get('ref', '')
                
                if not source_branch:
                    continue
                
                commits_url = f"https://api.github.com/repos/{owner}/{repo_name}/pulls/{pr_number}/commits"
                logger.info(f"[Enrichment] Fetching commits for PR #{pr_number} (branch: {source_branch}) from {commits_url}")
                
                # Fetch commits for this PR
                commits = self.fetch_pr_commits(owner, repo_name, pr_number, api_token)
                
                if not commits:
                    continue
                
                # Create Code Committed events for each commit
                for commit in commits:
                    commit_sha = commit.get('sha', '')
                    
                    # Skip if already extracted (to avoid duplicates)
                    if (repo_name, commit_sha) in self.extracted_commits:
                        logger.debug(f"[Enrichment] Skipping already extracted commit {commit_sha[:8]}")
                        continue
                    
                    # Get commit details
                    commit_data = commit.get('commit', {})
                    message = commit_data.get('message', '')
                    author_data = commit_data.get('author', {})
                    author = author_data.get('name', '')
                    
                    # Get parent commit SHAs
                    parents = commit.get('parents', [])
                    parent_ids = [p.get('sha', '') for p in parents if p.get('sha')]
                    
                    # Get commit date
                    commit_dt = Utils.convert_to_utc(author_data.get('date'))
                    if not commit_dt:
                        continue
                    
                    # Skip merge commits (commits with multiple parents)
                    if self._is_merge_commit(message) or len(parent_ids) > 1:
                        continue
                    
                    # Extended attributes for commits: store parent_ids
                    extended_attrs = {'parent_ids': parent_ids}
                    
                    enriched_events.append(CodeCommitEvent.create_event(
                        timestamp_utc=commit_dt,
                        repo_name=repo_name,
                        event_type='Code Committed',
                        source_branch='',
                        target_branch=source_branch,  # Use PR source branch
                        revision=commit_sha,
                        author=author,
                        comment=message,
                        extended_attributes=extended_attrs
                    ))
                    self.stats['Code Committed'] += 1
                    
                    # Track extracted commit in memory
                    self.extracted_commits.add((repo_name, commit_sha))
                
            except Exception as e:
                logger.error(f"[Enrichment] Error processing PR #{pr_number}: {e}")
                continue
        
        return enriched_events
    
    # ============================================================================
    # MAIN ORCHESTRATION
    # ============================================================================
    
    def run_extraction(self, cursor, config: Dict, start_date: Optional[str], last_modified: Optional[datetime], export_path: str = None):
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

        if not config.get('owner'):
            logger.error("Missing required configuration: Organization (Owner)")
            sys.exit(1)

        if not config.get('repos'):
            logger.error("No repositories configured")
            sys.exit(1)

        owner = config['owner']
        api_token = config.get('api_token', '')
        repos = config['repos']

        # Determine start date and mode
        is_enriched_mode = False
        if start_date:
            start_date_dt = datetime.strptime(start_date, '%Y-%m-%d')
            # Convert to naive UTC datetime
            if start_date_dt.tzinfo is not None:
                start_date_dt = start_date_dt.astimezone(timezone.utc).replace(tzinfo=None)
            else:
                start_date_dt = start_date_dt.replace(tzinfo=timezone.utc).replace(tzinfo=None)
        else:
            if last_modified:
                # Convert to naive datetime if timezone-aware
                if last_modified.tzinfo is not None:
                    last_modified = last_modified.replace(tzinfo=None)
                start_date_dt = last_modified
                is_enriched_mode = True  # Enriched mode when doing incremental extraction
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
            csv_file = Utils.create_csv_file("github_events", export_path, logger)

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
        logger.info(f"Owner: {owner}")
        logger.info(f"Repositories: {', '.join(repos)}")

        # Process repositories
        all_events = self.process_repositories(owner, repos, api_token, start_date_dt, is_enriched_mode)
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
            
            # Reset and recount stats from filtered events only
            for event_type in ['Pull Request Created', 'Pull Request Merged', 'Pull Request Closed',
                              'Pull Request Approved', 'Pull Request Cherry-picked', 'Code Committed',
                              'Code Pushed', 'Initial Push', 'Branch Deleted', 'Tag Created']:
                self.stats[event_type] = 0
            
            # Count event types from filtered events
            for event in filtered_events:
                event_type = event.get('event_type', '')
                if event_type in self.stats:
                    self.stats[event_type] += 1
            
            if filtered_events:
                total_events, inserted_count, duplicate_count = save_output_fn(filtered_events)
            else:
                total_events, inserted_count, duplicate_count = 0, 0, 0

        # Save checkpoint in CSV mode
        if not cursor and max_timestamp:
            if Utils.save_checkpoint(prefix="github", last_dt=max_timestamp, export_path=export_path):
                logger.info(f"Checkpoint saved successfully: {max_timestamp}")
            else:
                logger.warning("Failed to save checkpoint")

        # Print summary
        logger.info(f"Pull Request Created:      {self.stats['Pull Request Created']:>6}")
        logger.info(f"Pull Request Merged:       {self.stats['Pull Request Merged']:>6}")
        logger.info(f"Pull Request Closed:       {self.stats['Pull Request Closed']:>6}")
        logger.info(f"Pull Request Approved:     {self.stats['Pull Request Approved']:>6}")
        logger.info(f"Pull Request Cherry-picked:{self.stats['Pull Request Cherry-picked']:>6}")
        logger.info(f"Code Committed:            {self.stats['Code Committed']:>6}")
        logger.info(f"Code Pushed:               {self.stats['Code Pushed']:>6}")
        logger.info(f"Initial Push:              {self.stats['Initial Push']:>6}")
        logger.info(f"Branch Deleted:            {self.stats['Branch Deleted']:>6}")
        logger.info(f"Tag Created:               {self.stats['Tag Created']:>6}")
        logger.info(f"Total Events:              {total_events:>6}")
        logger.info(f"Inserted to DB:            {inserted_count:>6}")
        logger.info(f"Duplicates Skipped:        {duplicate_count:>6}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Extract GitHub data")
    parser.add_argument('-p', '--product', help='Product name (if provided, saves to database; otherwise saves to CSV)')
    parser.add_argument('-s', '--start-date', help='Start date (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    extractor = GitHubExtractor()
    
    if args.product is None:
        # CSV Mode: Load configuration from config.json
        config = json.load(open(os.path.join(common_dir, "config.json")))
        
        # Build config dictionary
        repos_str = config.get("GITHUB_REPOS", '')
        repos_list = [repo.strip() for repo in repos_str.split(",") if repo.strip()]

        config = {
            'owner': config.get('GITHUB_OWNER'),
            'api_token': config.get('GITHUB_API_TOKEN'),
            'repos': repos_list
        }

        # Use checkpoint file for last modified date
        last_modified = Utils.load_checkpoint("github")

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


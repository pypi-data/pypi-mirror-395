#!/usr/bin/env python3
"""
GitLab Data Extraction Script

This script extracts code events from GitLab repositories and saves them to the database.
Supports both fast and enriched extraction modes.

Usage:
    python extract_gitlab.py -p <product_name> [-s <start_date>]

Modes:
    - Fast Mode: Used for initial extraction or when start_date is specified
    - Enriched Mode: Automatically used for incremental extraction (no start_date)
      * In enriched mode, push events are checked for missing commits
      * Missing commits are fetched using /commits/{commit_id} API
      * Parent walking up to num_commits depth

Extended Attributes:
    - Code Committed: parent_ids (list of parent commit SHAs)
    - Code Pushed/Initial Push: num_commits (number of commits in push)
    - Pull Request Events: pull_request_number and pull_request_title

Note:
    - Merge commits (commits with 2+ parent_ids) are excluded from Code Committed events
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
import urllib3
from urllib.parse import quote
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
logger = logging.getLogger('extract_gitlab')

# Set logger for CodeCommitEvent
CodeCommitEvent.LOGGER = logger

class GitLabExtractor:
    """Extracts code events from GitLab repositories with extended_attributes support."""
    
    def __init__(self):
        self.db_connection = None
        
        # Track extracted commits in memory (repo, commit_id)
        self.extracted_commits = set()
        
        # Statistics
        self.stats = {
            'mr_created': 0,
            'mr_merged': 0,
            'mr_approved': 0,
            'code_committed': 0,
            'code_pushed': 0,
            'initial_push': 0,
            'branch_deleted': 0,
            'tag_created': 0,
            'total_inserted': 0,
            'total_duplicates': 0
        }
        
    def get_config_from_database(self, cursor):
        """Get GitLab configuration from data_source_config table."""
        query = """
        SELECT config_item, config_value 
        FROM data_source_config 
        WHERE data_source = 'source_code_revision_control' 
        AND config_item IN ('Organization', 'Personal Access Token', 'Projects', 'Repos')
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
                # Store base URL without /api/v4 suffix
                base_url = config_value.rstrip('/') if config_value else ''
                if base_url:
                    # Remove /api/v4 if it exists
                    if base_url.endswith('/api/v4'):
                        base_url = base_url[:-7]
                    # Ensure proper protocol
                if not base_url.startswith(('http://', 'https://')):
                    base_url = f"https://{base_url}"
                config['base_url'] = base_url
            elif config_item == 'Personal Access Token':
                config['api_token'] = config_value
            elif config_item == 'Projects':
                try:
                    projects = json.loads(config_value) if config_value else []
                    config['project'] = projects[0] if projects else None
                except (json.JSONDecodeError, TypeError):
                    config['project'] = None
            
        return config
    
    def get_last_modified_date(self, cursor) -> Optional[datetime]:
        """Get the last modified date from the database."""
        last_modified = CodeCommitEvent.get_last_event(cursor)
        if last_modified:
            # Convert to naive datetime if timezone-aware
            if last_modified.tzinfo is not None:
                last_modified = last_modified.replace(tzinfo=None)
        return last_modified



    def _make_api_request(self, url: str, api_token: str, params: Dict = None) -> Optional[Dict]:
        """
        Make an API request to GitLab with retry logic.

        Args:
            url: Full API URL
            api_token: GitLab Access Token
            params: Query parameters

        Returns:
            Response JSON as dict or list, or None if request fails
        """
        headers = {
            'Content-Type': 'application/json'
        }
        if api_token and api_token.strip():
            headers['PRIVATE-TOKEN'] = api_token
        
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers, params=params, timeout=30, verify=False)
                
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
            
    def _is_merge_commit(self, commit_title: str) -> bool:
        """
        Check if a commit title indicates a merge commit from a pull request.
        
        Returns:
            True if this is a merge commit, False otherwise
        """
        if not commit_title:
            return False
        
        merge_patterns = [
            r"^[Mm]erge\s+branch\s+['\"]?.+['\"]?\s+into\s+['\"]?.+['\"]?",
            r"^[Mm]erge\s+branch\s+['\"]?.+['\"]?$",
        ]
        
        for pattern in merge_patterns:
            if re.match(pattern, commit_title):
                return True
        
        return False

    # ============================================================================
    # EXTRACTION METHODS 
    # ============================================================================

    def process_repositories(self, base_url: str, repos: List[str], api_token: str, start_date: datetime, project: str, is_enriched_mode: bool = False) -> List[Dict]:
        """Process all repositories using v2 fast mode extraction logic with optional enrichment."""
        all_events = []
        
        for repo_name in repos:
            logger.info(f"Processing repository: {repo_name}")
            
            # Construct full project path
            project_id = f"{project}/{repo_name}"
            
            try:
                # 1. Merge Requests (PR Created/Merged)
                mr_events = self.fetch_merge_requests(base_url, project_id, repo_name, api_token, start_date)
                all_events.extend(mr_events)
                
                # 2. Approved Events
                approved_events = self.fetch_events(base_url, project_id, repo_name, api_token, start_date, 'approved')
                all_events.extend(approved_events)
                
                # 3. Commits (Code Committed with parent_ids in extended_attributes)
                # Process commits FIRST to track them in memory
                commit_events = self.fetch_commits(base_url, project_id, repo_name, api_token, start_date)
                all_events.extend(commit_events)
                
                # 4. Push Events (Code Pushed, Initial Push, Branch Deleted)
                push_events = self.fetch_events(base_url, project_id, repo_name, api_token, start_date, 'pushed')
                all_events.extend(push_events)
                
                # 4.5. Enriched Mode: Fetch missing commits from push events
                if is_enriched_mode and push_events:
                    logger.info(f"[Enriched Mode] Processing push events for missing commits in '{repo_name}'")
                    enriched_commits = self.enrich_push_events_with_commits(
                        base_url, project_id, repo_name, api_token, push_events
                    )
                    if enriched_commits:
                        logger.info(f"[Enriched Mode] Added {len(enriched_commits)} enriched commits for '{repo_name}'")
                        all_events.extend(enriched_commits)
                
                # 5. Tags
                tag_events = self.fetch_tags(base_url, project_id, repo_name, api_token)
                all_events.extend(tag_events)
                    
            except Exception as e:
                logger.error(f"Error processing repository {repo_name}: {e}")
                continue
                
        return all_events

    def fetch_merge_requests(self, base_url: str, project_id: str, repo_name: str, api_token: str, start_date: datetime) -> List[Dict]:
        """Fetch merge requests and extract PR events with extended_attributes."""
        encoded_project_id = quote(str(project_id), safe='')
        url = f"{base_url}/api/v4/projects/{encoded_project_id}/merge_requests"
        params = {
            'state': 'all',
            'created_after': start_date.isoformat(),
            'per_page': 100,
            'page': 1
        }
        
        events = []
        page = 1
        
        while True:
            params['page'] = page
            logger.info(f"[MR] Fetching page {page} for repo '{repo_name}'...")

            data = self._make_api_request(url, api_token, params)
            if not data or not isinstance(data, list):
                break

            mrs = data
            if not mrs:
                break
                
            for mr in mrs:
                mr_id = mr.get('iid')
                title = mr.get('title', '')
                description = mr.get('description', '')
                source_branch = mr.get('source_branch', '')
                target_branch = mr.get('target_branch', '')
                author = mr.get('author', {}).get('name', '')
                state = mr.get('state', '')
                sha = mr.get('sha', '')
                merge_commit_sha = mr.get('merge_commit_sha', '')

                created_dt = Utils.convert_to_utc(mr.get('created_at'))
                if not created_dt:
                    continue

                merged_dt = Utils.convert_to_utc(mr.get('merged_at')) if state == 'merged' else None

                # Extended attributes for PR events
                extended_attrs = {
                    'pull_request_number': mr_id,
                    'pull_request_title': title
                }

                # PR Created event
                events.append(CodeCommitEvent.create_event(
                    timestamp_utc=created_dt,
                    repo_name=repo_name,
                    event_type='Pull Request Created',
                    source_branch=source_branch,
                    target_branch=target_branch,
                    revision=sha,
                    author=author,
                    comment=description,
                    extended_attributes=extended_attrs
                ))
                self.stats['mr_created'] += 1

                # PR Merged event
                if state == 'merged' and merged_dt:
                    events.append(CodeCommitEvent.create_event(
                        timestamp_utc=merged_dt,
                        repo_name=repo_name,
                        event_type='Pull Request Merged',
                        source_branch=source_branch,
                        target_branch=target_branch,
                        revision=merge_commit_sha,
                        author=author,
                        comment=title,
                        extended_attributes=extended_attrs
                    ))
                    self.stats['mr_merged'] += 1

            logger.info(f"[MR] Page {page}: Fetched {len(mrs)} merge requests")
            
            if len(mrs) < 100:
                break
            page += 1
            
        logger.info(f"[MR] Fetched {len(events)} MR events for '{repo_name}'")
        logger.info(f"[MR] Completed processing merge requests for repo '{repo_name}'")
        return events

    def fetch_events(self, base_url: str, project_id: str, repo_name: str, api_token: str, start_date: datetime, action_name: str) -> List[Dict]:
        """Fetch events (approved or pushed) with extended_attributes."""
        encoded_project_id = quote(str(project_id), safe='')
        url = f"{base_url}/api/v4/projects/{encoded_project_id}/events"
        
        # Use start_date - 1 day for after param since it only accepts date (not datetime)
        after_date = (start_date - timedelta(days=1)).strftime('%Y-%m-%d')
        
        params = {
            'action': action_name,
            'after': after_date,
            'per_page': 100,
            'page': 1
        }
        
        events = []
        page = 1
        
        while True:
            params['page'] = page
            logger.info(f"[Events:{action_name}] Fetching page {page} for repo '{repo_name}'...")

            data = self._make_api_request(url, api_token, params)
            if not data or not isinstance(data, list):
                break

            events_data = data
            if not events_data:
                break
                
            for event_data in events_data:
                if action_name == 'approved':
                    event = self._extract_approved_event(event_data, repo_name, start_date)
                elif action_name == 'pushed':
                    event = self._extract_pushed_event(event_data, repo_name, start_date)
                else:
                    continue

                if event:
                    events.append(event)

            logger.info(f"[Events:{action_name}] Page {page}: Fetched {len(events_data)} events")
            
            if len(events_data) < 100:
                break
            page += 1
            
        logger.info(f"[Events:{action_name}] Fetched {len(events)} events for '{repo_name}'")
        logger.info(f"[Events:{action_name}] Completed processing events for repo '{repo_name}'")
        return events

    def _extract_approved_event(self, event_data: Dict, repo_name: str, start_date: datetime) -> Optional[Dict]:
        """Extract Pull Request Approved events."""
        event_dt = Utils.convert_to_utc(event_data.get('created_at'))
        if not event_dt:
            return None
        
        # Ensure start_date is naive for comparison (convert_to_utc returns naive UTC)
        start_date_naive = start_date if not start_date.tzinfo else start_date.replace(tzinfo=None)
        
        # Only create event if timestamp is >= start_date
        if event_dt < start_date_naive:
            return None

        author = event_data.get('author', {}).get('name', '')
        mr_iid = event_data.get('target_iid')
        title = event_data.get('target_title', '')
        
        if not mr_iid:
            return None

        # Extended attributes for PR Approved
        extended_attrs = {
            'pull_request_number': mr_iid,
            'pull_request_title': title
        }

        self.stats['mr_approved'] += 1

        return CodeCommitEvent.create_event(
            timestamp_utc=event_dt,
            repo_name=repo_name,
            event_type='Pull Request Approved',
            source_branch='',
            target_branch='',
            revision='',
            author=author,
            comment=title,
            extended_attributes=extended_attrs
        )

    def _extract_pushed_event(self, event_data: Dict, repo_name: str, start_date: datetime) -> Optional[Dict]:
        """Extract push-related events (Code Pushed, Initial Push, Branch Deleted) with extended_attributes."""
        event_dt = Utils.convert_to_utc(event_data.get('created_at'))
        if not event_dt:
            return None
        
        # Ensure start_date is naive for comparison (convert_to_utc returns naive UTC)
        start_date_naive = start_date if not start_date.tzinfo else start_date.replace(tzinfo=None)
        
        # Only create event if timestamp is >= start_date
        if event_dt < start_date_naive:
            return None

        author = event_data.get('author', {}).get('name', '')
        push_data = event_data.get('push_data', {})
        if not push_data:
            return None

        action_name = event_data.get('action_name', '')
        push_action = push_data.get('action', '')
        ref = push_data.get('ref', '')
        ref_type = push_data.get('ref_type', '')
        commit_from = push_data.get('commit_from')
        commit_to = push_data.get('commit_to')
        commit_title = push_data.get('commit_title', '')
        commit_count = push_data.get('commit_count', 0)

        # Only process branch events
        if ref_type != 'branch':
            return None

        # Extended attributes for push events (Code Pushed and Initial Push)
        extended_attrs = None

        # Determine event type
        if action_name == 'pushed new' and push_action == 'created' and commit_from is None:
            event_type = 'Initial Push'
            revision = commit_to if commit_to else ''
            extended_attrs = {'num_commits': commit_count}
            self.stats['initial_push'] += 1
        elif action_name == 'deleted' and push_action == 'removed' and commit_to is None:
            event_type = 'Branch Deleted'
            revision = commit_from if commit_from else ''
            self.stats['branch_deleted'] += 1
        elif action_name == 'pushed to' and push_action == 'pushed':
            if self._is_merge_commit(commit_title):
                return None
            event_type = 'Code Pushed'
            revision = commit_to if commit_to else ''
            extended_attrs = {'num_commits': commit_count}
            self.stats['code_pushed'] += 1
        else:
            return None

        return CodeCommitEvent.create_event(
            timestamp_utc=event_dt,
            repo_name=repo_name,
            event_type=event_type,
            source_branch='',
            target_branch=ref,
            revision=revision,
            author=author,
            comment=commit_title if commit_title else f"{event_type} to {ref}",
            extended_attributes=extended_attrs
        )

    def fetch_tags(self, base_url: str, project_id: str, repo_name: str, api_token: str) -> List[Dict]:
        """Fetch tags."""
        encoded_project_id = quote(str(project_id), safe='')
        url = f"{base_url}/api/v4/projects/{encoded_project_id}/repository/tags"
        params = {'per_page': 100, 'page': 1}

        events = []
        page = 1

        while True:
            params['page'] = page
            logger.info(f"[Tags] Fetching page {page} for repo '{repo_name}'...")

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
                commit_id = commit.get('id', '')
                created_dt = Utils.convert_to_utc(commit.get('created_at'))
                author = commit.get('author_name', '')

                events.append(CodeCommitEvent.create_event(
                    timestamp_utc=created_dt,
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
            
            if len(tags) < 100:
                break
            page += 1

        logger.info(f"[Tags] Fetched {len(events)} tag events for '{repo_name}'")
        logger.info(f"[Tags] Completed processing tags for repo '{repo_name}'")
        return events
        
    def fetch_commits(self, base_url: str, project_id: str, repo_name: str, api_token: str, start_date: datetime) -> List[Dict]:
        """Fetch commits with parent_ids in extended_attributes and track them in memory."""
        encoded_project_id = quote(str(project_id), safe='')
        url = f"{base_url}/api/v4/projects/{encoded_project_id}/repository/commits"
        params = {
            'since': start_date.isoformat(),
            'per_page': 100,
            'page': 1
        }

        events = []
        page = 1

        while True:
            params['page'] = page
            logger.info(f"[Commit] Fetching page {page} for repo '{repo_name}'...")

            data = self._make_api_request(url, api_token, params)
            if not data or not isinstance(data, list):
                break

            commits = data
            if not commits:
                break

            for commit in commits:
                commit_id = commit.get('id', '')
                message = commit.get('message', '')
                author = commit.get('author_name', '')
                parent_ids = commit.get('parent_ids', [])

                commit_dt = Utils.convert_to_utc(commit.get('created_at'))
                if not commit_dt:
                    continue

                # Skip merge commits (commits with 2+ parents or merge commit message patterns)
                # Merge commits are automatically generated when branches are merged
                if len(parent_ids) >= 2 or self._is_merge_commit(message):
                    logger.debug(f"[Commit] Skipping merge commit {commit_id[:8]}: {message[:50]}...")
                    continue

                # Extended attributes for commits: store parent_ids
                extended_attrs = {'parent_ids': parent_ids}

                events.append(CodeCommitEvent.create_event(
                    timestamp_utc=commit_dt,
                    repo_name=repo_name,
                    event_type='Code Committed',
                    source_branch='',
                    target_branch='',
                    revision=commit_id,
                    author=author,
                    comment=message,
                    extended_attributes=extended_attrs
                ))
                self.stats['code_committed'] += 1
                
                # Track extracted commit in memory
                self.extracted_commits.add((repo_name, commit_id))

            logger.info(f"[Commit] Page {page}: Fetched {len(commits)} commits")
            
            if len(commits) < 100:
                break
            page += 1

        logger.info(f"[Commit] Fetched {len(events)} commit events for '{repo_name}'")
        logger.info(f"[Commit] Completed processing commits for repo '{repo_name}'")
        return events
    
    def fetch_commit_by_id(self, base_url: str, project_id: str, repo_name: str, api_token: str, commit_id: str) -> Optional[Dict]:
        """Fetch a single commit by commit ID and return as Code Committed event."""
        encoded_project_id = quote(str(project_id), safe='')
        url = f"{base_url}/api/v4/projects/{encoded_project_id}/repository/commits/{commit_id}"
        
        logger.debug(f"[Commit Detail] Fetching commit {commit_id[:8]} for repo '{repo_name}'...")
        
        data = self._make_api_request(url, api_token)
        if not data:
            return None
        
        commit = data
        message = commit.get('message', '')
        author = commit.get('author_name', '')
        parent_ids = commit.get('parent_ids', [])
        
        commit_dt = Utils.convert_to_utc(commit.get('created_at'))
        if not commit_dt:
            return None

        # Skip merge commits (commits with 2+ parents or merge commit message patterns)
        # Merge commits are automatically generated when branches are merged
        if len(parent_ids) >= 2 or self._is_merge_commit(message):
            logger.debug(f"[Commit Detail] Skipping merge commit {commit_id[:8]}: {message[:50]}...")
            return None

        # Extended attributes for commits: store parent_ids
        extended_attrs = {'parent_ids': parent_ids}

        event = CodeCommitEvent.create_event(
            timestamp_utc=commit_dt,
            repo_name=repo_name,
            event_type='Code Committed',
            source_branch='',
            target_branch='',
            revision=commit_id,
            author=author,
            comment=message,
            extended_attributes=extended_attrs
        )
        
        # Track extracted commit in memory
        self.extracted_commits.add((repo_name, commit_id))
        
        return event
    
    def enrich_push_events_with_commits(self, base_url: str, project_id: str, repo_name: str, api_token: str, 
                                        push_events: List[Dict]) -> List[Dict]:
        """
        Enrich push events by fetching missing commits up to num_commits depth.
        
        For each push event (Initial Push or Code Pushed):
        - Check if the commit was already extracted from /commits API
        - If not, fetch it using /commits/{commit_id} API
        - Walk back through parents up to num_commits depth
        """
        enriched_events = []
        
        for push_event in push_events:
            event_type = push_event.get('event', '')
            if event_type not in ('Initial Push', 'Code Pushed'):
                continue
            
            commit_id = push_event.get('revision', '')
            if not commit_id:
                continue
            
            # Get num_commits from extended_attributes
            extended_attrs = push_event.get('extended_attributes', {})
            num_commits = extended_attrs.get('num_commits', 1) if extended_attrs else 1
            
            # Check if this commit was already extracted
            if (repo_name, commit_id) in self.extracted_commits:
                logger.debug(f"[Enrichment] Commit {commit_id[:8]} already extracted, skipping enrichment for this push")
                continue
            
            logger.info(f"[Enrichment] Enriching {event_type} for commit {commit_id[:8]} with depth {num_commits}")
            
            # Fetch commits up to num_commits depth
            current_commit_id = commit_id
            commits_fetched = 0
            
            while current_commit_id and commits_fetched < num_commits:
                # Fetch commit details
                commit_event = self.fetch_commit_by_id(base_url, project_id, repo_name, api_token, current_commit_id)
                
                if not commit_event:
                    logger.warning(f"[Enrichment] Failed to fetch commit {current_commit_id[:8]}, stopping enrichment")
                    break
                
                enriched_events.append(commit_event)
                commits_fetched += 1
                self.stats['code_committed'] += 1
                
                logger.debug(f"[Enrichment] Fetched commit {current_commit_id[:8]} ({commits_fetched}/{num_commits})")
                
                # Get parent for next iteration
                commit_extended_attrs = commit_event.get('extended_attributes', {})
                parent_ids = commit_extended_attrs.get('parent_ids', [])
                
                if parent_ids and len(parent_ids) > 0:
                    # Use first parent for linear history
                    current_commit_id = parent_ids[0]
                else:
                    # No more parents, stop
                    break
            
            logger.info(f"[Enrichment] Enriched {event_type}: fetched {commits_fetched} commits")
        
        return enriched_events
    
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

        if not config.get('base_url'):
            logger.error("Missing required configuration: Organization (Base URL)")
            sys.exit(1)

        if not config.get('project'):
            logger.error("Missing required configuration: Projects")
            sys.exit(1)

        if not config.get('repos'):
            logger.error("No repositories configured")
            sys.exit(1)

        base_url = config['base_url']
        api_token = config['api_token'] if config.get('api_token') else None
        project = config['project']
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
            csv_file = Utils.create_csv_file("gitlab_events", export_path, logger)

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
        logger.info(f"Base URL: {base_url}")
        logger.info(f"Project: {project}")
        logger.info(f"Repositories: {', '.join(repos)}")

        # Process repositories with enrichment if in enriched mode
        all_events = self.process_repositories(base_url, repos, api_token, start_date_dt, project, is_enriched_mode)
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
            if Utils.save_checkpoint(prefix="gitlab", last_dt=max_timestamp, export_path=export_path):
                logger.info(f"Checkpoint saved successfully: {max_timestamp}")
            else:
                logger.warning("Failed to save checkpoint")

        # Print summary
        logger.info(f"Merge Request Created:     {self.stats['mr_created']:>6}")
        logger.info(f"Merge Request Merged:      {self.stats['mr_merged']:>6}")
        logger.info(f"Merge Request Approved:    {self.stats['mr_approved']:>6}")
        logger.info(f"Code Committed:            {self.stats['code_committed']:>6}")
        logger.info(f"Code Pushed:               {self.stats['code_pushed']:>6}")
        logger.info(f"Initial Push:              {self.stats['initial_push']:>6}")
        logger.info(f"Branch Deleted:            {self.stats['branch_deleted']:>6}")
        logger.info(f"Tag Created:               {self.stats['tag_created']:>6}")
        logger.info(f"Total Events:              {total_events:>6}")
        logger.info(f"Inserted to DB:            {inserted_count:>6}")
        logger.info(f"Duplicates Skipped:        {duplicate_count:>6}")

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Extract GitLab data")
    parser.add_argument('-p', '--product', help='Product name (if provided, saves to database; otherwise saves to CSV)')
    parser.add_argument('-s', '--start-date', help='Start date (YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    extractor = GitLabExtractor()
    
    if args.product is None:
        # CSV Mode: Load configuration from config.json
        config = json.load(open(os.path.join(common_dir, "config.json")))
        
        # Build config dictionary
        repos_str = config.get("GITLAB_REPOS", '')
        repos_list = [repo.strip() for repo in repos_str.split(",") if repo.strip()]

        # Get base URL from config
        gitlab_api_url = config.get('GITLAB_API_URL', 'https://gitlab.com/api/v4')
        # Remove /api/v4 suffix if present
        base_url = gitlab_api_url.rstrip('/')
        if base_url.endswith('/api/v4'):
            base_url = base_url[:-7]
        if not base_url.startswith(('http://', 'https://')):
            base_url = f"https://{base_url}"

        config = {
            'base_url': base_url,
            'api_token': config.get('GITLAB_API_TOKEN'),
            'project': config.get('GITLAB_PROJECT'),
            'repos': repos_list
        }

        # Use checkpoint file for last modified date
        last_modified = Utils.load_checkpoint("gitlab")

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


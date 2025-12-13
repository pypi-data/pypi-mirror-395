#!/usr/bin/env python3
"""
Azure DevOps Repos Data Extraction Script

This script extracts code events from Azure DevOps repositories and saves them page-by-page to the database.

Usage:
    python extract_azuredevops_repos.py [-p <product_name>] [-s <start_date>]

Arguments:
    -p, --product: Product name (if provided, saves to database; otherwise saves to CSV)
    -s, --start-date: Start date for extraction in YYYY-MM-DD format (optional)

Modes (automatically determined):
    Fast mode (when -s is provided):
        - Used for initial bulk extraction with explicit start date
        - Extracts basic events from standard APIs
        - Pull Request Approved events (one per approver, using PR closed_dt or created_dt)
        - Code Committed events without target_branch
        - Faster but uses approximate timestamps for approvals
        - All events saved page-by-page to database

    Enriched mode (when -s is NOT provided, using last_modified_date):
        - Used for incremental updates
        - Pull Request Created/Merged saved page-by-page
        - Pull Request Approved with ACTUAL timestamps from /threads API (saved per PR)
        - Code Committed with target_branch from /pushes/{id}/commits API (saved per push)
        - Slower but more complete and accurate data
        - Enrichment happens immediately after each page (not as separate phase)

Events extracted:
    All modes:
    - Pull Request Created
    - Pull Request Merged
    - Pull Request Approved (individual approver events)
    - Code Pushed
    - Initial Push (first push to a branch)
    - Branch Deleted
    - Tag Created
    - Tag Deleted

    Fast mode only:
    - Code Committed (without target_branch)
    - Pull Request Approved uses closed_dt or created_dt (approximate)

    Enriched mode only:
    - Pull Request Approved with actual approval timestamps from threads
    - Code Committed (with accurate target_branch from pushes)

Note:
    - Merge commits (identified by message patterns) are excluded from Code Committed events
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
logger = logging.getLogger('extract_azuredevops_repos')

# Set logger for CodeCommitEvent
CodeCommitEvent.LOGGER = logger

class AzureDevOpsReposExtractor:
    """Extracts code events from Azure DevOps repositories with page-by-page processing."""

    def __init__(self):

        # Statistics
        self.stats = {
            'pr_created': 0,
            'pr_merged': 0,
            'pr_approved': 0,
            'code_committed': 0,
            'code_pushed': 0,
            'initial_push': 0,
            'branch_deleted': 0,
            'tag_created': 0,
            'tag_deleted': 0,
            'total_inserted': 0,
            'total_duplicates': 0
        }

    def get_config_from_database(self, cursor) -> Dict:
        """Get Azure DevOps configuration from data_source_config table."""
        query = """
        SELECT config_item, config_value
        FROM data_source_config
        WHERE data_source = 'source_code_revision_control'
        AND config_item IN ('Organization', 'Personal Access Token', 'Repos', 'Projects')
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
                config['org_url'] = config_value
            elif config_item == 'Personal Access Token':
                config['api_token'] = config_value
            elif config_item == 'Projects':
                try:
                    projects = json.loads(config_value) if config_value else []
                    config['project'] = projects[0] if projects else None
                except (json.JSONDecodeError, TypeError):
                    config['project'] = None

        return config

    # ============================================================================
    # HELPER FUNCTIONS
    # ============================================================================

    def _is_merge_commit(self, commit_message: str) -> bool:
        """
        Check if a commit message indicates a merge commit.
        
        Returns:
            True if this is a merge commit, False otherwise
        """
        if not commit_message:
            return False
        
        merge_patterns = [
            r"^[Mm]erged PR \d+:",
            r"^[Mm]erge pull request #\d+",
            r"^[Mm]erge branch .+ into .+",
        ]
        
        for pattern in merge_patterns:
            if re.match(pattern, commit_message):
                return True
        
        return False

    # ============================================================================
    # API FUNCTIONS
    # ============================================================================

    def fetch_refs_and_save_tag_events(self, org_url: str, project: str, repo_id: str, repo_name: str, api_token: str, save_output) -> Dict[str, str]:
        """
        Fetch all refs and save Tag Created events from refs API.
        Also returns tag-to-commit mapping for push processing.

        Tag Created events from refs have:
        - target_branch = tag_name
        - revision = peeled_object_id
        - comment = object_id
        - repo = repo_name

        Returns:
            Dict mapping tag name to peeled commit ID
        """
        url = f"{org_url}/{project}/_apis/git/repositories/{repo_id}/refs"
        params = {
            'filter': 'tags',
            'peelTags': 'true',
            'api-version': '7.1'
        }

        logger.info(f"[Refs] Fetching refs for repo '{repo_id}'...")

        data = self._make_api_request(url, api_token, params)

        if not data or not isinstance(data, dict):
            logger.warning(f"[Refs] No data returned for repo '{repo_id}'")
            return {}

        refs = data.get('value', [])
        tag_to_commit = {}
        tag_events = []

        for ref in refs:
            name = ref.get('name', '')
            if not name.startswith('refs/tags/'):
                continue

            tag_name = name.replace('refs/tags/', '')
            peeled_id = ref.get('peeledObjectId')
            object_id = ref.get('objectId')
            commit_id = peeled_id or object_id

            if commit_id:
                tag_to_commit[tag_name] = commit_id

                # Create Tag Created event from refs
                # Note: No timestamp_utc from refs API
                tag_events.append(CodeCommitEvent.create_event(
                    timestamp_utc=None,
                    repo_name=repo_name,
                    event_type='Tag Created',
                    source_branch='',
                    target_branch=tag_name,
                    revision=commit_id if commit_id else '',
                    author='',
                    comment=object_id if object_id else ''
                ))

        logger.info(f"[Refs] Found {len(tag_to_commit)} tags")

        # Save tag events from refs to database
        # Note: These events have NULL timestamp_utc since refs API doesn't provide timestamps
        if tag_events:
            total, inserted, duplicates = save_output(tag_events, repo_name, "tags")
            logger.info(f"[Refs] Saved {len(tag_events)} Tag Created events from refs ({inserted} inserted, {duplicates} duplicates)")

        return tag_to_commit

    def _make_api_request(self, url: str, api_token: str, params: Dict = None) -> Optional[Dict]:
        """
        Make an API request to Azure DevOps with retry logic.

        Args:
            url: Full API URL
            api_token: Azure DevOps Personal Access Token
            params: Query parameters

        Returns:
            Response JSON as dict, or None if request fails
        """
        headers = {'Content-Type': 'application/json'}
        auth = ("", api_token)

        # Log the API URL
        if params:
            param_str = "&".join([f"{k}={v}" for k, v in params.items()])
            logger.info(f"[API] GET {url}?{param_str}")
        else:
            logger.info(f"[API] GET {url}")

        max_retries = 3
        retry_delay = 1

        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=headers, auth=auth, params=params, timeout=30)

                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 403:
                    # Rate limit exceeded
                    if 'X-RateLimit-Reset' in response.headers:
                        reset_time = int(response.headers['X-RateLimit-Reset'])
                        wait_time = reset_time - int(time.time()) + 10
                        logger.warning(f"Rate limit exceeded. Waiting {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        logger.warning(f"Rate limit exceeded, no reset time provided")
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

        return None

    # ============================================================================
    # PULL REQUEST PROCESSING
    # ============================================================================

    def fetch_pr_threads(self, org_url: str, project: str, repo_id: str, pr_id: int, api_token: str) -> List[Dict]:
        """
        Fetch threads for a specific pull request to get approval information.
        """
        url = f"{org_url}/{project}/_apis/git/repositories/{repo_id}/pullRequests/{pr_id}/threads"
        params = {'api-version': '7.1'}

        data = self._make_api_request(url, api_token, params)

        if not data or not isinstance(data, dict):
            return []

        return data.get('value', [])

    def fetch_push_commits(self, org_url: str, project: str, repo_id: str, push_id: int, api_token: str) -> List[Dict]:
        """
        Fetch commits for a specific push.
        """
        url = f"{org_url}/{project}/_apis/git/repositories/{repo_id}/pushes/{push_id}/commits"
        params = {'api-version': '7.1'}

        data = self._make_api_request(url, api_token, params)

        if not data or not isinstance(data, dict):
            return []

        return data.get('value', [])

    def fetch_and_process_pull_requests(
        self,
        org_url: str,
        project: str,
        repo_id: str,
        repo_name: str,
        api_token: str,
        start_date: datetime,
        save_output,
        fast_mode: bool = True
    ):
        """
        Fetch pull requests page-by-page and save to database after each page.

        In fast mode: Save PR Created, Merged, and Approved (with closed_dt/created_dt) after each page
        In enriched mode: Save PR Created and Merged after each page, then enrich Approved events
                         with actual timestamps from threads API (per PR after each page)
        """
        url = f"{org_url}/{project}/_apis/git/repositories/{repo_id}/pullrequests"
        params = {
            'searchCriteria.status': 'all',
            'searchCriteria.minTime': start_date.isoformat(),
            '$top': 100,
            'api-version': '7.1'
        }

        skip = 0
        page_num = 1

        while True:
            params['$skip'] = skip
            logger.info(f"[PR] Fetching page {page_num} for repo '{repo_name}' (skip={skip})...")

            data = self._make_api_request(url, api_token, params)

            if not data or not isinstance(data, dict):
                logger.warning(f"[PR] No data returned for repo '{repo_name}'")
                break

            prs = data.get('value', [])
            if not prs:
                logger.info(f"[PR] No more pull requests for repo '{repo_name}'")
                break

            # Process PRs from this page
            events = []
            for pr in prs:
                events.extend(self._extract_pr_events(pr, repo_name, fast_mode))

            # Save immediately after each page
            if events:
                total, inserted, duplicates = save_output(events, repo_name, "pull_requests")
                self.stats['total_inserted'] += inserted
                self.stats['total_duplicates'] += duplicates
                logger.info(f"[PR] Page {page_num}: {len(events)} events ({inserted} inserted, {duplicates} duplicates)")

            # In enriched mode, collect all approval events for batching
            all_approval_events = []
            if not fast_mode:
                for pr in prs:
                    pr_id = pr.get('pullRequestId')
                    if not pr_id or not self.is_pr_approved(pr):
                        continue

                    try:
                        # Fetch threads for this PR
                        threads = self.fetch_pr_threads(org_url, project, repo_name, pr_id, api_token)

                        if not threads:
                            continue

                        # Parse approval timestamps from threads
                        approvals = self.parse_approval_timestamps_from_threads(threads)

                        if not approvals:
                            continue

                        # Extract PR details
                        title = pr.get('title', '')
                        source_branch = pr.get('sourceRefName', '').replace('refs/heads/', '')
                        target_branch = pr.get('targetRefName', '').replace('refs/heads/', '')
                        revision = pr.get('lastMergeCommit', {}).get('commitId', '')

                        # Extended attributes for PR events
                        extended_attrs = {
                            'pull_request_number': pr_id,
                            'pull_request_title': title
                        }

                        # Create approval events with actual timestamps
                        for approval in approvals:
                            approval_dt = Utils.convert_to_utc(approval['approval_timestamp'])
                            if not approval_dt:
                                continue

                            all_approval_events.append(CodeCommitEvent.create_event(
                                timestamp_utc=approval_dt,
                                repo_name=repo_name,
                                event_type='Pull Request Approved',
                                source_branch=source_branch,
                                target_branch=target_branch,
                                revision=revision,
                                author=approval['approver_name'],
                                comment=title,
                                extended_attributes=extended_attrs
                            ))
                            self.stats['pr_approved'] += 1

                    except Exception as e:
                        logger.error(f"[PR Approval] Error enriching PR {pr_id}: {e}")
                        continue

                # Save all approval events in batch
                if all_approval_events:
                    total, inserted, duplicates = save_output(all_approval_events, repo_name, "pull_requests")
                    self.stats['total_inserted'] += inserted
                    self.stats['total_duplicates'] += duplicates
                    logger.info(f"[PR Approval] Batch saved {len(all_approval_events)} approval events ({inserted} inserted, {duplicates} duplicates)")

            skip += len(prs)
            page_num += 1

            # Check if this is the last page
            if len(prs) < 100:
                break

        logger.info(f"[PR] Completed processing pull requests for repo '{repo_name}'")

    def is_pr_approved(self, pr: Dict) -> bool:
        """
        Check if PR is approved by checking reviewers' votes.
        Returns True if all reviewers have approved (no negative votes).
        """
        if 'reviewers' not in pr:
            return False

        reviewers = pr.get('reviewers', [])
        if not reviewers:
            return False

        # Check if all reviewers have positive votes (vote == 10 means approved)
        negative_votes = [r for r in reviewers if r.get('vote', 0) != 10]
        return len(negative_votes) == 0

    def _extract_pr_events(self, pr: Dict, repo_name: str, fast_mode: bool = True) -> List[Dict]:
        """
        Extract PR Created, PR Approved, and PR Merged events from a pull request.

        In fast mode:
        - Creates PR Created, Merged, and Approved (with closed_dt/created_dt) events

        In enriched mode:
        - Creates only PR Created and Merged events
        - Approved events are created separately during enrichment with actual timestamps
        """
        events = []

        pr_id = pr.get('pullRequestId')
        title = pr.get('title', '')
        description = pr.get('description', '')
        source_branch = pr.get('sourceRefName', '').replace('refs/heads/', '')
        target_branch = pr.get('targetRefName', '').replace('refs/heads/', '')
        author = pr.get('createdBy', {}).get('displayName', '')
        status = pr.get('status', '')
        revision = pr.get('lastMergeCommit', {}).get('commitId', '')

        # Parse creation date
        created_dt = Utils.convert_to_utc(pr.get('creationDate'))
        if not created_dt:
            return events

        # Parse closed date
        closed_dt = Utils.convert_to_utc(pr.get('closedDate')) if status == 'completed' else None

        # Extended attributes for PR events
        extended_attrs = {
            'pull_request_number': pr_id,
            'pull_request_title': title
        }

        # PR Created event
        events.append(CodeCommitEvent.create_event(
            timestamp_utc=created_dt,
            repo_name=repo_name,
            event_type='Pull Request Created',
            source_branch=source_branch,
            target_branch=target_branch,
            revision=revision,
            author=author,
            comment=description,
            extended_attributes=extended_attrs
        ))
        self.stats['pr_created'] += 1

        # PR Approved events (only in fast mode)
        # In enriched mode, approval events are created during enrichment with actual timestamps
        if fast_mode and self.is_pr_approved(pr):
            # Use closed_date if PR is completed, otherwise use created_date
            approval_dt = closed_dt if status == 'completed' else created_dt

            reviewers = pr.get('reviewers', [])

            # Fast mode: Create one event per approver using closed_dt or created_dt
            for reviewer in reviewers:
                if reviewer.get('vote', 0) == 10:
                    approver_name = reviewer.get('displayName', '') or reviewer.get('uniqueName', '')
                    if approver_name:
                        events.append(CodeCommitEvent.create_event(
                            timestamp_utc=approval_dt,
                            repo_name=repo_name,
                            event_type='Pull Request Approved',
                            source_branch=source_branch,
                            target_branch=target_branch,
                            revision=revision,
                            author=approver_name,
                            comment=title,
                            extended_attributes=extended_attrs
                        ))
                        self.stats['pr_approved'] += 1

        # PR Merged event (if completed)
        if status == 'completed' and closed_dt:
            events.append(CodeCommitEvent.create_event(
                timestamp_utc=closed_dt,
                repo_name=repo_name,
                event_type='Pull Request Merged',
                source_branch=source_branch,
                target_branch=target_branch,
                revision=revision,
                author=author,
                comment=title,
                extended_attributes=extended_attrs
            ))
            self.stats['pr_merged'] += 1

        return events

    def parse_approval_timestamps_from_threads(self, threads: List[Dict]) -> List[Dict]:
        """
        Parse threads to extract individual approval timestamps for each approver.

        Returns list of dicts with 'approver_name' and 'approval_timestamp'
        """
        approvals = []

        for thread in threads:
            comments = thread.get('comments', [])
            properties = thread.get('properties', {})

            for comment in comments:
                author = comment.get('author', {})
                published_date = comment.get('publishedDate')
                comment_properties = comment.get('properties', {})

                # Check for vote information in comment properties
                vote_result = None
                if 'CodeReviewVoteResult' in comment_properties:
                    vote_result_obj = comment_properties.get('CodeReviewVoteResult', {})
                    vote_result = vote_result_obj.get('$value') if isinstance(vote_result_obj, dict) else vote_result_obj

                if not vote_result and 'Microsoft.VisualStudio.Services.CodeReview.Vote' in comment_properties:
                    vote_obj = comment_properties.get('Microsoft.VisualStudio.Services.CodeReview.Vote', {})
                    vote_result = vote_obj.get('$value') if isinstance(vote_obj, dict) else vote_obj

                # Vote value of 10 means approved
                if vote_result and str(vote_result) == '10':
                    if author and published_date:
                        approvals.append({
                            'approver_name': author.get('displayName', author.get('uniqueName', '')),
                            'approval_timestamp': published_date
                        })

            # Also check thread-level properties for vote information
            if 'CodeReviewVoteResult' in properties:
                vote_result_obj = properties.get('CodeReviewVoteResult', {})
                vote_result = vote_result_obj.get('$value') if isinstance(vote_result_obj, dict) else vote_result_obj

                if vote_result and str(vote_result) == '10':
                    # Get the first comment author as the voter
                    if comments and len(comments) > 0:
                        first_comment = comments[0]
                        author = first_comment.get('author', {})
                        published_date = first_comment.get('publishedDate')

                        if author and published_date:
                            approvals.append({
                                'approver_name': author.get('displayName', author.get('uniqueName', '')),
                                'approval_timestamp': published_date
                            })

        return approvals

    # ============================================================================
    # COMMIT PROCESSING
    # ============================================================================

    def fetch_and_process_commits(
        self,
        org_url: str,
        project: str,
        repo_id: str,
        repo_name: str,
        api_token: str,
        start_date: datetime,
        save_output
    ):
        """
        Fetch commits page-by-page and save to database after each page.
        Note: Commits do not include target_branch information.
        """
        url = f"{org_url}/{project}/_apis/git/repositories/{repo_id}/commits"
        params = {
            'searchCriteria.fromDate': start_date.isoformat(),
            '$top': 100,
            'api-version': '7.1'
        }

        skip = 0
        page_num = 1

        while True:
            params['$skip'] = skip
            logger.info(f"[Commit] Fetching page {page_num} for repo '{repo_name}' (skip={skip})...")

            data = self._make_api_request(url, api_token, params)

            if not data or not isinstance(data, dict):
                logger.warning(f"[Commit] No data returned for repo '{repo_name}'")
                break

            commits = data.get('value', [])
            if not commits:
                logger.info(f"[Commit] No more commits for repo '{repo_name}'")
                break

            # Process commits from this page
            events = []
            for commit in commits:
                event = self._extract_commit_event(commit, repo_name)
                if event:
                    events.append(event)

            # Save this page's events to database
            if events:
                total, inserted, duplicates = save_output(events, repo_name, "commits")
                self.stats['total_inserted'] += inserted
                self.stats['total_duplicates'] += duplicates
                logger.info(f"[Commit] Page {page_num}: {len(events)} events ({inserted} inserted, {duplicates} duplicates)")

            skip += len(commits)
            page_num += 1

            # Check if this is the last page
            if len(commits) < 100:
                break

        logger.info(f"[Commit] Completed processing commits for repo '{repo_name}'")

    def _extract_commit_event(self, commit: Dict, repo_name: str) -> Optional[Dict]:
        """Extract Code Committed event from a commit (without target_branch info)."""
        commit_id = commit.get('commitId', '')
        comment = commit.get('comment', '')
        author = commit.get('author', {}).get('name', '')

        # Parse commit date
        commit_dt = Utils.convert_to_utc(commit.get('author', {}).get('date'))
        if not commit_dt:
            return None

        # Skip merge commits (identified by message pattern)
        # Note: Azure DevOps /commits API doesn't provide parent information
        if self._is_merge_commit(comment):
            return None

        self.stats['code_committed'] += 1

        return CodeCommitEvent.create_event(
            timestamp_utc=commit_dt,
            repo_name=repo_name,
            event_type='Code Committed',
            source_branch='',
            target_branch='',  # Not available in /commits API
            revision=commit_id,
            author=author,
            comment=comment
        )

    # ============================================================================
    # PUSH PROCESSING
    # ============================================================================

    def fetch_and_process_pushes(
        self,
        org_url: str,
        project: str,
        repo_id: str,
        repo_name: str,
        api_token: str,
        start_date: datetime,
        tag_to_commit: Dict[str, str],
        save_output,
        fast_mode: bool = True
    ):
        """
        Fetch pushes page-by-page and save to database after each page.
        Extracts: Code Pushed, Initial Push, Branch Deleted, Tag Created, Tag Deleted events.

        In enriched mode: After saving each page, enriches Code Committed events with target_branch
                         by calling /pushes/{pushId}/commits API per push and saving immediately.
        """
        url = f"{org_url}/{project}/_apis/git/repositories/{repo_id}/pushes"
        params = {
            'searchCriteria.includeRefUpdates': 'true',
            'searchCriteria.fromDate': start_date.isoformat(),
            '$top': 100,
            'api-version': '7.1'
        }

        skip = 0
        page_num = 1

        while True:
            params['$skip'] = skip
            logger.info(f"[Push] Fetching page {page_num} for repo '{repo_name}' (skip={skip})...")

            data = self._make_api_request(url, api_token, params)

            if not data or not isinstance(data, dict):
                logger.warning(f"[Push] No data returned for repo '{repo_name}'")
                break

            pushes = data.get('value', [])
            if not pushes:
                logger.info(f"[Push] No more pushes for repo '{repo_name}'")
                break

            # Process pushes from this page
            events = []
            push_ids_for_commits = []  # Track push IDs for commit enrichment

            for push in pushes:
                events.extend(self._extract_push_events(push, repo_name, tag_to_commit))

                # In enriched mode, collect push IDs with branch refs for commit enrichment
                if not fast_mode:
                    push_id = push.get('pushId')
                    ref_updates = push.get('refUpdates', [])

                    for ref_update in ref_updates:
                        ref_name = ref_update.get('name', '')
                        # Only collect pushes with branch refs (refs/heads/)
                        if ref_name.startswith('refs/heads/'):
                            branch_name = ref_name.replace('refs/heads/', '')
                            old_object_id = ref_update.get('oldObjectId', '')
                            new_object_id = ref_update.get('newObjectId', '')

                            # Skip branch deletion (newObjectId is all zeros)
                            if new_object_id == "0000000000000000000000000000000000000000":
                                continue

                            if push_id and branch_name:
                                push_ids_for_commits.append((push_id, branch_name))
                            break  # Only need one branch per push

            # Save this page's events to database
            if events:
                total, inserted, duplicates = save_output(events, repo_name, "pushes")
                self.stats['total_inserted'] += inserted
                self.stats['total_duplicates'] += duplicates
                logger.info(f"[Push] Page {page_num}: {len(events)} events ({inserted} inserted, {duplicates} duplicates)")

            # In enriched mode, collect all commit events for batching
            all_commit_events = []
            if not fast_mode and push_ids_for_commits:
                for push_id, branch_name in push_ids_for_commits:
                    try:
                        # Fetch commits for this push
                        commits = self.fetch_push_commits(org_url, project, repo_id, push_id, api_token)

                        if not commits:
                            continue

                        # Create Code Committed events with target_branch from push
                        for commit in commits:
                            commit_id = commit.get('commitId', '')
                            comment = commit.get('comment', '')
                            author = commit.get('author', {}).get('name', '')

                            # Parse commit date
                            commit_dt = Utils.convert_to_utc(commit.get('author', {}).get('date'))
                            if not commit_dt:
                                continue

                            # Skip merge commits (identified by message pattern)
                            if self._is_merge_commit(comment):
                                continue

                            all_commit_events.append(CodeCommitEvent.create_event(
                                timestamp_utc=commit_dt,
                                repo_name=repo_name,
                                event_type='Code Committed',
                                source_branch='',
                                target_branch=branch_name,  # From push ref
                                revision=commit_id,
                                author=author,
                                comment=comment
                            ))
                            self.stats['code_committed'] += 1

                    except Exception as e:
                        logger.error(f"[Commit Enrichment] Error processing push {push_id}: {e}")
                        continue

                # Save all commit events in batch
                if all_commit_events:
                    total, inserted, duplicates = save_output(all_commit_events, repo_name, "pushes")
                    self.stats['total_inserted'] += inserted
                    self.stats['total_duplicates'] += duplicates
                    logger.info(f"[Commit Enrichment] Batch saved {len(all_commit_events)} commit events ({inserted} inserted, {duplicates} duplicates)")

            skip += len(pushes)
            page_num += 1

            # Check if this is the last page
            if len(pushes) < 100:
                break

        logger.info(f"[Push] Completed processing pushes for repo '{repo_name}'")

    def _extract_push_events(self, push: Dict, repo_name: str, tag_to_commit: Dict[str, str]) -> List[Dict]:
        """
        Extract push-related events from a push.

        Args:
            push: Push data from API
            repo_name: Repository name
            tag_to_commit: Mapping of tag names to commit IDs (not used for Tag Created)

        Events:
        - Code Pushed: Normal push to a branch
        - Initial Push: First push to a branch (oldObjectId is all zeros)
        - Branch Deleted: Branch deletion (newObjectId is all zeros)
        - Tag Created: Tag creation from pushes (revision empty, new_object_id in comment)
        - Tag Deleted: Tag deletion

        Note: Tag Created events from pushes have:
        - revision = empty
        - comment = new_object_id
        This pairs with Tag Created events from refs API for later merging.
        """
        events = []

        # Parse push date
        push_dt = Utils.convert_to_utc(push.get('date'))
        if not push_dt:
            return events

        # Get pusher information
        pusher = push.get('pushedBy', {})
        author = pusher.get('displayName', '') or pusher.get('uniqueName', '')

        # Process each refUpdate
        ref_updates = push.get('refUpdates', [])
        for ref_update in ref_updates:
            old_object_id = ref_update.get('oldObjectId', '')
            new_object_id = ref_update.get('newObjectId', '')
            ref_name = ref_update.get('name', '')

            # Handle TAG refs (refs/tags/)
            if ref_name.startswith('refs/tags/'):
                tag_name = ref_name.replace('refs/tags/', '')

                # Tag Created
                if old_object_id == "0000000000000000000000000000000000000000":
                    # Tag Created event from pushes: revision empty, new_object_id in comment
                    events.append(CodeCommitEvent.create_event(
                        timestamp_utc=push_dt,
                        repo_name=repo_name,
                        event_type='Tag Created',
                        source_branch='',
                        target_branch=tag_name,
                        revision='',  # Leave revision empty for pushes
                        author=author,
                        comment=new_object_id  # Put new_object_id in comment
                    ))
                    self.stats['tag_created'] += 1

                # Tag Deleted
                elif new_object_id == "0000000000000000000000000000000000000000":
                    events.append(CodeCommitEvent.create_event(
                        timestamp_utc=push_dt,
                        repo_name=repo_name,
                        event_type='Tag Deleted',
                        source_branch='',
                        target_branch=tag_name,
                        revision=old_object_id,
                        author=author,
                        comment=f"Tag '{tag_name}' deleted"
                    ))
                    self.stats['tag_deleted'] += 1

                continue

            # Handle BRANCH refs (refs/heads/)
            if not ref_name.startswith('refs/heads/'):
                continue

            # Extract branch name
            branch_name = ref_name.replace('refs/heads/', '')

            # Determine event type based on objectIds
            if old_object_id == "0000000000000000000000000000000000000000":
                event_type = 'Initial Push'
                self.stats['initial_push'] += 1
            elif new_object_id == "0000000000000000000000000000000000000000":
                event_type = 'Branch Deleted'
                self.stats['branch_deleted'] += 1
            else:
                event_type = 'Code Pushed'
                self.stats['code_pushed'] += 1

            events.append(CodeCommitEvent.create_event(
                timestamp_utc=push_dt,
                repo_name=repo_name,
                event_type=event_type,
                target_branch=branch_name,
                revision=new_object_id,
                author=author
            ))

        return events

    # ============================================================================
    # MAIN ORCHESTRATION
    # ============================================================================

    def run_extraction(self, cursor, config: Dict, start_date: datetime, last_modified, export_path: str = None):
        """
        Run extraction: fetch and save data page-by-page.

        Args:
            cursor: Database cursor (None for CSV mode)
            start_date: Start date for extraction
            config: Configuration dictionary with org_url, api_token, project, repos
            fast_mode: If True, skip enrichment; if False, perform enrichment for approvals and commits
            export_path: Export path for CSV mode
        """
        # Track maximum timestamp for checkpoint saving
        max_timestamp = None

        if not config.get('org_url') or not config.get('api_token'):
            logger.error("Missing required configuration: Organization or Personal Access Token")
            sys.exit(1)

        if not config.get('project'):
            logger.error("Missing required configuration: Project")
            sys.exit(1)

        if not config.get('repos'):
            logger.error("No repositories configured")
            sys.exit(1)

        org_url = config.get('org_url')
        api_token = config.get('api_token')
        project = config.get('project')
        repos = config.get('repos', [])

        if not org_url.startswith('http'):
            org_url = f"https://dev.azure.com/{org_url}"

        # Determine start date and mode
        # If explicit start_date provided: use fast mode (for bulk extraction)
        # If last_modified exists and is not default: use enriched mode (for incremental updates)
        # If no last_modified or default date: use fast mode (for bulk extraction)
        if start_date:
            start_date = datetime.fromisoformat(start_date)
            if start_date.tzinfo is None:
                start_date = start_date.replace(tzinfo=timezone.utc)
            fast_mode = True
        else:
            # Check if last_modified is the default date (2000-01-01) or None
            default_date = datetime(2000, 1, 1, tzinfo=timezone.utc)
            if last_modified and last_modified != default_date:
                start_date = last_modified
                fast_mode = False
            else:
                start_date = datetime(2024, 1, 1, tzinfo=timezone.utc)
                fast_mode = True

        mode_str = "FAST" if fast_mode else "ENRICHED"
        logger.info(f"Starting {mode_str} extraction from {start_date}")
        logger.info(f"Organization: {org_url}")
        logger.info(f"Project: {project}")
        logger.info(f"Repositories: {', '.join(repos)}")

        # Set up function wrappers to avoid repeated if checks
        if cursor:
            # Database mode
            save_output = lambda events, repo_name, event_type: CodeCommitEvent.save_events_to_database(events, cursor)
        else:
            # CSV mode - create CSV file at the start
            csv_file = Utils.create_csv_file("azuredevops_repos_events", export_path, logger)
            def save_output_with_tracking(events, repo_name, event_type):
                result = Utils.save_events_to_csv(events, csv_file, logger)
                # Track maximum timestamp for checkpoint
                if len(result) == 4 and result[3]:  # result[3] is max_ts
                    nonlocal max_timestamp
                    if not max_timestamp or result[3] > max_timestamp:
                        max_timestamp = result[3]
                return result[:3]  # Return first 3 values for compatibility
            save_output = save_output_with_tracking

        # Process each repository
        for repo_name in repos:
            logger.info(f"Processing repository: {repo_name}")

            repo_id = repo_name  # Azure DevOps uses repo name as ID

            try:
                # 1. Pull Requests
                logger.info(f"[{repo_name}] Extracting Pull Requests...")
                self.fetch_and_process_pull_requests(
                    org_url, project, repo_id, repo_name, api_token, start_date, save_output, fast_mode
                )

                # 2. Commits (only in fast mode - in enriched mode, commits come from pushes)
                if fast_mode:
                    logger.info(f"[{repo_name}] Extracting Commits...")
                    self.fetch_and_process_commits(
                        org_url, project, repo_id, repo_name, api_token, start_date, save_output
                    )

                # 3. Fetch refs and save Tag Created events from refs API
                logger.info(f"[{repo_name}] Fetching refs for tags...")
                tag_to_commit = self.fetch_refs_and_save_tag_events(org_url, project, repo_id, repo_name, api_token, save_output)

                # 4. Pushes (Code Pushed, Initial Push, Branch Deleted, Tag Created, Tag Deleted)
                logger.info(f"[{repo_name}] Extracting Pushes and Tags...")
                self.fetch_and_process_pushes(
                    org_url, project, repo_id, repo_name, api_token, start_date, tag_to_commit, save_output, fast_mode
                )

            except Exception as e:
                logger.error(f"Error processing repository '{repo_name}': {e}")
                continue

        # Save checkpoint in CSV mode
        if not cursor and max_timestamp:
            if Utils.save_checkpoint(prefix="azuredevops_repos", last_dt=max_timestamp, export_path=export_path):
                logger.info(f"Checkpoint saved successfully: {max_timestamp}")
            else:
                logger.warning("Failed to save checkpoint")

        # Print summary statistics
        self._print_summary()

    def _print_summary(self):
        """Print extraction summary statistics."""
        logger.info(f"Pull Request Created:  {self.stats['pr_created']:>6}")
        logger.info(f"Pull Request Merged:   {self.stats['pr_merged']:>6}")
        logger.info(f"Pull Request Approved: {self.stats['pr_approved']:>6}")
        logger.info(f"Code Committed:        {self.stats['code_committed']:>6}")
        logger.info(f"Code Pushed:           {self.stats['code_pushed']:>6}")
        logger.info(f"Initial Push:          {self.stats['initial_push']:>6}")
        logger.info(f"Branch Deleted:        {self.stats['branch_deleted']:>6}")
        logger.info(f"Tag Created:           {self.stats['tag_created']:>6}")
        logger.info(f"Tag Deleted:           {self.stats['tag_deleted']:>6}")

        total_events = sum([
            self.stats['pr_created'],
            self.stats['pr_merged'],
            self.stats['pr_approved'],
            self.stats['code_committed'],
            self.stats['code_pushed'],
            self.stats['initial_push'],
            self.stats['branch_deleted'],
            self.stats['tag_created'],
            self.stats['tag_deleted']
        ])
        logger.info(f"Total Events:          {total_events:>6}")
        logger.info(f"Inserted to DB:        {self.stats['total_inserted']:>6}")
        logger.info(f"Duplicates Skipped:    {self.stats['total_duplicates']:>6}")

def main():
    parser = argparse.ArgumentParser(description="Extract Azure DevOps Repos data")
    parser.add_argument('-p', '--product', help='Product name (if provided, saves to database; otherwise saves to CSV)')
    parser.add_argument('-s', '--start-date', help='Start date (YYYY-MM-DD)')
    args = parser.parse_args()

    extractor = AzureDevOpsReposExtractor()

    if args.product is None:
        # CSV Mode: Load configuration from config.json
        config = json.load(open(os.path.join(common_dir, "config.json")))
        
        # Get configuration from config dictionary
        # comma-separated repos
        repos = config.get("AZDO_REPOS", '')
        repos_list = [repo.strip() for repo in repos.split(",") if repo.strip()]

        config = {
            'org_url': config.get('AZDO_ORGANIZATION'),
            'api_token': config.get('AZDO_API_TOKEN'),
            'project': config.get("AZDO_PROJECT"),
            'repos': repos_list
        }

        # Use checkpoint file for last modified date
        checkpoint_file = "azuredevops_repos"
        last_modified = Utils.load_checkpoint(checkpoint_file)

        extractor.run_extraction(None, config, args.start_date, last_modified)

    else:
        from database import DatabaseConnection
        db = DatabaseConnection()
        with db.product_scope(args.product) as conn:
            with conn.cursor() as cursor:
                config = extractor.get_config_from_database(cursor)
                last_modified = CodeCommitEvent.get_last_event(cursor)
                extractor.run_extraction(cursor, config, args.start_date, last_modified)

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)

#!/usr/bin/env python3
"""
BitBucket Pipelines Data Extraction Script

This script extracts pipeline events from BitBucket and inserts them directly into the database.
It follows the same structure as extract_jira.py but uses BitBucket REST API.

Usage:
    python extract_bitbucket_pipelines.py -p <product_name> [-s <start_date>]
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from typing import List, Dict, Optional
from urllib.parse import urljoin

base_dir = os.path.dirname(os.path.abspath(__file__))
common_dir = os.path.join(base_dir, "common")
if not os.path.isdir(common_dir):
    # go up one level to find "common" (for installed package structure)
    base_dir = os.path.dirname(base_dir)
    common_dir = os.path.join(base_dir, "common")

if os.path.isdir(common_dir) and base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import requests

from common.utils import Utils

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('bitbucket_pipelines_extractor')


class BitbucketPipelinesExtractor:
    """Extracts build and deployment events from BitBucket pipelines."""

    def __init__(self):
        # Statistics
        self.stats = {
            'build_events_inserted': 0,
            'build_events_duplicates': 0,
            'deployment_events_inserted': 0,
            'deployment_events_duplicates': 0
        }

    def get_config_from_database(self, cursor) -> Dict:
        """Get BitBucket Pipelines configuration from database."""
        query = """
        SELECT config_item, config_value
        FROM data_source_config
        WHERE data_source = 'integration_and_build'
        AND config_item IN ('Workspace', 'Personal Access Token', 'Repos')
        """
        cursor.execute(query)
        results = cursor.fetchall()

        config = {}
        for row in results:
            config_item, config_value = row
            if config_item == 'Repos':
                try:
                    repos = json.loads(config_value)
                    config['repos'] = repos if repos else []
                except (json.JSONDecodeError, TypeError):
                    config['repos'] = []
            elif config_item == 'Workspace':
                config['workspace'] = config_value
            elif config_item == 'Personal Access Token':
                config['api_token'] = config_value

        return config

    def get_last_modified_date(self, cursor) -> Optional[datetime]:
        """Get the last modified date from the database."""
        query = "SELECT MAX(timestamp_utc) FROM build_event"
        cursor.execute(query)
        result = cursor.fetchone()
        if result[0]:
            return result[0]
        else:
            return datetime(2024, 1, 1)

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

        if not config.get('workspace') or not config.get('api_token'):
            logger.error("Missing BitBucket workspace or token in configuration")
            sys.exit(1)

        if not config.get('repos'):
            logger.error("No repositories configured")
            sys.exit(1)

        api_url = config.get('api_url', 'https://api.bitbucket.org/2.0')
        workspace = config.get('workspace')
        api_token = config.get('api_token')
        repos = config.get('repos', [])

        # Determine start date
        if start_date:
            try:
                extraction_start_date = datetime.strptime(start_date, '%Y-%m-%d')
                # Convert to naive UTC datetime
                if extraction_start_date.tzinfo is not None:
                    extraction_start_date = extraction_start_date.astimezone(timezone.utc).replace(tzinfo=None)
            except ValueError:
                logger.error("Invalid date format. Please use YYYY-MM-DD format.")
                sys.exit(1)
        else:
            if last_modified:
                # Convert to naive datetime if timezone-aware
                if last_modified.tzinfo is not None:
                    last_modified = last_modified.replace(tzinfo=None)
                extraction_start_date = last_modified
            else:
                extraction_start_date = datetime(2024, 1, 1)

        # Set up save function
        if cursor:
            # Database mode

            def save_output_fn(events):
                if events:
                    build_inserted, build_duplicates, deploy_inserted, deploy_duplicates = save_events_to_database(events, cursor)
                    self.stats['build_events_inserted'] += build_inserted
                    self.stats['build_events_duplicates'] += build_duplicates
                    self.stats['deployment_events_inserted'] += deploy_inserted
                    self.stats['deployment_events_duplicates'] += deploy_duplicates
                    return build_inserted + deploy_inserted, build_duplicates + deploy_duplicates
                return 0, 0
        else:
            # CSV mode - create CSV files lazily
            build_csv_file = None
            deploy_csv_file = None

            build_columns = [
                'timestamp_utc', 'event', 'repo', 'source_branch',
                'workflow_name', 'build_number', 'comment', 'actor', 'build_id'
            ]
            deploy_columns = [
                'timestamp_utc', 'event', 'build_name', 'repo', 'source_branch',
                'comment', 'environment', 'is_major_release', 'release_version', 'build_id'
            ]

            def save_output_fn(events):
                nonlocal build_csv_file, deploy_csv_file

                # Separate build and deployment events
                build_events = []
                deployment_events = []

                for event in events:
                    if event.get('event_type') == 'Build Created':
                        # Convert created_at to naive UTC datetime for CSV
                        created_at = event.get('created_at')
                        if created_at:
                            if isinstance(created_at, datetime):
                                if created_at.tzinfo is not None:
                                    created_at = created_at.astimezone(timezone.utc).replace(tzinfo=None)
                            else:
                                created_at = datetime.fromisoformat(str(created_at).replace('Z', '+00:00'))
                                if created_at.tzinfo is not None:
                                    created_at = created_at.astimezone(timezone.utc).replace(tzinfo=None)

                            # Map to build_event CSV format
                            build_event_dict = {
                                'timestamp_utc': created_at,
                                'event': event.get('event_type'),
                                'repo': event.get('repo_name', '').lower() if event.get('repo_name') else '',
                                'source_branch': event.get('branch_name', ''),
                                'workflow_name': '',
                                'build_number': event.get('target_iid', ''),
                                'comment': event.get('comment', ''),
                                'actor': event.get('author', 'BitBucket Pipelines'),
                                'build_id': event.get('commit_sha', '')
                            }
                            build_events.append(build_event_dict)
                    elif event.get('event_type') == 'Build Deployed':
                        # Convert created_at to naive UTC datetime for CSV
                        created_at = event.get('created_at')
                        if created_at:
                            if isinstance(created_at, datetime):
                                if created_at.tzinfo is not None:
                                    created_at = created_at.astimezone(timezone.utc).replace(tzinfo=None)
                            else:
                                created_at = datetime.fromisoformat(str(created_at).replace('Z', '+00:00'))
                                if created_at.tzinfo is not None:
                                    created_at = created_at.astimezone(timezone.utc).replace(tzinfo=None)

                            # Map to deployment_event CSV format
                            deploy_event_dict = {
                                'timestamp_utc': created_at,
                                'event': event.get('event_type'),
                                'build_name': event.get('target_iid', ''),
                                'repo': event.get('repo_name', '').lower() if event.get('repo_name') else '',
                                'source_branch': event.get('branch_name', ''),
                                'comment': event.get('comment', ''),
                                'environment': event.get('environment', 'production'),
                                'is_major_release': False,
                                'release_version': '',
                                'build_id': event.get('commit_sha', '')
                            }
                            deployment_events.append(deploy_event_dict)

                # Create CSV files lazily when first events arrive
                if build_events and not build_csv_file:
                    build_csv_file = Utils.create_csv_file("bitbucket_pipelines_build_events", export_path, logger)
                if deployment_events and not deploy_csv_file:
                    deploy_csv_file = Utils.create_csv_file("bitbucket_pipelines_deployment_events", export_path, logger)

                # Save build events
                build_max_ts = None
                if build_events:
                    result = Utils.save_events_to_csv(build_events, build_csv_file, logger)
                    if result[3]:
                        build_max_ts = result[3]

                # Save deployment events
                deploy_max_ts = None
                if deployment_events:
                    result = Utils.save_events_to_csv(deployment_events, deploy_csv_file, logger)
                    if result[3]:
                        deploy_max_ts = result[3]

                # Track maximum timestamp for checkpoint
                nonlocal max_timestamp
                if build_max_ts and (not max_timestamp or build_max_ts > max_timestamp):
                    max_timestamp = build_max_ts
                if deploy_max_ts and (not max_timestamp or deploy_max_ts > max_timestamp):
                    max_timestamp = deploy_max_ts

                total_inserted = len(build_events) + len(deployment_events)
                return total_inserted, 0  # Return inserted and duplicates

        # Log the fetch information
        logger.info(f"Starting extraction from {extraction_start_date}")
        logger.info(f"Fetching data from {api_url}")

        # Process repositories
        all_events = []
        for repo_name in repos:
            logger.info(f"Processing repository: {repo_name}")

            try:
                # Fetch pipelines for this repository
                pipelines = fetch_pipelines(api_url, workspace, api_token, repo_name, extraction_start_date)
                logger.info(f"Found {len(pipelines)} pipelines for repository {repo_name}")

                if pipelines:
                    # Get environment mapping for deployments
                    environment_mapping = get_pipeline_environment_mapping(api_url, workspace, api_token, repo_name)

                    for pipeline in pipelines:
                        # Create events from pipeline
                        events = create_events_from_pipeline(pipeline, repo_name, environment_mapping, min_timestamp=extraction_start_date)
                        if events:
                            all_events.extend(events)
                            # Save events immediately
                            if cursor:
                                build_inserted, build_duplicates = save_output_fn(events)
                            else:
                                inserted, duplicates = save_output_fn(events)

            except Exception as e:
                logger.error(f"Error processing repository {repo_name}: {e}")
                continue

        # Save checkpoint in CSV mode
        if not cursor and max_timestamp:
            if Utils.save_checkpoint(prefix="bitbucket_pipelines", last_dt=max_timestamp, export_path=export_path):
                logger.info(f"Checkpoint saved successfully: {max_timestamp}")
            else:
                logger.warning("Failed to save checkpoint")

        # Print summary
        if cursor:
            total_inserted = self.stats['build_events_inserted'] + self.stats['deployment_events_inserted']
            total_duplicates = self.stats['build_events_duplicates'] + self.stats['deployment_events_duplicates']
            logger.info(f"Total: inserted {total_inserted} events, skipped {total_duplicates} duplicates")
        else:
            logger.info(f"Total events processed: {len(all_events)}")


def fetch_pipelines(api_url: str, workspace: str, api_token: str, repo: str, start_date: datetime) -> List[Dict]:
    """Fetch pipelines for a specific repository since start_date."""
    url = f"{api_url}/repositories/{workspace}/{repo}/pipelines/"
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

    all_pipelines = []
    page = 1

    try:
        while True:
            params = {
                'pagelen': 50,
                'page': page,
                'sort': '-created_on'
            }

            # Retry logic for failed requests
            max_retries = 3
            retry_delay = 1  # seconds

            for attempt in range(max_retries):
                try:
                    response = requests.get(url, headers=headers, params=params, timeout=30)

                    if response.status_code == 200:
                        data = response.json()
                        # Check if data is a dict with expected structure
                        if isinstance(data, dict) and 'values' in data:
                            pipelines = data.get('values', [])
                            if not pipelines:
                                break
                        else:
                            logger.warning(f"Unexpected response format for pipelines in {repo}: {data}")
                            break
                        break
                    elif response.status_code == 429:
                        # Rate limit exceeded
                        if 'Retry-After' in response.headers:
                            wait_time = int(response.headers['Retry-After'])
                            logging.warning(f"Rate limit exceeded. Waiting {wait_time} seconds...")
                            time.sleep(wait_time)
                            continue
                        else:
                            logging.warning("Rate limit exceeded for pipelines")
                            break
                    else:
                        logging.warning(f"Failed to fetch pipelines for {repo}: {response.status_code} - {response.text}")
                        if attempt < max_retries - 1:
                            time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                            continue
                        else:
                            break

                except requests.exceptions.RequestException as e:
                    logging.warning(f"Request failed for pipelines in {repo} (attempt {attempt + 1}): {e}")
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                        continue
                    else:
                        break
                except Exception as ex:
                    logging.error(f"Error fetching pipelines for {repo}: {ex}")
                    break
            else:
                break

            # Filter pipelines since start_date
            filtered_pipelines = []
            for pipeline in pipelines:
                created_on = pipeline.get('created_on')
                if created_on:
                    # Parse ISO datetime and convert to naive UTC
                    pipeline_date = datetime.fromisoformat(created_on.replace('Z', '+00:00'))
                    if pipeline_date.tzinfo is not None:
                        pipeline_date = pipeline_date.astimezone(timezone.utc).replace(tzinfo=None)
                    # Compare with naive start_date
                    if pipeline_date >= start_date:
                        pipeline['repo_name'] = repo
                        pipeline['pipeline_date'] = pipeline_date
                        filtered_pipelines.append(pipeline)
                    else:
                        # Since we're sorted by created_on desc, if we find one older than start_date, we can stop
                        logger.info(f"Reached pipelines older than {start_date}, stopping processing")
                        break

            all_pipelines.extend(filtered_pipelines)

            # Check if we've gone past the start_date (if the last filtered pipeline is older, stop)
            if filtered_pipelines and filtered_pipelines[-1]['pipeline_date'] < start_date:
                break

            # Check if this is the last page
            if len(pipelines) < params['pagelen']:
                break

            page += 1

    except requests.RequestException as e:
        logger.error(f"Error fetching pipelines for repo {repo}: {e}")
        return []

    return all_pipelines


def get_pipeline_steps(api_url: str, workspace: str, api_token: str, repo: str, pipeline_uuid: str) -> List[Dict]:
    """Get detailed steps for a specific pipeline."""
    url = f"{api_url}/repositories/{workspace}/{repo}/pipelines/{pipeline_uuid}/steps"
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        data = response.json()
        return data.get('values', [])

    except requests.RequestException as e:
        logger.error(f"Error fetching pipeline steps for {pipeline_uuid}: {e}")
        return []


def get_pipeline_environment_mapping(api_url: str, workspace: str, api_token: str, repo: str) -> Dict:
    """Get pipeline to environment mapping for deployments."""
    url = f"{api_url}/repositories/{workspace}/{repo}/deployments/"
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

    pipeline_to_env = {}

    try:
        page = 1
        while True:
            params = {'pagelen': 100, 'page': page}
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            deployments = data.get('values', [])

            if not deployments:
                break

            for deployment in deployments:
                release = deployment.get('release', {})
                pipeline = release.get('pipeline', {})
                environment = deployment.get('environment', {})

                pipeline_uuid = pipeline.get('uuid', '')
                environment_uuid = environment.get('uuid', '')

                if pipeline_uuid and environment_uuid:
                    # Get environment name
                    env_url = f"{api_url}/repositories/{workspace}/{repo}/environments/{environment_uuid}"
                    env_response = requests.get(env_url, headers=headers, timeout=30)
                    if env_response.status_code == 200:
                        env_data = env_response.json()
                        env_name = env_data.get('name', '')
                        if env_name:
                            pipeline_to_env[pipeline_uuid] = env_name

            if len(deployments) < 100:
                break
            page += 1

    except requests.RequestException as e:
        logger.error(f"Error fetching environment mapping for repo {repo}: {e}")

    return pipeline_to_env


def create_events_from_pipeline(pipeline: Dict, repo: str, environment_mapping: Dict, min_timestamp=None) -> List[Dict]:
    """Create SDLC events from a BitBucket pipeline."""
    events = []

    pipeline_uuid = pipeline.get('uuid', '')
    pipeline_date = pipeline.get('pipeline_date')
    state = pipeline.get('state', {}).get('name', 'UNKNOWN')
    build_number = pipeline.get('build_number', 0)

    # Get environment from mapping
    environment = environment_mapping.get(pipeline_uuid, 'production')

    # Convert pipeline_date to naive UTC datetime
    if pipeline_date:
        if isinstance(pipeline_date, datetime):
            if pipeline_date.tzinfo is not None:
                pipeline_date = pipeline_date.astimezone(timezone.utc).replace(tzinfo=None)
        else:
            pipeline_date = datetime.fromisoformat(str(pipeline_date).replace('Z', '+00:00'))
            if pipeline_date.tzinfo is not None:
                pipeline_date = pipeline_date.astimezone(timezone.utc).replace(tzinfo=None)
    else:
        return events  # Skip if no valid date

    # Filter: Skip events before or at min_timestamp (checkpoint)
    if min_timestamp and pipeline_date <= min_timestamp:
        return events

    # Create Build Created event for all pipelines
    build_event = {
        'data_source': 'integration_and_build',
        'event_type': 'Build Created',
        'created_at': pipeline_date,
        'author': 'BitBucket Pipelines',
        'target_iid': str(build_number),
        'repo_name': repo,
        'branch_name': '',  # BitBucket pipelines don't always have branch info in the main response
        'commit_sha': '',   # Will be extracted from pipeline details if needed
        'comment': f"Pipeline {build_number} for repository {repo}",
        'environment': environment,
        'test_result': 'SUCCESS' if state == 'COMPLETED' else 'UNKNOWN'
    }
    events.append(build_event)

    # If pipeline is completed, also create a Build Deployed event
    if state == 'COMPLETED':
        deployed_event = build_event.copy()
        deployed_event['event_type'] = 'Build Deployed'
        deployed_event['comment'] = f"Deployment of pipeline {build_number} for repository {repo}"
        events.append(deployed_event)

    return events


def save_events_to_database(events: List[Dict], cursor) -> tuple:
    """Save events to database and return counts."""
    if not events:
        return 0, 0, 0, 0  # build_inserted, build_duplicates, deploy_inserted, deploy_duplicates

    # Separate build and deployment events
    build_events = []
    deployment_events = []

    for event in events:
        if event.get('event_type') == 'Build Created':
            build_events.append(event)
        elif event.get('event_type') == 'Build Deployed':
            deployment_events.append(event)

    build_inserted = 0
    build_duplicates = 0
    deploy_inserted = 0
    deploy_duplicates = 0

    # Insert build events
    if build_events:
        build_inserted, build_duplicates = save_build_events(build_events, cursor)
        logger.info(f"Build events: inserted {build_inserted}, skipped {build_duplicates} duplicates")

    # Insert deployment events
    if deployment_events:
        deploy_inserted, deploy_duplicates = save_deployment_events(deployment_events, cursor)
        logger.info(f"Deployment events: inserted {deploy_inserted}, skipped {deploy_duplicates} duplicates")

    return build_inserted, build_duplicates, deploy_inserted, deploy_duplicates


def save_build_events(events: List[Dict], cursor) -> tuple:
    """Save build events to build_event table."""
    if not events:
        return 0, 0

    from psycopg2.extras import execute_values

    # Get current count for duplicate detection
    count_query = "SELECT COUNT(*) FROM build_event"
    cursor.execute(count_query)
    initial_count = cursor.fetchone()[0]

    # Prepare data for insertion
    values = []
    for event in events:
        values.append((
            event.get('created_at'),
            event.get('event_type'),
            event.get('repo_name', '').lower(),
            event.get('branch_name', ''),
            event.get('commit_sha', ''),
            event.get('target_iid', ''),
            event.get('comment', ''),
            event.get('author', 'BitBucket Pipelines')
        ))

    # Insert build events
    insert_query = """
    INSERT INTO build_event (
        timestamp_utc, event, repo, source_branch, build_id, build_number,
        comment, actor
    ) VALUES %s
    ON CONFLICT ON CONSTRAINT build_event_hash_unique DO NOTHING
    """

    execute_values(cursor, insert_query, values, template=None)

    # Get final count
    cursor.execute(count_query)
    final_count = cursor.fetchone()[0]

    inserted_count = final_count - initial_count
    duplicate_count = len(events) - inserted_count

    return inserted_count, duplicate_count


def save_deployment_events(events: List[Dict], cursor) -> tuple:
    """Save deployment events to deployment_event table."""
    if not events:
        return 0, 0

    from psycopg2.extras import execute_values

    # Get current count for duplicate detection
    count_query = "SELECT COUNT(*) FROM deployment_event"
    cursor.execute(count_query)
    initial_count = cursor.fetchone()[0]

    # Prepare data for insertion
    values = []
    for event in events:
        values.append((
            event.get('created_at'),
            event.get('event_type'),
            event.get('target_iid', ''),  # build_name
            event.get('repo_name', '').lower(),
            event.get('branch_name', ''),
            event.get('commit_sha', ''),
            event.get('comment', ''),
            event.get('environment', 'production'),
            False,  # is_major_release
            ''  # release_version
        ))

    # Insert deployment events
    insert_query = """
    INSERT INTO deployment_event (
        timestamp_utc, event, build_name, repo, source_branch, build_id,
        comment, environment, is_major_release, release_version
    ) VALUES %s
    ON CONFLICT ON CONSTRAINT deployment_event_hash_unique DO NOTHING
    """

    execute_values(cursor, insert_query, values, template=None)

    # Get final count
    cursor.execute(count_query)
    final_count = cursor.fetchone()[0]

    inserted_count = final_count - initial_count
    duplicate_count = len(events) - inserted_count

    return inserted_count, duplicate_count


def process_repositories(config: Dict, start_date: datetime, cursor) -> tuple:
    """Process all configured repositories and extract pipeline events."""
    api_url = config.get('api_url', 'https://api.bitbucket.org/2.0')
    workspace = config.get('workspace')
    api_token = config.get('api_token')
    configured_repos = config.get('repos', [])

    if not workspace or not api_token:
        logger.error("Missing BitBucket workspace or token in configuration")
        return [], 0

    all_events = []

    # If specific repos are configured, use those; otherwise fetch all repos
    if configured_repos:
        repo_names = configured_repos
    else:
        logger.info("No specific repositories configured, fetching all repositories...")
        # For now, we'll require repos to be configured
        logger.error("BitBucket Pipelines requires specific repositories to be configured")
        return [], 0

    logger.info(f"Processing {len(repo_names)} repositories...")

    for repo in repo_names:
        logger.info(f"Processing repository: {repo}")

        # Fetch pipelines for this repository
        pipelines = fetch_pipelines(api_url, workspace, api_token, repo, start_date)
        logger.info(f"Found {len(pipelines)} pipelines for repository {repo}")

        if pipelines:
            # Get environment mapping for deployments
            environment_mapping = get_pipeline_environment_mapping(api_url, workspace, api_token, repo)

            for pipeline in pipelines:
                # Create events from pipeline
                events = create_events_from_pipeline(pipeline, repo, environment_mapping)
                all_events.extend(events)

    return all_events, 0  # No cherry-pick events for BitBucket Pipelines


def main():
    """Main function to run BitBucket Pipelines extraction."""
    parser = argparse.ArgumentParser(description="Extract BitBucket Pipelines events")
    parser.add_argument('-p', '--product', help="Product name (if provided, saves to database; otherwise saves to CSV)")
    parser.add_argument('-s', '--start-date', help="Start date (YYYY-MM-DD format)")
    args = parser.parse_args()

    extractor = BitbucketPipelinesExtractor()

    if args.product is None:
        # CSV Mode: Load configuration from config.json
        config = json.load(open(os.path.join(common_dir, "config.json")))
        
        # Get configuration from config dictionary
        repos_str = config.get("BITBUCKET_REPOS", '')
        repos_list = [repo.strip() for repo in repos_str.split(",") if repo.strip()]

        config = {
            'workspace': config.get('BITBUCKET_WORKSPACE_ID'),
            'api_token': config.get('BITBUCKET_API_TOKEN'),
            'api_url': config.get('BITBUCKET_API_URL', 'https://api.bitbucket.org/2.0'),
            'repos': repos_list
        }

        # Use checkpoint file for last modified date
        last_modified = Utils.load_checkpoint("bitbucket_pipelines")

        extractor.run_extraction(None, config, args.start_date, last_modified)

    else:
        # Database Mode: Connect to the database
        from database import DatabaseConnection
        db = DatabaseConnection()
        with db.product_scope(args.product) as conn:
            with conn.cursor() as cursor:
                config = extractor.get_config_from_database(cursor)
                last_modified = extractor.get_last_modified_date(cursor)
                extractor.run_extraction(cursor, config, args.start_date, last_modified)

    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

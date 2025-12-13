"""
Azure DevOps Pipelines Data Extraction Script

This script extracts build and deployment events from Azure DevOps pipelines and supports two modes of operation:

Usage:
    python extract_azuredevops_pipelines.py [-p <product_name>] [-s <start_date>]

Arguments:
    -p, --product: Product name (if provided, saves to database; otherwise saves to CSV)
    -s, --start-date: Start date for extraction in YYYY-MM-DD format (optional)

Modes (automatically determined):
    Database mode (when -p is provided):
        - Imports from the database module
        - Connects to the database
        - Reads the config from the data_source_config table
        - Gets the last extraction timestamp from the build_event table
        - Saves the extracted data to the database tables

    CSV mode (when -p is NOT provided):
        - Reads the config from environment variables:
          * AZDO_ORGANIZATION: Azure DevOps organization
          * AZDO_API_TOKEN: Azure DevOps API token
          * AZDO_PROJECT: Azure DevOps project name
          * AZDO_REPOS: Comma-separated list of repository names
          * EXPORT_PATH: Export Path (Optional)
        - Gets the last extraction timestamp from the checkpoint (JSON) file
        - Saves the extracted data to CSV files, updating the checkpoint (JSON) file
"""

import argparse
import json
import logging
import os
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

import pytz
import requests

from common.utils import Utils

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('extract_azuredevops_pipelines')


class AzureDevOpsPipelinesExtractor:
    """Extracts build and deployment events from Azure DevOps pipelines."""

    def __init__(self):
        self.stats = {
            'build_events_inserted': 0,
            'build_events_duplicates': 0,
            'deployment_events_inserted': 0,
            'deployment_events_duplicates': 0
        }

    def get_config_from_database(self, cursor):
        """Get configuration from data_source_config table."""
        query = """
        SELECT config_item, config_value 
        FROM data_source_config 
        WHERE data_source = 'integration_and_build' 
        AND config_item IN ('Organization', 'Personal Access Token', 'Projects', 'Repos')
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        config = {}
        for row in results:
            config_item, config_value = row
            if config_item == 'Projects':
                # Parse the JSON list and get the first project
                try:
                    projects = json.loads(config_value)
                    config['project'] = projects[0] if projects else None
                except (json.JSONDecodeError, IndexError):
                    config['project'] = None
            elif config_item == 'Repos':
                try:
                    repos = json.loads(config_value)
                    config['repos'] = repos if repos else []
                except (json.JSONDecodeError, TypeError):
                    config['repos'] = []
            elif config_item == 'Organization':
                config['org_url'] = config_value
            elif config_item == 'Personal Access Token':
                config['api_token'] = config_value
        
        return config

    def get_last_modified_date(self, cursor):
        """Get the last modified date from the database."""
        query = """
            SELECT MAX(timestamp_utc) 
        FROM build_event 
            WHERE timestamp_utc IS NOT NULL
        """
        cursor.execute(query)
        result = cursor.fetchone()
        if result[0]:
            # Convert to naive datetime if timezone-aware
            dt = result[0]
            if dt.tzinfo is not None:
                dt = dt.replace(tzinfo=None)
            return dt
        else:
            return datetime(2000, 1, 1)

    def run_extraction(self, cursor, config: Dict, start_date: Optional[datetime], last_modified: Optional[datetime], export_path: str = None):
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

        # Validate required configuration
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
        project = config.get('project')
        api_token = config.get('api_token')
        repos = config.get('repos', [])

        # Construct proper Azure DevOps URL
        if not org_url.startswith('http'):
            org_url = f"https://dev.azure.com/{org_url}"
        config['org_url'] = org_url

        # Determine start date
        if start_date:
            # If timezone-aware, convert to naive UTC
            if start_date.tzinfo is not None:
                start_date = start_date.astimezone(timezone.utc).replace(tzinfo=None)
            extraction_start_date = start_date
        else:
            if last_modified:
                # If timezone-aware, convert to naive UTC
                if last_modified.tzinfo is not None:
                    last_modified = last_modified.replace(tzinfo=None)
                extraction_start_date = last_modified
            else:
                extraction_start_date = datetime(2024, 1, 1)

        # Set up save function
        if cursor:
            # Database mode

            def save_output_fn(events):
                return save_events_to_database(events, cursor)
        else:
            # CSV mode - create CSV files only if we have events to save
            # We'll create them lazily in save_output_fn when first events arrive
            build_csv_file = None
            deploy_csv_file = None
            
            # Define columns matching database schema
            build_columns = [
                'timestamp_utc', 'event', 'repo', 'source_branch', 'workflow_name', 
                'build_number', 'comment', 'actor', 'build_id'
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
                        if created_at and created_at.tzinfo is not None:
                            created_at = created_at.astimezone(timezone.utc).replace(tzinfo=None)
                        
                        # Map to build_event CSV format
                        build_event_dict = {
                            'timestamp_utc': created_at,
                            'event': event.get('event_type'),
                            'repo': event.get('repo_name', '').lower() if event.get('repo_name') else '',
                            'source_branch': event.get('branch_name', ''),
                            'workflow_name': event.get('pipeline_name', ''),
                            'build_number': event.get('target_iid', ''),
                            'comment': event.get('comment', ''),
                            'actor': event.get('author', 'Azure DevOps Pipelines'),
                            'build_id': event.get('commit_sha', '')  # build_id maps to commit_sha
                        }
                        build_events.append(build_event_dict)
                    elif event.get('event_type') == 'Build Deployed':
                        # Convert created_at to naive UTC datetime for CSV
                        created_at = event.get('created_at')
                        if created_at and created_at.tzinfo is not None:
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
                            'build_id': event.get('commit_sha', '')  # build_id maps to commit_sha
                        }
                        deployment_events.append(deploy_event_dict)
                
                # Create CSV files lazily when first events arrive
                if build_events and not build_csv_file:
                    build_csv_file = Utils.create_csv_file("azuredevops_pipelines_build_events", export_path, logger)
                if deployment_events and not deploy_csv_file:
                    deploy_csv_file = Utils.create_csv_file("azuredevops_pipelines_deployment_events", export_path, logger)
                
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
        logger.info(f"Fetching data from {org_url}")

        # Process repositories
        all_events = []
        for repo_name in repos:
            logger.info(f"Processing repository: {repo_name}")

            try:
                # Fetch pipeline runs for this repository
                pipeline_runs = fetch_pipelines(org_url, project, repo_name, api_token, extraction_start_date)
                logger.info(f"Found {len(pipeline_runs)} pipeline runs for repository {repo_name}")

                # Create events from pipeline runs
                for run in pipeline_runs:
                    events = create_events_from_pipeline_run(run, repo_name, min_timestamp=extraction_start_date)
                    if events:
                        all_events.extend(events)
                        # Save events immediately
                        if cursor:
                            build_inserted, build_duplicates, deploy_inserted, deploy_duplicates = save_output_fn(events)
                            self.stats['build_events_inserted'] += build_inserted
                            self.stats['build_events_duplicates'] += build_duplicates
                            self.stats['deployment_events_inserted'] += deploy_inserted
                            self.stats['deployment_events_duplicates'] += deploy_duplicates
                        else:
                            inserted, duplicates = save_output_fn(events)

            except Exception as e:
                logger.error(f"Error processing repository {repo_name}: {e}")
                continue

        # Save checkpoint in CSV mode
        if not cursor and max_timestamp:
            if Utils.save_checkpoint(prefix="azuredevops_pipelines", last_dt=max_timestamp, export_path=export_path):
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




def fetch_pipelines(org_url, project, repo, api_token, start_date):
    """Fetch build runs from Azure DevOps."""
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Use proper Azure DevOps authentication
    auth = ("", api_token)
    
    # Construct API URL for builds (not pipelines)
    api_url = f"{org_url}/{project}/_apis/build/builds"
    
    # Get builds with parameters
    params = {
        'api-version': '6.0',
        'definitions': '',  # Get all build definitions
        'statusFilter': 'completed',
        'maxBuildsPerDefinition': 100,
        '$orderby': 'finishTime desc'  # Sort by finish time, newest first
    }
    
    # Add date filtering if start_date is provided
    if start_date:
        # Convert start_date to ISO format for Azure DevOps API
        start_date_iso = start_date.isoformat()
        params['minTime'] = start_date_iso
    
    # Retry logic for failed requests
    max_retries = 3
    retry_delay = 1  # seconds
    
    for attempt in range(max_retries):
        try:
            builds_response = requests.get(api_url, headers=headers, params=params, auth=auth, timeout=30)
            
            if builds_response.status_code == 200:
                builds_data = builds_response.json()
                builds = builds_data.get('value', [])
                break
            elif builds_response.status_code == 429:
                # Rate limit exceeded
                if 'Retry-After' in builds_response.headers:
                    wait_time = int(builds_response.headers['Retry-After'])
                    logger.warning(f"Rate limit exceeded. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.warning("Rate limit exceeded for builds")
                    return []
            else:
                logger.warning(f"Failed to fetch builds: {builds_response.status_code} - {builds_response.text}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                    continue
                else:
                    return []
                    
        except requests.exceptions.RequestException as e:
            logger.warning(f"Request failed for builds (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                continue
            else:
                return []
        except Exception as ex:
            logger.error(f"Error fetching builds: {ex}")
            return []
    else:
        return []
    
    # Convert builds to pipeline-like format for compatibility
    all_runs = []
    for build in builds:
        # Check if we've gone past our date range (since we're sorted by finishTime desc)
        if start_date and build.get('finishTime'):
            try:
                build_finish_time = datetime.fromisoformat(build['finishTime'].replace('Z', '+00:00'))
                # Convert to naive UTC for comparison
                if build_finish_time.tzinfo is not None:
                    build_finish_time = build_finish_time.astimezone(timezone.utc).replace(tzinfo=None)
                # Compare full datetime, not just date
                if build_finish_time < start_date:
                    logger.info(f"Reached builds older than {start_date}, stopping processing")
                    break
            except ValueError:
                pass  # Continue if date parsing fails
        
        # Convert build to pipeline run format
        run = {
            'id': build.get('id', 0),
            'createdDate': build.get('queueTime', ''),
            'state': 'completed',
            'result': build.get('result', 'unknown'),
            'pipeline_name': build.get('definition', {}).get('name', ''),
            'pipeline_id': build.get('definition', {}).get('id', 0)
        }
        all_runs.append(run)
    
    return all_runs


def create_events_from_pipeline_run(run, repo_name, min_timestamp=None):
    """Create build and deployment events from a pipeline run.
    
    Args:
        run: Pipeline run data
        repo_name: Repository name
        min_timestamp: Optional minimum timestamp to filter events (events before this are skipped)
    """
    events = []
    
    run_id = run.get('id', 0)
    run_date = run.get('createdDate', '')
    state = run.get('state', 'unknown')
    result = run.get('result', 'unknown')
    pipeline_name = run.get('pipeline_name', '')
    
    # Convert date
    if run_date:
        try:
            run_dt = datetime.fromisoformat(run_date.replace('Z', '+00:00'))
            # Convert to naive UTC datetime
            if run_dt.tzinfo is not None:
                run_dt = run_dt.astimezone(timezone.utc).replace(tzinfo=None)
        except (ValueError, AttributeError):
            return events
    else:
        return events
    
    # Filter: Skip events before or at min_timestamp (checkpoint)
    # We want events strictly AFTER the checkpoint
    if min_timestamp and run_dt <= min_timestamp:
        return events
    
    # Create Build Created event for all runs
    build_event = {
        'data_source': 'integration_and_build',
        'event_type': 'Build Created',
        'created_at': run_dt,
        'author': 'Azure DevOps Pipelines',
        'target_iid': str(run_id),
        'repo_name': repo_name,
        'branch_name': '',  # Azure DevOps pipelines don't always have branch info in the main response
        'commit_sha': '',   # Will be extracted from run details if needed
        'comment': f"Pipeline run {run_id} for {pipeline_name}",
        'environment': 'production',  # Default environment
        'test_result': result if result in ['succeeded', 'failed', 'canceled'] else 'unknown',
        'pipeline_name': pipeline_name  # Add pipeline_name for workflow_name column
    }
    events.append(build_event)
    
    # Create Build Deployed event if successful
    if result == 'succeeded':
        deployed_event = build_event.copy()
        deployed_event['event_type'] = 'Build Deployed'
        deployed_event['comment'] = f"Deployment of pipeline run {run_id} for {pipeline_name}"
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
            event.get('author', 'Azure DevOps Pipelines')
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
    org_url = config.get('org_url')
    project = config.get('project')
    api_token = config.get('api_token')
    repos = config.get('repos', [])
    
    if not org_url or not project or not api_token:
        logger.error("Missing required configuration: Organization, Project, or Personal Access Token")
        return [], 0
    
    if not repos:
        logger.error("No repositories configured")
        return [], 0
    
    all_events = []
    
    for repo_name in repos:
        logger.info(f"Processing repository: {repo_name}")
        
        try:
            # Fetch pipeline runs for this repository
            pipeline_runs = fetch_pipelines(org_url, project, repo_name, api_token, start_date)
            logger.info(f"Found {len(pipeline_runs)} pipeline runs for repository {repo_name}")
            
            # Create events from pipeline runs
            for run in pipeline_runs:
                events = create_events_from_pipeline_run(run, repo_name)
                all_events.extend(events)
                
        except Exception as e:
            logger.error(f"Error processing repository {repo_name}: {e}")
            continue
    
    return all_events, 0  # No cherry-pick events for pipelines


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Extract Azure DevOps Pipelines data to database or CSV.")
    parser.add_argument('-p', '--product', type=str, help='Product name (if provided, saves to database; otherwise saves to CSV)')
    parser.add_argument('-s', '--start-date', type=str, help='Start date in YYYY-MM-DD format')
    
    args = parser.parse_args()
    
    extractor = AzureDevOpsPipelinesExtractor()
    
    # Parse start date if provided (common for both modes)
    start_date = None
    if args.start_date:
        try:
            start_date = datetime.strptime(args.start_date, '%Y-%m-%d')
        except ValueError:
            logger.error("Invalid start date format. Please use YYYY-MM-DD format.")
            sys.exit(1)

    if args.product is None:
        # CSV Mode: Load configuration from config.json
        config = json.load(open(os.path.join(common_dir, "config.json")))
        
        # Get configuration from config dictionary
        repos_str = config.get('AZDO_REPOS', '')
        repos_list = [repo.strip() for repo in repos_str.split(',') if repo.strip()]

        config = {
            'org_url': config.get('AZDO_ORGANIZATION'),
            'api_token': config.get('AZDO_API_TOKEN'),
            'project': config.get('AZDO_PROJECT'),
            'repos': repos_list
        }

        # Use checkpoint file for last modified date
        last_modified = Utils.load_checkpoint("azuredevops_pipelines")

        extractor.run_extraction(None, config, start_date, last_modified)

    else:
        # Database Mode: Connect to the database
        from database import DatabaseConnection
        db = DatabaseConnection()
    
        with db.product_scope(args.product) as conn:
            with conn.cursor() as cursor:
                config = extractor.get_config_from_database(cursor)
                last_modified = extractor.get_last_modified_date(cursor)
                
                extractor.run_extraction(cursor, config, start_date, last_modified)


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)

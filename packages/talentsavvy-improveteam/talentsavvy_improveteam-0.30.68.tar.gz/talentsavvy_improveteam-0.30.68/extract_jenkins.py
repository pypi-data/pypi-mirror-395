#!/usr/bin/env python3
"""
Jenkins Data Extraction Script

This script extracts build and deployment events from Jenkins and inserts them directly into the database.
It follows the same structure as extract_jira.py but uses Jenkins REST API.

Usage:
    python extract_jenkins.py -p <product_name> [-s <start_date>]
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
logger = logging.getLogger('jenkins_extractor')


class JenkinsExtractor:
    """Extracts build and deployment events from Jenkins."""

    def __init__(self):
        self.stats = {
            'build_events_inserted': 0,
            'build_events_duplicates': 0,
            'deployment_events_inserted': 0,
            'deployment_events_duplicates': 0
        }

    def get_config_from_database(self, cursor):
        """Get Jenkins configuration from database."""
        query = """
        SELECT config_item, config_value
        FROM data_source_config
        WHERE data_source = 'integration_and_build'
        AND config_item IN ('URL', 'User', 'Personal Access Token', 'Jobs')
        """
        cursor.execute(query)
        results = cursor.fetchall()

        config = {}
        for row in results:
            config_item, config_value = row
            if config_item == 'Jobs':
                try:
                    jobs = json.loads(config_value)
                    config['jobs'] = jobs if jobs else []
                except (json.JSONDecodeError, TypeError):
                    config['jobs'] = []
            elif config_item == 'URL':
                # For Jenkins, URL is the base URL
                base_url = config_value.rstrip('/')
                if not base_url.startswith(('http://', 'https://')):
                    config['jenkins_url'] = f"http://{base_url}"
                else:
                    config['jenkins_url'] = base_url
            elif config_item == 'User':
                config['jenkins_user'] = config_value
            elif config_item == 'Personal Access Token':
                config['jenkins_token'] = config_value

        return config

    def get_last_modified_date(self, cursor) -> Optional[datetime]:
        """Get the last modified date from the database."""
        query = "SELECT MAX(timestamp_utc) FROM build_event"
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

        # Validate configuration
        if not config.get('jenkins_url') or not config.get('jenkins_token'):
            logger.error("Missing Jenkins URL or token in configuration")
            sys.exit(1)

        jenkins_url = config.get('jenkins_url')
        jenkins_user = config.get('jenkins_user', 'admin')
        jenkins_token = config.get('jenkins_token')
        configured_jobs = config.get('jobs', [])

        # Determine start date
        if start_date:
            try:
                extraction_start_date = datetime.strptime(start_date, '%Y-%m-%d')
                # Convert to naive UTC datetime
                if extraction_start_date.tzinfo is not None:
                    extraction_start_date = extraction_start_date.astimezone(timezone.utc).replace(tzinfo=None)
                # Convert to timezone-aware for fetch_builds_for_job
                extraction_start_date_tz = extraction_start_date.replace(tzinfo=timezone.utc)
            except ValueError:
                logger.error("Invalid date format. Please use YYYY-MM-DD format.")
                sys.exit(1)
        else:
            if last_modified:
                # Convert to naive datetime if timezone-aware
                if last_modified.tzinfo is not None:
                    last_modified = last_modified.replace(tzinfo=None)
                extraction_start_date = last_modified
                # Convert to timezone-aware for fetch_builds_for_job
                extraction_start_date_tz = extraction_start_date.replace(tzinfo=timezone.utc)
            else:
                extraction_start_date = datetime(2024, 1, 1)
                extraction_start_date_tz = extraction_start_date.replace(tzinfo=timezone.utc)

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

            def save_output_fn(events):
                nonlocal build_csv_file, deploy_csv_file, max_timestamp

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
                                created_at = Utils.convert_to_utc(str(created_at))

                            # Map to build_event CSV format
                            build_event_dict = {
                                'timestamp_utc': created_at,
                                'event': event.get('event_type'),
                                'repo': event.get('repo_name', '').lower() if event.get('repo_name') else '',
                                'source_branch': event.get('branch_name', ''),
                                'workflow_name': '',
                                'build_number': event.get('target_iid', ''),
                                'comment': event.get('comment', ''),
                                'actor': event.get('author', 'Jenkins System'),
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
                                created_at = Utils.convert_to_utc(str(created_at))

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
                    build_csv_file = Utils.create_csv_file("jenkins_build_events", export_path, logger)
                if deployment_events and not deploy_csv_file:
                    deploy_csv_file = Utils.create_csv_file("jenkins_deployment_events", export_path, logger)

                # Save build events
                build_max_ts = None
                if build_events:
                    result = Utils.save_events_to_csv(build_events, build_csv_file, logger)
                    if len(result) > 3 and result[3]:
                        build_max_ts = result[3]

                # Save deployment events
                deploy_max_ts = None
                if deployment_events:
                    result = Utils.save_events_to_csv(deployment_events, deploy_csv_file, logger)
                    if len(result) > 3 and result[3]:
                        deploy_max_ts = result[3]

                # Track maximum timestamp for checkpoint
                if build_max_ts and (not max_timestamp or build_max_ts > max_timestamp):
                    max_timestamp = build_max_ts
                if deploy_max_ts and (not max_timestamp or deploy_max_ts > max_timestamp):
                    max_timestamp = deploy_max_ts

                total_inserted = len(build_events) + len(deployment_events)
                return total_inserted, 0  # Return inserted and duplicates

        # Log the fetch information
        logger.info(f"Starting extraction from {extraction_start_date}")
        logger.info(f"Fetching data from {jenkins_url}")

        # Process jobs
        if configured_jobs:
            job_names = configured_jobs
        else:
            logger.info("No specific jobs configured, fetching all jobs...")
            jobs_data = fetch_jobs(jenkins_url, jenkins_user, jenkins_token)
            job_names = [job.get('name') for job in jobs_data if job.get('name')]

        logger.info(f"Processing {len(job_names)} jobs...")

        for job_name in job_names:
            logger.info(f"Processing job: {job_name}")

            try:
                # Fetch builds for this job
                builds = fetch_builds_for_job(jenkins_url, jenkins_user, jenkins_token, job_name, extraction_start_date_tz)
                logger.info(f"Found {len(builds)} builds for job {job_name}")

                for build in builds:
                    # Get detailed build information
                    build_details = get_build_details(jenkins_url, jenkins_user, jenkins_token,
                                                    job_name, build.get('number', 0))

                    if build_details:
                        # Extract Git information
                        git_info = extract_git_info(build_details)

                        # Create events from build
                        events = create_events_from_build(build, job_name, git_info)
                        if events:
                            # Save events immediately
                            save_output_fn(events)

            except Exception as e:
                logger.error(f"Error processing job {job_name}: {e}")
                continue

        # Save checkpoint in CSV mode
        if not cursor and max_timestamp:
            if Utils.save_checkpoint(prefix="jenkins", last_dt=max_timestamp, export_path=export_path):
                logger.info(f"Checkpoint saved successfully: {max_timestamp}")
            else:
                logger.warning("Failed to save checkpoint")

        # Print summary
        if cursor:
            total_inserted = self.stats['build_events_inserted'] + self.stats['deployment_events_inserted']
            total_duplicates = self.stats['build_events_duplicates'] + self.stats['deployment_events_duplicates']
            logger.info(f"Total: inserted {total_inserted} events, skipped {total_duplicates} duplicates")
        else:
            logger.info(f"Extraction completed")


def fetch_jobs(jenkins_url: str, jenkins_user: str, jenkins_token: str) -> List[Dict]:
    """Fetch all jobs from Jenkins."""
    url = urljoin(f"{jenkins_url}/", "api/json?tree=jobs[name]&depth=10")
    auth = (jenkins_user, jenkins_token)

    # Retry logic for failed requests
    max_retries = 3
    retry_delay = 1  # seconds
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, auth=auth, verify=False, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                # Check if data is a dict with expected structure
                if isinstance(data, dict) and 'jobs' in data:
                    jobs_data = data.get("jobs", [])
                    return jobs_data
                else:
                    logging.warning(f"Unexpected response format for jobs: {data}")
                    return []
            else:
                logging.warning(f"Failed to fetch jobs: {response.status_code} - {response.text}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                    continue
                else:
                    return []

        except requests.RequestException as e:
            logger.warning(f"Request failed for jobs (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                continue
            else:
                return []
        except Exception as ex:
            logger.error(f"Error fetching jobs from Jenkins: {ex}")
            return []
    
    return []


def fetch_builds_for_job(jenkins_url: str, jenkins_user: str, jenkins_token: str,
                       job_name: str, start_date: datetime) -> List[Dict]:
    """Fetch builds for a specific job since start_date."""
    url = urljoin(f"{jenkins_url}/", f"job/{job_name}/api/json?tree=allBuilds[*,actions[*,parameters[name,value]]]&depth=2")
    auth = (jenkins_user, jenkins_token)

    # Retry logic for failed requests
    max_retries = 3
    retry_delay = 1  # seconds
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, auth=auth, verify=False, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                # Check if data is a dict with expected structure
                if isinstance(data, dict) and 'allBuilds' in data:
                    builds_data = data.get("allBuilds", [])
                    break
                else:
                    logging.warning(f"Unexpected response format for builds in {job_name}: {data}")
                    return []
            else:
                logging.warning(f"Failed to fetch builds for {job_name}: {response.status_code} - {response.text}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                    continue
                else:
                    return []

        except requests.RequestException as e:
            logger.warning(f"Request failed for builds in {job_name} (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                continue
            else:
                return []
        except Exception as ex:
            logger.error(f"Error fetching builds for {job_name}: {ex}")
            return []
    else:
        return []

    # Filter builds since start_date
    filtered_builds = []
    for build in builds_data:
        build_timestamp = build.get('timestamp', 0)
        build_date = datetime.fromtimestamp(build_timestamp / 1000, tz=timezone.utc)

        if build_date >= start_date:
            build['job_name'] = job_name
            build['build_date'] = build_date
            filtered_builds.append(build)

    return filtered_builds


def get_build_details(jenkins_url: str, jenkins_user: str, jenkins_token: str,
                     job_name: str, build_number: int) -> Optional[Dict]:
    """Get detailed information for a specific build."""
    url = urljoin(f"{jenkins_url}/", f"job/{job_name}/{build_number}/api/json")
    auth = (jenkins_user, jenkins_token)

    # Retry logic for failed requests
    max_retries = 3
    retry_delay = 1  # seconds
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, auth=auth, verify=False, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                # Check if data is a dict
                if isinstance(data, dict):
                    return data
                else:
                    logging.warning(f"Unexpected response format for build details: {data}")
                    return {}
            else:
                logging.warning(f"Failed to fetch build details: {response.status_code} - {response.text}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                    continue
                else:
                    return {}

        except requests.RequestException as e:
            logger.warning(f"Request failed for build details {job_name}#{build_number} (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                continue
            else:
                return {}
        except Exception as ex:
            logger.error(f"Error fetching build details for {job_name}#{build_number}: {ex}")
            return {}
    
    return {}


def extract_git_info(build_details: Dict) -> Dict:
    """Extract Git information from build details."""
    git_info = {
        'commit_sha': '',
        'branch_name': '',
        'repo_name': ''
    }

    # Look for Git information in actions
    actions = build_details.get('actions', [])
    for action in actions:
        if action.get('_class') == 'hudson.plugins.git.util.BuildData':
            # Extract commit SHA and branch name from lastBuiltRevision
            last_build = action.get('lastBuiltRevision', {})
            if last_build:
                git_info['commit_sha'] = last_build.get('SHA1', '')
                git_info['branch_name'] = last_build.get('branch', [{}])[0].get('name', '')

            # Extract repository name from remoteUrls
            remote_urls = action.get('remoteUrls', [])
            if remote_urls:
                # Extract repo name from URL
                repo_url = remote_urls[0]
                if 'github.com' in repo_url:
                    git_info['repo_name'] = repo_url.split('/')[-1].replace('.git', '')
                elif 'gitlab.com' in repo_url:
                    git_info['repo_name'] = repo_url.split('/')[-1].replace('.git', '')

    return git_info


def create_events_from_build(build: Dict, job_name: str, git_info: Dict) -> List[Dict]:
    """Create SDLC events from a Jenkins build."""
    events = []

    build_number = build.get('number', 0)
    build_date = build.get('build_date')
    result = build.get('result', 'UNKNOWN')
    duration = build.get('duration', 0)

    # Create Build Created event
    build_created_event = {
        'data_source': 'integration_and_build',
        'event_type': 'Build Created',
        'created_at': build_date,
        'author': 'Jenkins System',
        'target_iid': str(build_number),
        'repo_name': git_info.get('repo_name', ''),
        'branch_name': git_info.get('branch_name', ''),
        'commit_sha': git_info.get('commit_sha', ''),
        'comment': f"Build #{build_number} for job {job_name}",
        'environment': 'production',  # Default environment
        'test_result': result if result in ['SUCCESS', 'FAILURE', 'UNSTABLE'] else 'UNKNOWN'
    }
    events.append(build_created_event)

    # Create Build Deployed event if successful
    if result == 'SUCCESS':
        deployed_event = build_created_event.copy()
        deployed_event['event_type'] = 'Build Deployed'
        deployed_event['comment'] = f"Deployment of build #{build_number} for job {job_name}"
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
            event.get('author', 'Jenkins System')
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


def process_jobs(config: Dict, start_date: datetime, cursor) -> tuple:
    """Process all configured jobs and extract events."""
    jenkins_url = config.get('jenkins_url')
    jenkins_user = config.get('jenkins_user', 'admin')
    jenkins_token = config.get('jenkins_token')
    configured_jobs = config.get('jobs', [])

    if not jenkins_url or not jenkins_token:
        logger.error("Missing Jenkins URL or token in configuration")
        return 0, 0

    all_events = []

    # If specific jobs are configured, use those; otherwise fetch all jobs
    if configured_jobs:
        job_names = configured_jobs
    else:
        logger.info("No specific jobs configured, fetching all jobs...")
        jobs_data = fetch_jobs(jenkins_url, jenkins_user, jenkins_token)
        job_names = [job.get('name') for job in jobs_data if job.get('name')]

    logger.info(f"Processing {len(job_names)} jobs...")

    for job_name in job_names:
        logger.info(f"Processing job: {job_name}")

        # Fetch builds for this job
        builds = fetch_builds_for_job(jenkins_url, jenkins_user, jenkins_token, job_name, start_date)
        logger.info(f"Found {len(builds)} builds for job {job_name}")

        for build in builds:
            # Get detailed build information
            build_details = get_build_details(jenkins_url, jenkins_user, jenkins_token,
                                            job_name, build.get('number', 0))

            if build_details:
                # Extract Git information
                git_info = extract_git_info(build_details)

                # Create events from build
                events = create_events_from_build(build, job_name, git_info)
                all_events.extend(events)

    return all_events, 0  # No cherry-pick events for Jenkins


def main():
    """Main function to run Jenkins extraction."""
    parser = argparse.ArgumentParser(description="Extract Jenkins build and deployment events")
    parser.add_argument('-p', '--product', help="Product name (if provided, saves to database; otherwise saves to CSV)")
    parser.add_argument('-s', '--start-date', help="Start date (YYYY-MM-DD format)")
    args = parser.parse_args()

    extractor = JenkinsExtractor()

    if args.product is None:
        # CSV Mode: Load configuration from config.json
        config = json.load(open(os.path.join(common_dir, "config.json")))
        
        # Get configuration from config dictionary
        jobs_str = config.get("JENKINS_JOBS", '')
        jobs_list = [job.strip() for job in jobs_str.split(",") if job.strip()] if jobs_str else []

        config = {
            'jenkins_url': config.get('JENKINS_API_URL', 'http://localhost:8080'),
            'jenkins_user': config.get('JENKINS_USER', 'root'),
            'jenkins_token': config.get('JENKINS_API_TOKEN'),
            'jobs': jobs_list
        }

        # Use checkpoint file for last modified date
        last_modified = Utils.load_checkpoint("jenkins")

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
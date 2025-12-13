import requests
import json
import time
from datetime import datetime
from typing import Optional, Dict
import pytz  # Import pytz to handle timezone conversions
import sys
import os
import argparse

base_dir = os.path.dirname(os.path.abspath(__file__))
common_dir = os.path.join(base_dir, "common")
if not os.path.isdir(common_dir):
    # go up one level to find "common" (for installed package structure)
    base_dir = os.path.dirname(base_dir)
    common_dir = os.path.join(base_dir, "common")

if os.path.isdir(common_dir) and base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from common.utils import Utils
import logging

# Configure logging to print messages on stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)

# GitHub and CI/CD API details - Configuration will be loaded from database
repos = None
repo_owner = None
personal_access_token = None
headers = None
valid_workflow_names = None


class GitHubActionsExtractor:
    """Extracts build events from GitHub Actions."""

    def __init__(self):
        self.stats = {
            'build_events_inserted': 0,
            'build_events_duplicates': 0
        }

    def get_config_from_database(self, cursor):
        """Fetch GitHub Actions configuration from data_source_config table."""
        cursor.execute("""
            SELECT config_item, config_value
            FROM data_source_config
            WHERE data_source = 'integration_and_build'
            AND config_item IN ('Organization', 'Repos', 'Personal Access Token', 'Workflows')
        """)

        config = {}
        for row in cursor.fetchall():
            config[row[0]] = row[1]

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

        # Set up global variables from configuration (needed by fetch_builds)
        global repo_owner, repos, personal_access_token, headers, valid_workflow_names
        repo_owner = config.get('Organization')

        # Parse repositories
        repos_config = config.get('Repos', '')
        if repos_config:
            try:
                repos = json.loads(repos_config)
            except (json.JSONDecodeError, TypeError):
                repos = repos_config.split(',')
        else:
            repos = []

        personal_access_token = config.get('Personal Access Token')

        # Parse workflows
        workflows_config = config.get('Workflows', '')
        if workflows_config:
            try:
                valid_workflow_names = json.loads(workflows_config)
            except (json.JSONDecodeError, TypeError):
                valid_workflow_names = workflows_config.split(',')
        else:
            valid_workflow_names = []

        # Validate configuration
        if not repo_owner or not repos or not personal_access_token:
            logging.error("Missing required configuration: Organization / Personal Access Token / Repos")
            sys.exit(1)

        # Set up headers
        headers = {
            'Authorization': f'Bearer {personal_access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        # Determine start date
        if start_date:
            try:
                extraction_start_date = datetime.strptime(start_date, '%Y-%m-%d')
                # Convert to naive UTC datetime
                if extraction_start_date.tzinfo is not None:
                    extraction_start_date = extraction_start_date.astimezone(pytz.utc).replace(tzinfo=None)
                else:
                    # Ensure naive datetime
                    extraction_start_date = extraction_start_date.replace(tzinfo=None)
            except ValueError:
                logging.error("Invalid date format. Please use YYYY-MM-DD format.")
                sys.exit(1)
        else:
            if last_modified:
                # Convert to naive datetime if timezone-aware
                if last_modified.tzinfo is not None:
                    last_modified = last_modified.replace(tzinfo=None)
                extraction_start_date = last_modified
            else:
                extraction_start_date = datetime(2000, 1, 1)

        # Set up save function
        if cursor:
            # Database mode

            def save_output_fn(build_data_list):
                if build_data_list:
                    data_count, inserted_count, duplicate_count = insert_build_data_batch(cursor, build_data_list)
                    self.stats['build_events_inserted'] += inserted_count
                    self.stats['build_events_duplicates'] += duplicate_count
                    return data_count, inserted_count, duplicate_count
                return 0, 0, 0
        else:
            # CSV mode - create CSV file lazily
            build_csv_file = None

            def save_output_fn(build_data_list):
                nonlocal build_csv_file, max_timestamp

                if not build_data_list:
                    return 0, 0, 0

                # Convert tuples to dictionaries for CSV
                # Tuple format: (source_branch, repo, event, timestamp_utc, actor, workflow_name, build_number, build_id)
                build_events = []
                for build_tuple in build_data_list:
                    timestamp_utc = build_tuple[3]
                    # Convert to naive UTC datetime if needed
                    if timestamp_utc:
                        if isinstance(timestamp_utc, datetime):
                            if timestamp_utc.tzinfo is not None:
                                timestamp_utc = timestamp_utc.astimezone(pytz.utc).replace(tzinfo=None)
                        else:
                            timestamp_utc = datetime.fromisoformat(str(timestamp_utc).replace('Z', '+00:00'))
                            if timestamp_utc.tzinfo is not None:
                                timestamp_utc = timestamp_utc.astimezone(pytz.utc).replace(tzinfo=None)

                    build_event_dict = {
                        'timestamp_utc': timestamp_utc,
                        'event': build_tuple[2],
                        'repo': build_tuple[1].lower() if build_tuple[1] else '',
                        'source_branch': build_tuple[0],
                        'workflow_name': build_tuple[5],
                        'build_number': build_tuple[6],
                        'comment': '',
                        'actor': build_tuple[4],
                        'build_id': build_tuple[7]
                    }
                    build_events.append(build_event_dict)

                # Create CSV file lazily when first events arrive
                if build_events and not build_csv_file:
                    build_csv_file = Utils.create_csv_file("github_actions_build_events", export_path, logging)

                # Save build events
                build_max_ts = None
                if build_events:
                    result = Utils.save_events_to_csv(build_events, build_csv_file, logging)
                    if len(result) > 3 and result[3]:
                        build_max_ts = result[3]

                # Track maximum timestamp for checkpoint
                if build_max_ts and (not max_timestamp or build_max_ts > max_timestamp):
                    max_timestamp = build_max_ts

                return len(build_events), 0, 0

        # Log the fetch information
        logging.info(f"Workflow names: {valid_workflow_names}")
        logging.info(f"Starting extraction from {extraction_start_date}")

        # Fetch builds for each repository
        for repo in repos:
            repo = repo.strip()  # Remove any whitespace
            logging.info(f"Fetching data from https://api.github.com/repos/{repo_owner}/{repo}")

            try:
                # Fetch builds and get actual counts
                build_data_list = fetch_builds(repo, extraction_start_date)

                if build_data_list:
                    # Save events
                    save_output_fn(build_data_list)

            except Exception as e:
                logging.error(f"Error processing repository {repo}: {str(e)}")
                continue

        # Save checkpoint in CSV mode
        if not cursor and max_timestamp:
            if Utils.save_checkpoint(prefix="github_actions", last_dt=max_timestamp, export_path=export_path):
                logging.info(f"Checkpoint saved successfully: {max_timestamp}")
            else:
                logging.warning("Failed to save checkpoint")

        # Print summary
        if cursor:
            total_inserted = self.stats['build_events_inserted']
            total_duplicates = self.stats['build_events_duplicates']
            logging.info(f"Total: inserted {total_inserted} events, skipped {total_duplicates} duplicates")
        else:
            logging.info(f"Extraction completed")


# Function to safely extract data and handle missing or invalid fields
def safe_get(data, keys, default_value='NULL'):
    try:
        for key in keys:
            data = data[key]
        return data
    except (KeyError, TypeError):
        return default_value


# Function to insert build data into the build_event table using batch insertion
def insert_build_data_batch(cursor, build_data_list):
    """Insert build data into the database using batch insertion."""
    if not build_data_list:
        return 0, 0, 0

    from psycopg2.extras import execute_values

    # Get count before insertion
    cursor.execute("SELECT COUNT(*) FROM build_event")
    count_before = cursor.fetchone()[0]

    # Use execute_values for batch insertion
    columns = [
        'source_branch', 'repo', 'event', 'timestamp_utc', 'actor', 'workflow_name', 'build_number', 'build_id'
    ]

    execute_values(
        cursor,
        f"INSERT INTO build_event ({', '.join(columns)}) VALUES %s ON CONFLICT DO NOTHING",
        build_data_list,
        template=None,
        page_size=1000
    )

    # Get count after insertion to determine actual inserted records
    cursor.execute("SELECT COUNT(*) FROM build_event")
    count_after = cursor.fetchone()[0]

    # Calculate actual inserted and skipped records
    inserted_count = count_after - count_before
    duplicate_count = len(build_data_list) - inserted_count

    return len(build_data_list), inserted_count, duplicate_count

# Function to fetch build from CI/CD system with If-Modified-Since header
def fetch_builds(repo, last_modified_date):
    # Format the last modified date to the proper HTTP date format
    if_modified_since = last_modified_date.strftime("%a, %d %b %Y %H:%M:%S GMT")
    headers['If-Modified-Since'] = if_modified_since

    builds_url = f"https://api.github.com/repos/{repo_owner}/{repo}/actions/runs?per_page=100"
    build_data_list = []

    while builds_url:
        # Retry logic for failed requests
        max_retries = 3
        retry_delay = 1  # seconds

        for attempt in range(max_retries):
            try:
                response = requests.get(builds_url, headers=headers, timeout=30)

                if response.status_code == 200:
                    builds = response.json()

                    for build in builds['workflow_runs']:
                        timestamp_utc = Utils.convert_to_utc(safe_get(build, ['run_started_at'], None))
                        branch = safe_get(build, ['head_branch'], 'NULL')
                        build_number = safe_get(build, ['run_number'], 'NULL')
                        short_sha = safe_get(build, ['head_sha'], 'NULL')[:7] if len(safe_get(build, ['head_sha'], 'NULL')) >= 7 else safe_get(build, ['head_sha'], 'NULL')

                        # Getting the build id to match with deployment event
                        if not timestamp_utc:
                            build_id = 'NULL'
                        else:
                            date_str = timestamp_utc.date().isoformat()
                            release_str = None
                            if branch.startswith("release/"):
                                release_str = branch.split("release/")[1]
                            elif branch == "main":
                                release_str = "0.0"
                    break
                elif response.status_code == 304:
                    # Not modified since last check
                    break
                elif response.status_code == 429:
                    # Rate limit exceeded
                    if 'Retry-After' in response.headers:
                        wait_time = int(response.headers['Retry-After'])
                        logging.warning(f"Rate limit exceeded. Waiting {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        logging.warning("Rate limit exceeded for GitHub Actions")
                        break
                else:
                    logging.warning(f"Failed to fetch GitHub Actions runs: {response.status_code} - {response.text}")
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                        continue
                    else:
                        break

            except requests.RequestException as e:
                logging.warning(f"Request failed for GitHub Actions runs (attempt {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                    continue
                else:
                    break
            except Exception as ex:
                logging.error(f"Error fetching GitHub Actions runs: {ex}")
                break
        else:
            break

        # Process the builds from the response
        if response.status_code == 200:
            for build in builds['workflow_runs']:
                timestamp_utc = Utils.convert_to_utc(safe_get(build, ['run_started_at'], None))
                branch = safe_get(build, ['head_branch'], 'NULL')
                build_number = safe_get(build, ['run_number'], 'NULL')
                short_sha = safe_get(build, ['head_sha'], 'NULL')[:7] if len(safe_get(build, ['head_sha'], 'NULL')) >= 7 else safe_get(build, ['head_sha'], 'NULL')

                # Getting the build id to match with deployment event
                if not timestamp_utc:
                    build_id = 'NULL'
                else:
                    date_str = timestamp_utc.date().isoformat()
                    release_str = None
                    if branch.startswith("release/"):
                        release_str = branch.split("release/")[1]
                    elif branch == "main":
                        release_str = "0.0"

                    if not release_str:
                        build_id = 'NULL'
                    else:
                        build_id = f"{release_str}.{build_number}-{date_str}-{short_sha}"

                workflow_name = safe_get(build, ['name'], 'NULL')
                # Skip builds that don't match the valid workflow names
                if workflow_name not in valid_workflow_names:
                    continue

                # Skip builds older than the last known modification date
                if timestamp_utc and timestamp_utc <= last_modified_date:
                    continue
                event = get_event(build)

                build_data = (
                    branch,
                    repo,
                    event,  # e.g., success, failure
                    timestamp_utc,
                    safe_get(build, ['actor', 'login'], 'NULL'),
                    safe_get(build, ['name'], 'NULL'),
                    build_number,
                    build_id
                )
                build_data_list.append(build_data)

            # Check for pagination
            if 'next' in response.links:
                builds_url = response.links['next']['url']
            else:
                builds_url = None  # No more pages to fetch
        elif response.status_code == 304:
            # No new builds to fetch
            logging.info(f"No new builds since {last_modified_date}.")
            break
        else:
            logging.error(f"Error fetching builds for repo '{repo}': {response.status_code} {response.text}")
            break

    return build_data_list


def get_event(build):
    """
    This method extracts event from the build using a custom logic

    :param build: Build Object
    :return: str event object
    """
    result = safe_get(build, ['conclusion'], 'NULL')
    event = result
    if result and result != 'NULL':
        if result == 'success':
            event = 'Build Created'
        elif result == 'cancelled':
            event = 'Build Cancelled'
        elif result == 'startup_failure':
            event = 'Build Startup Failure'
        elif result == 'failure':
            event = 'Build Failed'
    return event


# Main Execution: Fetching data for each repo and writing to the database
def main():
    parser = argparse.ArgumentParser(description="Add new events in the build_event table.")

    parser.add_argument('-p', '--product', type=str, help='Product name (if provided, saves to database; otherwise saves to CSV)')
    parser.add_argument('-s', '--start-date', type=str, help='Start date in YYYY-MM-DD format')
    args = parser.parse_args()

    extractor = GitHubActionsExtractor()

    if args.product is None:
        # CSV Mode: Load configuration from config.json
        config = json.load(open(os.path.join(common_dir, "config.json")))
        
        # Get configuration from config dictionary
        repos_str = config.get("GITHUB_REPOS", '')
        repos_list = [repo.strip() for repo in repos_str.split(",") if repo.strip()] if repos_str else []

        workflows_str = config.get("GITHUB_WORKFLOWS", '')
        workflows_list = [wf.strip() for wf in workflows_str.split(",") if wf.strip()] if workflows_str else []

        config = {
            'Organization': config.get('GITHUB_ORGANIZATION'),
            'Repos': json.dumps(repos_list) if repos_list else '',
            'Personal Access Token': config.get('GITHUB_API_TOKEN'),
            'Workflows': json.dumps(workflows_list) if workflows_list else ''
        }

        # Use checkpoint file for last modified date
        last_modified = Utils.load_checkpoint("github_actions")

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


# Run the main function
if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)


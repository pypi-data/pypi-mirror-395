import requests
import json
import time
from datetime import datetime
from typing import Optional, Dict
import pytz
import sys
import os
import argparse
import logging

base_dir = os.path.dirname(os.path.abspath(__file__))
common_dir = os.path.join(base_dir, "common")
if not os.path.isdir(common_dir):
    # go up one level to find "common" (for installed package structure)
    base_dir = os.path.dirname(base_dir)
    common_dir = os.path.join(base_dir, "common")

if os.path.isdir(common_dir) and base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from common.utils import Utils

# Octopus API details - Configuration will be loaded from database
octopus_server_url = None
api_key = None
headers = None

# Configure logging to print messages on stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)



# Fetch environment name by its ID
def fetch_environment_name(environment_id):
    url = f"{octopus_server_url}/api/environments/{environment_id}"

    # Retry logic for failed requests
    max_retries = 3
    retry_delay = 1  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                environment = response.json()
                return environment.get('Name', None)
            else:
                logging.warning(f"Failed to fetch environment {environment_id}: {response.status_code} - {response.text}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                    continue
                else:
                    return None
        except requests.RequestException as e:
            logging.warning(f"Request failed for environment {environment_id} (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                continue
            else:
                return None
        except Exception as ex:
            logging.error(f"Error fetching environment {environment_id}: {ex}")
            return None

    return None

# Fetch project name by its ID
def fetch_project_name(project_id):
    url = f"{octopus_server_url}/api/projects/{project_id}"

    # Retry logic for failed requests
    max_retries = 3
    retry_delay = 1  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code == 200:
                project = response.json()
                return project.get('Name', None)
            else:
                logging.warning(f"Failed to fetch project {project_id}: {response.status_code} - {response.text}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                    continue
                else:
                    return None
        except requests.RequestException as e:
            logging.warning(f"Request failed for project {project_id} (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                continue
            else:
                return None
        except Exception as ex:
            logging.error(f"Error fetching project {project_id}: {ex}")
            return None

    return None

# Function to extract the required columns from the deployment response
def extract_columns_from_deployment(deployment, project_cache, environment_cache):
    # Extract the timestamp and convert to UTC
    timestamp_dt = Utils.convert_to_utc(deployment.get('Created', None))
    timestamp_utc = timestamp_dt.strftime("%Y-%m-%d %H:%M:%S") if timestamp_dt else None

    # Extract the build_name using the ProjectId with caching
    project_id = deployment.get('ProjectId', None)
    build_name = None
    if project_id:
        if project_id not in project_cache:
            project_cache[project_id] = fetch_project_name(project_id)
        build_name = project_cache[project_id]

    # Extract the build_id from the Changes array
    build_id = None
    changes = deployment.get('Changes', [])
    if changes and 'Version' in changes[0]:
        build_id = changes[0]['Version']

    # Extract the environment name using the EnvironmentId with caching
    environment_id = deployment.get('EnvironmentId', None)
    env = None
    if environment_id:
        if environment_id not in environment_cache:
            environment_cache[environment_id] = fetch_environment_name(environment_id)
        env = environment_cache[environment_id]

    return {
        'timestamp_utc': timestamp_utc,
        'build_name': build_name,
        'env': env,
        'build_id': build_id
    }


class OctopusExtractor:
    """Extracts deployment events from Octopus Deploy."""

    def __init__(self):
        self.stats = {
            'deployment_events_inserted': 0,
            'deployment_events_duplicates': 0
        }

    def get_config_from_database(self, cursor):
        """Fetch Octopus configuration from data_source_config table."""
        cursor.execute("""
            SELECT config_item, config_value
            FROM data_source_config
            WHERE data_source = 'deployment'
            AND config_item IN ('Organization', 'Personal Access Token')
        """)

        config = {}
        for row in cursor.fetchall():
            config[row[0]] = row[1]

        return config

    def get_last_modified_date(self, cursor) -> Optional[datetime]:
        """Get the last modified date from the database."""
        query = "SELECT MAX(timestamp_utc) FROM deployment_event"
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

        # Set up global variables from configuration (needed by fetch_deployments)
        global octopus_server_url, api_key, headers
        organization = config.get('Organization')
        api_key = config.get('Personal Access Token')

        # Validate configuration
        if not organization or not api_key:
            logging.error("Missing required configuration: Organization / Personal Access Token")
            sys.exit(1)

        # Construct the Octopus server URL
        octopus_server_url = f"https://{organization}.octopus.app"

        # Set up headers
        headers = {
            'X-Octopus-ApiKey': api_key,
            'Content-Type': 'application/json'
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

            # Load existing deployments into memory for release version calculation
            deployment_dict = load_existing_deployments(cursor)

            def save_output_fn(extracted_data):
                if extracted_data:
                    data_count, inserted_count, duplicate_count = insert_into_deployment_batch(cursor, extracted_data, deployment_dict)
                    self.stats['deployment_events_inserted'] += inserted_count
                    self.stats['deployment_events_duplicates'] += duplicate_count
                    return data_count, inserted_count, duplicate_count
                return 0, 0, 0
        else:
            # CSV mode - create CSV file lazily
            deploy_csv_file = None
            deployment_dict = {}  # Empty dict for CSV mode

            def save_output_fn(extracted_data):
                nonlocal deploy_csv_file, max_timestamp, deployment_dict

                if not extracted_data:
                    return 0, 0, 0

                # Convert to deployment_event CSV format
                deployment_events = []
                for row in extracted_data:
                    # Calculate release_version and is_major_release (same logic as database mode)
                    release_version, is_major_release = calculate_release_version_and_major_release(
                        row['env'], row['build_name'], row['build_id'], row['timestamp_utc'], deployment_dict
                    )

                    # Convert timestamp to naive UTC datetime if needed
                    timestamp_utc = row['timestamp_utc']
                    if timestamp_utc:
                        if isinstance(timestamp_utc, datetime):
                            if timestamp_utc.tzinfo is not None:
                                timestamp_utc = timestamp_utc.astimezone(pytz.utc).replace(tzinfo=None)
                        else:
                            timestamp_utc = datetime.fromisoformat(str(timestamp_utc).replace('Z', '+00:00'))
                            if timestamp_utc.tzinfo is not None:
                                timestamp_utc = timestamp_utc.astimezone(pytz.utc).replace(tzinfo=None)

                    # Map to deployment_event CSV format
                    deploy_event_dict = {
                        'timestamp_utc': timestamp_utc,
                        'event': 'Deployed',
                        'build_name': row.get('build_name', ''),
                        'repo': '',
                        'source_branch': '',
                        'comment': '',
                        'environment': row.get('env', ''),
                        'is_major_release': is_major_release,
                        'release_version': release_version,
                        'build_id': row.get('build_id', '')
                    }
                    deployment_events.append(deploy_event_dict)

                    # Update deployment_dict for subsequent calculations
                    if row.get('build_id') and row['build_id'] != 'None' and '.' in row['build_id']:
                        parts = row['build_id'].split('.')
                        if len(parts) >= 2:
                            major_version = f"{parts[0]}.{parts[1]}"
                            key = (row['env'], row['build_name'], major_version)

                            if key not in deployment_dict:
                                deployment_dict[key] = []

                            deployment_dict[key].append({
                                'build_id': row['build_id'],
                                'timestamp_utc': row['timestamp_utc'],
                                'release_version': release_version,
                                'is_major_release': is_major_release
                            })

                # Create CSV file lazily when first events arrive
                if deployment_events and not deploy_csv_file:
                    deploy_csv_file = Utils.create_csv_file("octopus_deployment_events", export_path, logging)

                # Save deployment events
                deploy_max_ts = None
                if deployment_events:
                    result = Utils.save_events_to_csv(deployment_events, deploy_csv_file, logging)
                    if len(result) > 3 and result[3]:
                        deploy_max_ts = result[3]

                # Track maximum timestamp for checkpoint
                if deploy_max_ts and (not max_timestamp or deploy_max_ts > max_timestamp):
                    max_timestamp = deploy_max_ts

                return len(deployment_events), 0, 0

        # Log the fetch information
        logging.info(f"Starting extraction from {extraction_start_date}")
        logging.info(f"Fetching data from {octopus_server_url}")

        try:
            # Fetch deployments
            extracted_data = fetch_deployments(cursor, extraction_start_date)

            if extracted_data:
                # Save events
                save_output_fn(extracted_data)

        except Exception as e:
            logging.error(f"Error during Octopus extraction: {e}")

        # Save checkpoint in CSV mode
        if not cursor and max_timestamp:
            if Utils.save_checkpoint(prefix="octopus", last_dt=max_timestamp, export_path=export_path):
                logging.info(f"Checkpoint saved successfully: {max_timestamp}")
            else:
                logging.warning("Failed to save checkpoint")

        # Print summary
        if cursor:
            total_inserted = self.stats['deployment_events_inserted']
            total_duplicates = self.stats['deployment_events_duplicates']
            logging.info(f"Total: inserted {total_inserted} events, skipped {total_duplicates} duplicates")
        else:
            logging.info(f"Extraction completed")


# Function to insert deployment data into the deployment_event table using batch insertion
def insert_into_deployment_batch(cursor, data_list, deployment_dict):
    """Insert deployment data into the database using batch insertion."""
    if not data_list:
        return 0, 0, 0

    from psycopg2.extras import execute_values

    # Prepare data for batch insertion with calculated release_version and is_major_release
    batch_data = []
    for row in data_list:
        # Calculate release_version and is_major_release
        release_version, is_major_release = calculate_release_version_and_major_release(
            row['env'], row['build_name'], row['build_id'], row['timestamp_utc'], deployment_dict
        )

        batch_data.append((
            row['timestamp_utc'], 'Deployed', row['build_name'], row['env'],
            row['build_id'], release_version, is_major_release
        ))

        # Add the new record to the in-memory dictionary for subsequent calculations
        if row['build_id'] and row['build_id'] != 'None' and '.' in row['build_id']:
            parts = row['build_id'].split('.')
            if len(parts) >= 2:
                major_version = f"{parts[0]}.{parts[1]}"
                key = (row['env'], row['build_name'], major_version)

                if key not in deployment_dict:
                    deployment_dict[key] = []

                deployment_dict[key].append({
                    'build_id': row['build_id'],
                    'timestamp_utc': row['timestamp_utc'],
                    'release_version': release_version,
                    'is_major_release': is_major_release
                })

    # Get count before insertion
    cursor.execute("SELECT COUNT(*) FROM deployment_event")
    count_before = cursor.fetchone()[0]

    # Use execute_values for batch insertion
    columns = [
        'timestamp_utc', 'event', 'build_name', 'environment', 'build_id', 'release_version', 'is_major_release'
    ]

    execute_values(
        cursor,
        f"INSERT INTO deployment_event ({', '.join(columns)}) VALUES %s ON CONFLICT DO NOTHING",
        batch_data,
        template=None,
        page_size=1000
    )

    # Get count after insertion to determine actual inserted records
    cursor.execute("SELECT COUNT(*) FROM deployment_event")
    count_after = cursor.fetchone()[0]

    # Calculate actual inserted and skipped records
    inserted_count = count_after - count_before
    duplicate_count = len(batch_data) - inserted_count

    return len(batch_data), inserted_count, duplicate_count

# Function to fetch deployments with pagination support and simulated delta token
def fetch_deployments(cursor, last_timestamp):
    # Initialize caches for project and environment names
    project_cache = {}
    environment_cache = {}
    all_extracted_data = []

    skip = 0
    take = 50  # Number of items to retrieve per page
    has_more_items = True

    while has_more_items:
        url = f"{octopus_server_url}/api/deployments?skip={skip}&take={take}&createdSince={last_timestamp.isoformat()}"
        response = requests.get(url, headers=headers)

        # Debugging: Print the status code and URL

        if response.status_code == 200:
            try:
                # Parse the response JSON
                deployments = response.json()

                # Check if 'Items' exists in the response
                if 'Items' in deployments:
                    extracted_data = []
                    for deployment in deployments['Items']:
                        data = extract_columns_from_deployment(deployment, project_cache, environment_cache)

                        # Only insert deployments that are newer than the last known timestamp
                        if data['timestamp_utc']:
                            # Convert the timestamp string back to datetime for comparison
                            deployment_timestamp = datetime.strptime(data['timestamp_utc'], "%Y-%m-%d %H:%M:%S")
                            if deployment_timestamp > last_timestamp:
                                extracted_data.append(data)

                    all_extracted_data.extend(extracted_data)

                    # Update skip for the next set of deployments
                    skip += take

                    # If fewer than 'take' items are returned, stop pagination
                    if len(deployments['Items']) < take:
                        has_more_items = False
                else:
                    logging.warning(f"'Items' not found in the response. Full response: {deployments}")
                    has_more_items = False
            except json.JSONDecodeError as e:
                logging.error(f"Error decoding JSON: {e}")
                has_more_items = False
        else:
            logging.error(f"Error fetching deployments: {response.status_code} {response.text}")
            has_more_items = False

    return all_extracted_data

def load_existing_deployments(cursor):
    """Load all existing deployment records into memory for release version calculation."""
    query = """
    SELECT id, environment, build_name, build_id, timestamp_utc, release_version, is_major_release
    FROM deployment_event
    WHERE build_id != 'None'
    ORDER BY timestamp_utc, id
    """
    cursor.execute(query)
    records = cursor.fetchall()

    # Create a dictionary keyed by (environment, build_name, major_version)
    deployment_dict = {}
    for record in records:
        id_val, environment, build_name, build_id, timestamp_utc, release_version, is_major_release = record

        # Extract major version (first two parts of build_id)
        if build_id and '.' in build_id:
            parts = build_id.split('.')
            if len(parts) >= 2:
                major_version = f"{parts[0]}.{parts[1]}"
                key = (environment, build_name, major_version)

                if key not in deployment_dict:
                    deployment_dict[key] = []

                deployment_dict[key].append({
                    'id': id_val,
                    'build_id': build_id,
                    'timestamp_utc': timestamp_utc,
                    'release_version': release_version,
                    'is_major_release': is_major_release
                })

    return deployment_dict

def calculate_release_version_and_major_release(environment, build_name, build_id, timestamp_utc, deployment_dict):
    """Calculate release_version and is_major_release for a new deployment record."""
    if not build_id or build_id == 'None' or '.' not in build_id:
        return build_id, False

    # Extract major version (first two parts of build_id)
    parts = build_id.split('.')
    if len(parts) < 2:
        return build_id, False

    major_version = f"{parts[0]}.{parts[1]}"
    key = (environment, build_name, major_version)

    # Get existing records for this key
    existing_records = deployment_dict.get(key, [])

    # Add current record to the list for ranking
    all_records = existing_records + [{
        'build_id': build_id,
        'timestamp_utc': timestamp_utc,
        'is_new': True
    }]

    # Sort by timestamp_utc, then by build_id for consistent ordering
    # Convert all timestamps to datetime objects for consistent sorting
    def get_sort_key(record):
        timestamp = record['timestamp_utc']
        if isinstance(timestamp, str):
            try:
                timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                # If parsing fails, use a default timestamp
                timestamp = datetime(2000, 1, 1)
        return (timestamp, record['build_id'])

    all_records.sort(key=get_sort_key)

    # Find the rank of the current record
    current_rank = None
    for i, record in enumerate(all_records):
        if record.get('is_new', False) and record['build_id'] == build_id and record['timestamp_utc'] == timestamp_utc:
            current_rank = i + 1
            break

    if current_rank is None:
        return build_id, False

    # Calculate release_version and is_major_release
    if current_rank == 1:
        # First deployment of this major version
        release_version = major_version
        is_major_release = True
    else:
        # Subsequent deployment
        release_version = build_id
        is_major_release = False

    return release_version, is_major_release

# Main execution
def main():
    parser = argparse.ArgumentParser(description="Add new events in the deployment_event table.")

    # Add command-line arguments
    parser.add_argument('-p', '--product', type=str, help='Product name (if provided, saves to database; otherwise saves to CSV)')
    parser.add_argument('-s', '--start-date', type=str, help='Start date in YYYY-MM-DD format')

    # Parse the arguments
    args = parser.parse_args()

    extractor = OctopusExtractor()

    if args.product is None:
        # CSV Mode: Load configuration from config.json
        config = json.load(open(os.path.join(common_dir, "config.json")))
        
        # Get configuration from config dictionary
        config = {
            'Organization': config.get('OCTOPUS_ORGANIZATION'),
            'Personal Access Token': config.get('OCTOPUS_API_TOKEN')
        }

        # Use checkpoint file for last modified date
        last_modified = Utils.load_checkpoint("octopus")

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
if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

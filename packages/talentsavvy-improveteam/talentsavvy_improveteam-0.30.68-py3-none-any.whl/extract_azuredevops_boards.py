#!/usr/bin/env python3
"""
Azure DevOps Boards Data Extraction Script

This script extracts work item events from Azure DevOps Boards and supports two modes of operation:

Usage:
    python extract_azuredevops_boards.py [-p <product_name>] [-s <start_date>]

Arguments:
    -p, --product: Product name (if provided, saves to database; otherwise saves to CSV)
    -s, --start-date: Start date for extraction in YYYY-MM-DD format (optional)

Modes (automatically determined):
    Database mode (when -p is provided):
        - Imports from the database module
        - Connects to the database
        - Reads the config from the data_source_config table
        - Gets the last extraction timestamp from the work_item_event table
        - Saves the extracted data to the database table

    CSV mode (when -p is NOT provided):
        - Reads the config from environment variables:
          * AZDO_ORGANIZATION: Azure DevOps organization
          * AZDO_API_TOKEN: Azure DevOps API token
          * AZDO_PROJECT: Azure DevOps project name
        - Gets the last extraction timestamp from the checkpoint (JSON) file
        - Saves the extracted data to one CSV file, updating the checkpoint (JSON) file

Events extracted:
    - Work Item Created
    - Work Item Updated
    - Work Item State Changed
"""

import requests
import base64
import json
from datetime import datetime
import pytz
import sys
import os
import argparse
import time
from typing import Dict

base_dir = os.path.dirname(os.path.abspath(__file__))
common_dir = os.path.join(base_dir, "common")
if not os.path.isdir(common_dir):
    # go up one level to find "common" (for installed package structure)
    base_dir = os.path.dirname(base_dir)
    common_dir = os.path.join(base_dir, "common")

if os.path.isdir(common_dir) and base_dir not in sys.path:
    sys.path.insert(0, base_dir)

import logging
from common.utils import Utils

# Configure logging to print messages on stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)
logger = logging.getLogger('extract_azuredevops_boards')

class AzureDevOpsBoardsExtractor:
    """Extracts work item events from Azure DevOps Boards with page-by-page processing."""

    def __init__(self):
        # Statistics
        self.stats = {
            'work_items_created': 0,
            'work_items_updated': 0,
            'total_inserted': 0,
            'total_duplicates': 0
        }

    def get_config_from_database(self, cursor):
        """Get Azure DevOps configuration from data_source_config table."""
        query = """
        SELECT config_item, config_value
        FROM data_source_config
        WHERE data_source = 'work_item_management'
        AND config_item IN ('Organization', 'Projects', 'Personal Access Token')
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
            else:
                config[config_item.lower().replace(' ', '_')] = config_value

        return config

    def get_last_modified_date(self, cursor):
        """Get the last modified date from the database."""
        query = """
        SELECT MAX(timestamp_utc) FROM work_item_event;
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

    def save_events_to_database(self, events, cursor):
        """Save events to database."""
        if not events:
            return 0, 0

        from psycopg2.extras import execute_values

        # Define the columns for the insert
        columns = [
            'work_item_id', 'project', 'type', 'parent_work_item_id',
            'state', 'title', 'timestamp_utc', 'extended_attributes', 'description_revisions'
        ]

        # Get count before insertion
        cursor.execute("SELECT COUNT(*) FROM work_item_event")
        count_before = cursor.fetchone()[0]

        # Use execute_values for batch insertion
        execute_values(
            cursor,
            f"INSERT INTO work_item_event ({', '.join(columns)}) VALUES %s ON CONFLICT DO NOTHING",
            events,
            template=None,
            page_size=1000
        )

        # Get count after insertion to determine actual inserted records
        cursor.execute("SELECT COUNT(*) FROM work_item_event")
        count_after = cursor.fetchone()[0]

        # Calculate actual inserted and skipped records
        inserted_count = count_after - count_before
        duplicate_count = len(events) - inserted_count

        return inserted_count, duplicate_count

    def run_extraction(self, cursor, config: Dict, start_date, last_modified, export_path: str = None):
        """
        Run extraction: fetch and save data page-by-page.

        Args:
            cursor: Database cursor (None for CSV mode)
            config: Configuration dictionary with organization, project, personal_access_token
            start_date: Start date string from command line (optional)
            last_modified: Last modified datetime from database or checkpoint
            export_path: Export path for CSV mode
        """
        # Track maximum timestamp for checkpoint saving
        max_timestamp = None

        # Validate required configuration
        if not config.get('organization'):
            logger.error("Missing required configuration: Organization")
            sys.exit(1)
        if not config.get('project'):
            logger.error("Missing required configuration: Project")
            sys.exit(1)
        if not config.get('personal_access_token'):
            logger.error("Missing required configuration: Personal Access Token")
            sys.exit(1)

        # Set up Azure DevOps API configuration
        organization = config['organization']
        project = config['project']
        personal_access_token = config['personal_access_token']
        pat_token = base64.b64encode(f":{personal_access_token}".encode()).decode()

        # Set headers for API call
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {pat_token}'
        }

        # Determine the start date
        if start_date:
            try:
                last_modified_date = datetime.strptime(start_date, '%Y-%m-%d')
            except ValueError:
                logger.error("Invalid date format. Please use YYYY-MM-DD format.")
                sys.exit(1)
        else:
            last_modified_date = last_modified

        # Set up function wrappers
        if cursor:
            # Database mode
            def save_output_fn(events):
                return self.save_events_to_database(events, cursor)
        else:
            # CSV mode - create CSV file at the start
            csv_file = Utils.create_csv_file("azuredevops_boards_events", export_path, logger)
            # Define columns matching database schema (same as in save_events_to_database)
            columns = [
                'work_item_id', 'project', 'type', 'parent_work_item_id',
                'state', 'title', 'timestamp_utc', 'extended_attributes', 'description_revisions'
            ]
            def save_output_fn(events):
                # Convert tuples to dictionaries using column names
                dict_events = [dict(zip(columns, event)) for event in events]
                result = Utils.save_events_to_csv(dict_events, csv_file, logger)
                nonlocal max_timestamp
                if result[3] and (not max_timestamp or result[3] > max_timestamp):
                    max_timestamp = result[3]
                return result[1:3]  # Return only inserted and duplicates

        # Log the fetch information
        logger.info(f"Starting extraction from {last_modified_date}")
        logger.info(f"Fetching data from https://dev.azure.com/{organization}/{project}")

        # Run the WIQL query to fetch modified work items since last modification date
        try:
            modified_work_items = run_wiql_query(last_modified_date, organization, project, headers)
        except Exception as e:
            logger.error(f"Error running WIQL query: {str(e)}")
            return

        # Check if Azure DevOps services are unavailable
        if not modified_work_items:
            logger.warning("No work items found. This could be due to:")
            logger.warning("1. No work items modified since the last extraction date")
            logger.warning("2. Azure DevOps services being temporarily unavailable")
            logger.warning("3. Authentication or permission issues")
            logger.warning("If you suspect a service outage, check: https://status.dev.azure.com/")

        # Initialize counters
        total_inserted = 0
        total_duplicates = 0

        if modified_work_items:
            logger.info(f"Processing {len(modified_work_items)} work items...")

            # Process each modified work item individually
            for i, item in enumerate(modified_work_items, 1):
                try:
                    revision_data_list = fetch_work_item_revisions(item['id'], last_modified_date, organization, project, headers)

                    # Save this work item's data
                    if revision_data_list:
                        inserted, duplicates = save_output_fn(revision_data_list)
                        total_inserted += inserted
                        total_duplicates += duplicates

                    # Log progress every 10 work items
                    if i % 10 == 0:
                        logger.info(f"Processed {i}/{len(modified_work_items)} work items ({total_inserted} inserted, {total_duplicates} duplicates)")

                except Exception as e:
                    logger.error(f"Error fetching work item revisions for {item['id']}: {str(e)}")
                    continue

        # Save checkpoint in CSV mode
        if not cursor and max_timestamp:
            if Utils.save_checkpoint(prefix="azuredevops_boards", last_dt=max_timestamp, export_path=export_path):
                logger.info(f"Checkpoint saved successfully: {max_timestamp}")
            else:
                logger.warning("Failed to save checkpoint")

        # Print summary statistics
        logger.info(f"Inserted {total_inserted} records, skipped {total_duplicates} duplicate records.")
        self.stats['total_inserted'] = total_inserted
        self.stats['total_duplicates'] = total_duplicates

# Function to safely extract data and handle missing or invalid fields
def safe_get(data, keys, default_value='NULL'):
    try:
        for key in keys:
            data = data[key]
        if isinstance(data, str):
            return "'{}'".format(data.replace("'", "''"))  # Escape single quotes for SQL
        if isinstance(data, (int, float)):
            return data
        return "'{}'".format(data)
    except (KeyError, TypeError):
        return default_value


# Function to build extended_attributes JSON with only keys that Azure DevOps provides
def build_extended_attributes(revision, fields):
    """
    Build extended_attributes JSON including only keys that Azure DevOps actually provides.
    """
    extended_attrs = {}

    area_path_value = fields.get('System.AreaPath')
    if area_path_value is not None:
        extended_attrs['area_path'] = area_path_value

    iteration_path_value = fields.get('System.IterationPath')
    if iteration_path_value is not None:
        extended_attrs['iteration_path'] = iteration_path_value

    priority_value = fields.get('Microsoft.VSTS.Common.Priority')
    if priority_value is not None:
        extended_attrs['priority'] = priority_value

    assignee_value = fields.get('System.AssignedTo', {}).get('displayName') if isinstance(fields.get('System.AssignedTo'), dict) else fields.get('System.AssignedTo')
    if assignee_value is not None:
        extended_attrs['assignee'] = assignee_value

    story_points_value = fields.get('Microsoft.VSTS.Scheduling.StoryPoints')
    if story_points_value is not None:
        extended_attrs['story_points'] = story_points_value

    return json.dumps(extended_attrs) if extended_attrs else None

# Function to check if Title/Description/Acceptance Criteria changed
def has_content_changed(current_revision, previous_revision):
    """
    Check if Title, Description, or Acceptance Criteria changed between revisions.
    Returns 1 if any of these fields changed, 0 otherwise.
    """
    if not previous_revision:
        return 0  # First revision, no change to count

    current_fields = current_revision.get('fields', {})
    previous_fields = previous_revision.get('fields', {})

    # Fields to track for changes (Title/Description/Acceptance Criteria)
    fields_to_track = [
        'System.Title',
        'System.Description',
        'Microsoft.VSTS.Common.AcceptanceCriteria'
    ]

    for field in fields_to_track:
        current_value = current_fields.get(field, '')
        previous_value = previous_fields.get(field, '')

        # Normalize None to empty string for comparison
        current_value = current_value if current_value is not None else ''
        previous_value = previous_value if previous_value is not None else ''

        if current_value != previous_value:
            return 1  # Change detected in Title/Description/Acceptance Criteria

    return 0  # No changes detected in tracked fields

# Function to prepare revision data for batch insertion
def prepare_revision_data(revision, work_item_id, description_revisions):
    fields = revision.get('fields', {})

    # Convert and rename state_change_date to timestamp_utc
    state_change_date = safe_get(fields, ['System.ChangedDate'])
    timestamp_utc = Utils.convert_to_utc(state_change_date.strip("'")) if state_change_date != 'NULL' else None

    # Build extended_attributes JSON
    extended_attributes = build_extended_attributes(revision, fields)

    # Extract field values safely
    def safe_extract(field_path, default=None):
        try:
            current_data = fields
            for key in field_path:
                if isinstance(current_data, dict):
                    current_data = current_data[key]
                else:
                    return default
            return current_data if current_data is not None else default
        except (KeyError, TypeError):
            return default

    return (
        work_item_id,
        safe_extract(['System.TeamProject']),
        safe_extract(['System.WorkItemType']),
        safe_extract(['System.Parent']),
        safe_extract(['System.State']),
        safe_extract(['System.Title']),
        timestamp_utc,
        extended_attributes,
        description_revisions
    )

# Function to check if the response is in JSON format
def is_json(response_text):
    try:
        json.loads(response_text)
        return True
    except ValueError:
        return False

# Function to run a Wiql query to fetch work items modified after the last known date (date-only)
def run_wiql_query(last_modified_date, organization, project, headers):
    last_modified_date_str = last_modified_date.strftime('%Y-%m-%d')  # Truncate time for WIQL
    query_url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/wiql?api-version=6.0"
    wiql_query = {
        "query": f"SELECT [System.Id], [System.ChangedDate] FROM WorkItems WHERE [System.TeamProject] = '{project}' AND [System.ChangedDate] >= '{last_modified_date_str}' ORDER BY [System.ChangedDate] DESC"
    }

    # Retry logic for failed requests
    max_retries = 3
    retry_delay = 1  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.post(query_url, headers=headers, json=wiql_query, timeout=30)

            if response.status_code == 200 and is_json(response.text):
                return response.json().get('workItems', [])
            elif response.status_code == 403:
                # Rate limit exceeded
                if 'X-RateLimit-Reset' in response.headers:
                    reset_time = int(response.headers['X-RateLimit-Reset'])
                    wait_time = reset_time - int(time.time()) + 10  # Add 10 seconds buffer
                    logger.warning(f"Rate limit exceeded. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.warning(f"Rate limit exceeded for WIQL query")
                    return []
            else:
                logger.error(f"Error running WIQL query: {response.status_code}")
                if not is_json(response.text):
                    logging.error("Response is not valid JSON. Azure DevOps services may be unavailable.")
                    logging.error("Raw response (first 500 chars):")
                    logging.error(response.text[:500])
                else:
                    logging.error(f"Response: {response.text}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                    continue
                else:
                    return []

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed for WIQL query (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                continue
            else:
                return []

    return []

# Fetch Work Item Revisions from Azure DevOps API for modified work items
def fetch_work_item_revisions(work_item_id, last_modified_date, organization, project, headers):
    revisions_url = f"https://dev.azure.com/{organization}/{project}/_apis/wit/workitems/{work_item_id}/revisions?api-version=6.0&$expand=relations"

    # Retry logic for failed requests
    max_retries = 3
    retry_delay = 1  # seconds

    for attempt in range(max_retries):
        try:
            response = requests.get(revisions_url, headers=headers, timeout=30)

            # Check if the response is valid JSON
            if response.status_code == 200 and is_json(response.text):
                revisions_data = response.json()
                break
            elif response.status_code == 403:
                # Rate limit exceeded
                if 'X-RateLimit-Reset' in response.headers:
                    reset_time = int(response.headers['X-RateLimit-Reset'])
                    wait_time = reset_time - int(time.time()) + 10
                    logging.warning(f"Rate limit exceeded. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.warning(f"Rate limit exceeded for work item revisions {work_item_id}")
                    return []
            else:
                logger.error(f"Error fetching work item revisions: {response.status_code}")
                if not is_json(response.text):
                    logging.error("Response is not valid JSON. Azure DevOps services may be unavailable.")
                    logging.error("Raw response (first 500 chars):")
                    logging.error(response.text[:500])
                else:
                    logging.error(f"Response: {response.text}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                    continue
                else:
                    return []

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed for work item revisions {work_item_id} (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
                continue
            else:
                return []
    else:
        return []

    # Process the revisions and collect data for batch insertion
    revision_data_list = []
    if 'value' in revisions_data:
        revisions = revisions_data['value']

        for i, revision in enumerate(revisions):
            changed_date = revision['fields'].get('System.ChangedDate')
            if changed_date:
                changed_date_dt = Utils.convert_to_utc(changed_date)  # Convert to naive UTC datetime

                # Only process if changed date is after the last modified date
                if changed_date_dt > last_modified_date:
                    # Get previous revision for comparison (if exists)
                    previous_revision = revisions[i-1] if i > 0 else None

                    description_revisions = has_content_changed(revision, previous_revision)

                    # Prepare data for batch insertion
                    revision_data = prepare_revision_data(revision, work_item_id, description_revisions)
                    revision_data_list.append(revision_data)

    return revision_data_list

# Main Execution: Fetch work items modified since the last known date
def main():
    parser = argparse.ArgumentParser(description="Extract Azure DevOps Boards work item events to database or CSV.")

    # Add command-line arguments
    parser.add_argument('-p', '--product', type=str, help='Product name (if provided, saves to database; otherwise saves to CSV)')
    parser.add_argument('-s', '--start-date', type=str, help='Start date in YYYY-MM-DD format')

    # Parse the arguments
    args = parser.parse_args()

    extractor = AzureDevOpsBoardsExtractor()

    if args.product is None:
        # CSV Mode: Load configuration from config.json
        config = json.load(open(os.path.join(common_dir, "config.json")))
        
        # Get configuration from config dictionary
        config = {
            'organization': config.get('AZDO_ORGANIZATION'),
            'personal_access_token': config.get('AZDO_API_TOKEN'),
            'project': config.get('AZDO_PROJECT')
        }

        # Use checkpoint file for last modified date
        checkpoint_file = "azuredevops_boards"
        last_modified = Utils.load_checkpoint(checkpoint_file)

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

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)

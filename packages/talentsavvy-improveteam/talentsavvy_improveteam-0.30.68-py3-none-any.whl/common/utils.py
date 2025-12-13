import datetime
import json
import os

import pandas as pd
from dateutil.parser import isoparse

config = json.load(open(os.path.join(os.path.dirname(__file__), "config.json")))
EXPORT_PATH = config.get("EXPORT_PATH", os.path.join(os.path.dirname(__file__), "export"))

class Utils:
    DATE_FORMAT = "%Y-%m-%d"
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    DATE_TIME_FORMAT_WITH_TZ = "%Y-%m-%dT%H:%M:%SZ"
    LOGGER = None

    @staticmethod
    def load_checkpoint(prefix, export_path=None) -> datetime:
        """
        This method loads the json checkpoint, exported last time

        :param prefix: filename prefix
        :param export_path: Optional export path, defaults to EXPORT_PATH
        :return: datetime (naive UTC)
        """
        if not prefix:
            return None
        try:
            # Use provided export_path or fall back to global EXPORT_PATH
            path_to_use = export_path if export_path is not None else EXPORT_PATH
            os.makedirs(path_to_use, exist_ok=True)
            filepath = os.path.join(path_to_use, f"{prefix}_checkpoint.json")
            if not os.path.exists(filepath):
                return None
            with open(filepath, "r") as f:
                ts_str = json.load(f).get(f"last_run")
                if ts_str:
                    return Utils.convert_to_utc(ts_str)
                return None
        except Exception as ex:
            print(ex)
            return None

    @staticmethod
    def save_checkpoint(prefix: str, last_dt: datetime, export_path=None):
        """
        This method saves the latest datetime to a checkpoint json file

        :param prefix: filename prefix
        :param last_dt: last date time (naive UTC)
        :param export_path: Optional export path, defaults to EXPORT_PATH
        :return: bool
        """
        if not last_dt or last_dt == '':
            Utils.LOGGER.warning("No last date found to save as checkpoint")
            return None
        try:
            # Use provided export_path or fall back to global EXPORT_PATH
            path_to_use = export_path if export_path is not None else EXPORT_PATH
            filepath = os.path.join(path_to_use, f"{prefix}_checkpoint.json")
            with open(filepath, "w") as f:
                if type(last_dt) == str:
                    last_dt = Utils.convert_to_utc(last_dt)
                else:
                    # Ensure datetime is naive UTC
                    if last_dt.tzinfo is not None:
                        last_dt = last_dt.astimezone(datetime.timezone.utc).replace(tzinfo=None)
                # Save as ISO format (naive datetime will be saved without timezone)
                json.dump({"last_run": last_dt.isoformat(sep='T', timespec='auto')}, f)
                return True
        except Exception as ex:
            Utils.LOGGER.error(ex)
        return None

    @staticmethod
    def convert_to_utc(timestamp):
        """
        Convert a timestamp string to a naive UTC datetime using dateutil.isoparse.
        Returns None if parsing fails or input is falsy.
        """
        if not timestamp:
            return None
        try:
            dt = isoparse(timestamp)
        except Exception:
            # Fallback: attempt common 'Z' replacement
            try:
                dt = datetime.datetime.fromisoformat(str(timestamp).replace('Z', '+00:00'))
            except Exception:
                return None
        if dt.tzinfo is not None:
            return dt.astimezone(datetime.timezone.utc).replace(tzinfo=None)
        # Treat naive as UTC
        return dt

    @staticmethod
    def create_csv_file(csv_filename, export_path, logger=None):
        """
        Create a CSV file with timestamped filename.
        The header will be written when the first events are saved.
        
        :param csv_filename: Base CSV filename (e.g., "jira_events")
        :param export_path: Directory path where CSV file will be saved
        :param logger: Optional logger for info messages
        :return: Full path to the created CSV file
        """
        # Generate timestamped filename
        current_time = datetime.datetime.now()
        timestamp_str = current_time.strftime("%Y_%m_%d_%H_%M_%S")
        path_to_use = export_path if export_path is not None else EXPORT_PATH
        csv_file = os.path.join(path_to_use, f"{csv_filename}_{timestamp_str}.csv")
        
        # Create empty file - header will be written with first event
        with open(csv_file, 'w') as f:
            pass
        
        if logger:
            logger.info(f"Created CSV file: {csv_file}")
        
        return csv_file

    @staticmethod
    def save_events_to_csv(events, csv_file, logger=None):
        """
        Save events to CSV file by appending to existing file.
        Writes header if file is empty (first call).
        
        :param events: List of event dictionaries to save
        :param csv_file: Full path to the CSV file (created by create_csv_file())
        :param logger: Optional logger for info messages
        :return: Tuple of (total_events, inserted_events, duplicates, max_timestamp)
        """
        if not events:
            return 0, 0, 0, None

        # Find the maximum timestamp from events and convert extended_attributes to JSON strings
        max_ts = None
        processed_events = []
        for event in events:
            # Convert extended_attributes dict to JSON string if present
            if event.get('extended_attributes') and isinstance(event.get('extended_attributes'), dict):
                event = event.copy()  # Don't modify original event
                # Ensure JSON is properly formatted - parse and re-serialize to normalize
                try:
                    normalized_json = json.dumps(event['extended_attributes'], ensure_ascii=False)
                    event['extended_attributes'] = normalized_json
                except (TypeError, ValueError) as e:
                    # If JSON serialization fails, log and set to None
                    if logger:
                        logger.warning(f"Failed to serialize extended_attributes to JSON: {e}")
                    event['extended_attributes'] = None
            
            if event.get('timestamp_utc'):
                if not max_ts or event['timestamp_utc'] > max_ts:
                    max_ts = event['timestamp_utc']
            
            processed_events.append(event)

        # Convert events to DataFrame
        df = pd.DataFrame(processed_events)
        
        # Check if file is empty (first write) to determine if header should be written
        file_is_empty = os.path.getsize(csv_file) == 0
        
        # Append to CSV file (with header if file is empty, otherwise without)
        # Use default quoting (QUOTE_MINIMAL) which handles JSON strings correctly
        df.to_csv(csv_file, mode='a', header=file_is_empty, index=False)
        
        if logger:
            logger.info(f"Saved {len(events)} events to {csv_file}")

        return len(events), len(events), 0, max_ts

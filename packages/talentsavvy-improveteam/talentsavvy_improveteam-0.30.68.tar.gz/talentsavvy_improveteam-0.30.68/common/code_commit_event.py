import json
import logging
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class CodeCommitEvent:
    """Utility class for code_commit_event table operations."""
    
    LOGGER = None
    
    def __init__(self):
        pass
    
    @staticmethod
    def get_last_event(cursor) -> Optional[datetime]:
        """
        Get the last modified date from the code_commit_event table.
        
        Args:
            cursor: Database cursor
            
        Returns:
            Last modified timestamp_utc or None if no records exist
        """
        query = """
        SELECT MAX(timestamp_utc)
        FROM code_commit_event
        """
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result and result[0] else None
    
    @staticmethod
    def create_event(
        timestamp_utc: datetime,
        repo_name: str,
        event_type: str,
        work_item_id: Optional[str] = None,
        source_branch: str = '',
        target_branch: str = '',
        revision: str = '',
        author: str = '',
        comment: str = '',
        extended_attributes: Optional[Dict] = None
    ) -> Dict:
        """
        Create event dictionary with all required fields for code_commit_event table.
        
        Args:
            timestamp_utc: Event timestamp in UTC
            repo_name: Repository name
            event_type: Event type (e.g., 'Pull Request Created', 'Code Committed')
            work_item_id: Work item ID (optional)
            source_branch: Source branch name (optional)
            target_branch: Target branch name (optional)
            revision: Commit SHA/revision (optional)
            author: Author name (optional)
            comment: Commit message or comment (optional)
            extended_attributes: Additional attributes as dict (optional)
            
        Returns:
            Event dictionary ready for database insertion
        """
        return {
            'timestamp_utc': timestamp_utc,
            'work_item_id': work_item_id,
            'source_branch': source_branch,
            'repo': repo_name,
            'target_branch': target_branch,
            'revision': revision,
            'author': author,
            'comment': comment,
            'event': event_type,
            'extended_attributes': extended_attributes
        }
    
    @staticmethod
    def convert_event_to_tuple(event: Dict) -> tuple:
        """
        Convert event dictionary to tuple for database insertion.
        
        Args:
            event: Event dictionary
            
        Returns:
            Tuple of event values ready for database insertion
        """
        timestamp = event.get('timestamp_utc')
        timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S') if timestamp is not None else None
        
        # Convert extended_attributes to JSON string if present
        extended_attrs_json = json.dumps(event.get('extended_attributes')) if event.get('extended_attributes') else None
        
        return (
            timestamp_str,
            event.get('work_item_id'),
            event.get('source_branch', ''),
            event.get('repo'),
            event.get('target_branch', ''),
            event.get('revision', ''),
            event.get('author', ''),
            event.get('comment', ''),
            event.get('event'),
            extended_attrs_json
        )
    
    @staticmethod
    def save_events_to_database(
        events: List[Dict],
        cursor,
        connection=None
    ) -> Tuple[int, int, int]:
        """
        Save events to the code_commit_event table.
        
        Args:
            events: List of event dictionaries
            cursor: Database cursor
            connection: Database connection (optional, uses cursor.connection if not provided)
            
        Returns:
            tuple: (total_events, inserted_count, duplicate_count)
        """
        if not events:
            if CodeCommitEvent.LOGGER:
                CodeCommitEvent.LOGGER.info("No events to save")
            return 0, 0, 0
    
        from psycopg2.extras import execute_values

        insert_sql = """
        INSERT INTO code_commit_event (
            timestamp_utc, work_item_id, source_branch, repo,
            target_branch, revision, author, comment, event, extended_attributes
        ) VALUES %s
        ON CONFLICT ON CONSTRAINT code_commit_event_hash_unique DO NOTHING
        """
        
        # Convert events to tuples for insertion
        values = [CodeCommitEvent.convert_event_to_tuple(event) for event in events]
        
        # Get count before insertion
        cursor.execute("SELECT COUNT(*) FROM code_commit_event")
        count_before = cursor.fetchone()[0]
        
        # Execute batch insert
        execute_values(cursor, insert_sql, values)
        
        # Commit transaction
        if connection:
            connection.commit()
        else:
            cursor.connection.commit()
        
        # Get count after insertion
        cursor.execute("SELECT COUNT(*) FROM code_commit_event")
        count_after = cursor.fetchone()[0]
        
        # Calculate actual inserted and skipped records
        inserted_count = count_after - count_before
        duplicate_count = len(events) - inserted_count
        
        if CodeCommitEvent.LOGGER:
            CodeCommitEvent.LOGGER.info(
                f"Inserted {inserted_count} events into database, "
                f"skipped {duplicate_count} duplicate records"
            )
        
        return len(events), inserted_count, duplicate_count


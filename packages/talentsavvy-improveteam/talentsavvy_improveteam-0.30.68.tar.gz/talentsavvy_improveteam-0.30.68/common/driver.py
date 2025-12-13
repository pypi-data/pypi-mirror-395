import argparse
import os
import logging
from pathlib import Path
from datetime import datetime

from database import DatabaseConnection
from reader import CsvEventReader

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Driver:
    LOGGER = logging.getLogger(__name__)

    def run(self, db_loader_class, event_parser_class, processor_class, required_columns=None, encoding="utf-8"):
        """
        This is a driver method that accepts cli arguments and run the load
        """
        parser = argparse.ArgumentParser(
            description="Load Code Commit Events from CSV files to database."
        )
        parser.add_argument('-p', '--product', required=True, help='Product name')
        parser.add_argument('-d', '--directory', help='Directory of CSV files')
        parser.add_argument('-f', '--file', help='CSV File')
        args = parser.parse_args()
        file = args.file
        directory = args.directory
        product = args.product

        db = DatabaseConnection()
        with db.product_scope(product) as conn:

            reader = CsvEventReader()
            loader = db_loader_class(conn)
            regex_configuration = loader.get_regex_configuration(product)
            parser = event_parser_class(regex_configuration)

            processor_obj = processor_class(reader, parser, loader, encoding=encoding, required_columns=required_columns)
            if file:
                if not os.path.exists(file):
                    self.LOGGER.error(f"Error: File not found: {file}")
                    return 1
                my_dir = Path(file)
                if my_dir.is_dir():
                    self.LOGGER.error("The path you provided is a directory")
                    return 1
                processor_obj.process_single_file(file)
            elif directory:
                self.LOGGER.info(f"Processing Directory {directory}")
                if not os.path.exists(directory):
                    print(f"Error: Directory not found: {directory}")
                    return 1
                my_dir = Path(directory)
                if my_dir.is_dir():
                    processor_obj.process_directory(directory)
                else:
                    self.LOGGER.error("The path you provided is not a file but a directory")
                    return 1
            else:
                self.LOGGER.error("Please provide file/directory to load")

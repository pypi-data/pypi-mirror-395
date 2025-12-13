import csv
import os
from typing import List


class CsvEventReader:
    """
    Reads raw event data from CSV files in a directory.
    """

    def list_files(self, directory, file_pattern=None) -> List[str]:
        """
        This method lists the files in a directory, optionally filtering by pattern

        :param directory: Directory path
        :param file_pattern: Optional file pattern to match (e.g., "azuredevops_*_pipelines_*")
        :return: list of filepaths
        """
        import fnmatch

        files = []
        for f in os.listdir(directory):
            if f.lower().endswith(f".csv"):
                if file_pattern:
                    # Check if filename matches the pattern
                    if fnmatch.fnmatch(f.lower(), file_pattern.lower()):
                        files.append(os.path.join(directory, f))
                else:
                    files.append(os.path.join(directory, f))
        return files

    def read(self, path: str, logger, required_columns=None, encoding="utf-8") -> List[dict]:
        """
        This method reads the csv file and appends str row to list

        :param logger:
        :param encoding:
        :param required_columns:
        :param path: File path
        :return: List of str rows
        """
        rows = []
        with open(path, 'r', encoding=encoding) as fh:
            reader = csv.DictReader(fh)
            for i, row in enumerate(reader, start=2):
                if required_columns and not required_columns.issubset(row.keys()):
                    logger.warning("Skipping line %d in %s: missing columns", i, path)
                    continue
                rows.append(row)
        return rows

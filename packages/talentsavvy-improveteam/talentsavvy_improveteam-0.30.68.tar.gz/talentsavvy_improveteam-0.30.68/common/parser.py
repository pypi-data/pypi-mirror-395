import datetime as dtime
from typing import Optional

from dateutil import parser as date_parser


class Parser:

    def __init__(self):
        pass

    def parse_timestamp(self, timestamp_str: str):
        """
        This method parses the timestamp from CSV file

        :param timestamp_str: timestamp value
        :return: datetime object
        """
        if not timestamp_str:
            return timestamp_str
        dt = date_parser.parse(timestamp_str)
        if dt.tzinfo:
            dt = dt.astimezone(dtime.timezone.utc).replace(tzinfo=None)
        return dt

    def safe_check_dict_value(self, dict_obj, key, type_obj, default_value=None):
        """
        This method checks a certain key exists in dict and if yes then
        if it is of valid data type

        :param dict_obj: Dictionary object
        :param key: key
        :param type_obj: type int, str etc
        :param default_value: None, ''
        :return: dict value or default value
        """
        if key in dict_obj and type(dict_obj[key]) == type_obj:
            return dict_obj.get(key)
        else:
            return default_value

    def extract_work_item_id(self, work_item_regex, val: str) -> Optional[str]:
        """
        This method extracts the `work_item_id` from input str value

        :param val: Input val
        :return: matching `work_item_id`
        """
        if not work_item_regex:
            return ''
        match = work_item_regex.search(val or '')
        return match.group(0) if match else None

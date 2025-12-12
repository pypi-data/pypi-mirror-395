from datetime import datetime
import enum


class DT_FORMAT(enum):
    DEFAULT_PATTERN = "%Y-%m-%d %H:%M:%S"
    DEFAULT_PATTERN_V2 = "%Y%m%d_%H%M%S"


def timestamp_to_datetime_second(timestamp):
    return datetime.fromtimestamp(timestamp)


def timestamp_to_datetime_millisecond(timestamp):
    return datetime.fromtimestamp(timestamp / 1000)


def datetime_to_str(dt: datetime, format: str = DT_FORMAT.DEFAULT_PATTERN):
    return dt.strftime(format)


def str_to_datetime(s: str, format: str = DT_FORMAT.DEFAULT_PATTERN):
    return datetime.strptime(s, format)

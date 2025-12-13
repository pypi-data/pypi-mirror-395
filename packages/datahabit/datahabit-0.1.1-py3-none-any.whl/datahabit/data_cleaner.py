"""
data_cleaner.py
--------------------
Provides utilities for timestamp cleaning, validation, and conversion.
Returns datetime objects for downstream use.
"""

from datetime import datetime
import re

class DataCleanerError(Exception):
    """Base exception for DataCleaner."""
    def __init__(self, message):
        super().__init__(f"[DataCleanerError] {message}")


class InvalidTimestampError(DataCleanerError):
    """Raised when a timestamp string is invalid."""
    def __init__(self, value):
        super().__init__(f"Invalid timestamp format: '{value}'. Could not parse into a datetime.")


class NullEntryError(DataCleanerError):
    """Raised when encountering unexpected None or empty entries."""
    def __init__(self):
        super().__init__("Encountered a null or empty timestamp entry.")


class DataCleaner:
    """Handles cleaning and validation of timestamp data and normalization."""

    # common possible formats (extend if needed)
    _formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y/%m/%d",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y %H:%M",
        "%m/%d/%Y",
        "%d-%m-%Y %H:%M:%S",
        "%d-%m-%Y %H:%M",
        "%d-%m-%Y",
        "%Y.%m.%d %H:%M:%S",
        "%Y.%m.%d"
    ]

    @staticmethod
    def is_blank(ts):
        return ts is None or (isinstance(ts, str) and ts.strip() == "")

    @staticmethod
    def parse_timestamp(ts):
        """
        Parse a timestamp into a datetime object.
        Accepts:
          - datetime.datetime -> returned as-is
          - pandas.Timestamp -> uses .to_pydatetime() if available
          - numeric epoch (int/float) -> treated as seconds since epoch
          - string in many common formats
        Raises:
          NullEntryError, InvalidTimestampError
        """
        if DataCleaner.is_blank(ts):
            raise NullEntryError()

        # if it's already a datetime-like
        try:
            import datetime as _dt
            if isinstance(ts, _dt.datetime):
                return ts
        except Exception:
            pass

        # pandas Timestamp or numpy datetime64
        try:
            import pandas as _pd
            if isinstance(ts, _pd.Timestamp):
                return ts.to_pydatetime()
        except Exception:
            # pandas may not be installed; that's fine
            pass

        # numeric epoch
        if isinstance(ts, (int, float)):
            try:
                return datetime.fromtimestamp(ts)
            except Exception:
                raise InvalidTimestampError(ts)

        # strings: try to clean known anomalies
        if isinstance(ts, str):
            s = ts.strip()

            # remove trailing timezone offsets like +08:00 or Z
            s = re.sub(r'Z$', '', s)
            s = re.sub(r'([+-]\d{2}:?\d{2})$', '', s).strip()

            # Try ISO-like parse by trying our known formats
            for fmt in DataCleaner._formats:
                try:
                    return datetime.strptime(s, fmt)
                except Exception:
                    continue

            # As last resort try Python's fromisoformat (py3.7+)
            try:
                return datetime.fromisoformat(s)
            except Exception:
                pass

        raise InvalidTimestampError(ts)


    @staticmethod
    def validate_timestamp(timestamp_str):
        """Returns True if a timestamp can be parsed into a datetime."""
        try:
            DataCleaner.parse_timestamp(timestamp_str)
            return True
        except Exception:
            return False

    @staticmethod
    def fix_missing(entries, replacement="MISSING"):
        """
        Replaces missing timestamps (None or "") with a replacement string.
        """
        cleaned = []
        for ts in entries:
            if DataCleaner.is_blank(ts):
                cleaned.append(replacement)
            else:
                cleaned.append(ts)
        return cleaned

    @staticmethod
    def convert_all(entries):
        """
        Converts all valid timestamps into datetime objects.
        Raises structured errors on bad entries.
        """
        converted = []
        for ts in entries:
            if DataCleaner.is_blank(ts):
                raise NullEntryError()
            converted.append(DataCleaner.parse_timestamp(ts))
        return converted

    def __repr__(self):
        return "DataCleaner(timestamp utilities)"






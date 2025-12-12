"""
data_cleaner.py
--------------------
Provides utilities for timestamp cleaning, validation, and conversion.
Includes custom error types for robust data processing.
"""

from datetime import datetime


class DataCleanerError(Exception):
    """Base exception for DataCleaner."""
    def __init__(self, message):
        super().__init__(f"[DataCleanerError] {message}")


class InvalidTimestampError(DataCleanerError):
    """Raised when a timestamp string is invalid."""
    def __init__(self, value):
        super().__init__(f"Invalid timestamp format: '{value}'. Expected 'YYYY-MM-DD HH:MM:SS'.")


class NullEntryError(DataCleanerError):
    """Raised when encountering unexpected None or empty entries."""
    def __init__(self):
        super().__init__("Encountered a null or empty timestamp entry.")


class DataCleaner:
    """Handles cleaning and validation of timestamp data."""

    # --------------------------------------------------------

    @staticmethod
    def validate_timestamp(timestamp_str):
        """
        Returns True if a timestamp follows the correct format.
        """
        if timestamp_str is None or timestamp_str == "":
            return False

        try:
            datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            return True
        except Exception:
            return False

    # --------------------------------------------------------

    @staticmethod
    def fix_missing(entries, replacement="MISSING"):
        """
        Replaces missing timestamps (None or "") with a replacement.
        """
        cleaned = []

        for ts in entries:
            if ts is None or ts == "":
                cleaned.append(replacement)
            else:
                cleaned.append(ts)

        return cleaned

    # --------------------------------------------------------

    @staticmethod
    def convert_all(entries):
        """
        Converts all valid timestamps into datetime objects.
        Invalid entries raise structured errors.
        """
        converted = []

        for ts in entries:
            if ts is None or ts == "":
                raise NullEntryError()

            try:
                converted.append(datetime.strptime(ts, "%Y-%m-%d %H:%M:%S"))
            except Exception:
                raise InvalidTimestampError(ts)

        return converted

    # --------------------------------------------------------

    def __repr__(self):
        return "DataCleaner(timestamp utilities)"



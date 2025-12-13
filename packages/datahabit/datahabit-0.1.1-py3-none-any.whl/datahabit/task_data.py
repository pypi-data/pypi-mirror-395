"""
task_data.py
--------------------
TaskData is now forgiving: accepts dicts, dataclass-like, DataFrame rows, strings, datetimes.
"""

from datetime import datetime
from .data_cleaner import DataCleaner, NullEntryError, InvalidTimestampError

class TaskDataError(Exception):
    """Base exception for TaskData."""
    def __init__(self, message):
        super().__init__(f"[TaskDataError] {message}")


class InvalidTimestampErrorTask(TaskDataError):
    """Raised when timestamp format is invalid for TaskData."""
    def __init__(self, value):
        super().__init__(f"Invalid timestamp format for TaskData: '{value}'.")


class MissingFieldError(TaskDataError):
    """Raised when required fields are missing."""
    def __init__(self, field_name):
        super().__init__(f"Missing required field: {field_name}")


class TaskData:
    """
    Stores task-related information and provides delay computations.

    Accepts constructor inputs:
      - (student_id, task_name, submission_time)
      - a dict-like object with keys: student_id, task_name, submission_time, optionally due_date
      - a pandas Series / DataFrame row with same keys
    """

    def __init__(self, student_id=None, task_name=None, submission_time=None, **kwargs):
        # allow dict-like single arg usage
        if student_id is not None and task_name is None and submission_time is None and isinstance(student_id, (dict,)):
            data = student_id
            student_id = data.get("student_id") or data.get("student") or data.get("user") or None
            task_name = data.get("task_name") or data.get("task") or data.get("assignment") or None
            submission_time = data.get("submission_time") or data.get("submitted_at") or data.get("timestamp") or None
            # optional due_date can be stored too
            self._due_date_raw = data.get("due_date") or data.get("due") or kwargs.get("due_date", None)
        else:
            # allow direct kwargs override
            self._due_date_raw = kwargs.get("due_date", None)

        if not student_id:
            raise MissingFieldError("student_id")

        if not task_name:
            raise MissingFieldError("task_name")

        if submission_time is None:
            raise MissingFieldError("submission_time")

        self._student_id = student_id
        self._task_name = task_name
        self._submission_time_raw = submission_time

        # parse submission_time into datetime
        try:
            self._submission_time = DataCleaner.parse_timestamp(submission_time)
        except NullEntryError:
            raise MissingFieldError("submission_time")
        except InvalidTimestampError as e:
            raise InvalidTimestampErrorTask(submission_time) from e

        # parse due_date if present
        self._due_date = None
        if self._due_date_raw is not None:
            try:
                self._due_date = DataCleaner.parse_timestamp(self._due_date_raw)
            except Exception:
                # leave as None, up to caller to pass due_date externally
                self._due_date = None

    # --------------------------------------------------------

    def get_delay(self, due_date=None):
        """
        Computes delay relative to a due date.
        Returns datetime.timedelta.

        If due_date is None, and the TaskData has an internal due_date, it uses that.
        due_date may be a string/datetime/pandas Timestamp.
        """
        if due_date is None:
            if self._due_date is None:
                raise TaskDataError("No due_date provided to compute delay.")
            due_dt = self._due_date
        else:
            try:
                due_dt = DataCleaner.parse_timestamp(due_date)
            except Exception as e:
                raise InvalidTimestampErrorTask(due_date) from e

        return self._submission_time - due_dt

    # --------------------------------------------------------

    def as_dict(self):
        return {
            "student_id": self._student_id,
            "task_name": self._task_name,
            "submission_time": self._submission_time,
            "submission_time_raw": self._submission_time_raw,
            "due_date": self._due_date
        }

    def __str__(self):
        sub = self._submission_time.strftime("%Y-%m-%d %H:%M:%S")
        return f"TaskData(student={self._student_id}, task='{self._task_name}', submitted='{sub}')"



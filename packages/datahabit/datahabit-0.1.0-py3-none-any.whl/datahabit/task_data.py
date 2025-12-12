"""
task_data.py
--------------------
Defines the TaskData class and its custom error types.
"""

from datetime import datetime

class TaskDataError(Exception):
    """Base exception for TaskData."""
    def __init__(self, message):
        super().__init__(f"[TaskDataError] {message}")


class InvalidTimestampError(TaskDataError):
    """Raised when timestamp format is invalid."""
    def __init__(self, value):
        super().__init__(f"Invalid timestamp format: '{value}'. Expected 'YYYY-MM-DD HH:MM:SS'")


class MissingFieldError(TaskDataError):
    """Raised when required fields (student_id, task_name, etc.) are missing."""
    def __init__(self, field_name):
        super().__init__(f"Missing required field: {field_name}")

class TaskData:
    """
    Stores task-related information and provides delay computations.
    """

    def __init__(self, student_id, task_name, submission_time):
        # Validate required fields
        if not student_id:
            raise MissingFieldError("student_id")

        if not task_name:
            raise MissingFieldError("task_name")

        if not submission_time:
            raise MissingFieldError("submission_time")

        self._student_id = student_id
        self._task_name = task_name
        self._submission_time_raw = submission_time

        # Convert timestamp → datetime
        self._submission_time = self._parse_timestamp(submission_time)

    # --------------------------------------------------------

    @staticmethod
    def _parse_timestamp(ts):
        """Parses string timestamps into datetime objects with validation."""
        try:
            return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
        except Exception:
            raise InvalidTimestampError(ts)

    # --------------------------------------------------------

    def get_delay(self, due_date):
        """
        Computes delay relative to a due date.
        Returns datetime.timedelta.
        """
        if isinstance(due_date, str):
            try:
                due_date = datetime.strptime(due_date, "%Y-%m-%d %H:%M:%S")
            except:
                raise InvalidTimestampError(due_date)

        return self._submission_time - due_date

    # --------------------------------------------------------

    def __str__(self):
        return (
            f"TaskData(student={self._student_id}, "
            f"task='{self._task_name}', "
            f"submitted='{self._submission_time_raw}')"
        )


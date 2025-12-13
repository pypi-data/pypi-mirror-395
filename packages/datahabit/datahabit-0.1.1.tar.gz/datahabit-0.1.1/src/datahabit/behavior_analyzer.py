"""
behavior_analyzer.py
-------------------------
Analyzes student submission behavior across multiple tasks.
Accepts TaskData objects or dict-like rows. Uses DataCleaner for parsing dates.
"""

import statistics
from datetime import datetime
from .task_data import TaskData, TaskDataError
from .data_cleaner import DataCleaner

class BehaviorAnalyzerError(Exception):
    """Base error for BehaviorAnalyzer."""
    def __init__(self, message):
        super().__init__(f"[BehaviorAnalyzerError] {message}")


class InvalidTaskListError(BehaviorAnalyzerError):
    """Raised when the input to BehaviorAnalyzer is not a list of TaskData-like objects."""
    def __init__(self):
        super().__init__("Tasks must be provided as a list of TaskData objects or dict-like rows.")


class DelayComputationError(BehaviorAnalyzerError):
    """Raised when delay cannot be computed."""
    def __init__(self, task, original=None):
        msg = f"Failed to compute delay for task: {task}"
        if original:
            msg += f" | original error: {original}"
        super().__init__(msg)


class ClassificationError(BehaviorAnalyzerError):
    """Raised when behavior classification cannot be determined."""
    def __init__(self):
        super().__init__("Unable to classify behavior. Ensure tasks and due dates are valid.")


class BehaviorAnalyzer:
    """
    Analyzes submission behavior patterns based on multiple tasks.

    tasks: list of TaskData instances or dict-like objects (can be DataFrame rows).
    If a per-task due_date exists (in the TaskData), it will be used; otherwise
    provide a global due_date when calling classify_behavior.
    """

    def __init__(self, tasks):
        if not isinstance(tasks, list):
            raise InvalidTaskListError()

        # Convert dict-like rows into TaskData where possible
        converted = []
        for t in tasks:
            if isinstance(t, TaskData):
                converted.append(t)
            elif isinstance(t, dict):
                try:
                    converted.append(TaskData(t))
                except Exception as e:
                    raise InvalidTaskListError() from e
            else:
                # try to accept pandas Series (which behaves like dict)
                try:
                    as_dict = dict(t)
                    converted.append(TaskData(as_dict))
                except Exception:
                    raise InvalidTaskListError()
        self.tasks = converted
        self._delay_history = []
        self._behavior_label = None

    # --------------------------------------------------------

    def classify_behavior(self, due_date=None):
        """
        Computes delays for all tasks and classifies user behavior.

        due_date: global due_date used if tasks don't have their own due_date.
                  Accepts string/datetime/pandas Timestamp.
        """

        # Reset previous
        self._delay_history = []

        # normalize global due_date if provided
        global_due = None
        if due_date is not None:
            try:
                global_due = DataCleaner.parse_timestamp(due_date)
            except Exception as e:
                raise BehaviorAnalyzerError(f"Invalid global due_date: {due_date}") from e

        for task in self.tasks:
            try:
                # if TaskData has its own due_date, TaskData.get_delay will use it when due_date None
                delay_td = task.get_delay(due_date=global_due) if global_due is not None else task.get_delay(None)
            except Exception as e:
                # try again: call get_delay with provided global due_date if available
                try:
                    if global_due is not None:
                        delay_td = task.get_delay(global_due)
                    else:
                        raise
                except Exception as inner:
                    raise DelayComputationError(task, inner) from inner

            delay_hours = delay_td.total_seconds() / 3600.0
            self._delay_history.append(delay_hours)

        if not self._delay_history:
            raise ClassificationError()

        avg_delay = statistics.mean(self._delay_history)

        # ------------------------------
        # ADVANCED CLASSIFICATION RULES
        # ------------------------------
        if avg_delay > 48:
            self._behavior_label = "Severe Procrastinator"
        elif 24 < avg_delay <= 48:
            self._behavior_label = "Procrastinator"
        elif -3 <= avg_delay <= 3:
            self._behavior_label = "Consistent Worker"
        elif avg_delay < -24:
            self._behavior_label = "Early Finisher"
        else:
            self._behavior_label = "Normal / Mixed"

        return self._behavior_label

    # --------------------------------------------------------

    def get_statistics(self):
        """
        Returns a dictionary summary of behavior statistics.
        Requires classify_behavior() to be run first.
        """

        if not self._delay_history:
            raise ClassificationError()

        avg_delay = statistics.mean(self._delay_history)
        std_dev = statistics.stdev(self._delay_history) if len(self._delay_history) > 1 else 0

        return {
            "tasks_analyzed": len(self.tasks),
            "avg_delay_hours": avg_delay,
            "std_dev_delay": std_dev,
            "behavior_label": self._behavior_label
        }

    # --------------------------------------------------------

    def __str__(self):
        return f"BehaviorAnalyzer(label={self._behavior_label})"



"""
behavior_analyzer.py
-------------------------
Analyzes student submission behavior across multiple tasks.
Includes structured error handling and advanced behavior classification.
"""

import statistics
from datetime import datetime
from .task_data import TaskData


class BehaviorAnalyzerError(Exception):
    """Base error for BehaviorAnalyzer."""
    def __init__(self, message):
        super().__init__(f"[BehaviorAnalyzerError] {message}")


class InvalidTaskListError(BehaviorAnalyzerError):
    """Raised when the input to BehaviorAnalyzer is not a list of TaskData objects."""
    def __init__(self):
        super().__init__("Tasks must be provided as a list of TaskData objects.")


class DelayComputationError(BehaviorAnalyzerError):
    """Raised when delay cannot be computed."""
    def __init__(self, task):
        super().__init__(f"Failed to compute delay for task: {task}")


class ClassificationError(BehaviorAnalyzerError):
    """Raised when behavior classification cannot be determined."""
    def __init__(self):
        super().__init__("Unable to classify behavior. Ensure tasks and due dates are valid.")


class BehaviorAnalyzer:
    """
    Analyzes submission behavior patterns based on multiple tasks.
    Computes delay history, behavior labels, and statistical summaries.
    """

    def __init__(self, tasks):
        if not isinstance(tasks, list) or not all(isinstance(t, TaskData) for t in tasks):
            raise InvalidTaskListError()

        self.tasks = tasks
        self._delay_history = []
        self._behavior_label = None

    # --------------------------------------------------------

    def classify_behavior(self, due_date):
        """
        Computes delays for all tasks and classifies user behavior.
        Raises errors if delay computation fails.
        """

        # Reset previous delay history
        self._delay_history = []

        for task in self.tasks:
            try:
                delay = task.get_delay(due_date)
            except Exception:
                raise DelayComputationError(task)

            delay_hours = delay.total_seconds() / 3600
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



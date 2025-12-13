from datetime import timedelta
import statistics
from .data_cleaner import DataCleaner

class DeadlinePredictor:
    """Predicts future submission timing based on past delay history (hours)."""

    def __init__(self):
        self._delay_history = []  # stored in hours (floats)

    def _to_hours(self, delay):
        """
        Accepts:
         - float/int (hours)
         - timedelta
        Returns hours as float.
        """
        from datetime import timedelta as _td
        if delay is None:
            raise ValueError("delay cannot be None")
        if isinstance(delay, (int, float)):
            return float(delay)
        if isinstance(delay, _td):
            return delay.total_seconds() / 3600.0
        # try parseable objects: strings -> parse as timestamp difference not supported here
        raise TypeError("Unsupported delay type: pass float hours or timedelta")

    def add_delay(self, delay):
        """Stores delay (in hours or timedelta) from previous tasks."""
        hours = self._to_hours(delay)
        self._delay_history.append(hours)

    def predict_next_delay(self):
        """Predicts next delay (hours) based on average."""
        if not self._delay_history:
            return None  # caller should handle
        avg_delay = statistics.mean(self._delay_history)
        return avg_delay  # hours

    def predict_submission_date(self, next_due_date):
        """
        Returns predicted submission datetime based on past delays.
        next_due_date: datetime or parseable string.
        """
        if next_due_date is None:
            raise ValueError("next_due_date is required")

        due_dt = DataCleaner.parse_timestamp(next_due_date)

        predicted_delay_hours = self.predict_next_delay()
        if predicted_delay_hours is None:
            return due_dt

        return due_dt + timedelta(hours=predicted_delay_hours)



from datetime import timedelta
import statistics

class DeadlinePredictor:
    """Predicts future submission timing based on past delay history."""

    def __init__(self):
        self._delay_history = []

    def add_delay(self, delay_hours):
        """Stores delay (in hours) from previous tasks."""
        self._delay_history.append(delay_hours)

    def predict_next_delay(self):
        """Predicts next delay based on average."""
        if not self._delay_history:
            return "Not enough data to predict."
        
        avg_delay = statistics.mean(self._delay_history)
        return avg_delay  # return in hours

    def predict_submission_date(self, next_due_date):
        """Returns predicted submission datetime based on past delays."""
        if not self._delay_history:
            return next_due_date
        
        avg_delay = statistics.mean(self._delay_history)
        return next_due_date + timedelta(hours=avg_delay)

import statistics

class HabitScore:
    """Computes an overall productivity and consistency score."""

    def __init__(self):
        self.delays = []  # in hours (floats)

    def add_delay(self, delay):
        if hasattr(delay, "total_seconds"):
            hours = delay.total_seconds() / 3600.0
        else:
            hours = float(delay)
        self.delays.append(hours)

    def compute_score(self):
        if not self.delays:
            return None

        avg_delay = statistics.mean(self.delays)
        variation = statistics.stdev(self.delays) if len(self.delays) > 1 else 0

        score = 100.0
        score -= min(50.0, avg_delay)            # penalize heavy delays
        score -= min(30.0, variation)            # penalize inconsistency

        if avg_delay < 0:
            score += 10.0                        # bonus for early submissions

        score = max(0.0, min(100.0, round(score)))
        return int(score)


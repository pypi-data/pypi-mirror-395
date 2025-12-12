import statistics

class HabitScore:
    """Computes an overall productivity and consistency score."""

    def __init__(self):
        self.delays = []

    def add_delay(self, delay_hours):
        self.delays.append(delay_hours)

    def compute_score(self):
        if not self.delays:
            return "Score unavailable"

        avg_delay = statistics.mean(self.delays)
        variation = statistics.stdev(self.delays) if len(self.delays) > 1 else 0

        score = 100

        # penalize heavy delays
        score -= min(50, avg_delay)

        # penalize inconsistency
        score -= min(30, variation)

        # bonus for early submissions
        if avg_delay < 0:
            score += 10

        return max(0, min(100, round(score)))

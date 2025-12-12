from collections import Counter

class PatternDetector:
    """Detects consistent patterns in submission habits."""

    def __init__(self):
        self.times_of_day = []

    def add_submission(self, submission_time):
        hour = submission_time.hour
        self.times_of_day.append(hour)

    def detect_pattern(self):
        if not self.times_of_day:
            return "No data"

        most_common_hour = Counter(self.times_of_day).most_common(1)[0][0]

        if 0 <= most_common_hour <= 5:
            return "Night Owl"
        elif 6 <= most_common_hour <= 11:
            return "Morning Worker"
        elif 12 <= most_common_hour <= 17:
            return "Afternoon Productive"
        else:
            return "Evening Finisher"

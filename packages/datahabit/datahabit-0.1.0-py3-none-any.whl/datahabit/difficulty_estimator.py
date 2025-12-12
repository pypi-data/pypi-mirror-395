class DifficultyEstimator:
    """Estimates which tasks the student finds difficult based on delay."""

    def __init__(self):
        self.task_delays = {}

    def record_task(self, task_name, delay_hours):
        self.task_delays[task_name] = delay_hours

    def get_difficult_tasks(self, top_n=3):
        if not self.task_delays:
            return "No data"

        sorted_tasks = sorted(self.task_delays.items(), key=lambda x: x[1], reverse=True)

        return sorted_tasks[:top_n]

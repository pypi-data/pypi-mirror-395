class ReportGenerator:
    """Generates a combined report dictionary for any student."""

    def __init__(self, student_id):
        self.student_id = student_id
        self.summary = {}

    def add_section(self, title, data):
        self.summary[title] = data

    def generate(self):
        return {
            "student_id": self.student_id,
            "report": self.summary
        }

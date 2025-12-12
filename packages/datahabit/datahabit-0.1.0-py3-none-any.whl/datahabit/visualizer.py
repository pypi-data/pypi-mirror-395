"""
visualizer.py
-------------------------
Visualizes submission behavior and productivity.
Includes structured error handling and multiple chart types.
"""

import matplotlib.pyplot as plt


class VisualizationError(Exception):
    """Base error for visualization-related issues."""
    def __init__(self, message):
        super().__init__(f"[VisualizerError] {message}")


class EmptyDataError(VisualizationError):
    """Raised when visualization is attempted with no data."""
    def __init__(self):
        super().__init__("Cannot visualize empty or invalid data.")


class ExportError(VisualizationError):
    """Raised when saving/exporting the visualization fails."""
    def __init__(self, filename):
        super().__init__(f"Failed to export visualization to: {filename}")


class Visualizer:
    """
    Visualizes numerical delay data or summary statistics.
    Supports timeline, scatter, and summary bar plots.
    """

    def __init__(self, data):
        # Clean data automatically (remove None, strings, etc.)
        self._data = self._clean_data(data)

        if not self._data:
            raise EmptyDataError()

    # --------------------------------------------------------

    def _clean_data(self, data):
        """Removes invalid entries and returns a list of floats."""
        cleaned = []
        for d in data:
            try:
                cleaned.append(float(d))
            except Exception:
                continue
        return cleaned

    # --------------------------------------------------------

    def plot_timeline(self, show=True):
        """Line plot showing progression of delays across tasks."""
        if not self._data:
            raise EmptyDataError()

        plt.figure(figsize=(8, 4))
        plt.plot(self._data, marker="o", linewidth=2)
        plt.title("Submission Delay Timeline")
        plt.xlabel("Task Index")
        plt.ylabel("Delay (hours)")
        plt.grid(True)

        if show:
            plt.show()

    # --------------------------------------------------------

    def plot_scatter(self, show=True):
        """Scatter plot of delays to visualize spread and consistency."""
        if not self._data:
            raise EmptyDataError()

        plt.figure(figsize=(7, 4))
        plt.scatter(range(len(self._data)), self._data)
        plt.title("Delay Scatter Plot")
        plt.xlabel("Task Index")
        plt.ylabel("Delay (hours)")
        plt.grid(True)

        if show:
            plt.show()

    # --------------------------------------------------------

    def plot_summary(self, show=True):
        """
        Summary bar chart:
            - average delay
            - max delay
            - min delay
        """
        if not self._data:
            raise EmptyDataError()

        avg_val = sum(self._data) / len(self._data)
        max_val = max(self._data)
        min_val = min(self._data)

        labels = ["Average Delay", "Max Delay", "Min Delay"]
        values = [avg_val, max_val, min_val]

        plt.figure(figsize=(7, 4))
        plt.bar(labels, values)
        plt.title("Behavior Summary Overview")
        plt.ylabel("Delay (hours)")

        if show:
            plt.show()

    # --------------------------------------------------------

    def export(self, filename="visual.png"):
        """
        Saves the last generated plot.
        Raises ExportError if saving fails.
        """
        try:
            plt.savefig(filename)
        except Exception:
            raise ExportError(filename)

    # --------------------------------------------------------

    def __str__(self):
        return f"Visualizer(data_points={len(self._data)})"


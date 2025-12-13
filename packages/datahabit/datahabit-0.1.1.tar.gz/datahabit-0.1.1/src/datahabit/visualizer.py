"""
visualizer.py
-------------------------
Visualizes submission behavior and productivity.
Accepts list-like numbers, pandas Series, or DataFrame columns. Cleans data to floats.
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
    Visualizer that cleans mixed-type inputs into float delay-hours.
    """

    def __init__(self, data):
        self._data = self._clean_data(data)
        if not self._data:
            raise EmptyDataError()

    def _clean_data(self, data):
        cleaned = []
        # try to handle pandas Series/DataFrame column
        try:
            import pandas as _pd
            if isinstance(data, (_pd.Series, _pd.Index, _pd.DataFrame)):
                # if DataFrame, take first numeric column
                if isinstance(data, _pd.DataFrame):
                    # find numeric columns
                    nums = data.select_dtypes(include=["number"])
                    if nums.shape[1] > 0:
                        data_iter = nums.iloc[:, 0].tolist()
                    else:
                        # fallback to flatten
                        data_iter = data.values.flatten().tolist()
                else:
                    data_iter = data.tolist()
            else:
                data_iter = data
        except Exception:
            data_iter = data

        for d in data_iter:
            if d is None:
                continue
            try:
                # if timedelta-like
                if hasattr(d, "total_seconds"):
                    cleaned.append(d.total_seconds() / 3600.0)
                else:
                    cleaned.append(float(d))
            except Exception:
                # ignore non-numeric entries
                continue
        return cleaned

    def plot_timeline(self, show=True):
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

    def plot_scatter(self, show=True):
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

    def plot_summary(self, show=True):
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

    def export(self, filename="visual.png"):
        try:
            plt.savefig(filename)
        except Exception:
            raise ExportError(filename)

    def __str__(self):
        return f"Visualizer(data_points={len(self._data)})"


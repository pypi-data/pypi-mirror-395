# DataHabit
DataHabit — Academic Behavior Analyzer (OOP Python library)

## Project Overview
**DataHabit** is a Python library designed to analyze academic behavior and productivity patterns based on students’ task timestamps. It reads submission records, detects time-based habits, and classifies users according to their working style—such as procrastinator, steady worker, or early finisher. By using data-driven insights, the library helps students and educators understand academic performance trends and improve time-management strategies.

## Objectives
The main goal of **DataHabit** is to provide a simple yet powerful tool for analyzing and visualizing study habits through timestamp data.
Specifically, it aims to:
1. Process and interpret task submission timestamps to identify behavioral patterns.
2. Classify students according to their productivity and consistency levels.
3. Generate summary reports and visualizations that reflect weekly academic activity.
4. Encourage self-reflection and better academic planning through data analytics.
5. Offer a reusable, open-source Python package that demonstrates Object-Oriented Programming (OOP) concepts applied to real-world data science.

# Features

**Timestamp Analyzer** — classifies submissions as early, on-time, or late.

**Behavior Classifier** — categorizes students (e.g., Procrastinator, Consistent Worker) based on submission patterns.

**Productivity Summary** — computes weekly activity metrics such as average submission gaps and submission counts.

**Visualizer** — generates simple graphs to show time-based behavior and activity trends.

**Data Cleaner / Utility** — fixes missing timestamps and resolves incorrect date formats.

**Deadline Predictor** — estimates the next expected submission date based on historical delays.

**Pattern Detector** — identifies the usual submission time of day (e.g., night-owl or early-bird patterns).

**Difficulty Estimator** — highlights tasks with the longest delays to indicate potential difficulty levels.

**Habit Score Generator** — computes a combined score based on delay patterns, consistency, and task difficulty.

**Report Generator** — produces clean, structured summaries that can be exported as JSON or printed for review.

# Installation
```
pip install datahabit
```

# Example usage
```python
from datahabit import (
    TaskData,
    DataCleaner,
    BehaviorAnalyzer
)

tasks = [
    TaskData("Quiz 1", "2024-10-01 23:59", "2024-10-01 21:30"),
    TaskData("Assignment", "2024-10-05 23:59", "2024-10-06 01:10")
]

clean = DataCleaner().clean(tasks)
analyze = BehaviorAnalyzer(clean).classify()

print(analyze)

```

# Module descriptions
| **Module**               | **Description**                                                                                                                                                               |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **behavior_analyzer.py** | Groups all behavior-related features, including behavior classification, pattern detection, difficulty estimation, habit scoring, and general performance analysis. Identifies trends such as procrastination, consistency, night-owl patterns, and problem tasks. |
| **data_cleaner.py**      | Cleans and preprocesses raw task data by fixing missing timestamps, correcting invalid date formats, and standardizing input before analysis.                                 |
| **task_data.py**         | Stores and manages task information (deadlines, submission times, task names) and provides structured data used by all analyzers and predictors.                              |
| **visualizer.py**        | Generates visual graphs (line charts, bar charts, timelines) to show submission patterns, productivity trends, and behavior insights.                                         |


# Contributors
| **Name**                     | **Role / Position**           | **Main Contribution**                    |
| ---------------------------- | ----------------------------- | ---------------------------------------- |
| **Dahe, Aira Grettel C.**    | Project Lead / GitHub Manager | Repository setup, documentation, testing |
| **Dellosa, Karylle L.**      | Concept Proposer / Main Coder | Core analysis functions                  |
| **Hayag, Carmel Mariane T.** | Documentation Writer          | README creation and narrative reports    |
| **Java, Armisty Genia L.**   | Visualization Developer       | Graphs, plots, and visual output designs |
| **Trillo, Rodney G.**        | Data Handler                  | Timestamp processing and data cleaning   |


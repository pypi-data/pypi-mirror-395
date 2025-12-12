# Data Table

The data table acts as the main navigation tool for users to switch between experiments. By selecting a row, users can focus all plots on the chosen experiment. It is tightly integrated with the rest of the Plotmon application, enabling experiment selection, highlighting, and metadata display.

---

## Features

### 1. Experiment Overview

- The data table lists all experiments (TUIDs) that have been started and tracked by Plotmon.
- For each experiment, the table displays:
  - **TUID**: The unique identifier for the experiment.
  - **Start Date**: When the experiment was started.
  - **End Date**: When the experiment was finished (if applicable).

### 2. Selection and Highlighting

- The table supports selection via checkboxes.
- Selecting a TUID in the table will highlight all graphs associated with that experiment across the dashboard.
- Only one experiment can be actively selected at a time; selecting a new TUID will update the highlight across all plots.
- When an experiment is finished, it is automatically set as selected in the table for all sessions.

### 3. Synchronization with Plots

- The data table is synchronized with the plot data sources:
  - When a new experiment is started, it is added to the table.
  - When an experiment ends, its end date is updated in the table.
  - The selection state in the table is reflected in the plot highlights and vice versa.

---

## Example

When you start a new experiment, it appears in the data table:

| Previous Experiments | Start Date         | End Date           |
|----------------------|--------------------|--------------------|
| tuid_123             | 2025-09-29 10:00   | 2025-09-29 10:30   |
| tuid_456             | 2025-09-29 11:00   |                    |

- Clicking the checkbox next to `tuid_456` will highlight all plots for that experiment.
- When `tuid_456` is finished, the end date is filled in, and it becomes the selected experiment.

---

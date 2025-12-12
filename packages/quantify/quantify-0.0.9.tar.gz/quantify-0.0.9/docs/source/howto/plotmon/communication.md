# Commands

Plotmon uses a command-based messaging system to control experiments, update data, and configure the dashboard. Commands are sent as structured messages (typically over ZeroMQ) and processed by the Plotmon to update the state of the application in real time.

---

## Command Types

The main commands in Plotmon are:

1. **GRAPH_CONFIG**: Set or update the graph layout and configuration.
2. **START**: Start a new experiment (register a new TUID).
3. **UPDATE**: Send new data for a plot in a specific experiment.
4. **STOP**: Mark an experiment as finished.

Each command is sent as a JSON message with a specific structure, including a timestamp and an `event_type` field.

---

## 1. GRAPH_CONFIG

**Purpose:**
Define or update the layout and configuration of all plots (graphs) in Plotmon.

**How it works:**
- The message contains a `graph_configs` field, which is a nested list describing the layout (see [Layouts documentation](layouts)).
- When received, Plotmon **resets** its dashboard to match the new configuration.

**Example:**

```json
{
  "event": {
    "data_source_name": "default_source",
    "graph_configs": [
      [
        {
          "plot_name": "voltage_vs_time",
          "plot_type": "1d",
          "x_key": "time_ns",
          "y_key": "voltage_mV"
        }
      ],
      [
        {
          "plot_name": "spectrogram",
          "plot_type": "heatmap",
          "x_key": "frequency_GHz",
          "y_key": "time_ns",
          "image_key": "amplitude",
          "dw_key": "df",
          "dh_key": "dt"
        }
      ]
    ],
    "title": "My Experiment Dashboard"
  },
  "timestamp": "2025-09-29_12-00-00_UTC",
  "event_type": "GRAPH_CONFIG"
}
```

---

## 2. START

**Purpose:**
Register the start of a new experiment, identified by a unique TUID.

**How it works:**
- The message includes the `data_source_name` and the new `tuid`.
- Plotmon adds the experiment to the data table and prepares data sources for it.

**Example:**

```json
{
  "event": {
    "data_source_name": "default_source",
    "tuid": "tuid_123"
  },
  "timestamp": "2025-09-29_12-01-00_UTC",
  "event_type": "START"
}
```

---

## 3. UPDATE

**Purpose:**
Send new data points for a specific plot in a specific experiment.

**How it works:**
- The message specifies the `plot_name`, `tuid`, and a list of data points.
- Each data point includes a `sequence_id` (for ordering) and any required fields for the plot (e.g., `x`, `y`, or `image`).
- Plotmon updates the relevant plot with the new data.

**Example: Update line plot**

```json
{
  "event": {
    "data_source_name": "default_source",
    "tuid": "tuid_123",
    "plot_name": "voltage_vs_time",
    "data": [
      {
        "sequence_id": 1,
        "tuid": "tuid_123",
        "time_ns": 0,
        "voltage_mV": 10.5
      },
      {
        "sequence_id": 2,
        "tuid": "tuid_123",
        "time_ns": 1,
        "voltage_mV": 10.7
      }
    ]
  },
  "timestamp": "2025-09-29_12-01-05_UTC",
  "event_type": "UPDATE"
}
```

---

**Example: Update heatmap**
```json
{
  "event": {
    "data_source_name": "my_source",
    "tuid": "tuid_001",
    "plot_name": "spectrogram",
    "data": [
      {
        "sequence_id": 1,
        "tuid": "tuid_001",
        "frequency_GHz": [1.0, 1.1, 1.2, 1.3],
        "time_ns": [0, 1, 2, 3],
        "amplitude": [
          [0.1, 0.2, 0.3, 0.4],
          [0.2, 0.3, 0.4, 0.5],
          [0.3, 0.4, 0.5, 0.6],
          [0.4, 0.5, 0.6, 0.7]
        ],
        "df": 0.1,
        "dt": 1
      }
    ]
  },
  "timestamp": "2025-09-29_12-01-10_UTC",
  "event_type": "UPDATE"
}
```

## 4. STOP

**Purpose:**
Mark an experiment as finished.

**How it works:**
- The message includes the `data_source_name` and the `tuid` to stop.
- Plotmon updates the data table, marks the experiment as finished, and highlights it.

**Example:**

```json
{
  "event": {
    "data_source_name": "default_source",
    "tuid": "tuid_123"
  },
  "timestamp": "2025-09-29_12-02-00_UTC",
  "event_type": "STOP"
}
```

---

## Command Processing Flow

1. **Message Reception:**
   Plotmon receives a message (typically via ZeroMQ).

2. **Event Type Detection:**
   The `event_type` field determines which handler is called.

3. **State Update:**
   - For `GRAPH_CONFIG`, the dashboard layout is reset.
   - For `START`, a new experiment is added.
   - For `UPDATE`, plot data is updated.
   - For `STOP`, the experiment is marked as finished.

4. **UI Synchronization:**
   All connected users see the updated state immediately.

---

## Summary Table

| Command       | Purpose                        | Required Fields                        | Example Section      |
|---------------|-------------------------------|----------------------------------------|----------------------|
| GRAPH_CONFIG  | Set/update plot layout         | `graph_configs`, `data_source_name`    | [GRAPH_CONFIG](#1-graph_config) |
| START         | Start new experiment           | `tuid`, `data_source_name`             | [START](#2-start)    |
| UPDATE        | Send new plot data             | `tuid`, `plot_name`, `data`            | [UPDATE](#3-update)  |
| STOP          | Mark experiment as finished    | `tuid`, `data_source_name`             | [STOP](#4-stop)      |

---

Visualization of the data flow can also bee seen in the next figure:

```{figure} /images/plotmon/plotmon-data-flow.svg
:name: plotmon-overview
:width: 850
```

---

For more details on plot configuration and layout, see [Customizing Graphs](graphs) and [Layouts](layouts).

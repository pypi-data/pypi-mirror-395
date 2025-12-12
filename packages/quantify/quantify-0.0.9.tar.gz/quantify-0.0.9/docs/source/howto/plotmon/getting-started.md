# Getting Started

Plotmon can be launched in two main ways, depending on your workflow and integration needs. This guide explains both approaches: launching Plotmon directly from Measurement Control, and running Plotmon as a standalone server.

---

## 1. Launching Plotmon via Measurement Control

If you are using the Quantify Measurement Control framework, you can start Plotmon directly by passing the `plotmon=True` argument when initializing your measurement control object.

**Example:**

```python
from qunatify.app.measurnment_control import MeasurementControl

mc = MeasurementControl(plotmon=True)
```

- This will automatically launch the Plotmon dashboard in a browser window.
- The dashboard will update in real time as your experiment progresses.

---

## 2. Running Plotmon as a Standalone Server

For more advanced use cases, such as remote monitoring or integration with multiple data providers, you can run Plotmon as a standalone server. In this mode, Plotmon listens for commands and data over ZeroMQ.

**How to launch:**

- Use the provided function to start the Plotmon server, specifying the port and data source name.
- The function returns a Bokeh application, which you can serve using the Bokeh server.

**Example:**

```python
from quantify.visualization.plotmon.plotmon_server import run_plotmon_server

# Start Plotmon on port 5006, listening for data on topic "my_source" from zero mq on adress "tcp://localhost:5555"
app = run_plotmon_server(server_port=5006, zero_mq_adress="tcp://localhost:5555", data_source_name="my_source")
```

- Plotmon will listen for ZeroMQ messages on the specified port and topic.
- You can now send commands (such as graph configuration, data updates, etc.) to Plotmon from any compatible data provider.

---

## Publishing Commands with ZeroMQ

To send commands to Plotmon, you can use ZeroMQ's PUB socket. Here is a minimal example using Python and `pyzmq`:

```python
import zmq

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.connect("tcp://localhost:5555")  # Use the address your Plotmon server is listening on

# Example: Send a JSON command as a string
msg = """{
// json content here
}"""
socket.send_string(msg)
```

- Replace the `msg` string with any of the example commands described below.
- Make sure the address matches the one used by your Plotmon server.

---

Below are example JSON commands you can send to Plotmon when running in standalone server mode:

### 1. Set Graph Layout

```json
{
  "event": {
    "data_source_name": "my_source",
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
    ]
  },
  "timestamp": "2025-09-29_12-00-00_UTC",
  "event_type": "GRAPH_CONFIG"
}
```

### 2. Start a New Experiment

```json
{
  "event": {
    "data_source_name": "my_source",
    "tuid": "tuid_001"
  },
  "timestamp": "2025-09-29_12-01-00_UTC",
  "event_type": "START"
}
```

### 3. Send Data to a Plot

```json
{
  "event": {
    "data_source_name": "my_source",
    "tuid": "tuid_001",
    "plot_name": "voltage_vs_time",
    "data": [
      {
        "sequence_id": 1,
        "tuid": "tuid_001",
        "time_ns": 0,
        "voltage_mV": 10.5
      },
      {
        "sequence_id": 2,
        "tuid": "tuid_001",
        "time_ns": 1,
        "voltage_mV": 10.7
      }
    ]
  },
  "timestamp": "2025-09-29_12-01-05_UTC",
  "event_type": "UPDATE"
}
```

### 4. Stop an Experiment

```json
{
  "event": {
    "data_source_name": "my_source",
    "tuid": "tuid_001"
  },
  "timestamp": "2025-09-29_12-02-00_UTC",
  "event_type": "STOP"
}
```

---

## Next Steps

- For details on configuring plots and layouts, see [Customizing Graphs](graphs) and [Layouts](layouts).
- To learn about the command protocol, see [Commands](communication.md).

---

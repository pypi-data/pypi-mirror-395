# Streaming & Extensions

Advanced features for integrating Instrument Monitor with external systems.

## Streaming API

The streaming API allows you to receive real-time parameter updates in your own code, enabling custom logging, alerts, data export, and integration with external systems.

### Basic Streaming

```python
from quantify.visualization.instrument_monitor import start_instrument_monitor_stream

def my_update_handler(update):
    """Called whenever parameters change."""
    print(f"Update mode: {update.mode}")
    print(f"Number of readings: {len(update.readings)}")
    print(f"Number of changes: {len(update.change_events)}")

    # Access individual readings
    for reading in update.readings:
        print(f"{reading.full_name} = {reading.value} {reading.unit}")

# Start streaming
stream = start_instrument_monitor_stream(
    handler=my_update_handler,
    poll_interval=1.0,  # Check for updates every second
)

# Your experiments run here...
# Handler is called automatically when parameters change

# Stop streaming
stream.stop()
```

### Understanding Updates

The `InstrumentMonitorUpdate` object contains:

- **`mode`**: Either `"snapshot"` (during warmup) or `"delta"` (after warmup)
- **`readings`**: List of `Reading` objects with current parameter values
- **`change_events`**: List of `ChangeEvent` objects describing what changed
- **`current_state()`**: Callable that returns full current state

```python
def detailed_handler(update):
    if update.mode == "snapshot":
        print("Warmup snapshot received")
    else:
        print("Real-time delta update")

    # Process changes
    for event in update.change_events:
        reading = event.reading
        changed_fields = event.changed_fields

        print(f"{reading.instrument}.{reading.parameter} changed:")
        print(f"  New value: {reading.value}")
        print(f"  Changed fields: {changed_fields}")
        print(f"  Timestamp: {event.ts}")

    # Get full state if needed
    if update.mode == "delta" and len(update.change_events) > 10:
        full_state = update.current_state()
        print(f"Total parameters: {len(full_state)}")

stream = start_instrument_monitor_stream(handler=detailed_handler)
```

## Use Cases

### 1. Custom Data Logging

Log parameter changes to a file or database:

```python
import json
from datetime import datetime

class ParameterLogger:
    def __init__(self, filename):
        self.file = open(filename, 'w')

    def handle_update(self, update):
        for event in update.change_events:
            log_entry = {
                'timestamp': event.ts.isoformat() if event.ts else None,
                'instrument': event.reading.instrument,
                'parameter': event.reading.parameter,
                'value': event.reading.value,
                'unit': event.reading.unit,
            }
            self.file.write(json.dumps(log_entry) + '\n')
            self.file.flush()

    def close(self):
        self.file.close()

# Usage
logger = ParameterLogger('parameters.jsonl')
stream = start_instrument_monitor_stream(
    handler=logger.handle_update,
    poll_interval=0.5,
)

# Run experiments...

stream.stop()
logger.close()
```

### 2. Real-Time Alerts

Send notifications when parameters exceed thresholds:

```python
def alert_handler(update):
    for event in update.change_events:
        reading = event.reading

        # Check temperature threshold
        if 'temperature' in reading.parameter.lower():
            if isinstance(reading.value, (int, float)) and reading.value > 50:
                print(f"⚠️  ALERT: {reading.full_name} = {reading.value} (threshold: 50)")
                # Send email, Slack message, etc.

        # Check voltage limits
        if 'voltage' in reading.parameter.lower():
            if isinstance(reading.value, (int, float)) and abs(reading.value) > 10:
                print(f"⚠️  ALERT: {reading.full_name} = {reading.value}V exceeds ±10V limit")

stream = start_instrument_monitor_stream(handler=alert_handler)
```

### 3. Database Export

Export to a time-series database:

```python
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxDBExporter:
    def __init__(self, url, token, org, bucket):
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.bucket = bucket

    def handle_update(self, update):
        points = []
        for event in update.change_events:
            reading = event.reading

            # Only export numeric values
            if isinstance(reading.value, (int, float)):
                point = Point(reading.instrument) \
                    .tag("parameter", reading.parameter) \
                    .field("value", reading.value)

                if reading.unit:
                    point = point.tag("unit", reading.unit)

                if event.ts:
                    point = point.time(event.ts)

                points.append(point)

        if points:
            self.write_api.write(bucket=self.bucket, record=points)

    def close(self):
        self.client.close()

# Usage
exporter = InfluxDBExporter(
    url="http://localhost:8086",
    token="your-token",
    org="your-org",
    bucket="instrument-data"
)

stream = start_instrument_monitor_stream(
    handler=exporter.handle_update,
    poll_interval=1.0,
)
```

### 4. Live Plotting

Create custom real-time plots:

```python
import matplotlib.pyplot as plt
from collections import deque
from datetime import datetime

class LivePlotter:
    def __init__(self, parameter_name, max_points=100):
        self.parameter_name = parameter_name
        self.times = deque(maxlen=max_points)
        self.values = deque(maxlen=max_points)

        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [])
        self.ax.set_xlabel('Time')
        self.ax.set_ylabel('Value')
        self.ax.set_title(f'Live: {parameter_name}')

    def handle_update(self, update):
        for event in update.change_events:
            if self.parameter_name in event.reading.full_name:
                if isinstance(event.reading.value, (int, float)):
                    self.times.append(datetime.now())
                    self.values.append(event.reading.value)

                    # Update plot
                    self.line.set_data(self.times, self.values)
                    self.ax.relim()
                    self.ax.autoscale_view()
                    self.fig.canvas.draw()
                    self.fig.canvas.flush_events()

# Usage
plotter = LivePlotter('qubit.frequency')
stream = start_instrument_monitor_stream(
    handler=plotter.handle_update,
    poll_interval=0.1,
)
```

## OrangeQS-Juice Extension

The OrangeQS-Juice extension provides enhanced visualization capabilities for quantum computing workflows.

### What It Provides

- Advanced quantum state visualization
- Multi-qubit correlation displays
- Custom quantum-specific widgets
- Integration with quantum compilation pipelines

### Enabling the Extension

The extension is automatically detected if the `orangeqs-juice` package is installed:

```bash
pip install orangeqs-juice
```

Once installed, additional features become available in the Instrument Monitor UI automatically.

### Extension Features

When the extension is active:

1. **Quantum State Viewer**: Visualize qubit states in Bloch sphere representation
2. **Correlation Matrix**: See multi-qubit correlations in real-time
3. **Pulse Visualization**: Monitor pulse sequences and timing
4. **Custom Metrics**: Quantum-specific performance metrics

### Using Extension Hooks

The extension system allows custom visualizations:

```python
from quantify.visualization.instrument_monitor import launch_instrument_monitor

# Extensions are loaded automatically if available
monitor = launch_instrument_monitor()

# Extension features appear in the UI automatically
```

## Creating Custom Extensions

You can create your own extensions to add custom functionality.

### Extension Structure

```python
from quantify.visualization.instrument_monitor.models import Reading
from typing import Callable

class MyCustomExtension:
    """Custom extension for instrument monitor."""

    def __init__(self):
        self.name = "my_extension"
        self.version = "1.0.0"

    def on_reading(self, reading: Reading) -> None:
        """Called for each parameter reading."""
        if 'custom' in reading.parameter:
            # Do something with custom parameters
            print(f"Custom parameter: {reading.full_name} = {reading.value}")

    def get_ui_components(self):
        """Return custom Bokeh UI components."""
        from bokeh.models import Div
        return [Div(text="<h3>Custom Extension Active</h3>")]

# Register extension (implementation depends on extension API)
```

### Extension Best Practices

1. **Minimal Overhead**: Extensions run in the main monitoring loop
2. **Error Handling**: Always catch exceptions to avoid breaking the monitor
3. **Performance**: Keep processing lightweight
4. **Documentation**: Document what your extension does and requires

## Advanced Streaming Patterns

### Filtered Streaming

Only receive updates for specific instruments:

```python
def filtered_handler(update):
    for event in update.change_events:
        # Only process qubit-related parameters
        if 'qubit' in event.reading.instrument.lower():
            print(f"{event.reading.full_name} = {event.reading.value}")

stream = start_instrument_monitor_stream(handler=filtered_handler)
```

### Batched Processing

Accumulate updates and process in batches:

```python
from collections import defaultdict

class BatchProcessor:
    def __init__(self, batch_size=100):
        self.batch_size = batch_size
        self.buffer = defaultdict(list)

    def handle_update(self, update):
        for event in update.change_events:
            key = event.reading.full_name
            self.buffer[key].append(event.reading.value)

            if len(self.buffer[key]) >= self.batch_size:
                self.process_batch(key, self.buffer[key])
                self.buffer[key] = []

    def process_batch(self, parameter, values):
        avg = sum(values) / len(values)
        print(f"{parameter}: batch avg = {avg:.3f}")

processor = BatchProcessor(batch_size=50)
stream = start_instrument_monitor_stream(handler=processor.handle_update)
```

### Multi-Consumer Pattern

Send updates to multiple handlers:

```python
class MultiConsumer:
    def __init__(self):
        self.handlers = []

    def add_handler(self, handler):
        self.handlers.append(handler)

    def handle_update(self, update):
        for handler in self.handlers:
            try:
                handler(update)
            except Exception as e:
                print(f"Handler error: {e}")

# Setup
multi = MultiConsumer()
multi.add_handler(logger.handle_update)
multi.add_handler(alert_handler)
multi.add_handler(plotter.handle_update)

stream = start_instrument_monitor_stream(handler=multi.handle_update)
```

## Performance Considerations

### Streaming Overhead

- Streaming adds minimal overhead (~1-2% CPU)
- Handler execution time affects overall performance
- Keep handlers fast and non-blocking

### Best Practices

1. **Async Processing**: Use queues for heavy processing
2. **Sampling**: Don't process every single update if not needed
3. **Filtering**: Filter early to reduce processing
4. **Error Handling**: Always catch exceptions in handlers

```python
import queue
import threading

class AsyncProcessor:
    def __init__(self):
        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def handle_update(self, update):
        # Quick: just enqueue
        self.queue.put(update)

    def _worker(self):
        # Slow processing in background thread
        while True:
            update = self.queue.get()
            # Do expensive processing here
            self.process(update)
            self.queue.task_done()

    def process(self, update):
        # Heavy processing goes here
        pass

processor = AsyncProcessor()
stream = start_instrument_monitor_stream(handler=processor.handle_update)
```

## Next Steps

- [See integration examples](integration.md) with other tools
- [Understand the architecture](technical-architecture.md)
- [Return to introduction](intro.md)

# Integration Examples

Simple patterns for integrating Instrument Monitor with QCoDeS and Jupyter notebooks.

## With QCoDeS Station

Best practices for integrating with QCoDeS Station.

### Recommended Pattern

```python
from qcodes import Station
from quantify.visualization.instrument_monitor import launch_instrument_monitor

# Create station
station = Station()

# Add all instruments to station
# station.add_component(qubit)
# station.add_component(readout)
# station.add_component(flux_control)

# Set as default (recommended for auto-discovery)
Station.default = station

# Launch monitor - automatically discovers all station instruments
monitor = launch_instrument_monitor()

# Work with instruments
# qubit.frequency(5.2e9)  # Change visible in monitor immediately

# Cleanup
monitor.stop()
```

### Multiple Stations

Handle multiple stations:

```python
from qcodes import Station
from quantify.visualization.instrument_monitor import launch_instrument_monitor

# Station 1: Control instruments
control_station = Station(name="control")
# control_station.add_component(...)

# Station 2: Readout instruments
readout_station = Station(name="readout")
# readout_station.add_component(...)

# Set one as default for auto-discovery
Station.default = control_station

# Monitor sees default station instruments
monitor = launch_instrument_monitor()

# To see both stations, add readout instruments to default:
for name, component in readout_station.components.items():
    Station.default.add_component(component)

# Now both stations are monitored
```

## Jupyter Notebook Integration

Use Instrument Monitor effectively in Jupyter notebooks.

### Basic Notebook Usage

```python
# Cell 1: Setup
from quantify.visualization.instrument_monitor import launch_instrument_monitor
from qcodes import Station

station = Station()
# Add instruments...

# Cell 2: Launch monitor
monitor = launch_instrument_monitor()
print(f"Monitor at: {monitor.url}")

# Cell 3: Run experiments
# Your experiment code here
# Parameter changes appear in monitor

# Cell 4: Cleanup (optional - monitor stops when kernel restarts)
monitor.stop()
```

### IPython Display Integration

Display monitor status in notebook:

```python
from IPython.display import display, HTML

monitor = launch_instrument_monitor()

# Display clickable link
display(HTML(f'<a href="{monitor.url}" target="_blank">Open Instrument Monitor</a>'))

# Display status
print(f"Status: {'Running' if monitor.running else 'Stopped'}")
print(f"Host: {monitor.host}")
print(f"Port: {monitor.port}")
```

### Notebook Best Practices

```python
# Use context manager for automatic cleanup
from quantify.visualization.instrument_monitor import launch_instrument_monitor

with launch_instrument_monitor() as monitor:
    # Run experiments
    # Monitor stops automatically when cell finishes
    pass

# Or keep monitor running across cells
monitor = launch_instrument_monitor()

# ... many cells later ...

# Explicitly stop when done
monitor.stop()
```


## Next Steps

- [Learn about configuration](configuration.md)
- [Explore streaming features](streaming.md)
- [Understand the architecture](technical-architecture.md)

# Getting Started

Get up and running with Instrument Monitor in less than 5 minutes.

## Installation

Instrument Monitor is included with Quantify. If you have Quantify installed, you're ready to go:

```bash
pip install quantify
```

## Basic Usage

### Minimal Example

The simplest way to start monitoring:

```python
from quantify.visualization.instrument_monitor import launch_instrument_monitor

# Launch the monitor
handle = launch_instrument_monitor()
# Browser opens automatically at http://localhost:5006 (or next available port)

# Your instruments are now being monitored!
# Any QCoDeS instruments in your session will appear automatically

# When done:
handle.stop()
```

### With QCoDeS Station

If you're using QCoDeS Station (recommended):

```python
from qcodes import Station
from quantify.visualization.instrument_monitor import launch_instrument_monitor

# Create and configure your station
station = Station()

# Add your instruments
# station.add_component(my_instrument)
# station.add_component(another_instrument)

# Launch the monitor
monitor = launch_instrument_monitor(
    port=5007,           # Specific port (optional)
    open_browser=True,   # Auto-open browser (default: True)
    log_level="INFO"     # Logging verbosity
)

print(f"Monitor running at: {monitor.url}")

# Run your experiments...
# All parameter changes are tracked automatically

# Stop when done
monitor.stop()
```

### As Context Manager

For automatic cleanup:

```python
from quantify.visualization.instrument_monitor import launch_instrument_monitor

with launch_instrument_monitor() as monitor:
    print(f"Monitoring at {monitor.url}")

    # Do your experiments here
    # Monitor stops automatically when exiting the context
```

## Using the Dashboard

Once launched, the Instrument Monitor dashboard has two main sections:

### 1. Current State Table (Left Panel)

- **Search/Filter:** Type in the filter box to find specific instruments or parameters
- **Sorting:** Click column headers to sort by instrument, parameter, value, or unit
- **Live Updates:** Values update in real-time as parameters change
- **Selection:** Click a row to jump to that parameter in the tree view

### 2. Hierarchy Explorer (Right Panel)

- **Tree Structure:** See your instruments organized hierarchically
- **Expand/Collapse:** Click ▶/▼ to expand or collapse instrument sections
- **Submodules:** Navigate through nested instrument components
- **Parameter Details:** View parameter values in their instrument context

### 3. Resource Monitor (Bottom Right)

- **CPU Usage:** Current CPU utilization
- **Memory:** RAM usage
- **Threads:** Active thread count
- **Updates:** Refreshes every 2 seconds

## Basic Workflow

1. **Launch the monitor** before or after creating your instruments
2. **Navigate to the URL** (opens automatically by default)
3. **Verify instruments appear** in both table and tree views
4. **Use the filter** to find specific parameters
5. **Run your experiments** - watch parameters update live
6. **Stop the monitor** when done

## Example: Complete Session

```python
from qcodes import Station
from qcodes.instrument_drivers.mock_instruments import DummyInstrument
from quantify.visualization.instrument_monitor import launch_instrument_monitor

# Setup
station = Station()
dummy = DummyInstrument("dummy", gates=["ch1", "ch2"])
station.add_component(dummy)

# Launch monitor
monitor = launch_instrument_monitor()

# Interact with instruments - changes appear in monitor
dummy.ch1(1.5)  # This update appears immediately
dummy.ch2(2.3)  # This too!

# Do more work...
for i in range(10):
    dummy.ch1(i * 0.1)
    # Watch the value change in real-time in the monitor

# Cleanup
monitor.stop()
dummy.close()
```

## Troubleshooting Quick Tips

**Monitor doesn't start:**

- Check if port is already in use
- Try specifying a different port: `launch_instrument_monitor(port=5008)`

**No instruments appear:**

- Ensure instruments are added to `Station.default`
- Or create instruments before launching the monitor
- Check that instruments are QCoDeS `Instrument` instances

**UI not updating:**

- Refresh the browser page
- Check browser console for WebSocket errors
- Verify parameters are being set (not just read)

For more troubleshooting, see the [Technical Architecture](technical-architecture.md) page.

## Next Steps

- [Configure the monitor](configuration.md) for your specific needs
- [Learn about streaming](streaming.md) to external systems
- [See integration examples](integration.md) with QCoDeS Station

# What is Instrument Monitor?

**Instrument Monitor** is a lightweight, live monitoring dashboard for QCoDeS instruments and parameters. It provides real-time visibility into your quantum computing hardware, making it easy to track parameter changes, debug configurations, and monitor system health during experiments.

## Key Features

- **Automatic Discovery:** Finds all QCoDeS instruments in your setup automatically
- **Live Updates:** See parameter changes in real-time as they happen
- **Low Latency:** Efficient streaming via QCoDeS global callbacks after initial warmup
- **Dual View Modes:**
  - **Current State Table:** Filterable, sortable table of all parameters
  - **Hierarchy Explorer:** Tree view showing instrument structure
- **Resource Monitoring:** Built-in CPU, memory, and thread usage tracking
- **Non-Blocking:** Runs in background thread, doesn't interfere with experiments
- **Responsive UI:** Smart gating prevents UI updates during user interactions

## Use Cases

### Real-Time Parameter Monitoring

Monitor instrument parameters during experiments without writing custom logging code. Perfect for:

- Tracking qubit frequencies during calibration
- Monitoring amplifier settings during gate optimization
- Observing temperature drift in cryogenic systems

### Debugging Instrument Configurations

Quickly verify that instruments are configured correctly:

- Check all parameters at a glance
- Identify misconfigured settings
- Validate instrument initialization

### System Health Checks

Keep an eye on system resources and instrument status:

- Monitor CPU and memory usage
- Track number of active parameters
- Identify performance bottlenecks

### Multi-Instrument Coordination

When working with complex setups involving multiple instruments:

- See all instruments in one dashboard
- Navigate hierarchical instrument structures
- Filter to specific instruments or parameters

## When to Use Instrument Monitor vs Plotmon

| Feature | Instrument Monitor | Plotmon |
|---------|-------------------|---------|
| **Purpose** | Live parameter monitoring | Experiment data visualization |
| **Data Source** | QCoDeS instruments | Measurement Control |
| **View Type** | Table + Tree | Plots + Graphs |
| **Best For** | Debugging, monitoring | Analysis, results |
| **Updates** | Every parameter change | Experiment data points |

## Quick Example

```python
from quantify.visualization.instrument_monitor import launch_instrument_monitor

# Launch the monitor
handle = launch_instrument_monitor()
# Browser opens automatically showing all your instruments

# Do your experiments...

# Stop when done
handle.stop()
```

## Next Steps

- [Get started in 5 minutes](getting-started.md)
- [Learn about configuration options](configuration.md)
- [Explore advanced features](streaming.md)

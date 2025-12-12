# Configuration

Detailed guide to configuring Instrument Monitor for your specific needs.

## Launch Parameters

### Basic Parameters

```python
from quantify.visualization.instrument_monitor import launch_instrument_monitor

handle = launch_instrument_monitor(
    host="localhost",      # Server host
    port=None,            # Port (None = auto-select)
    open_browser=True,    # Auto-open browser
    log_level="INFO",     # Logging verbosity
)
```

#### `host` (str, default: "localhost")

The hostname or IP address where the server will listen.

**Examples:**

```python
# Local only (default)
launch_instrument_monitor(host="localhost")

# Allow remote access (use with caution!)
launch_instrument_monitor(host="0.0.0.0")

# Specific network interface
launch_instrument_monitor(host="192.168.1.100")
```

#### `port` (int | None, default: None)

The port number for the Bokeh server. If `None`, automatically finds an available port.

**Examples:**

```python
# Auto-select port (recommended)
handle = launch_instrument_monitor(port=None)
print(f"Running on port: {handle.port}")

# Specific port
launch_instrument_monitor(port=5007)

# Multiple monitors on different ports
monitor1 = launch_instrument_monitor(port=5007)
monitor2 = launch_instrument_monitor(port=5008)
```

#### `open_browser` (bool, default: True)

Whether to automatically open the dashboard in your default browser.

**Examples:**

```python
# Auto-open (default)
launch_instrument_monitor(open_browser=True)

# Don't open browser (useful for remote servers)
handle = launch_instrument_monitor(open_browser=False)
print(f"Visit: {handle.url}")
```

#### `log_level` (str, default: "INFO")

Logging verbosity. Options: "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"

**Examples:**

```python
# Verbose logging for debugging
launch_instrument_monitor(log_level="DEBUG")

# Quiet mode
launch_instrument_monitor(log_level="WARNING")
```

## Ingestion Configuration

Advanced parameters for tuning data collection performance.

### Performance Parameters

```python
handle = launch_instrument_monitor(
    warmup_total_passes=5,      # Number of snapshot warmup passes
    warmup_interval_s=1.0,      # Seconds between warmup passes
    event_batch_limit=10000,    # Max events processed per batch
)
```

#### `warmup_total_passes` (int, default: 5)

Number of full instrument snapshot passes during startup warmup.

**When to adjust:**

- **Increase (7-10):** Large number of instruments, want thorough initialization
- **Decrease (2-3):** Few instruments, want faster startup

**Examples:**

```python
# Fast startup for simple setups
launch_instrument_monitor(warmup_total_passes=2)

# Thorough warmup for complex systems
launch_instrument_monitor(warmup_total_passes=10)
```

#### `warmup_interval_s` (float, default: 1.0)

Time in seconds between warmup snapshot passes.

**When to adjust:**

- **Increase (2-5s):** Slow instruments, avoid overwhelming hardware
- **Decrease (0.5s):** Fast instruments, want quicker initialization

**Examples:**

```python
# Quick warmup
launch_instrument_monitor(warmup_interval_s=0.5)

# Gentle warmup for slow instruments
launch_instrument_monitor(warmup_interval_s=3.0)
```

#### `event_batch_limit` (int, default: 10000)

Maximum number of parameter change events processed per batch.

**When to adjust:**

- **Increase (50000+):** High-throughput systems with many rapid parameter changes
- **Decrease (1000-5000):** Low-memory systems, want to limit memory usage

**Examples:**

```python
# High-throughput configuration
launch_instrument_monitor(event_batch_limit=50000)

# Memory-constrained system
launch_instrument_monitor(event_batch_limit=2000)
```

## Configuration Profiles

Pre-configured settings for common scenarios.

### High-Throughput Profile

For systems with many instruments and frequent parameter updates:

```python
monitor = launch_instrument_monitor(
    warmup_total_passes=3,       # Fast startup
    warmup_interval_s=0.5,       # Quick warmup
    event_batch_limit=50000,     # Handle many events
    log_level="WARNING",         # Reduce logging overhead
)
```

**Best for:**

- Large quantum computing systems
- Rapid calibration routines
- High-frequency parameter sweeps

### Low-Latency Profile

For systems where immediate parameter visibility is critical:

```python
monitor = launch_instrument_monitor(
    warmup_total_passes=10,      # Thorough initialization
    warmup_interval_s=2.0,       # Careful warmup
    event_batch_limit=1000,      # Small batches for quick processing
    log_level="INFO",            # Normal logging
)
```

**Best for:**

- Interactive debugging sessions
- Manual instrument tuning
- Real-time monitoring during experiments

### Memory-Constrained Profile

For systems with limited RAM:

```python
monitor = launch_instrument_monitor(
    warmup_total_passes=2,       # Minimal warmup
    warmup_interval_s=1.0,       # Standard interval
    event_batch_limit=2000,      # Limit memory usage
    log_level="WARNING",         # Reduce logging memory
)
```

**Best for:**

- Embedded systems
- Shared computing resources
- Long-running monitoring sessions

### Debug Profile

For troubleshooting and development:

```python
monitor = launch_instrument_monitor(
    warmup_total_passes=5,       # Standard warmup
    warmup_interval_s=1.0,       # Standard interval
    event_batch_limit=10000,     # Standard batch size
    log_level="DEBUG",           # Verbose logging
)
```

**Best for:**

- Investigating issues
- Understanding system behavior
- Contributing to development

## Advanced Configuration

### Multiple Monitors

Run multiple monitors simultaneously:

```python
# Monitor different instrument groups on different ports
monitor_qubits = launch_instrument_monitor(port=5007)
monitor_readout = launch_instrument_monitor(port=5008)

# Each monitor sees all instruments, but you can filter in the UI
```

### Remote Access

Configure for remote monitoring (use appropriate security measures):

```python
# WARNING: This exposes the monitor to your network
# Only use on trusted networks or with proper firewall rules
monitor = launch_instrument_monitor(
    host="0.0.0.0",              # Listen on all interfaces
    port=5007,                   # Fixed port for firewall rules
    open_browser=False,          # Don't open browser on server
)

print(f"Remote access at: http://your-server-ip:{monitor.port}")
```

### Programmatic Control

Access monitor state programmatically:

```python
monitor = launch_instrument_monitor()

# Check if running
if monitor.running:
    print(f"Monitor active at {monitor.url}")

# Get connection details
print(f"Host: {monitor.host}")
print(f"Port: {monitor.port}")

# Wait for monitor to finish (blocks until stopped)
# monitor.wait()

# Stop with timeout
monitor.stop(timeout=5.0)
```

## Environment Variables

Configure via environment variables (useful for CI/CD):

```bash
# Set default log level
export QUANTIFY_INSTRUMENT_MONITOR_LOG_LEVEL=DEBUG

# Set default port
export QUANTIFY_INSTRUMENT_MONITOR_PORT=5007
```

```python
# These will use environment variable defaults
monitor = launch_instrument_monitor()
```

## Performance Tuning Guidelines

### Optimize for Your System

1. **Start with defaults** - They work well for most cases
2. **Monitor resource usage** - Check the Resource Panel in the UI
3. **Adjust based on behavior:**
   - High CPU → Increase `event_batch_limit`
   - High memory → Decrease `event_batch_limit`
   - Slow startup → Decrease `warmup_total_passes`
   - Missing initial values → Increase `warmup_total_passes`

### Benchmarking

Test different configurations:

```python
import time

# Configuration A
start = time.time()
monitor = launch_instrument_monitor(
    warmup_total_passes=3,
    event_batch_limit=50000,
)
print(f"Startup time: {time.time() - start:.2f}s")

# Run experiments and observe performance
# ...

monitor.stop()
```

## Next Steps

- [Learn about streaming](streaming.md) to external systems
- [See integration examples](integration.md) with other tools
- [Understand the architecture](technical-architecture.md)

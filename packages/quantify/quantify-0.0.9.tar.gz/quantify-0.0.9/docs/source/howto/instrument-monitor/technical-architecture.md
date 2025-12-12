# Technical Architecture

Deep dive into Instrument Monitor's design, implementation, and internals.

## Architecture Overview

Instrument Monitor uses a clean separation of concerns with three main layers:

1. **Ingestion Layer**: Discovery, polling, and callback management
2. **State Layer**: Thread-safe storage and change detection
3. **UI Layer**: Bokeh-based web interface

```
┌─────────────────────────────────────────────────────────────┐
│                         Browser                              │
│                  (Bokeh Document / UI)                       │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ WebSocket
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Bokeh Server                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │            InstrumentMonitorApp                      │   │
│  │  ┌────────────────┐  ┌──────────────────────────┐   │   │
│  │  │ InstrumentUI   │  │  Periodic Update Loop    │   │   │
│  │  │ - Table        │  │  (333ms)                 │   │   │
│  │  │ - Tree         │  │                          │   │   │
│  │  │ - Resources    │  │                          │   │   │
│  │  └────────────────┘  └──────────────────────────┘   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ get_current_state()
                            │ get_recent_changes()
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  InstrumentDiscovery                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │                   StateStore                         │   │
│  │  - Current readings (dict)                           │   │
│  │  - Change events (ring buffer)                       │   │
│  │  - Thread-safe access (RLock)                        │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ update_readings()
                            │ direct_update_readings()
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    SnapshotPoller                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Warmup Phase (5 passes)                             │   │
│  │  - Discover instruments                              │   │
│  │  - Take snapshots                                    │   │
│  │  - Parse to Readings                                 │   │
│  │  - Update StateStore                                 │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Streaming Phase                                     │   │
│  │  - Drain callback queue                              │   │
│  │  - Batch process events                              │   │
│  │  - Direct update StateStore                          │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ enqueue Reading
                            │
┌─────────────────────────────────────────────────────────────┐
│          GlobalParameterCallbackManager                      │
│  - Installs single callback on ParameterBase                │
│  - Captures all parameter.set() calls                       │
│  - Creates Reading objects                                  │
│  - Pushes to poller queue                                   │
└─────────────────────────────────────────────────────────────┘
                            ▲
                            │ parameter.set()
                            │
┌─────────────────────────────────────────────────────────────┐
│                   QCoDeS Instruments                         │
│  - Station.default                                          │
│  - Instrument.instances()                                   │
│  - Parameters with callbacks                                │
└─────────────────────────────────────────────────────────────┘
```

## Module Breakdown

### `server.py` - Server Lifecycle

**Purpose**: Manages Bokeh server process and thread lifecycle.

**Key Components**:

- `launch_instrument_monitor()`: Main entry point, returns `MonitorHandle`
- `MonitorHandle`: Control interface (stop, wait, status)
- `_create_server()`: Server configuration and initialization

**Design Decisions**:

- Background thread for non-blocking operation
- Queue-based handoff for thread-safe server startup
- Automatic port selection to avoid conflicts

```python
# Simplified implementation
def launch_instrument_monitor(**kwargs):
    queue = Queue()

    def server_thread():
        server = create_bokeh_server(**kwargs)
        server.start()
        queue.put(("ok", server))
        server.io_loop.start()  # Blocks until stopped

    thread = Thread(target=server_thread, daemon=True)
    thread.start()

    status, server = queue.get(timeout=10)
    return MonitorHandle(server=server, thread=thread)
```

### `app.py` - Application Core

**Purpose**: Wires together UI and ingestion, manages document lifecycle.

**Key Components**:

- `InstrumentMonitorApp`: Main application class
- `create_document()`: Per-session document setup
- `_periodic_update()`: 333ms update loop
- `_apply_updates()`: Gated UI updates

**Design Decisions**:

- 333ms update interval balances responsiveness and performance
- UI updates gated during user interactions (typing, scrolling)
- Dependency injection for testability

```python
# Simplified update loop
def _periodic_update(self):
    current_readings = self.discovery.get_current_state()
    recent_changes = self.discovery.get_recent_changes(limit=50)

    # Schedule on next tick to avoid blocking
    self.doc.add_next_tick_callback(
        lambda: self._apply_updates(current_readings, recent_changes)
    )
```

### `discovery.py` - Instrument Discovery

**Purpose**: Find QCoDeS instruments and delegate state management.

**Discovery Strategy** (fallback chain):

1. `Station.default.components` (preferred)
2. `Instrument.__subclasses__()` + `.instances()`
3. Garbage collection scan (last resort)

**Design Decisions**:

- Three-tier fallback ensures instruments are found
- Root instrument extraction avoids duplicates
- All state delegated to `StateStore`

```python
# Simplified discovery
def discover_instruments(self):
    discovered = {}

    # Try Station first
    if Station.default:
        for comp in Station.default.components.values():
            if isinstance(comp, Instrument):
                discovered[comp.name] = comp

    # Fallback to subclass scan
    if not discovered:
        for subcls in Instrument.__subclasses__():
            for inst in subcls.instances():
                discovered[inst.name] = inst

    return list(discovered.values())
```

### `poller.py` - Snapshot Polling

**Purpose**: Orchestrate warmup snapshots and callback event ingestion.

**Two-Phase Operation**:

**Phase 1: Warmup** (first ~5 seconds)

- Periodic snapshot passes
- Full instrument discovery each pass
- Parallel snapshot collection (ThreadPoolExecutor)
- Change detection via `StateStore.update_readings()`

**Phase 2: Streaming** (after warmup)

- Drain callback event queue
- Batch processing (configurable limit)
- Direct updates via `StateStore.direct_update_readings()`
- No more snapshots (callback-only)

**Design Decisions**:

- Warmup ensures initial state capture
- Callback-only mode minimizes overhead
- Batch draining prevents queue overflow
- Deque with maxlen prevents unbounded growth

```python
# Simplified polling tick
def _tick_once(self):
    # Always drain callback queue
    drained = []
    while self.event_queue and len(drained) < self.batch_limit:
        drained.append(self.event_queue.popleft())

    if drained:
        if self.warmup_complete:
            self.discovery.direct_update_readings(drained)
        else:
            self.discovery.update_readings(drained)

    # Warmup snapshots
    if not self.warmup_complete:
        if should_run_snapshot_pass():
            instruments = self.discovery.discover_instruments()
            self.run_snapshot_pass(instruments)
            self.warmup_passes += 1

            if self.warmup_passes >= self.warmup_total_passes:
                self.warmup_complete = True
```

### `callbacks.py` - Global Callback Manager

**Purpose**: Install single global callback on QCoDeS `ParameterBase`.

**How It Works**:

1. Sets `ParameterBase.global_on_set_callback` to custom function
2. Callback fires on every `parameter.set(value)`
3. Extracts instrument name, parameter path, value, unit
4. Creates `Reading` object
5. Pushes to poller's event queue

**Design Decisions**:

- Single global callback (not per-parameter) for efficiency
- Extracts root instrument to avoid submodule duplication
- Graceful error handling to never break parameter sets
- Thread-safe queue for cross-thread communication

```python
# Simplified callback
def _make_global_callback(self):
    def callback(param, value):
        try:
            root_instr = param.root_instrument
            instrument_name = root_instr.name
            parameter_path = param.name
            unit = param.unit

            reading = Reading(
                full_name=f"{instrument_name}.{parameter_path}",
                instrument=instrument_name,
                parameter=parameter_path,
                value=value,
                unit=unit,
                ts=datetime.now(timezone.utc),
            )

            self.on_change(reading)  # Push to queue
        except Exception:
            pass  # Never break parameter sets

    return callback
```

### `state_store.py` - State Management

**Purpose**: Thread-safe storage of readings and change events.

**Data Structures**:

- `_last_readings`: `dict[str, Reading]` - Current state
- `_change_buffer`: `deque[ChangeEvent]` - Recent changes (bounded)
- `_lock`: `threading.RLock` - Thread safety

**Operations**:

- `update_readings()`: With change detection
- `direct_update_readings()`: Without change detection (post-warmup)
- `get_current_state()`: Snapshot of all readings
- `get_recent_changes()`: Last N change events

**Design Decisions**:

- Immutable Pydantic models for thread safety
- Change detection only during warmup
- Bounded ring buffer prevents memory growth
- RLock allows reentrant access

```python
# Simplified state update
def update_readings(self, new_readings):
    change_events = []

    with self._lock:
        for reading in new_readings:
            old_reading = self._last_readings.get(reading.full_name)

            # Detect changes
            if old_reading is None or old_reading.value != reading.value:
                change_event = ChangeEvent(
                    reading=reading,
                    changed_fields={"value"},
                    ts=datetime.now(timezone.utc),
                )
                change_events.append(change_event)
                self._change_buffer.append(change_event)

            self._last_readings[reading.full_name] = reading

    return change_events
```

### `snapshot_parser.py` - Snapshot Parsing

**Purpose**: Convert QCoDeS snapshot dicts to `Reading` objects.

**Parsing Strategy**:

- Recursive descent through snapshot structure
- Handle submodules and nested parameters
- Extract value, unit, timestamp
- Construct full parameter paths

**Design Decisions**:

- Pure function (no side effects)
- Handles malformed snapshots gracefully
- Preserves instrument hierarchy in parameter names

### `ui.py` - UI Composition

**Purpose**: Compose Bokeh UI components and manage client-side interactions.

**Components**:

- `CurrentStateTable`: Filterable, sortable parameter table
- `SnapshotTree`: Hierarchical instrument tree
- `ResourcePanel`: System resource monitoring

**Design Decisions**:

- Client-side listeners for focus/scroll detection
- Gated updates prevent UI churn during interaction
- Hash-based ColumnDataSource updates minimize DOM changes

### `models.py` - Data Models

**Purpose**: Immutable, thread-safe data structures.

**Models**:

- `Reading`: Single parameter reading
- `ChangeEvent`: Parameter change with metadata
- `TreeNode`: UI tree view node

**Design Decisions**:

- Pydantic models for validation and immutability
- `frozen=True` for thread safety
- Timezone-aware timestamps (UTC)

## Performance Characteristics

### Memory Usage

**Typical**: 50-100 MB
**Factors**:

- Number of instruments: ~1 KB per instrument
- Number of parameters: ~100 bytes per parameter
- Change buffer size: `max_events * ~200 bytes`
- UI overhead: ~20-30 MB (Bokeh)

**Memory Bounds**:

- Change buffer: Fixed size (default 1000 events)
- Event queue: Fixed size (default 10000 events)
- Current state: Grows with parameter count (typically <1000 parameters)

### CPU Usage

**Typical**: 1-5% on modern CPU
**Breakdown**:

- Polling loop: <1%
- Callback processing: 1-2%
- UI updates: 1-2%
- Bokeh server: 1%

**Spikes**:

- Warmup: 10-20% (brief, during snapshot collection)
- High update rate: Scales with parameter change frequency

### Latency

**Parameter Change → UI Update**:

- Warmup phase: 1-2 seconds (snapshot interval)
- Streaming phase: 333-666 ms (UI update interval)

**Factors**:

- UI update interval: 333 ms
- Callback queue drain: <10 ms
- Network latency: 10-50 ms (local), 50-200 ms (remote)

## Scalability

### Tested Limits

- **Instruments**: 50+ instruments
- **Parameters**: 1000+ parameters
- **Update Rate**: 100+ updates/second
- **Sessions**: 10+ concurrent browser sessions

### Bottlenecks

1. **Snapshot Collection**: Parallel execution helps, but limited by instrument response time
2. **UI Updates**: Bokeh DOM updates are the main bottleneck at scale
3. **WebSocket**: Network bandwidth for remote access

### Optimization Strategies

**For Many Instruments**:

- Reduce `warmup_total_passes`
- Increase `warmup_interval_s`
- Use filtering in UI

**For High Update Rate**:

- Increase `event_batch_limit`
- Reduce UI update frequency (modify app.py)
- Use streaming API for custom processing

**For Memory Constraints**:

- Reduce `max_events` in StateStore
- Decrease `event_batch_limit`
- Limit number of monitored instruments

## Extension Points

### Custom Discovery

Inject custom discovery logic:

```python
class CustomDiscovery(InstrumentDiscovery):
    def discover_instruments(self):
        # Custom discovery logic
        return my_instruments

app = InstrumentMonitorApp(discovery=CustomDiscovery())
```

### Custom Poller

Inject custom polling logic:

```python
class CustomPoller(SnapshotPoller):
    def _tick_once(self):
        # Custom polling logic
        pass

app = InstrumentMonitorApp(poller=CustomPoller(discovery))
```

### Custom UI Components

Add custom Bokeh components:

```python
class CustomUI(InstrumentMonitorUI):
    def create_layout(self):
        layout = super().create_layout()
        # Add custom components
        return layout
```

## Testing Strategy

### Unit Tests

- Pure functions (snapshot_parser, models)
- State management (state_store)
- Discovery logic (discovery)

### Integration Tests

- Fake instruments
- Mock QCoDeS Station
- Injected dependencies

### End-to-End Tests

- Playwright for UI testing
- Real Bokeh server
- Simulated parameter changes

## Design Principles

1. **Separation of Concerns**: Ingestion, state, UI are independent
2. **Thread Safety**: Immutable models, locks, queues
3. **Performance**: Batch processing, gated updates, bounded buffers
4. **Testability**: Dependency injection, pure functions
5. **Robustness**: Graceful degradation, error handling

## Future Enhancements

Potential improvements:

- **Persistence**: Save/load parameter history
- **Alerts**: Configurable threshold alerts
- **Export**: CSV/JSON export functionality
- **Filtering**: Server-side filtering for large datasets
- **Compression**: WebSocket compression for remote access
- **Authentication**: User authentication for multi-user setups

## References

- [Bokeh Documentation](https://docs.bokeh.org/)
- [QCoDeS Documentation](https://qcodes.github.io/Qcodes/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## Next Steps

- [Return to introduction](intro.md)
- [See configuration options](configuration.md)
- [Explore streaming features](streaming.md)

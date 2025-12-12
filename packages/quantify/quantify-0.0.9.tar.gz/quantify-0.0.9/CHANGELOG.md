# Changelog

## Unreleased

## Release v0.0.9 (2025-12-04)

### 🐛 Bug Fixes and Closed Issues

- Compilation: Removed erroneous instance check from graph compilation ([!110](https://gitlab.com/quantify-os/quantify/-/merge_requests/110)).

### 🔧 Other

- CI: Pin Python 3.14 to 3.14.0 to avoid CPython dataclasses regression in 3.14.1 ([python/cpython#142214](https://github.com/python/cpython/issues/142214), [!112](https://gitlab.com/quantify-os/quantify/-/merge_requests/112)).

## Release v0.0.8 (2025-11-28)

### 🔧 Other

- **Dependency Updates:** Updated package versions (pydantic, and others) to ensure compatibility with proprietary packages and resolve pip dependency resolution issues.
- **CI/CD:** Automated multi-version documentation build with version switcher dropdown. The docs site now hosts `dev` (latest from main) plus the last 3 stable release tags, with the newest marked as "(stable)". Simplified GitLab Pages redirects to always point to dev docs.

## Release v0.0.7 (2025-11-20)

🐛 Bug Fixes and Closed Issues

Plot Monitor (Plotmon): Fixed an issue where the live update mechanism could get stuck, ensuring plots refresh correctly during acquisition.

📚 Documentation

Updated all tutorials to use the new Plot Monitor (Plotmon) and removed references to the deprecated plotmon.

🔧 Other

Removed the dependency on quantify-scheduler by eliminating inline Q1ASM functionality.

CI/CD: Simplified the GitLab CI/CD configuration and added clear onboarding documentation for new developers.

## Release v1.0.0b8 (2025-11-13)

### 🐛 Bug Fixes and Closed Issues

- Instrument Monitor: prevent collapse in embedded hosts via Bokeh sizing.

### 📚 Documentation

- Add Migration Guide.
- Add Reference guide to index and expand Reference section.
- Fix version number in the navbar and use a local `switcher.json`.
- Add acquisition documentation from quantify-scheduler.
- General markdown cleanups.

### 🔧 Other

- CI/CD: refactor and harden pipelines; add Python 3.13 and 3.14; fix pyright and pre-commit; update ruff ignore rules; pin quantify-scheduler commit enabling Python 3.14.
- Docs CI: split MR docs preview from Pages deploy to avoid duplicate pipelines; enable Mermaid; build docs on Merge Requests.

## Release v1.0.0b7 (2025-10-31)

### 🚀 Features

- Added an option to display **previous experiments** via a dropdown menu, with support for saving and loading experiment state.
  ([!87](https://gitlab.com/quantify-os/quantify/-/merge_requests/87) by [@Kristian Gogora](https://gitlab.com/kikigogo9-OQS))

- **Pulse-Level Rabi Schedule** — Added support for multiple pulse amplitudes, making the pulse-level Rabi schedule consistent with the regular Rabi schedule.
  ([!91](https://gitlab.com/quantify-os/quantify/-/merge_requests/91) by [@Timo van Abswoude](https://gitlab.com/Timo_van_Abswoude))

---

### 🐛 Bug Fixes and Closed Issues

- **Plot Monitor**
  - Fixed lag and blinking graphs caused by constant re-rendering.
  - Fixed missing start date on page load for short experiments (less than one second).
  - Fixed first experiment not being plotted when switching configurations.
  - Fixed duplication in Bokeh server `io_loop` startup.
  - Fixed incorrect heatmap display.
  ([!87](https://gitlab.com/quantify-os/quantify/-/merge_requests/87) by [@Kristian Gogora](https://gitlab.com/kikigogo9-OQS))

---

### 🔧 Other

- **Align Units Notation with SCQT** — Updated physical-units notation to be compatible with `superconducting-qubit-tools` (SCQT), improving interoperability between Quantify and SCQT and avoiding unit-interpretation mismatches.
  ([!88](https://gitlab.com/quantify-os/quantify/-/merge_requests/88) by [@Olga Lebiga](https://gitlab.com/olga.lebiga) and [@Mahmut Cetin](https://gitlab.com/cetin-oqs))

## Release v1.0.0b4 (2025-10-23)

### 🚀 Features

- **Instrument Monitor - OrangeQS-Juice Extension Support:** Extended instrument monitor with support hooks for the OrangeQS-Juice extension package, enabling advanced visualization capabilities ([!81](https://gitlab.com/quantify-os/quantify/-/merge_requests/81)).
- **Measurement Client Documentation:** Added comprehensive documentation for measurement client, including usage examples and API reference ([!77](https://gitlab.com/quantify-os/quantify/-/merge_requests/77)).

### 🐛 Bug Fixes and Closed Issues

- **Packaging Fix:** Added `py.typed` marker file following PEP 561 for proper type checking support in downstream packages ([!78](https://gitlab.com/quantify-os/quantify/-/merge_requests/78), closes [#104](https://gitlab.com/quantify-os/quantify/-/issues/104)).
- **Missing Init Files:** Added missing `__init__.py` files in recently added plotmon modules to ensure proper package structure ([!82](https://gitlab.com/quantify-os/quantify/-/merge_requests/82), closes [#105](https://gitlab.com/quantify-os/quantify/-/issues/105)).
- **Dependency Pin:** Pinned `h5netcdf!=1.7.0` to avoid compatibility issues with data serialization ([!79](https://gitlab.com/quantify-os/quantify/-/merge_requests/79)).
- **Plotmon Migration:** Made migration to new plotmon seamless for measurement control users with backward-compatible API.

### 📚 Documentation

- **Instrument Monitor User Documentation:** Added comprehensive user-facing documentation covering introduction, quick start, configuration, streaming API, integration patterns, and technical architecture.
- **Scheduler Concepts:** Copied basic concepts documentation from quantify-scheduler to improve user onboarding ([!83](https://gitlab.com/quantify-os/quantify/-/merge_requests/83), closes [#103](https://gitlab.com/quantify-os/quantify/-/issues/103)).

### 🔧 Other

- **Instrument Monitor Refactoring:** Migrated `InstrumentMonitorStreamHandle` to a Pydantic model with improved type safety and validation ([!81](https://gitlab.com/quantify-os/quantify/-/merge_requests/81)).
- **Testing Infrastructure:** Added comprehensive test scaffolding for all instrument monitor modules ([!81](https://gitlab.com/quantify-os/quantify/-/merge_requests/81)).
- **CI Improvements:** Added `libatomic1` to CI image for improved build support across platforms ([!80](https://gitlab.com/quantify-os/quantify/-/merge_requests/80)).

## Release v1.0.0b3 (2025-10-21)

### 🚀 Features

#### Instrument Monitor - Live QCoDeS Instruments/Parameters Tracking

Introduced **Instrument Monitor**, a lightweight Bokeh-based dashboard for live monitoring of QCoDeS instruments and parameters:

- **Automatic Discovery:** Discovers QCoDeS instruments from Station.default, instrument subclasses, or garbage collection fallback
- **Low-Latency Streaming:** Short snapshot warmup (5 passes) followed by efficient streaming via QCoDeS global parameter callbacks
- **Responsive UI:** Gated updates during user interactions (typing/scrolling) to maintain smooth performance
- **Dual View Modes:**
  - **Current State Table:** Filterable, sortable table of all parameter values with real-time updates
  - **Hierarchy Explorer:** Tree view showing instrument structure and nested submodules
- **Resource Monitoring:** Built-in panel tracking CPU, memory, and thread usage
- **Thread-Safe Architecture:** Immutable Pydantic models (`Reading`, `ChangeEvent`) for safe concurrent access
- **Extensibility Hooks:** Support for external streaming consumers via `InstrumentMonitorStreamHandle`
- **Non-Blocking API:** Background server with `MonitorHandle` for start/stop/wait control

**Technical Implementation:**

- Separation of concerns: discovery, state management, polling, and UI are fully decoupled
- `StateStore` with change detection and bounded ring buffer for recent events
- Batch-drained event queue to prevent unbounded memory growth
- Hash-based Bokeh ColumnDataSource updates to minimize DOM churn
- Configurable ingestion parameters (warmup passes, intervals, batch limits)

#### Plotmon - Real-Time Experiment Visualization

Introduced **Plotmon**, a comprehensive live data visualization tool for quantum experiments. Plotmon enables real-time monitoring of experimental results directly in the browser with the following capabilities:

- **Live Monitoring:** Instant visualization of experiment progress and results as data is collected
- **Multi-Experiment Management:** Quick switching between ongoing and completed experiments via an interactive data table
- **Flexible Plot Types:** Support for 1D line plots, 2D heatmaps, and multi-line overlays
- **Customizable Layouts:** Row-based graph arrangement with shared axis ranges for easy comparison
- **ZeroMQ Integration:** Standalone server mode for remote monitoring and integration with multiple data providers
- **Measurement Control Integration:** Seamless launch via `MeasurementControl(plotmon=True)` for instant setup
- **Modern UI:** Bokeh-based dashboard with responsive design, styled cards, and smooth animations
- **Session Management:** Per-session data isolation ensuring clean multi-user support
- **Comprehensive Documentation:** Full user guides covering setup, configuration, and communication protocols

**Technical Implementation:**

- Server wrapper with Bokeh handler for web-based rendering
- Event-driven architecture with command processing (START, STOP, UPDATE_DATA, GRAPH_CONFIG)
- In-memory caching with configurable data retention
- Pydantic models for type-safe message validation
- Graph builder with figure factory pattern for extensible plot types

#### Measurement Control Enhancements

- **Update Functionality:** Added real-time update capabilities for measurement client and measurement control
- **Plot Configuration:** Automatic plot configuration creation from measurement control for seamless Plotmon integration
- **Client Documentation:** Comprehensive documentation for measurement client API and usage patterns

### 🐛 Bug Fixes and Closed Issues

- **Type Checking:** Fixed Pyright and linter issues across the codebase for improved type safety
- **QCoDeS Compatibility:** Fixed QCoDeS version compatibility issues in CI pipeline
- **Lazy Loading:** Added lazy loading for visualization modules to reduce import overhead and avoid circular dependencies

### 🔧 Other

- **Documentation:** Added comprehensive documentation for measurement client and Plotmon, including getting started guides, API references, and technical architecture details
- **Scheduler Integration:** Synced and merged documentation from `quantify-scheduler` for consistent user experience
- **Testing:** Added unit tests for Plotmon components and instrument monitor modules
- **UI Polish:** Enhanced Plotmon styling with modern card-based layouts, shadows, and responsive design

## Release v0.0.6 (2025-09-22)

### 🐛 Bug Fixes and Closed Issues

- Fixed `ImportError` when installing in editable mode by replacing `miniver` with `setuptools_scm`, adding a fallback version detection in `__init__.py`, and removing obsolete `setup.py` ([!61](https://gitlab.com/quantify-os/quantify/-/merge_requests/61) by [@Mahmut Cetin](https://gitlab.com/cetin-oqs)).
- Updated type hint in `set_setuptitle_from_dataset` to accept `SubFigure` ([!59](https://gitlab.com/quantify-os/quantify/-/merge_requests/59) by [@Timo van Abswoude](https://gitlab.com/Timo_van_Abswoude)).

### 🚀 Features

- Added optional `load_metadata` flag to `load_settings_onto_instrument`, allowing metadata to be reloaded for database-backed parameters while maintaining backward compatibility ([!60](https://gitlab.com/quantify-os/quantify/-/merge_requests/60) by [@Timo van Abswoude](https://gitlab.com/Timo_van_Abswoude)).
- Refined type hint for `BaseAnalysis.run` to return `Self` instead of `BaseAnalysis` ([!63](https://gitlab.com/quantify-os/quantify/-/merge_requests/63) by [@Timo van Abswoude](https://gitlab.com/Timo_van_Abswoude)).

### 🔧 Other

- Improved documentation UI/UX: removed duplicate search bar, aligned logo with navbar, unified OQS-doc icon link, added theme switching, renamed "Examples and how-to guides" to "Examples", and migrated from `RELEASE_NOTES` to `CHANGELOG.md` ([!58](https://gitlab.com/quantify-os/quantify/-/merge_requests/58) by [@Kristian Gogora](https://gitlab.com/kikigogo9-OQS)).

## Release v0.0.5 (2025-09-02)

### 🐛 Bug Fixes and Closed Issues

### 🚀 Features

- Added Pytest CI jobs for Windows and macOS across multiple Python versions ([!55](https://gitlab.com/quantify-os/quantify/-/merge_requests/55) by [@Mahmut Cetin](https://gitlab.com/cetin-oqs)).
- Introduced use of a static template for generating compilation files: moved generation logic to `device_element`, enabled child-class template overrides and extensions, improved `transmon_element` to reuse base logic from quantify ([!53](https://gitlab.com/quantify-os/quantify/-/merge_requests/53) by [@Dianto Bosman](https://gitlab.com/DiantoBosman)).
- Integrated Quantify-Core changes for ongoing compatibility: ported Merge Requests 566 and 568 into the `quantify` repository ([!56](https://gitlab.com/quantify-os/quantify/-/merge_requests/56), [!57](https://gitlab.com/quantify-os/quantify/-/merge_requests/57) by [@Mahmut Cetin](https://gitlab.com/cetin-oqs)).
- Expanded CI testing to support Python 3.10, 3.11, and 3.12; added parallel testing, Qt GUI support with ‘screen use’, pip and apt caching strategies ([!51](https://gitlab.com/quantify-os/quantify/-/merge_requests/51) by [@Mahmut Cetin](https://gitlab.com/cetin-oqs)).

---

### 🔧 Other

- Synced repository with upstream core changes to maintain consistency (#core-sync-july2025) ([!48](https://gitlab.com/quantify-os/quantify/-/merge_requests/48) by [@Olga Lebiga](https://gitlab.com/OlgaLebiga)).
- Resolved type-checking issues flagged by Pyright in the SCQT codebase ([!54](https://gitlab.com/quantify-os/quantify/-/merge_requests/54) by [@Mahmut Cetin](https://gitlab.com/cetin-oqs)).

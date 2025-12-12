# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Quantify visualization module.

Provides the comprehensive entry point for all visualization tools.
"""

# Core visualization modules - commonly imported across the codebase
# Utility modules
from typing import Any

__all__ = [
    "mpl_plotting",  # pyright: ignore
    "PlotMonitor_pyqt",  # pyright: ignore
    "SI_utilities",  # pyright: ignore
    "color_utilities",  # pyright: ignore
    "plot_interpolation",  # pyright: ignore
    "launch_instrument_monitor",  # pyright: ignore
    "MonitorHandle",  # pyright: ignore
    "PlotmonApp",  # pyright: ignore
    "process_messages",  # pyright: ignore
    "Message",  # pyright: ignore
    "InMemoryCache",  # pyright: ignore
]


_import_map = {
    "mpl_plotting": "quantify.visualization.mpl_plotting",
    "plot_interpolation": "quantify.visualization.plot_interpolation",
    "SI_utilities": "quantify.visualization.SI_utilities",
    "color_utilities": "quantify.visualization.color_utilities",
    "MonitorHandle": "quantify.visualization.instrument_monitor",
    "launch_instrument_monitor": "quantify.visualization.instrument_monitor",
    "PlotMonitor_pyqt": "quantify.visualization.pyqt_plotmon",
    "PlotmonApp": "quantify.visualization.plotmon.plotmon_app",
    "process_messages": "quantify.visualization.plotmon.plotmon_server",
    "Message": "quantify.visualization.plotmon.utils.communication",
    "InMemoryCache": "quantify.visualization.plotmon.caching.in_memory_cache",
}


def __getattr__(name: str) -> Any:
    if name in _import_map:
        mod_path = _import_map[name]
        try:
            mod = __import__(mod_path, fromlist=[name])
            return getattr(mod, name)
        except (ImportError, AttributeError) as e:
            raise AttributeError(f"Could not import '{name}' from '{mod_path}': {e}")
    else:
        # Try importing a submodule or attribute with the same name
        try:
            mod_path = f"{__name__}.{name}"
            mod = __import__(mod_path, fromlist=[name])
            return mod
        except ImportError as e:
            raise AttributeError(f"module '{__name__}' has no attribute '{name}': {e}")


def __dir__() -> list[str]:
    return __all__

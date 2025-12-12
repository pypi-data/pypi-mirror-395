# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Bokeh server management for startup."""

from __future__ import annotations

import contextlib
import queue
import socket
import threading

# Self is not available in typing for Python 3.10; import from typing_extensions
from typing import Any, Literal, TypeAlias
import webbrowser

from bokeh.server.server import Server
from typing_extensions import Self

from quantify.visualization.instrument_monitor.app import create_instrument_monitor_app
from quantify.visualization.instrument_monitor.config import (
    DEFAULT_INGESTION_CONFIG,
    IngestionConfig,
)
from quantify.visualization.instrument_monitor.logging_setup import (
    get_logger,
    setup_logging,
)

logger = get_logger(__name__)


# Message tuple types for inter-thread handoff
MsgOk: TypeAlias = tuple[Literal["ok"], Server, int, str]
MsgErr: TypeAlias = tuple[Literal["error"], Exception]
Msg: TypeAlias = MsgOk | MsgErr


def find_free_port() -> int:
    """Return an OS-assigned ephemeral free port."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("localhost", 0))
            return int(sock.getsockname()[1])
    except Exception as e:
        raise RuntimeError("Failed to acquire an ephemeral port") from e


def _create_server(
    *, host: str, port: int | None, kwargs: dict[str, Any]
) -> tuple[Server, int, str]:
    """Create a configured Bokeh ``Server`` and return it with port and URL.

    This consolidates the common logic used by instrument monitor server creation.
    """
    actual_port = port or find_free_port()
    logger.debug("Using port %s", actual_port)

    # Create configuration - only override defaults if specified
    config_overrides = {
        k: v
        for k, v in {
            "warmup_total_passes": kwargs.get("warmup_total_passes"),
            "warmup_interval_s": kwargs.get("warmup_interval_s"),
            "event_batch_limit": kwargs.get("event_batch_limit"),
        }.items()
        if v is not None
    }

    config = (
        IngestionConfig(**config_overrides)
        if config_overrides
        else DEFAULT_INGESTION_CONFIG
    )

    app = create_instrument_monitor_app(config=config)

    server_config = {
        "port": actual_port,
        "address": host,
        "num_procs": 1,
        "allow_websocket_origin": [f"{host}:{actual_port}"],
        **{
            k: v for k, v in kwargs.items() if k not in ["port", "address", "num_procs"]
        },
    }

    logger.debug("Starting server", extra=server_config)

    server = Server(
        {"/": app},
        **server_config,
        show=False,
        session_token_expiration=3600000,
    )

    url = f"http://{host}:{actual_port}/"
    return server, actual_port, url


class MonitorHandle:
    """Handle for a background instrument monitor server.

    Provides a minimal API to stop the server and can be used as a context manager.
    """

    def __init__(
        self,
        *,
        host: str,
        port: int,
        url: str,
        _server: Server,
        _thread: threading.Thread,
    ) -> None:
        """Initialize the monitor handle."""
        self.host = host
        self.port = port
        self.url = url
        self._server = _server
        self._thread = _thread
        self._stopped = False

    def stop(self, timeout: float | None = 5.0) -> None:
        """Stop the background server and join the thread.

        Parameters
        ----------
        timeout:
            Maximum time in seconds to wait for the server thread to finish. If
            ``None``, wait indefinitely.

        """
        if self._stopped:
            return
        self._stopped = True

        def _shutdown() -> None:
            try:
                self._server.stop()
            finally:
                with contextlib.suppress(Exception):
                    self._server.io_loop.stop()

        # Schedule a clean shutdown on the server's IOLoop (thread-safe)
        try:
            self._server.io_loop.add_callback(_shutdown)
        except Exception:
            # Fallback: try direct shutdown (best effort)
            with contextlib.suppress(Exception):
                _shutdown()

        if timeout is not None:
            self._thread.join(timeout)
        else:
            self._thread.join()

    @property
    def running(self) -> bool:
        """Whether the background server thread is still running."""
        return self._thread.is_alive() and not self._stopped

    def wait(self, timeout: float | None = None) -> None:
        """Block until the server thread terminates.

        Parameters
        ----------
        timeout:
            Maximum time in seconds to wait. If ``None``, wait indefinitely.

        """
        if timeout is not None:
            self._thread.join(timeout)
        else:
            self._thread.join()

    def __enter__(self) -> Self:
        """Enter the context manager."""
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        """Exit the context manager."""
        self.stop()


def launch_instrument_monitor(
    *,
    port: int | None = None,
    host: str = "localhost",
    open_browser: bool = True,
    log_level: str = "INFO",
    **kwargs: Any,
) -> MonitorHandle:
    """Launch the instrument monitor in a background thread and return a handle.

    This is the recommended, non-blocking API for interactive use (scripts,
    notebooks, and REPL). To block the current thread until the server stops,
    call :meth:`MonitorHandle.wait` on the returned handle.
    """
    setup_logging(log_level)
    logger.debug("Launching instrument monitor (background)")

    # Use a small handoff queue to pass the Server instance back to the caller
    q: queue.Queue[Msg] = queue.Queue(maxsize=1)

    def _server_thread() -> None:
        try:
            server, actual_port, url = _create_server(
                host=host, port=port, kwargs=kwargs
            )
            server.start()

            if open_browser:
                with contextlib.suppress(Exception):
                    webbrowser.open_new_tab(url)

            # Signal readiness to the main thread before entering the IOLoop
            q.put(("ok", server, actual_port, url))

            # Always run the Tornado IOLoop in the background thread
            logger.debug("Starting Tornado IOLoop (background)")
            try:
                server.io_loop.start()
            finally:
                logger.debug("IOLoop exited (background)")
        except Exception as e:
            logger.exception("Background server failed to start: %s", e)
            with contextlib.suppress(Exception):
                q.put(("error", e))

    thread = threading.Thread(
        target=_server_thread,
        name="InstrumentMonitorServer",
        daemon=True,
    )
    thread.start()

    # Wait for server to report readiness or error
    try:
        msg = q.get(timeout=10.0)
    except queue.Empty as e:
        raise RuntimeError("Instrument monitor did not start within 10 seconds") from e

    if msg[0] == "error":
        err = msg[1]
        # Ensure thread terminates soon-ish
        with contextlib.suppress(Exception):
            thread.join(timeout=1.0)
        raise RuntimeError("Instrument monitor failed to start") from err

    # Success tuple shape: ("ok", server, actual_port, url)
    _, server, actual_port, url = msg  # type: ignore[misc]
    handle = MonitorHandle(
        host=host, port=actual_port, url=url, _server=server, _thread=thread
    )
    logger.info("🚀 Instrument Monitor running at %s", url)
    return handle

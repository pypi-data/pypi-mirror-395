# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""UI tool service for handling UI updates during measurements."""

from abc import ABC, abstractmethod
import contextlib
import queue
import threading

from bokeh.application import Application
from bokeh.server.server import Server

from quantify.visualization.plotmon.caching.in_memory_cache import InMemoryCache
from quantify.visualization.plotmon.plotmon_app import PlotmonApp
from quantify.visualization.plotmon.plotmon_server import process_message
from quantify.visualization.plotmon.utils.communication import Message


class UITool(ABC):
    """Abstract base class for UI tools."""

    _name: str | None = None

    def init(self, name: str) -> None:
        """Initialize the data source name."""
        self._name = name

    @abstractmethod
    def callback(self, msg: Message) -> None:
        """Callback function to publish messages to Plotmon."""


class QuantifyUI(UITool):
    """Quantify UI tool for handling Plotmon updates during measurements."""

    def __init__(self) -> None:
        """Initializes the QuantifyUI tool with an in-memory cache."""
        self._plotmon_cache = InMemoryCache()
        self._plotmon_app = None

    def callback(self, msg: Message) -> None:
        """
        Callback function to process incoming messages and update the Plotmon app.

        Args:
            msg: Message object containing the event to process.

        """
        if not self._plotmon_app:
            self._plotmon_app = self._create_plotmon_app()
        process_message(msg, self._plotmon_app, self._plotmon_cache)

    def init(self, name: str) -> None:
        """
        Initialize the UI tool with a name and create the Plotmon application.

        Args:
            name: str Name of the data source.

        """
        super().init(name)
        self._plotmon_app = self._create_plotmon_app()

    def _create_plotmon_app(self) -> PlotmonApp:
        if not self._name:
            raise ValueError(
                "UITool not initialized with a name. Use tool.init(name) first."
            )
        plotmon_app = PlotmonApp(
            cache=self._plotmon_cache,
            data_source_name=self._name,
        )

        q: queue.Queue = queue.Queue(maxsize=1)

        # start server in a separate thread
        def _start() -> None:
            try:
                application = Application(plotmon_app)
                # Port 0 will pick a free port

                server = Server(
                    {"/": application},
                    port=0,
                    address="localhost",
                    num_procs=1,
                    show=True,
                    allow_websocket_origin=["*"],
                )
                server.start()
                # Signal readiness to the main thread before entering the IOLoop
                q.put(("ok", server.address, server.port))
                try:
                    server.io_loop.start()
                finally:
                    print("IOLoop exited (background)")
            except Exception as e:
                print(f"Background server failed to start: {e}")
                with contextlib.suppress(Exception):
                    q.put(("error", e))

        self.process = threading.Thread(
            target=_start,
            name="PlotmonServerThread",
            daemon=True,
        )
        self.process.start()

        # Wait for server to report readiness or error
        try:
            msg = q.get(timeout=10.0)
        except queue.Empty as e:
            raise RuntimeError("Plotmon server did not start within 10 seconds") from e

        if msg[0] == "error":
            err = msg[1]
            with contextlib.suppress(Exception):
                self.process.join(timeout=1.0)
            raise RuntimeError("Plotmon server failed to start") from err

        # Success tuple shape: ("ok", address, port)
        _, self.address, self.port = msg
        print(f"Plotmon server started at http://{self.address}:{self.port}")

        return plotmon_app

    def get_server_address(self) -> str:
        """Get the address of the Plotmon server.

        Returns:
            str: The address of the Plotmon server in the format 'address:port'.

        """
        if not self.address or not self.port:
            raise ValueError("Server not started yet.")
        return f"http://{self.address}:{self.port}"

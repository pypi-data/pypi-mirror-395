# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""
plotmon_app module: Bokeh application handler for Plotmon,
managing documents and data sources.
"""

from collections.abc import Callable, Sequence
import datetime
from functools import partial
import logging
import queue
from typing import Any

from bokeh.application.application import SessionContext
from bokeh.application.handlers.handler import Handler
from bokeh.core.types import ID
from bokeh.document import Document
from bokeh.events import MenuItemClick
from bokeh.models import ColumnDataSource, CustomJS, FlexBox
from bokeh.models.widgets import PreText
from bokeh.server.callbacks import SessionCallback

from quantify.visualization.plotmon.caching.base_cache import BaseCache
from quantify.visualization.plotmon.services import data_processor, graph_builder
from quantify.visualization.plotmon.services.session_manager import SessionManager
from quantify.visualization.plotmon.utils.commands import CommandType, ExperimentState
from quantify.visualization.plotmon.utils.communication import ParamInfo, PlotmonConfig
from quantify.visualization.plotmon.utils.figures import PlotType
from quantify.visualization.plotmon.utils.tuid_data import TuidData


class PlotmonApp(Handler):
    """
    Bokeh application handler for Plotmon.
    Manages multiple documents and their data sources, ensuring thread-safe updates.
    """

    UPDATE_RATE_MS: int = 1000 // 4
    MAX_QUEUE_ITEMS: int = 100

    def __init__(
        self,
        cache: BaseCache,
        data_source_name: str = "default_source",
    ) -> None:
        """
        Initialize the PlotmonApp with a cache and data source name.

        Parameters.
        ----------
        cache : BaseCache
            The cache instance to use for storing experiment data.
        data_source_name : str
            The name of the data source (default is "default_source").

        """
        super().__init__()
        self.config: None | PlotmonConfig = None
        self.cache = cache
        self.data_source_name = data_source_name
        self.session_manager = SessionManager()
        self.data_queue = queue.Queue()
        self._tuid_data = TuidData(tuids=set(), active_tuid="", selected_tuid={-1: ""})
        self._update_callback = None
        self.titles: dict[int, str] = {}
        self.current_index: int = -1
        self._rerender_callback: dict[int | ID, SessionCallback] = {}
        if self.config:
            base_sources = graph_builder.create_sources(self.config.graph_configs)
            for name, source in base_sources.items():
                self.session_manager.add_base_source(name, source)

    def modify_document(self, doc: Document) -> None:
        """
        Modify the given Bokeh document to
        set up the application layout and callbacks.

        Parameters
        ----------
        doc : Document
            The Bokeh document to modify.

        """
        doc, sources, layout = self.session_manager.get_doc_and_sources(doc)

        reload_holder = PreText(
            text=" ", css_classes=["hidden"], name="reload_holder", visible=False
        )
        reload_holder.width = 0
        reload_holder.height = 0
        callback = CustomJS(code="window.location.reload();")
        reload_holder.js_on_change("text", callback)
        doc.add_root(reload_holder)
        if self.config is None:
            config_dump = self.cache.get(f"{self.data_source_name}_config")
            if config_dump is None:
                logging.info(
                    "No configuration found for data source '%s'."
                    " Exiting document modification.",
                    self.data_source_name,
                )
                return
            self.config = PlotmonConfig.model_validate(config_dump)
        self._check_for_base_sources()
        self._tuid_data.selected_tuid[
            self.session_manager.get_current_session_id(doc)
        ] = self._tuid_data.selected_tuid.get(-1, "")
        # Set up the document with layout and
        # callbacks using the sources for this session.
        self.initialize_sources_from_cache(sources)
        logging.info(
            "Document modified for session %s",
            self.session_manager.get_current_session_id(doc),
        )

        self.serve(doc, sources, layout)

    def enqueue_data(self, plot_name: str, tuid: str, data: dict[str, list]) -> None:
        """
        Enqueue new data for a specific plot to be processed in the Bokeh event loop.

        Parameters
        ----------
        plot_name : str
            The name of the plot to update.
        tuid : str
            The TUID associated with the plot.
        data : dict[str, list]
            The new data to append to the plot.

        """
        self.data_queue.put((plot_name, tuid, data))

    def serve(
        self,
        doc: Document,
        sources: dict[str, ColumnDataSource],
        layout: None | FlexBox,
    ) -> None:
        """Set up the Bokeh document with the application layout and periodic callbacks.

        Parameters
        ----------
        doc : Document
            The Bokeh document to modify.
        sources : dict[str, ColumnDataSource]
            The data sources to be used in the document.
        layout : Column | None
            The existing layout to update, or None to create a new one.

        """
        if not self.config:
            logging.info(
                "No configuration found for data source '%s'."
                " Exiting document serving.",
                self.data_source_name,
            )
            return
        self._tuid_data.session_id = self.session_manager.get_current_session_id(doc)
        new_layout = graph_builder.build_layout(
            self.config,
            sources,
            self._tuid_data,
            self.cache.get_all(prefix=self.data_source_name, suffix="_meta"),
            partial(self._on_select, doc=doc),
            self._on_history_select,
            self.titles,
            layout,
        )

        if layout is None:
            self.session_manager.set_layout(doc, new_layout)
            doc.add_root(new_layout)
            doc.title = self.config.title

            doc.add_periodic_callback(self.check_for_update, self.UPDATE_RATE_MS)
            logging.info("Document root replaced")
        else:
            logging.info("Document layout updated")

    def _reset_state(self) -> None:
        """Reset the internal state of the handler, clearing TUIDs and data sources."""
        self._tuid_data = TuidData(tuids=set(), active_tuid="", selected_tuid={-1: ""})
        self.session_manager.clear()
        logging.info("PlotmonApp state has been reset.")

    def initialize_sources_from_cache(
        self, sources: dict[str, ColumnDataSource]
    ) -> None:
        """Initialize data sources from cached data if available."""
        for plot_name in self._get_plot_names():
            for tuid in self._tuid_data.tuids:
                cache_key = self._make_cache_key(plot_name, tuid)
                cached_data = self.cache.get(cache_key) or {}

                source, source_name = self._get_source(sources, plot_name, tuid)
                if cached_data and source and source_name:
                    plot_type, config = self._get_plot_type(plot_name)
                    data = data_processor.extract_data(cached_data, plot_type, config)
                    data = data_processor.process(plot_type, data, config)
                    source.data = data  # type: ignore[assignment]

    def check_for_update(self) -> None:
        """
        Check the data queue for new data and update plots accordingly.
        This method is called periodically in the Bokeh event loop.
        """
        if self.data_queue.qsize() > self.MAX_QUEUE_ITEMS:
            logging.info(
                "Data queue size exceeded %d items."
                " Clearing queue and reloading sources from cache.",
                self.MAX_QUEUE_ITEMS,
            )
            with self.data_queue.mutex:
                self.data_queue.queue.clear()
            for _, doc in self.session_manager.all_sessions():
                sources = self.session_manager.get_sources(
                    self.session_manager.get_current_session_id(doc)
                )
                self._safe_callback(
                    doc, lambda s=sources: self.initialize_sources_from_cache(s)
                )

        count = 0
        while not self.data_queue.empty() and count < self.MAX_QUEUE_ITEMS:
            plot_name, tuid, data = self.data_queue.get()
            for identifier, doc in self.session_manager.all_sessions():
                self._safe_callback(
                    doc,
                    lambda pn=plot_name,
                    d=data,
                    i=identifier,
                    t=tuid: self._update_plots(pn, d, i, t),
                )
            self.data_queue.task_done()
            count += 1
        if not self.data_queue.empty():
            logging.info("Task left in queue: %d", self.data_queue.qsize())
        # If there are more than MAX_QUEUE_ITEMS items in the queue,
        # empty the queue and load the sources from cache

    def start_experiment(self, tuid: str, timestamp: str) -> None:
        """
        Start tracking a new experiment by its TUID and create associated data sources.

        Parameters
        ----------
        tuid : str
            The TUID of the experiment to start.
        timestamp : str
            The timestamp when the experiment started.

        """
        if not self.config:
            logging.info("No graph configurations available. Cannot start experiment.")
            return
        self._tuid_data.tuids.add(tuid)
        self._tuid_data.active_tuid = tuid
        self._tuid_data.selected_tuid = {}
        tuid_sources = graph_builder.create_sources(self.config.graph_configs, tuid)
        self.session_manager.update_sources(tuid_sources)

        cache_key = f"{self.data_source_name}_{tuid}_meta"
        meta = self.cache.get(cache_key) or {}
        self.cache.set(
            cache_key,
            {
                **meta,
                "start_date": timestamp,
            },
        )
        logging.info("New experiment started with TUID: %s", tuid)
        self._re_render()

    def end_experiment(self, tuid: str, timestamp: str) -> None:
        """Mark an experiment as finished by removing it from the active TUIDs set."""
        self._tuid_data.selected_tuid[-1] = tuid
        session_ids = self.session_manager.get_all_session_ids()
        self._tuid_data.active_tuid = ""
        # Display the ended experiment as selected in all sessions
        for session_id in session_ids:
            self._tuid_data.selected_tuid[session_id] = tuid

        cache_key = f"{self.data_source_name}_{tuid}_meta"
        meta = self.cache.get(cache_key) or {}
        meta["end_date"] = timestamp
        self.cache.set(cache_key, meta)
        logging.info("Experiment ended with TUID: %s", tuid)
        self._re_render()

    #### PRIVATE METHODS ####

    def _change_graph_config(self, config: PlotmonConfig) -> None:
        """Change the graph configuration and reset internal state."""
        self._reset_state()
        self.config = config
        self._create_base_sources()
        self._check_for_base_sources()
        for _, doc in self.session_manager.all_sessions():
            reload_holder = doc.select_one({"name": "reload_holder"})
            logging.info("Reloading all documents due to graph config change.")
            if isinstance(reload_holder, PreText):
                doc.add_next_tick_callback(
                    partial(reload_holder.update, text="Refresh Me")
                )

    def _re_render(self) -> None:
        for identifier, doc in self.session_manager.all_sessions():
            if (
                identifier in self._rerender_callback
                and self._rerender_callback[identifier] in doc.session_callbacks
            ):
                # only re-render if there is no re-rerender already scheduled
                logging.info("Re-render already scheduled for session %s", identifier)
                continue
            sources = self.session_manager.get_sources(identifier)
            layout = self.session_manager.get_layout(doc)
            if layout is None:
                continue
            logging.info("Re-rendering layout for session %s", identifier)
            logging.info(self._rerender_callback.get(identifier))
            self._rerender_callback[identifier] = self._safe_callback(
                doc, lambda d=doc, s=sources, l=layout: self.serve(d, s, l)
            )

    def _update_plots(
        self,
        plot_name: str,
        data: dict[str, Sequence[Any]],
        identifier: int | ID,
        tuid: str,
    ) -> None:
        """
        Update the plots with new data and save the updated data to cache.

        Parameters
        ----------
        plot_name : str
            The name of the plot to update.
        data : dict[str, list]
            The new data to append to the plot.
        identifier : int | ID
            The session identifier for which to update the plot.
        tuid : str
            The TUID associated with the plot.

        """
        # get the plot source by name and append the new data,
        # then save the data to cache
        source, _ = self._get_source(
            self.session_manager.get_sources(identifier), plot_name, tuid
        )

        if not source:
            logging.info(
                "Data source for plot %s and TUID %s not found. Available sources: %s",
                plot_name,
                tuid,
                list(self.session_manager.get_sources(identifier).keys()),
            )
            if list(self.session_manager.get_sources(identifier).keys()) == []:
                # copy base sources to this session
                self.session_manager.copy_base_sources_to_session(identifier)
                self.initialize_sources_from_cache(
                    self.session_manager.get_sources(identifier)
                )
                logging.info("No base sources available.")
            return

        plot_type, config = self._get_plot_type(plot_name)
        if plot_type == PlotType.HEATMAP:
            # For heatmaps we get cache data and then process it
            cache_data = self.cache.get(self._make_cache_key(plot_name, tuid)) or {}
            data = data_processor.extract_data(cache_data, plot_type, config)

        processed_data = data_processor.process(plot_type, data, config)

        # Use Bokeh's stream method to efficiently
        # append new data to the plot's data source.
        # Validate data agains the source columns, they must have the same keys
        xkey = config.x_key

        source_data = source.data
        if not isinstance(source_data, dict):
            logging.info("Data for plot %s is not a valid DataDict.", plot_name)
            return
        if not set(processed_data.keys()).issubset(set(source_data.keys())):
            logging.info("Data for plot %s missing x_key %s", plot_name, xkey)
            return

        # if source data already contains data for the xkey ignore update
        if plot_type == PlotType.ONE_D:
            source.stream(new_data=processed_data, rollover=None)  # type: ignore[arg-type]
        elif plot_type == PlotType.HEATMAP:
            source.update(data=processed_data)
            # source.data = data

    async def on_session_destroyed(self, session_context: SessionContext) -> None:
        """
        Callback when a session is destroyed. Cleans up associated resources.

        Parameters
        ----------
        session_context : SessionContext
            The session context that was destroyed.

        """
        # Delete doc and sources associated with the destroyed session
        await super().on_session_destroyed(session_context)
        logging.info("Session %s destroyed", session_context.id)
        session_id = session_context.id if session_context else None
        self.session_manager.delete_session(session_id)

    def _get_plot_names(self) -> list[str]:
        """Retrieve all plot names from the graph configurations."""
        if not self.config:
            return []

        return [
            config.plot_name
            for row_config in self.config.graph_configs
            for config in row_config
        ]

    def _get_source(
        self, sources: dict[str, ColumnDataSource], plot_name: str, tuid: str
    ) -> tuple[ColumnDataSource | None, str | None]:
        """
        Retrieve the data source and its name associated with a given plot name.

        Parameters
        ----------
        sources : dict[str, ColumnDataSource]
            The dictionary of available data sources.
        plot_name : str
            The name of the plot to look up.
        tuid : str
            The TUID associated with the plot.

        Returns
        -------
        Tuple[ColumnDataSource | None, str | None]
            A tuple containing the data source and its name,
            or (None, None) if not found.

        """
        source_name = self._make_source_name(tuid, plot_name)
        return sources.get(source_name), source_name

    def _make_cache_key(self, plot_name: str, tuid: str) -> str:
        """Helper to construct a cache key for a given plot name."""
        return f"{self.data_source_name}_{tuid}_{plot_name}"

    def _make_source_name(self, tuid: str, plot_name: str) -> str:
        """Helper to construct a source name for a given TUID and plot name."""
        return f"{tuid}_{plot_name}"

    def _on_select(self, selected_tuids: set[str], doc: Document) -> None:
        """
        Callback for when TUIDs are selected in the DataTable.
        Only updates the plot for the current session/document.
        """
        session_id = self.session_manager.get_current_session_id(doc)
        if set(self._tuid_data.selected_tuid.get(session_id, "")) == selected_tuids:
            return  # No change in selection
        for tuid in selected_tuids:
            if tuid != self._tuid_data.selected_tuid[session_id]:
                self._tuid_data.selected_tuid[session_id] = tuid
                break

        sources = self.session_manager.get_sources(session_id)
        layout = self.session_manager.get_layout(doc)
        if layout is None:
            return
        if (
            session_id in self._rerender_callback
            and self._rerender_callback[session_id] in doc.session_callbacks
        ):
            logging.info("Re-rendering already scheduled for %s", session_id)
            return

        logging.info(
            "TUID selection changed to %s in session %s",
            self._tuid_data.selected_tuid[session_id],
            session_id,
        )
        self._rerender_callback[session_id] = self._safe_callback(
            doc, lambda d=doc, s=sources, l=layout: self.serve(d, s, l)
        )

    def _get_plot_type(self, plot_name: str) -> tuple[PlotType, ParamInfo]:
        """
        Retrieve the plot type for a given plot name from the graph configurations.

        Parameters
        ----------
        plot_name : str
            The name of the plot to look up.

        Returns
        -------
        PlotType
            The PlotType if found.

        """
        if not self.config:
            raise ValueError("No configuration available to get plot type from.")

        for row_config in self.config.graph_configs:
            for config in row_config:
                if config.plot_name == plot_name:
                    plot_type_str = config.plot_type
                    return PlotType.from_str(plot_type_str), config

        raise ValueError(f"Plot name '{plot_name}' not found in configurations.")

    def get_current_timestamp(self) -> str:
        """Get the current timestamp in ISO format."""
        now = datetime.datetime.now(datetime.timezone.utc)
        # Format: YYYY-MM-DD_HH-MM-SS.mmm_UTC
        return now.strftime("%Y-%m-%d_%H-%M-%S") + f".{now.microsecond // 1000:03d}"

    def add_event_next_tick(
        self, event: CommandType, data: str | PlotmonConfig
    ) -> None:
        """Add an event to be processed in the next tick of the Bokeh event loop."""
        for _, doc in self.session_manager.all_sessions():
            logging.info("Scheduling event %s for next tick", event)
            self._safe_callback(doc, lambda e=event, d=data: self._process_event(e, d))

    def _process_event(self, event: CommandType, data: str | PlotmonConfig) -> None:
        """
        Process an event. Currently supports 'start_experiment' and 'end_experiment'.

        Parameters
        ----------
        event : CommandType
            The type of event to process.
        data : Any
            The data associated with the event.

        """
        timestamp = self.get_current_timestamp()
        logging.info("Processing event %s at %s", event, timestamp)
        if event == CommandType.START and isinstance(data, str):
            self.start_experiment(data, timestamp)
        elif event == CommandType.STOP and isinstance(data, str):
            self.end_experiment(data, timestamp)
        elif event == CommandType.GRAPH_CONFIG:
            if isinstance(data, PlotmonConfig):
                self._change_graph_config(data)
            else:
                logging.info(
                    "Invalid type for GRAPH_CONFIG %s"
                    " given PlotmonConfig type expected",
                    type(data),
                )
        else:
            logging.info("Unknown event %s received.", event)

    def _check_for_base_sources(self) -> None:
        """Retrieve tuids from cache and ensure that they have base sources created."""
        experiment_state: dict[str, tuple[str, ExperimentState]] = (
            self.cache.get(f"{self.data_source_name}_experiments") or {}
        )
        for now, (tuid, status) in experiment_state.items():
            created = True
            if tuid in self._tuid_data.tuids:
                created = False

            logging.info("Processing TUID %s with status %s", tuid, status)
            self._tuid_data.tuids.add(tuid)
            if status == ExperimentState.STARTED:
                self._tuid_data.active_tuid = tuid
                self._tuid_data.selected_tuid[-1] = tuid
                cache_key = f"{self.data_source_name}_{tuid}_meta"
                meta = self.cache.get(cache_key) or {}
                meta["start_date"] = now
                self.cache.set(cache_key, meta)

            if status == ExperimentState.FINISHED:
                cache_key = f"{self.data_source_name}_{tuid}_meta"
                meta = self.cache.get(cache_key) or {}
                meta["end_date"] = meta.get("end_date", now)
                self.cache.set(cache_key, meta)
                if self._tuid_data.active_tuid == tuid:
                    self._tuid_data.active_tuid = ""

            if created and self.config:
                tuid_sources = graph_builder.create_sources(
                    self.config.graph_configs, tuid
                )
                self.session_manager.update_sources(tuid_sources)
            logging.info(
                "New TUID detected, that hasnt been initialized from cache: %s", tuid
            )

    def _create_base_sources(self) -> None:
        """Create base data sources for all TUIDs and plot configurations."""
        if not self.config:
            logging.info(
                "No graph configurations available. Cannot create base sources."
            )
            return
        base_sources = graph_builder.create_sources(self.config.graph_configs)
        for name, source in base_sources.items():
            self.session_manager.add_base_source(name, source)
        for session_id in self.session_manager.get_all_session_ids():
            self.session_manager.copy_base_sources_to_session(session_id)

    def _safe_callback(self, doc: Document, fn: Callable) -> SessionCallback:
        """
        Decorator to catch exceptions in Bokeh callbacks and refresh the page.

        Parameters
        ----------
        doc : Document
            The Bokeh document to modify.
        fn : Callable
            The callback function to execute in the next document tick.

        """
        return doc.add_next_tick_callback(fn)

    def _on_history_select(self, event: MenuItemClick) -> None:
        """
        Callback for when a history item is selected from the dropdown menu.
        Updates the selected TUID for the current session/document.
        """
        if not event.item:
            return
        index = int(event.item)
        self.cache.save(index=self.current_index)
        self.cache.load(index=index)
        self.current_index = index
        self.config = PlotmonConfig.model_validate(
            self.cache.get(f"{self.data_source_name}_config")
        )
        self._tuid_data = TuidData(
            tuids=set(),
            active_tuid="",
            selected_tuid={-1: ""},
        )
        for _, doc in self.session_manager.all_sessions():
            reload_holder = doc.select_one({"name": "reload_holder"})
            logging.info("Reloading all documents due to history selection.")
            if isinstance(reload_holder, PreText):
                doc.add_next_tick_callback(
                    partial(reload_holder.update, text="Refresh Me")
                )

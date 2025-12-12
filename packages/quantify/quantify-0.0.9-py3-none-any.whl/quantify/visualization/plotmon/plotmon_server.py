# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""
The module sets up and runs a Bokeh server for the Plotmon application,
 handling incoming messages via ZMQ.
"""

import logging

from quantify.visualization.plotmon.caching.base_cache import BaseCache
from quantify.visualization.plotmon.plotmon_app import PlotmonApp
from quantify.visualization.plotmon.utils.commands import ExperimentState
from quantify.visualization.plotmon.utils.communication import (
    Message,
    PlotmonConfig,
    StartExperimentMessage,
    StopExperimentMessage,
    UpdateDataMessage,
)


def process_message(msg: Message, handler: PlotmonApp, cache: BaseCache) -> None:
    """
    Process a received message and update the handler and cache accordingly.
    Uses structural pattern matching on the event type.
    """
    event = msg.event
    event_type = msg.event.event_type
    match event:
        case StartExperimentMessage():
            experiments = cache.get(f"{event.data_source_name}_experiments") or {}
            now = handler.get_current_timestamp()
            cache.set(
                f"{event.data_source_name}_experiments",
                {**experiments, now: (event.tuid, ExperimentState.STARTED)},
            )
            handler.add_event_next_tick(event_type, event.tuid)
        case StopExperimentMessage():
            experiments = cache.get(f"{event.data_source_name}_experiments") or {}
            now = handler.get_current_timestamp()
            cache.set(
                f"{event.data_source_name}_experiments",
                {**experiments, now: (event.tuid, ExperimentState.FINISHED)},
            )
            handler.add_event_next_tick(event_type, event.tuid)
        case UpdateDataMessage():
            plot_name = event.plot_name
            data = event.data
            old_data = (
                cache.get(f"{event.data_source_name}_{event.tuid}_{plot_name}") or {}
            )
            dump = data.model_dump(exclude={"sequence_ids"}).items()
            for i, seq_id in enumerate(data.sequence_ids):
                data_point = {key: value[i] for key, value in dump}
                old_data[seq_id] = data_point
            cache.set(f"{event.data_source_name}_{event.tuid}_{plot_name}", old_data)
            handler.enqueue_data(
                plot_name, event.tuid, data.model_dump(exclude={"sequence_ids"})
            )
        case PlotmonConfig():
            if handler.current_index != -1:
                cache.save(index=handler.current_index)
            index = cache.save()
            handler.current_index = index

            handler.titles[index] = event.title

            cache.clear()
            cache.set(f"{event.data_source_name}_config", event.model_dump())
            handler.add_event_next_tick(event_type, event)
        case _:
            logging.warning("Unknown message type: %s", type(event))

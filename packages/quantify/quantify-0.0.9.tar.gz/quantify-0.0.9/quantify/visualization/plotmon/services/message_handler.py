# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""ZMQ message handler for Plotmon application."""

from collections.abc import Callable
import json
import logging
import threading

from pydantic import ValidationError
import zmq

from quantify.visualization.plotmon.utils.communication import (
    Message,
)


class ZMQMessageHandler:
    """Handles incoming ZMQ messages and validates them against the Message schema."""

    def __init__(self, zmq_url: str = "tcp://localhost:5555") -> None:
        """
        Initialize the ZMQMessageHandler.
        Connects to the specified ZMQ URL and sets up a subscriber socket.

        Parameters.
        ----------
        zmq_url : str
            The ZMQ URL to connect to (default is "tcp://localhost:5555").

        """
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.SUB)
        self._socket.connect(zmq_url)
        self._socket.setsockopt_string(zmq.SUBSCRIBE, "")
        self._callback = lambda _: None
        logging.warning("ZMQMessageHandler subscribed to %s", zmq_url)

    def receive_message(self) -> Message | None:
        """
        Receives a message from the ZMQ socket and validates it.
        Returns a Message object if valid, otherwise None.
        """
        try:
            raw_msg = self._socket.recv_string()
            return Message.model_validate_json(raw_msg)
        except ValidationError as e:
            logging.error("Validation error: %s", e.json())
        except zmq.ZMQError as e:
            logging.error(
                "Error receiving ZMQ message: Code - %s; Error - %s",
                e.errno,
                e.strerror,
            )
        return None

    def _parse_json(self, msg: str) -> dict:
        try:
            return json.loads(msg)
        except json.JSONDecodeError as e:
            logging.error("JSON decode error: %s", e)
            return {}

    def listen(self, callback: Callable) -> None:
        """
        Continuously listens for messages and
        invokes the callback with each valid message.
        """
        self._callback = callback
        threading.Thread(target=self._listen_thread, daemon=True).start()

    def _listen_thread(self) -> None:
        while True:
            msg = self.receive_message()
            if msg:
                self._callback(msg)

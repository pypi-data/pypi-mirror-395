# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""
A module defining the TuidData class for
managing TUID-related data in the Plotmon application.
"""

from bokeh.core.types import ID
from pydantic import BaseModel


class TuidData(BaseModel):
    """
    A container for TUID related data in the Plotmon application.

    Attributes
    ----------
    tuids : set[str]
        A set of all TUIDs currently known to the application.
    active_tuids : set[str]
        A set of TUIDs that are currently active (e.g., experiments in progress).
    selected_tuid : str
        A set of TUIDs that are currently selected by the user for detailed viewing.

    """

    tuids: set[str]
    active_tuid: str
    selected_tuid: dict[ID | int, str]
    session_id: ID | int = -1  # Default session ID for non-session-specific data

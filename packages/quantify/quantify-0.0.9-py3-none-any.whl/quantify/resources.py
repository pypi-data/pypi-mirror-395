# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Common resources for use with the quantify."""

from __future__ import annotations

from collections import UserDict

from quantify.helpers.collections import make_hash
from quantify.helpers.importers import export_python_object_to_path_string


class Resource(UserDict):
    """
    A resource corresponds to a physical resource such as a port or a clock.

    Parameters
    ----------
    name :
        The resource name.

    """

    def __init__(self, name: str) -> None:
        """
        Initialize a Resource.

        Parameters
        ----------
        name : str
            The resource name

        """
        super().__init__()
        self.data["name"] = name

    @property
    def name(self) -> str:
        """
        Returns the name of the Resource.

        Returns
        -------
        :

        """
        return self.data["name"]

    def __eq__(self, other: object) -> bool:
        """
        Returns the equality of two instances based on its content :code:`self.data`.

        Parameters
        ----------
        other :
            The other instance to compare.

        Returns
        -------
        :

        """
        return repr(self) == repr(other)

    def __str__(self) -> str:
        """
        Returns a concise string representation which can be evaluated into a new
        instance using :code:`eval(str(operation))` only when the data dictionary has
        not been modified.

        This representation is guaranteed to be unique.
        """
        return f"{self.__class__.__name__}(name='{self.name}')"

    def __getstate__(self) -> dict[str, object]:
        """Return the state of the Resource."""
        return {
            "deserialization_type": export_python_object_to_path_string(self.__class__),
            "data": self.data,
        }

    def __setstate__(self, state: dict[str, dict]) -> None:
        """Set the state of the Resource."""
        self.data = state["data"]

    def __hash__(self) -> int:
        """Return a hash based on the contents of the Resource."""
        return make_hash(self.data)

    @property
    def hash(self) -> str:
        """A hash based on the contents of the Resource."""
        return str(hash(self))


class ClockResource(Resource):
    """
    The ClockResource corresponds to a physical clock used to modulate pulses.

    Parameters
    ----------
    name : str
        the name of this clock
    freq : float
        the frequency of the clock in Hz
    phase : float
        the starting phase of the clock in deg

    """

    def __init__(
        self,
        name: str,
        freq: float,
        phase: float = 0,
    ) -> None:
        """
        Initialize a ClockResource.

        Parameters
        ----------
        name : str
            the name of this clock
        freq : float
            the frequency of the clock in Hz
        phase : float
            the starting phase of the clock in deg

        """
        super().__init__(name)

        self.data = {
            "name": name,
            "type": str(self.__class__.__name__),
            "freq": freq,
            "phase": phase,
        }

    def __str__(self) -> str:
        """
        Returns a concise string representation which can be evaluated into a new
        instance using :code:`eval(str(operation))` only when the data dictionary has
        not been modified.

        This representation is guaranteed to be unique.
        """
        freq = self.data["freq"]
        phase = self.data["phase"]
        return f"{super().__str__()[:-1]}, freq={freq}, phase={phase})"


class BasebandClockResource(Resource):
    """
    Global identity for a virtual baseband clock.

    Baseband signals are assumed to be real-valued and will not be modulated.

    Parameters
    ----------
    name : str
        the name of this clock

    """

    IDENTITY = "cl0.baseband"

    def __init__(self, name: str) -> None:
        """
        Initialize a BasebandClockResource.

        Parameters
        ----------
        name : str
            the name of this clock

        """
        super().__init__(name)

        self.data = {
            "name": name,
            "type": str(self.__class__.__name__),
            "freq": 0,
            "phase": 0,
        }


class DigitalClockResource(Resource):
    """
    Global identity for a virtual digital clock.

    Digital clocks can only be associated with digital channels.

    Parameters
    ----------
    name : str
        the name of this clock

    """

    IDENTITY = "digital"

    def __init__(self, name: str) -> None:
        """
        Initialize a DigitalClockResource.

        Parameters
        ----------
        name : str
            the name of this clock

        """
        super().__init__(name)

        self.data = {
            "name": name,
            "type": str(self.__class__.__name__),
            "freq": 0,
            "phase": 0,
        }

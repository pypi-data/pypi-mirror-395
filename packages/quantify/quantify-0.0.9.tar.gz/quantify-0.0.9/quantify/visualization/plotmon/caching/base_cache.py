# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Abstract base class for caching mechanisms in Plotmon."""

from abc import ABC


class BaseCache(ABC):
    """
    Abstract class to cache data with id and retrieve it later.
    Future implementations could use in memory and redis based caching.
    """

    def set(self, cache_id: str, data: dict) -> None:
        """
        Store data in the cache with the given id.

        Parameters
        ----------
        cache_id : str
            The identifier for the cached data.
        data : dict
            The data to be cached.

        """
        raise NotImplementedError

    def get(self, cache_id: str) -> dict | None:
        """
        Retrieve data from the cache using the given id.

        Parameters
        ----------
        cache_id : str
            The identifier for the cached data.

        Returns
        -------
        dict | None
            The cached data if found, otherwise None.

        """
        raise NotImplementedError

    def get_all(self, prefix: str = "", suffix: str = "") -> dict[str, dict]:
        """
        Retrieve all cached data, optionally filtered by a prefix.

        Parameters
        ----------
        prefix : str
            The prefix to filter cached data keys.
        suffix : str
            The suffix to filter cached data keys.

        Returns
        -------
        dict[str, dict]
            A dictionary of all cached data, with keys as cache ids and
            values as the cached data.

        """
        raise NotImplementedError

    def clear(self) -> None:
        """Clear all data from the cache."""
        raise NotImplementedError

    def save(self, path: str = ".cache/", index: int | None = None) -> int:
        """
        Save the current cache state to disk.

        Parameters
        ----------
        path : str
            The directory path where the cache should be saved.
        index : int | None
            An optional index to differentiate multiple saves.

        """
        raise NotImplementedError

    def load(self, index: int, path: str = ".cache/") -> None:
        """
        Load the cache state from disk.

        Parameters
        ----------
        path : str
            The directory path where the cache is stored.
        index : int
            The index of the cache state to load.

        """
        raise NotImplementedError

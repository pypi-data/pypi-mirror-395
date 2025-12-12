# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""in_memory_cache module: In-memory cache implementation for Plotmon."""

import json
import os

from quantify.visualization.plotmon.caching.base_cache import BaseCache


class InMemoryCache(BaseCache):
    """Thread-safe in memory cache implementation."""

    def __init__(self) -> None:
        """Initializes the in-memory cache and its lock."""
        if not hasattr(self, "_cache"):
            self._cache = {}
        self._index = 0
        self.max_experiments = 25

    def set(self, cache_id: str, data: dict) -> None:
        """
        Set a cache entry by its ID.

        Parameters
        ----------
        cache_id : str
            The ID of the cache entry to set.
        data : Any
            The data to be cached.

        """
        self._cache[cache_id] = data

    def get(self, cache_id: str) -> dict | None:
        """
        Retrieve a cache entry by its ID.

        Parameters
        ----------
        cache_id : str
            The ID of the cache entry to retrieve.

        Returns
        -------
        Any | None
            The cache entry if found, otherwise None.

        """
        return self._cache.get(cache_id, None)

    def get_all(self, prefix: str = "", suffix: str = "") -> dict[str, dict]:
        """
        Retrieve all cache entries that match the given prefix and suffix.

        Parameters
        ----------
        prefix : str
            The prefix that the cache IDs should start with.
        suffix : str
            The suffix that the cache IDs should end with.

        Returns
        -------
        dict[str, Any]
            A dictionary of cache entries that match the criteria.

        """
        return {
            key: value
            for key, value in self._cache.items()
            if key.startswith(prefix) and key.endswith(suffix)
        }

    def clear(self) -> None:
        """Clear all data from the cache."""
        self._cache.clear()

    def save(self, path: str = ".cache/", index: int | None = None) -> int:
        """Save the current cache state to disk.

        Parameters
        ----------
        path : str
            The directory path where the cache files will be saved.
        index : int | None
            The index to use for the cache file. If None, a new index will be created

        """
        # Create the cache directory if it doesn't exist
        os.makedirs(path, exist_ok=True)
        if index is None:
            self._index += 1
            index = self._index

        with open(path + f"{index % self.max_experiments}.json", "w") as f:
            json.dump(self._cache, f, indent=4)

        return index

    def load(self, index: int, path: str = ".cache/") -> None:
        """Load the cache state from disk.

        Parameters
        ----------
        path : str
            The directory path where the cache files are saved.
        index : int
            The index of the cache file to load.

        """
        with open(path + f"{index % self.max_experiments}.json") as f:
            self._cache = json.load(f)

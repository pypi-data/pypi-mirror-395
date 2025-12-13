"""XER file cache management for PyP6Xer MCP Server.

This module provides an encapsulated cache for loaded XER files,
replacing the global dictionary with a structured class.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class CachedXer:
    """Structured container for cached XER data."""

    reader: Any
    projects: List[Any] = field(default_factory=list)
    activities: List[Any] = field(default_factory=list)
    resources: List[Any] = field(default_factory=list)
    calendars: List[Any] = field(default_factory=list)
    activityresources: List[Any] = field(default_factory=list)
    relations: List[Any] = field(default_factory=list)
    file_path: str = ""


class XerCache:
    """Encapsulated cache for loaded XER files.

    Provides a clean interface for storing and retrieving parsed XER data.
    All tools reference cached data via cache keys.
    """

    def __init__(self) -> None:
        self._cache: Dict[str, CachedXer] = {}

    def get(self, cache_key: str) -> CachedXer:
        """Get cached XER data by key.

        Args:
            cache_key: The key used when loading the XER file.

        Returns:
            CachedXer containing the parsed data.

        Raises:
            ValueError: If no data exists for the given key.
        """
        if cache_key not in self._cache:
            raise ValueError(
                f"No XER file loaded with key '{cache_key}'. Use pyp6xer_load_file first."
            )
        return self._cache[cache_key]

    def get_raw(self, cache_key: str) -> Dict[str, Any]:
        """Get cached XER data as a dictionary (backward compatibility).

        Args:
            cache_key: The key used when loading the XER file.

        Returns:
            Dictionary with reader, projects, activities, etc.

        Raises:
            ValueError: If no data exists for the given key.
        """
        cached = self.get(cache_key)
        return {
            "reader": cached.reader,
            "projects": cached.projects,
            "activities": cached.activities,
            "resources": cached.resources,
            "calendars": cached.calendars,
            "activityresources": cached.activityresources,
            "relations": cached.relations,
            "file_path": cached.file_path,
        }

    def set(self, cache_key: str, data: CachedXer) -> None:
        """Store XER data in the cache.

        Args:
            cache_key: Key to reference this data.
            data: CachedXer containing the parsed data.
        """
        self._cache[cache_key] = data

    def set_from_dict(self, cache_key: str, data: Dict[str, Any]) -> None:
        """Store XER data from a dictionary (backward compatibility).

        Args:
            cache_key: Key to reference this data.
            data: Dictionary with reader, projects, activities, etc.
        """
        cached = CachedXer(
            reader=data.get("reader"),
            projects=data.get("projects", []),
            activities=data.get("activities", []),
            resources=data.get("resources", []),
            calendars=data.get("calendars", []),
            activityresources=data.get("activityresources", []),
            relations=data.get("relations", []),
            file_path=data.get("file_path", ""),
        )
        self._cache[cache_key] = cached

    def delete(self, cache_key: str) -> bool:
        """Remove a cached XER file.

        Args:
            cache_key: Key of the data to remove.

        Returns:
            True if the key existed and was removed, False otherwise.
        """
        if cache_key in self._cache:
            del self._cache[cache_key]
            return True
        return False

    def clear(self) -> int:
        """Clear all cached data.

        Returns:
            Number of entries that were cleared.
        """
        count = len(self._cache)
        self._cache.clear()
        return count

    def keys(self) -> List[str]:
        """Get all cache keys.

        Returns:
            List of cache keys.
        """
        return list(self._cache.keys())

    def __contains__(self, key: str) -> bool:
        """Check if a key exists in the cache."""
        return key in self._cache

    def __len__(self) -> int:
        """Return the number of cached entries."""
        return len(self._cache)

    def __bool__(self) -> bool:
        """Return True if cache has entries."""
        return len(self._cache) > 0


# Global cache instance
xer_cache = XerCache()

"""
Path for identifying objects in a hierarchy.

Author: Juha Meskanen
Date: 2024-10-26
"""

from __future__ import annotations
from typing import List


class URL:
    """Hierarchical path for identifying objects in a hierarchy."""

    def __init__(self, path: str = "") -> None:
        """Initializes the URL with an optional starting path.

        Args:
            path (str): The initial path as a string (e.g., "/foo/bar").
        """
        self.segments: List[str] = [
            segment for segment in path.strip("/").split("/") if segment
        ]
        self.is_rooted: bool = path.startswith("/")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, URL):
            return self.segments == other.segments
        return False

    def __str__(self) -> str:
        return f"/{'/'.join(self.segments)}"

    def push_tail(self, name: str) -> None:
        """Adds a segment to the end of the URL path (child).

        Args:
            name (str): The name of the segment to add.
        """
        self.segments.append(name)

    def push_head(self, name: str) -> None:
        """Adds a segment to the beginning of the URL path (parent).

        Args:
            name (str): The name of the segment to add.
        """
        self.segments.insert(0, name)

    def pop_tail(self) -> str:
        """Removes and returns the last segment of the URL path.

        Returns:
            str: The last segment of the path.

        Raises:
            IndexError: If the path is empty.
        """
        if self.segments:
            return self.segments.pop()
        raise IndexError("Cannot pop from an empty URL")

    def pop_head(self) -> str:
        """Removes and returns the first segment of the URL path.

        Returns:
            str: The first segment of the path.

        Raises:
            IndexError: If the path is empty.
        """
        if self.segments:
            return self.segments.pop(0)
        raise IndexError("Cannot pop from an empty URL")

    def get(self) -> str:
        """Gets the full URL path as a string.

        Returns:
            str: The full path, starting with a forward slash if absolute.
        """
        prefix: str = "/" if self.is_rooted else ""
        return prefix + "/".join(self.segments)

    def normalize(self) -> URL:
        """Simplifies the URL path by resolving "." and "..".

        Returns:
            URL: The normalized path.
        """
        stack: List[str] = []
        for segment in self.segments:
            if segment == "..":
                if stack:
                    stack.pop()  # Go up one level
                elif not self.is_rooted:
                    stack.append("..")  # Preserve leading ".." for relative paths
            elif segment != ".":
                stack.append(segment)
        self.segments = stack
        return self

    def is_absolute(self) -> bool:
        """Checks if the URL path is absolute.

        Returns:
            bool: True if the path starts with "/", False otherwise.
        """
        return self.is_rooted

    def make_absolute(self, base: URL) -> URL:
        """Makes the path absolute using a given base path.

        Args:
            base (URL): The base path to combine with.

        Returns:
            URL: The absolute path.
        """
        if self.is_absolute():
            return self
        new_path: URL = base.copy()
        new_path.segments.extend(self.segments)
        return new_path.normalize()

    def starts_with(self, segment: str) -> bool:
        """Checks if the path starts with the given segment.

        Args:
            segment (str): The segment to check.

        Returns:
            bool: True if the path starts with the segment, False otherwise.
        """
        return bool(self.segments and self.segments[0] == segment)

    def prepend_base(self, base: str) -> None:
        """Prepends a base path if the current path is not absolute.

        Args:
            base (str): The base path to prepend.
        """
        if not self.is_absolute():
            base_segments: List[str] = [
                segment for segment in base.strip("/").split("/") if segment
            ]
            self.segments = base_segments + self.segments
            self.is_rooted = base.startswith("/")

    def is_empty(self) -> bool:
        """Checks if the URL path has no segments.

        Returns:
            bool: True if the path is empty, False otherwise.
        """
        return len(self.segments) == 0

    def copy(self) -> URL:
        """Creates a deep copy of the URL.

        Returns:
            URL: A new instance with the same segments.
        """
        return URL(self.get())

    def __repr__(self) -> str:
        """Returns the formal string representation of the URL.

        Returns:
            str: A string representation suitable for debugging.
        """
        return f"URL({self.get()!r})"

"""
Abstract base class for formats.

Author: Juha Meskanen
Date: 2024-10-26
"""

from abc import ABC, abstractmethod
from io import IOBase
from typing import Type

from .masterpiece import MasterPiece, classproperty


class Format(MasterPiece, ABC):
    """
    Abstract base class for formats. Implements two sets of methods for
    serializing both class attributes and instance attributes.
    """

    def __init__(self, stream: IOBase):
        """Initialize the format with a stream (file object).

        Args:
            stream (IOBase): The stream to write/read
        """
        self.stream = stream

    @abstractmethod
    def serialize(self, obj: MasterPiece) -> None:
        """Serialize the object to the given JSON stream.

        Args:
            obj (Any): The object to serialize.
        """

    @abstractmethod
    def deserialize(self, obj: MasterPiece) -> None:
        """Load attributes from the given JSON stream into the object.

        Args:
            obj (Any): The object to deserialize into.
        """

    @abstractmethod
    def save_configuration(self, clazz: Type[MasterPiece]) -> None:
        """Save class attributes to a stream.
        Args:
            clazz (Type[Piece]) class to be saved

        """

    @abstractmethod
    def load_configuration(self, clazz: Type[MasterPiece]) -> None:
        """Load class attributes from a strea.
        Args:
            clazz (Type[Piece]) class to be configured
        """

    @classproperty  # type: ignore
    def file_extension(cls) -> str:
        """Returns the file extension for the format."""
        raise NotImplementedError("Subclasses must define the file_extension property")

"""
Author: Juha Meskanen
Date: 2024-10-26
"""

from io import IOBase
import json
from typing import Type
from typing_extensions import override

from .masterpiece import MasterPiece, classproperty
from .format import Format


class JsonFormat(Format):
    """
    The `JsonFormat` class provides methods for serializing and deserializing objects
    to and from JSON format.

    Features:
    ---------
    - Serializes object attributes to a JSON file or stream.
    - Deserializes object attributes from a JSON file or stream.

    Usage:
    ------
    To use the `JsonFormat`, create an instance by passing the target stream. Then,
    call the `serialize` or `deserialize` method with the appropriate object.

    Example:
    --------
    .. code-block:: python

        from masterpiece.core import JsonFormat, MasterPiece

        # Create a JsonFormat instance with a file stream
        with open("output.json", "w") as f:
            json_format = JsonFormat(f)
            json_format.serialize(piece)  # piece is the object to serialize

        with open("output.json", "r") as f:
            json_format = JsonFormat(f)
            json_format.deserialize(piece)  # piece is the object to deserialize
    """

    @override
    def __init__(self, stream: IOBase) -> None:
        """Initialize the JsonFormat with a stream (file object).

        Args:
            stream (Any): The stream to write/read JSON data.
        """
        super().__init__(stream)

    @override
    def serialize(self, obj: MasterPiece) -> None:
        """Serialize the object to the given JSON stream.

        Args:
            obj (Any): The object to serialize.
        """
        json.dump(obj.to_dict(), self.stream, indent=4)

    @override
    def deserialize(self, obj: MasterPiece) -> None:
        """Load attributes from the given JSON stream into the object.

        Args:
            obj (Any): The object to deserialize into.
        """
        attributes = json.load(self.stream)
        obj.from_dict(attributes)

    @override
    def save_configuration(self, clazz: Type[MasterPiece]) -> None:
        """Create class configuration file, if configuration is enabled and
        if the file does not exist yet. See --config startup argument.
        Args:
            clazz (Type[Piece]) class to be saved

        """
        json.dump(clazz.classattrs_to_dict(), self.stream)

    @override
    def load_configuration(self, clazz: Type[MasterPiece]) -> None:
        """Load class attributes from a JSON file.
        Args:
            clazz (Type[Piece]) class to be configured
        """
        clazz.classattrs_from_dict(json.load(self.stream))

    # TODO: Fix this, if you can, beats me. According to mypy:
    # Argument 1 to "classproperty" has incompatible type "Callable[[JsonFormat], str]"
    # expected "Callable[[type[Any]], Any]"Mypy
    @classproperty  # type: ignore
    def file_extension(cls) -> str:
        """Fetch the file extension

        Returns:
            str: file extension including the dot
        """
        return ".json"

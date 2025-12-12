import inspect
import json
from typing import Type
import unittest
from io import StringIO

from masterpiece.format import Format
from masterpiece.masterpiece import MasterPiece
from masterpiece.jsonformat import JsonFormat
from masterpiece.composite import Composite


class TestJsonFormat(unittest.TestCase):

    def setUp(self) ->None:
        """Set up a hierarchical structure for testing."""
        self.parent = Composite("parent")
        self.child = MasterPiece("child")
        self.parent.add(self.child)

    def test_serialize(self) ->None:
        """Test serialization of the hierarchical object to JSON."""
        # Create a StringIO object to simulate a file
        stream = StringIO()
        json_format = JsonFormat(stream)

        # Serialize the parent object
        json_format.serialize(self.parent)

        # Verify the JSON output
        expected_output = json.dumps(self.parent.to_dict(), indent=4)
        self.assertEqual(stream.getvalue().strip(), expected_output)

    def test_deserialize(self) ->None:
        """Test deserialization of JSON back to the hierarchical object."""
        # Create a StringIO object to simulate a file
        stream = StringIO()

        # Serialize the parent object to JSON first
        json_format = JsonFormat(stream)
        json_format.serialize(self.parent)

        # Prepare a new Composite object for deserialization
        new_parent = Composite("")

        # Seek to the beginning of the stream for reading
        stream.seek(0)

        # Deserialize the JSON back to the new parent object
        json_format = JsonFormat(stream)
        json_format.deserialize(new_parent)

        # Verify that the new_parent object has the same attributes
        self.assertEqual(new_parent.name, self.parent.name)
        self.assertEqual(len(new_parent.children), len(self.parent.children))
        self.assertEqual(new_parent.children[0].name, self.child.name)

    def test_abstractness(self) -> None:
        """Test abstractness of the JsonFormat and its super class."""
        self.assertFalse(inspect.isabstract(JsonFormat))
        self.assertTrue(inspect.isabstract(Format))
        cl: Type[MasterPiece] = MasterPiece.factory()["JsonFormat"]
        self.assertFalse(inspect.isabstract(cl))


if __name__ == "__main__":
    unittest.main()

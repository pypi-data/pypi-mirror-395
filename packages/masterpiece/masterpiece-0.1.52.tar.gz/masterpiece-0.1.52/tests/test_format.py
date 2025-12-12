import inspect
import json
from typing import Type
import unittest
from io import StringIO

from masterpiece.format import Format
from masterpiece.masterpiece import MasterPiece

from masterpiece.composite import Composite


class TestFormat(unittest.TestCase):

    def setUp(self) ->None:
        """Empty by now."""

    def test_abstractness(self) -> None:
        """Test abstractness of the JsonFormat and its super class."""
        self.assertTrue(inspect.isabstract(Format))
        cl: Type[MasterPiece] = MasterPiece.factory()["JsonFormat"]
        self.assertFalse(inspect.isabstract(cl))


if __name__ == "__main__":
    unittest.main()

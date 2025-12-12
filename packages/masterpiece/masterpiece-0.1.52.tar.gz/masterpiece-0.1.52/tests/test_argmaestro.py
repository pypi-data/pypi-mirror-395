"""
Author: Juha Meskanen
Date: 2024-10-26
"""

import unittest
from unittest.mock import patch
from masterpiece.application import Application
from masterpiece.masterpiece import MasterPiece
from masterpiece.argmaestro import ArgMaestro


class TestSampleClass(MasterPiece):
    """A sample class for testing ArgMaestro."""

    attr1: int = 5
    attr2: float = 2.5
    attr3: str = "default"
    attr4: bool = False


class TestArgMaestro(unittest.TestCase):
    def setUp(self) ->None:
        """Set up the ArgMaestro instance for testing and reset TestSampleClass attributes."""
        self.argmaestro = ArgMaestro()
        self.argmaestro.add_class_arguments(TestSampleClass)

    def tearDown(self) ->None:
        """Reset TestSampleClass attributes to defaults after each test."""
        TestSampleClass.attr1 = 5
        TestSampleClass.attr2 = 2.5
        TestSampleClass.attr3 = "default"
        TestSampleClass.attr4 = False

    @patch(
        "sys.argv",
        new=[
            "argparser_test.py",
            "--testsampleclass_attr1",
            "10",
            "--testsampleclass_attr2",
            "3.14",
            "--testsampleclass_attr3",
            "new_value",
            "--testsampleclass_attr4",
        ],
    )
    def test_parse_args(self) ->None:
        """Test argument parsing and attribute assignment."""
        self.argmaestro.parse_args()
        self.assertEqual(TestSampleClass.attr1, 10)
        self.assertEqual(TestSampleClass.attr2, 3.14)
        self.assertEqual(TestSampleClass.attr3, "new_value")
        self.assertTrue(TestSampleClass.attr4)

    @patch("sys.argv", new=["argparser_test.py", "--testsampleclass_attr1", "20"])
    def test_parse_args_with_default(self) ->None:
        """Test argument parsing when some defaults are used."""
        self.argmaestro.parse_args()
        self.assertEqual(TestSampleClass.attr1, 20)  # Set by command-line argument
        self.assertEqual(TestSampleClass.attr2, 2.5)  # Default value
        self.assertEqual(TestSampleClass.attr3, "default")  # Default value
        self.assertFalse(TestSampleClass.attr4)  # Default value


if __name__ == "__main__":
    unittest.main()

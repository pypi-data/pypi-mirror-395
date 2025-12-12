"""
Author: Juha Meskanen
Date: 2024-10-26
"""

from typing import Any
import unittest

from io import StringIO
from unittest.mock import patch
from masterpiece.masterpiece import MasterPiece
from masterpiece.composite import Composite
from masterpiece.treevisualizer import TreeVisualizer


class TestComposite(unittest.TestCase):
    """Unit tests for `Composite` class."""

    def setUp(self) -> None:
        """Set up test data for each test."""
        self.composite = Composite(name="group")
        self.child1 = MasterPiece(name="child1")
        self.child2 = MasterPiece(name="child2")

    @patch("sys.stdout", new_callable=StringIO)
    def test_print_with_stdout_capture(self, mock_stdout: Any) -> None:
        """Test the hierarchical print method by capturing stdout."""
        self.composite.add(self.child1)
        self.composite.add(self.child2)
        visualizer = TreeVisualizer("blue")
        visualizer.print_tree(self.composite)

        # Capture the printed output
        output = mock_stdout.getvalue().strip()

        # Define the expected output, taking into account the correct spacing and symbols
        expected_output = (
            "\x1b[34mgroup\x1b[0m\n"
            "    \x1b[34m├─ \x1b[34mchild1\x1b[0m\n"
            "    \x1b[34m└─ \x1b[34mchild2\x1b[0m"
        )
        # Debugging prints
        print("Actual Output:")
        print(repr(output))
        print("Expected Output:")
        print(repr(expected_output))

        # Assert the expected output matches the actual printed output
        self.assertEqual(output, expected_output)


if __name__ == "__main__":
    unittest.main()

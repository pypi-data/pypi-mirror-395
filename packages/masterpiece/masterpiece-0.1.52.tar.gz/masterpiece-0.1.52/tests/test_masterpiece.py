"""
Author: Juha Meskanen
Date: 2024-10-26
"""

from logging import Logger
from typing import Callable
import unittest
import tempfile
import os
import json
from unittest.mock import Mock, patch
from masterpiece.jsonformat import JsonFormat
from masterpiece.masterpiece import MasterPiece


class TestMasterPiece(unittest.TestCase):
    """Unit tests for `MasterPiece` class."""

    def test_get_classid(self) -> None:
        classid = MasterPiece.get_class_id()
        self.assertEqual("MasterPiece", classid)

    def test_serialization(self) -> None:
        """Test serialization"""
        mp = MasterPiece("foo")

        with tempfile.TemporaryDirectory() as tmp:
            filename = os.path.join(tmp, "masterpiece.json")
            with open(filename, "w", encoding="utf-8") as f:
                json_format = JsonFormat(f)
                json_format.serialize(mp)
            mp2 = MasterPiece("bar")
            with open(filename, "r", encoding="utf-8") as f:
                json_format = JsonFormat(f)
                json_format.deserialize(mp2)
            self.assertEqual("foo", mp2.name)
            self.assertIsNone(mp2.payload)

    def test_serialization_with_payload(self) -> None:
        """Test serialization with payload object"""
        payload = MasterPiece("bar")
        mp = MasterPiece("foo", payload)

        with tempfile.TemporaryDirectory() as tmp:
            filename = os.path.join(tmp, "masterpiece.json")
            with open(filename, "w", encoding="utf-8") as f:
                json_format = JsonFormat(f)
                json_format.serialize(mp)
            mp2 = MasterPiece("bar")
            with open(filename, "r", encoding="utf-8") as f:
                json_format = JsonFormat(f)
                json_format.deserialize(mp2)
            self.assertEqual("foo", mp2.name)
            self.assertIsNotNone(mp2.payload)

            # Ensure payload has been deserialized correctly
            self.assertIsNotNone(mp2.payload)
            self.assertIsNotNone(mp2.payload)
            self.assertIsNotNone(mp2.payload)
            self.assertIsNotNone(mp2.payload)
            self.assertEqual("bar", mp2.payload.name)

    def test_masterpiece_initialization(self) -> None:
        """Test initialization of the MasterPiece object."""
        obj = MasterPiece(name="test", payload=None)
        self.assertEqual(obj.name, "test")
        self.assertIsNone(obj.payload)

    def test_masterpiece_to_dict(self) -> None:
        """Test that the to_dict method serializes the object correctly."""
        obj = MasterPiece(name="test")
        result = obj.to_dict()
        self.assertEqual(result["_class"], "MasterPiece")
        self.assertEqual(result["_object"]["name"], "test")
        self.assertIsNone(result["_object"]["payload"])

    def test_masterpiece_from_dict(self) -> None:
        """Test that the from_dict method deserializes the object correctly."""
        data = {
            "_class": "MasterPiece",
            "_object": {
                "name": "test",
                "payload": None,
            },
        }
        obj = MasterPiece(name="foo")  # Create an object with a different name
        obj.from_dict(data)
        self.assertEqual(obj.name, "test")
        self.assertIsNone(obj.payload)

    @patch("masterpiece.masterpiece.MasterPiece._log", new_callable=Mock)
    def test_logging_info(self, mock_logger: Mock) -> None:
        """Test logging functionality with info level."""
        obj = MasterPiece(name="test")
        obj.info("This is a test info message")

        # Check if the mock logger's info method was called with the expected message
        mock_logger.info.assert_called_once_with(
            "MasterPiece : test : This is a test info message"
        )

    @patch("masterpiece.masterpiece.MasterPiece._log", new_callable=Mock)
    def test_logging_debug(self, mock_logger: Mock) -> None:
        """Test logging functionality with debug level."""
        obj = MasterPiece(name="test")
        obj.debug("This is a test debug message")

        # Check if the mock logger's info method was called with the expected message
        mock_logger.debug.assert_called_once_with(
            "MasterPiece : test : This is a test debug message"
        )

    @patch("masterpiece.masterpiece.MasterPiece._log", new_callable=Mock)
    def test_logging_warning(self, mock_logger: Mock) -> None:
        """Test logging functionality with warning level."""
        obj = MasterPiece(name="test")
        obj.warning("This is a test warning message")

        # Check if the mock logger's info method was called with the expected message
        mock_logger.warning.assert_called_once_with(
            "MasterPiece : test : This is a test warning message"
        )

    @patch("masterpiece.masterpiece.MasterPiece._log", new_callable=Mock)
    def test_logging_error(self, mock_logger: Mock) -> None:
        """Test logging functionality with warning level."""
        obj = MasterPiece(name="test")
        obj.error("This is a test error message")

        # Check if the mock logger's info method was called with the expected message
        mock_logger.error.assert_called_once_with(
            "MasterPiece : test : This is a test error message"
        )

    def test_masterpiece_register(self) -> None:
        """Test the registration mechanism for the MasterPiece class."""

        class TestPiece(MasterPiece):
            pass

        self.assertEqual(TestPiece.get_class_id(), "TestPiece")

    def test_serialize_to_json(self) -> None:
        """Test serialization to a JSON file."""
        obj = MasterPiece(name="test")
        output_file = "output.json"

        with open(output_file, "w", encoding="utf-8") as f:
            json_format = JsonFormat(f)
            json_format.serialize(obj)

        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertEqual(data["_class"], "MasterPiece")
        self.assertEqual(data["_object"]["name"], "test")
        self.assertIsNone(data["_object"]["payload"])

    def test_deserialize_from_json(self) -> None:
        """Test deserialization from a JSON file."""
        input_file = "input.json"
        data = {
            "_class": "MasterPiece",
            "_object": {
                "name": "test",
                "payload": None,
            },
        }

        with open(input_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        obj = MasterPiece()

        with open(input_file, "r", encoding="utf-8") as f:
            json_format = JsonFormat(f)
            json_format.deserialize(obj)

        self.assertEqual(obj.name, "test")
        self.assertIsNone(obj.payload)

    def test_masterpiece_copy(self) -> None:
        """Test copying of a MasterPiece object."""
        obj = MasterPiece(name="test")
        obj_copy = obj.copy()

        self.assertEqual(obj_copy.name, "test")
        self.assertIsNot(obj_copy, obj)  # Ensure it's a different object

    @patch("builtins.print")  # Patch print to check output
    def test_run_with_valid_payload(self, mock_print: Mock) -> None:
        """Test the run method with a valid payload."""
        # Create a MasterPiece instance
        master_piece = MasterPiece()

        # Create a mock payload that is a MasterPiece
        mock_payload = Mock(spec=MasterPiece)
        master_piece.payload = mock_payload

        # Call the run method
        master_piece.run()

        # Verify that the payload's run method was called
        mock_payload.run.assert_called_once()

    @patch("builtins.print")  # Patch print to check output
    def test_run_with_invalid_payload(self, mock_print: Mock) -> None:
        """Test the run method with an invalid payload (not a MasterPiece)."""
        # Create a MasterPiece instance
        master_piece = MasterPiece()

        # Set an invalid payload (not a MasterPiece)
        master_piece.payload = MasterPiece("Invalid Payload")

        # Call the run method
        master_piece.run()

        # Verify that the payload's run method was not called
        mock_print.assert_not_called()

    @patch("builtins.print")  # Patch print to check output
    def test_run_forever_with_valid_payload(self, mock_print: Mock) -> None:
        """Test the run_forever method with a valid payload."""
        # Create a MasterPiece instance
        master_piece = MasterPiece()

        # Create a mock payload that is a MasterPiece
        mock_payload = Mock(spec=MasterPiece)
        master_piece.payload = mock_payload

        # Simulate the run_forever method
        mock_payload.run_forever = Mock()

        # Call the run_forever method
        master_piece.run_forever()

        # Verify that the payload's run_forever method was called
        mock_payload.run_forever.assert_called_once()
        mock_print.assert_called_once_with("Newtorking loop exit without exception")

    @patch("builtins.print")  # Patch print to check output
    def test_run_forever_with_invalid_payload(self, mock_print: Mock) -> None:
        """Test the run_forever method with an invalid payload (not a MasterPiece)."""
        # Create a MasterPiece instance
        master_piece = MasterPiece()

        # Set an invalid payload (not a MasterPiece)
        master_piece.payload = Mock()  # Assign a mock object instead of a string

        # Call the run_forever method
        master_piece.run_forever()

        # Verify that the print statement was not called
        mock_print.assert_not_called()

    @patch("builtins.print")  # Patch print to check output
    def test_run_forever_with_keyboard_interrupt(self, mock_print: Mock) -> None:
        """Test the run_forever method with KeyboardInterrupt."""
        # Create a MasterPiece instance
        master_piece = MasterPiece()

        # Create a mock payload that is a MasterPiece
        mock_payload = Mock(spec=MasterPiece)
        master_piece.payload = mock_payload

        # Set up the run_forever method to raise a KeyboardInterrupt
        mock_payload.run_forever.side_effect = KeyboardInterrupt

        # Call the run_forever method
        master_piece.run_forever()

        # Verify that the print statement for interruption was called
        mock_print.assert_called_once_with("Application interrupted by user.")

    @patch("builtins.print")  # Patch print to check output
    def test_run_forever_with_specific_error(self, mock_print: Mock) -> None:
        """Test the run_forever method with a specific error."""
        # Create a MasterPiece instance
        master_piece = MasterPiece()

        # Create a mock payload that is a MasterPiece
        mock_payload = Mock(spec=MasterPiece)
        master_piece.payload = mock_payload

        # Set up the run_forever method to raise a ValueError
        mock_payload.run_forever.side_effect = ValueError("Test ValueError")

        # Call the run_forever method
        master_piece.run_forever()

        # Verify that the print statement for the specific error was called
        mock_print.assert_called_once_with("Specific error occurred: Test ValueError")

    @patch("builtins.print")  # Patch print to check output
    def test_run_forever_with_general_exception(self, mock_print: Mock) -> None:
        """Test the run_forever method with a general exception."""
        # Create a MasterPiece instance
        master_piece = MasterPiece()

        # Create a mock payload that is a MasterPiece
        mock_payload = Mock(spec=MasterPiece)
        master_piece.payload = mock_payload

        # Set up the run_forever method to raise a generic exception
        mock_payload.run_forever.side_effect = Exception("Test Exception")

        # Call the run_forever method
        master_piece.run_forever()

        # Verify that the print statement for the general error was called
        mock_print.assert_called_once_with("An error occurred: Test Exception")


if __name__ == "__main__":
    unittest.main()

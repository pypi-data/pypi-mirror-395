"""
Author: Juha Meskanen
Date: 2024-10-26
"""

import os
import logging
import tempfile
import unittest
from logging import FileHandler

from masterpiece.log import Log


class TestLog(unittest.TestCase):
    """Unit tests for Log class."""

    def setUp(self) ->None:
        """Set up the test case, creating a logger instance."""
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.log_name = self.temp_file.name
        self.logger = Log("TestLogger", level=logging.DEBUG)

        # Set up the file handler with the temporary log file
        file_handler = FileHandler(self.log_name)
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)-5.5s]  %(message)-0.280s"
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.temp_file.close()  # Close after setting the file path

    def tearDown(self) ->None:
        """Clean up after each test, removing the log file and handlers."""
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)

        # Ensure the log file is removed if it exists
        if os.path.exists(self.log_name):
            os.remove(self.log_name)

    def test_logger_initialization(self) ->None:
        """Test if the logger is initialized correctly."""
        self.assertEqual(self.logger.name, "TestLogger")
        self.assertEqual(self.logger.level, logging.DEBUG)

    def test_file_handler_creation(self) ->None:
        """Test if the FileHandler is created."""
        file_handler_exists = any(
            isinstance(handler, FileHandler) for handler in self.logger.handlers
        )
        self.assertTrue(file_handler_exists)

    def test_console_handler_creation(self) ->None:
        """Test if the console handler is created."""
        console_handler_exists = any(
            isinstance(handler, logging.StreamHandler)
            for handler in self.logger.handlers
        )
        self.assertTrue(console_handler_exists)

    def test_logging_to_file_and_console(self) ->None:
        """Test logging messages to file and console."""
        self.logger.info("Test log message")

        # Flush the file handler to ensure all messages are written
        for handler in self.logger.handlers:
            if isinstance(handler, FileHandler):
                handler.flush()

        # Check if the message appears in the log file
        self.assertTrue(os.path.exists(self.log_name), "Log file was not created.")

        # Read the log file to verify the message
        with open(self.log_name, "r", encoding="utf-8") as f:
            log_contents = f.read()
            self.assertIn("Test log message", log_contents)

        # Check if the message appears in the console output
        with self.assertLogs(self.logger, level="INFO") as log:
            self.logger.info("Another test log message")
            self.assertIn("INFO:TestLogger:Another test log message", log.output)


if __name__ == "__main__":
    unittest.main()

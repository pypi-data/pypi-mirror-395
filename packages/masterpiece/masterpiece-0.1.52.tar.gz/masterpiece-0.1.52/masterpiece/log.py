"""
Author: Juha Meskanen
Date: 2024-10-26
"""

import logging
import argparse
import sys
from logging.handlers import TimedRotatingFileHandler


class Log(logging.Logger):
    """
    Default `logging.Logger`-based logger implementation for logging events to the MasterPiece
    application log and/or the console.

    TODO: While `logging.Logger` is the de facto logging implementation in Python, many Python components
    have undergone repeated deprecations. As a result, we should not assume that it will remain stable.
    Abstracting the logger API is a simple process that takes just a few minutes. By investing this small
    amount of time, we can shield our application code from potential quirks and deprecations introduced
    by third-party libraries, ensuring greater stability and flexibility in the long run.
    """

    # move these into a abstract base class for loggers
    DEBUG: int = logging.DEBUG
    INFO: int = logging.INFO
    WARNING: int = logging.WARNING
    ERROR: int = logging.ERROR
    CRITICAL: int = logging.CRITICAL

    def __init__(self, name: str, level: int = INFO) -> None:
        """Creates and initializes default logger with the given name and
        logging level. Typically the name is the name of the application.

        Args:
            name: name of the logger
            level: logging level, the default is logging.DEBUG
        """
        super().__init__(name, level)

        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            "-f",
            "--log_name",
            type=str,
            default=name + ".log",
            help="Name of the log file",
        )
        parser.add_argument(
            "-l", "--log_level", type=int, default=logging.DEBUG, help="Logging level"
        )
        args, remaining_argv = parser.parse_known_args()
        sys.argv = [sys.argv[0]] + remaining_argv

        self.setLevel(args.log_level)  # Set the logging level here

        # Create file formatter
        file_formatter = logging.Formatter(
            "%(asctime)s [%(levelname)-5.5s]  %(message)-0.280s"
        )

        # Create a timed rotating file handler
        file_handler = TimedRotatingFileHandler(
            args.log_name, when="midnight", interval=1, backupCount=7
        )
        file_handler.setFormatter(file_formatter)
        self.addHandler(file_handler)

        # Create console formatter
        console_formatter = logging.Formatter("[%(levelname)-5.5s]  %(message)-0.280s")
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        self.addHandler(console_handler)

    def close(self) -> None:
        """Close all handlers to free resources."""
        for handler in self.handlers:
            handler.close()
            self.removeHandler(handler)

    @classmethod
    def parse_level(cls, level: str) -> int:
        """Map the given symbolic log level to log level value.

        Args:
            level (str): DEBUG, WARNING, INFO, ERROR etc.

        Returns:
            int: Log.DEBUG etc.
        """
        if level == "DEBUG":
            return cls.DEBUG
        elif level == "INFO":
            return cls.INFO
        elif level == "WARNING":
            return cls.WARNING
        elif level == "ERROR":
            return cls.ERROR
        else:
            return cls.INFO

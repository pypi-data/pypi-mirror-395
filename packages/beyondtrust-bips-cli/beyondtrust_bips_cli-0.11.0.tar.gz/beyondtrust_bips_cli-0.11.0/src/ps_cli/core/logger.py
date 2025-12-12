import logging
import os
from logging.handlers import RotatingFileHandler

from ps_cli.core.exceptions import InvalidLogLevelException

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


class Logger:
    def __init__(
        self, log_file, max_bytes=10485760, backup_count=5, log_level_str="INFO"
    ):
        """
        Initialize the Logger class.

        Args:
            log_file (str): The path to the log file.
            max_bytes (int, optional): The maximum size of the log file in bytes before
            rolling over. Default is 10MB.
            backup_count (int, optional): The maximum number of backup log files to
            keep. Default is 5.
            log_level_str (str, optional): The logging level. Default is INFO. Possible
            values: CRITICAL, ERROR, WARNING, INFO, DEBUG or NOTSET.
        """
        # If log_file is not provided, use the user's home directory
        if log_file:
            self.log_file = log_file
        else:
            self.log_file = os.path.join(os.path.expanduser("~"), "pscli.log")

        self.max_bytes = max_bytes
        self.backup_count = backup_count

        log_level_str = log_level_str.upper()
        if log_level_str in LOG_LEVELS:
            self.log_level = LOG_LEVELS[log_level_str]
        else:
            raise InvalidLogLevelException(f"Invalid log level: {log_level_str}")

        # Create the log directory if it doesn't exist
        log_dir = os.path.dirname(self.log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Configure the logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.log_level)

        # Create a rotating file handler
        file_handler = RotatingFileHandler(
            self.log_file, maxBytes=self.max_bytes, backupCount=self.backup_count
        )
        file_handler.setLevel(self.log_level)

        # Create a formatter and add it to the file handler
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        self.logger.addHandler(file_handler)

    def debug(self, message):
        """Log a debug message."""
        self.logger.debug(message)

    def info(self, message):
        """Log an info message."""
        self.logger.info(message)

    def warning(self, message):
        """Log a warning message."""
        self.logger.warning(message)

    def error(self, message):
        """Log an error message."""
        self.logger.error(message)

    def critical(self, message):
        """Log a critical message."""
        self.logger.critical(message)

    def log(self, message):
        """Log a message according to the configured level."""
        self.logger.log(self.log_level, message)

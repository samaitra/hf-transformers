"""
Logging utilities for the project.
"""

import logging
import sys
from typing import Optional
from pathlib import Path


class Logger:
    """
    Centralized logging utility for the project.
    
    This class provides a consistent logging interface with configurable
    log levels, formatters, and output destinations.
    """
    
    def __init__(
        self,
        name: str = "app",
        level: int = logging.INFO,
        log_file: Optional[str] = None,
        format_string: Optional[str] = None
    ):
        """
        Initialize the logger.
        
        Args:
            name: Logger name
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional file path for logging output
            format_string: Custom format string for log messages
        """
        self.name = name
        self.level = level
        self.log_file = log_file
        
        # Default format string
        if format_string is None:
            format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        
        self.format_string = format_string
        
        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Create formatter
        formatter = logging.Formatter(format_string)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # File handler (if log_file is specified)
        if log_file:
            self._setup_file_handler(log_file, formatter)
    
    def _setup_file_handler(self, log_file: str, formatter: logging.Formatter) -> None:
        """
        Set up file handler for logging.
        
        Args:
            log_file: Path to the log file
            formatter: Log formatter to use
        """
        # Create log directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(self.level)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
    
    def debug(self, message: str) -> None:
        """Log a debug message."""
        self.logger.debug(message)
    
    def info(self, message: str) -> None:
        """Log an info message."""
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """Log a warning message."""
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """Log an error message."""
        self.logger.error(message)
    
    def critical(self, message: str) -> None:
        """Log a critical message."""
        self.logger.critical(message)
    
    def exception(self, message: str) -> None:
        """Log an exception message with traceback."""
        self.logger.exception(message)
    
    def set_level(self, level: int) -> None:
        """
        Set the logging level.
        
        Args:
            level: New logging level
        """
        self.level = level
        self.logger.setLevel(level)
        for handler in self.logger.handlers:
            handler.setLevel(level)
    
    def add_file_handler(self, log_file: str) -> None:
        """
        Add a file handler to the logger.
        
        Args:
            log_file: Path to the log file
        """
        formatter = logging.Formatter(self.format_string)
        self._setup_file_handler(log_file, formatter)
    
    def get_logger(self) -> logging.Logger:
        """
        Get the underlying logging.Logger instance.
        
        Returns:
            The logging.Logger instance
        """
        return self.logger 
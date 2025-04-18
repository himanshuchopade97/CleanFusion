"""
Logger module for consistent logging across the library.
"""

import logging
import sys
import os
import datetime
from pathlib import Path

class Logger:
    """
    A simple logger class for consistent logging across the library.
    
    Features:
    - Console and file logging
    - Configurable log levels
    - Timestamp formatting
    - Context-aware logging
    """
    
    # Class variable to track instances
    _instances = {}
    _log_dir = Path(os.getcwd()) / "logs"
    
    def __init__(self, name="cleanfusion", level=logging.INFO, log_to_file=True):
        """
        Initialize the logger.
        
        Parameters
        ----------
        name : str, default="cleanfusion"
            The name of the logger.
        
        level : int, default=logging.INFO
            The logging level.
        
        log_to_file : bool, default=True
            Whether to log to a file.
        """
        # Use existing logger if available for the name
        if name in self._instances:
            self.logger = self._instances[name]
            return
            
        # Create new logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Clear existing handlers to avoid duplicates
        if self.logger.hasHandlers():
            self.logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        
        # Add console handler to logger
        self.logger.addHandler(console_handler)
        
        # Add file handler if requested
        if log_to_file:
            self._add_file_handler(name, level, formatter)
        
        # Store instance
        self._instances[name] = self.logger
    
    def _add_file_handler(self, name, level, formatter):
        """Add a file handler to the logger."""
        # Ensure log directory exists
        if not self._log_dir.exists():
            self._log_dir.mkdir(parents=True)
        
        # Create log file with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = self._log_dir / f"{name}_{timestamp}.log"
        
        # Add file handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
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
    
    def exception(self, message):
        """Log an exception message with traceback."""
        self.logger.exception(message)
    
    @classmethod
    def set_log_directory(cls, directory):
        """
        Set the directory for log files.
        
        Parameters
        ----------
        directory : str
            The directory path for log files.
        """
        cls._log_dir = Path(directory)
        if not cls._log_dir.exists():
            cls._log_dir.mkdir(parents=True)
import logging
import os
from datetime import datetime
from pathlib import Path

class Logger:
    """Custom logger for the automation framework"""
    
    @staticmethod
    def setup_logger(name, log_file=None, level=logging.INFO):
        """
        Setup logger with file and console handlers
        Args:
            name (str): Logger name
            log_file (str): Log file path
            level: Logging level
        Returns:
            Logger: Configured logger instance
        """
        # Create logs directory if it doesn't exist
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True)
        
        # Generate log file name if not provided
        if log_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = logs_dir / f"automation_{timestamp}.log"
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # Create file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger
    
    @staticmethod
    def get_logger(name):
        """Get existing logger or create new one"""
        return logging.getLogger(name)
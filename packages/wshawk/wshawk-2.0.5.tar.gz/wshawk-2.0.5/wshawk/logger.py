"""
WSHawk Logging Configuration
Centralized logging for all modules
"""

import logging
import sys
from typing import Optional

# Color codes for terminal output
class LogColors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for terminal output"""
    
    FORMATS = {
        logging.DEBUG: LogColors.CYAN + "%(levelname)s" + LogColors.END + " - %(message)s",
        logging.INFO: LogColors.BLUE + "%(levelname)s" + LogColors.END + " - %(message)s",
        logging.WARNING: LogColors.YELLOW + "%(levelname)s" + LogColors.END + " - %(message)s",
        logging.ERROR: LogColors.RED + "%(levelname)s" + LogColors.END + " - %(message)s",
        logging.CRITICAL: LogColors.RED + LogColors.BOLD + "%(levelname)s" + LogColors.END + " - %(message)s",
    }
    
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def setup_logging(verbose: bool = False, log_file: Optional[str] = None):
    """
    Setup logging configuration
    
    Args:
        verbose: Enable debug logging
        log_file: Optional file path for logging
    """
    level = logging.DEBUG if verbose else logging.INFO
    
    # Root logger
    root_logger = logging.getLogger('wshawk')
    root_logger.setLevel(level)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(ColoredFormatter())
    root_logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        )
        root_logger.addHandler(file_handler)
    
    return root_logger

def get_logger(name: str) -> logging.Logger:
    """Get a logger for a specific module"""
    return logging.getLogger(f'wshawk.{name}')

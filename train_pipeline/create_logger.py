"""
This module provides a utility function for setting up a logger with file handling. 
It creates a log file in a structured directory based on a unique identifier and 
the current date, facilitating organized logging for applications.
"""

import logging
from pathlib import Path
from datetime import datetime

def get_logger(logger_save_ID,logger_name,level=logging.INFO):
    
    """
    Creates and configures a logger with a file handler.

    This function sets up a logger to write logs to a file, organized in a directory structure
    based on a unique identifier and the current date. The log files are stored in a 'logs'
    directory, and the filename includes the identifier and the current date.

    Args:
        logger_save_ID (str): A unique identifier for the logger, used in directory and file naming.
        logger_name (str): The name of the logger.
        level (Optional[logging.Level]): The logging level. Defaults to logging.INFO.

    Returns:
        logging.Logger: A configured Logger object with a file handler.

    Example:
        >>> logger = get_logger("my_app", "app_logger")
        >>> logger.info("This is an info message")
    """
    
    # Configure the directory with logger_save_ID and current year/month
    log_directory = Path('logs') / logger_save_ID/ datetime.now().strftime("%Y-%m")
    # Ensure the directory exists
    log_directory.mkdir(parents=True, exist_ok=True)
    
    # Configure the filename with logger_save_ID and current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    log_filename = f"{logger_save_ID}_{current_date}.log"
    # Full path for the log file
    log_file_path = log_directory / log_filename
    
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    # Create file handler which logs even debug messages
    fh = logging.FileHandler(log_file_path,mode='a')
    fh.setLevel(level)
    # Create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    #to avoid problems with logger names
    logger.propagate=False
    return logger





"""
This module provides functionalities for setting up and configuring loggers with specific naming and directory
structures. It allows for the creation of loggers with filenames that include a unique identifier and the 
current date, organized into directories based on the identifier and the current year and month.
This is particularly useful for maintaining organized logging in applications where log separation based on
time or specific identifiers is necessary.

Functions:
get_logger(logger_save_ID, logger_name, level=logging.INFO): Creates and configures a logger with
a specified name and logging level, saving the log files in a structured directory format.
"""
    
import logging
from pathlib import Path
from datetime import datetime

def get_logger(logger_save_ID,logger_name,level=logging.INFO):
    """
    Create and configure a logger with file handling.

    This function sets up a logger to write logs to a file, organized by date and logger ID.
    The log directory and file are created if they don't exist. If the logger with the specified name 
    already exists, it returns the existing logger without creating duplicate handlers.

    Args:
        logger_save_ID (str): Identifier for the logger, used in naming log files.
        logger_name (str): Name of the logger.
        level (int, optional): Logging level. Defaults to logging.INFO.

    Returns:
        logging.Logger: Configured logger with a file handler.

    Raises:
        Exception: If there is an error in setting up the logger, an exception is raised with the error message.       
    """
    
    try:
        # Configure the directory with logger_save_ID and current year/month
        log_directory = Path('logs') / logger_save_ID/ datetime.now().strftime("%Y-%m")
        # Ensure the directory exists
        log_directory.mkdir(parents=True, exist_ok=True)
    
        # Configure the filename with logger_save_ID and current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_filename = f"{logger_save_ID}_{current_date}.log"
        log_file_path = log_directory / log_filename
    
        logger = logging.getLogger(logger_name)
    
        # Check if the logger already has handlers to avoid duplicate entries
        if not logger.handlers:
            logger.setLevel(level)
            # Create file handler which logs even debug messages
            fh = logging.FileHandler(log_file_path,mode='a')
            fh.setLevel(level)
            # Create formatter and add it to the handlers
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            logger.addHandler(fh)
            logger.propagate=False
            
    except Exception as e:
        raise Exception(f"Error setting up logger {logger_name}: {e}")
        
    return logger

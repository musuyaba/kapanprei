import logging
import os
from datetime import datetime

def setup_logging(log_directory):
    """
    Sets up logging configuration.
    """
    current_date = datetime.now().strftime('%Y-%m-%d')
    os.makedirs(log_directory, exist_ok=True)
    log_filename = f'{log_directory}/{current_date}.log'

    # Create a custom logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Create handlers
    file_handler = logging.FileHandler(log_filename)
    console_handler = logging.StreamHandler()

    # Set levels
    file_handler.setLevel(logging.INFO)
    console_handler.setLevel(logging.DEBUG)

    # Create formatters and add them to handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
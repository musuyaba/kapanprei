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

    logging.basicConfig(filename=log_filename,
                        level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    return logging

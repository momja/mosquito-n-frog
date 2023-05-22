"""
Logging utility for saving log data to a .log file or outputting to terminal

"""

import logging
import platform

system = platform.system()

if system == 'Windows':
    _log_filename = 'C:\\Logs\\myapp.log'  # Windows path
else:
    _log_filename = '/var/log/mosquito.log'

logger = logging.getLogger('myapp')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(_log_filename)
file_handler.setLevel(logging.DEBUG)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Add the formatter to the file handler
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

def log_message(message: any):
    logger.info(message)

def log_warning(message: any):
    logger.error(message)

def log_error(message: any, log_exception: bool):
    logger.warning(message, exc_info=log_exception)
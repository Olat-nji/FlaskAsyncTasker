# Import necessary modules for date/time handling, environment variables, and file operations
from datetime import datetime
import pytz
from dotenv import load_dotenv
import os

# Log file path configuration
LOG_FILE_PATH = os.getenv('LOG_FILE_PATH')

# Load environment variables from .env file (assumes it is in the same directory)
load_dotenv()

def log_time():
    """
    Logs the current UTC time to a specified log file.

    Returns:
    - str: Confirmation message with the logged time.
    """
    # Get the current UTC time formatted as string
    now = datetime.now(pytz.utc).strftime('%Y-%m-%d %H:%M:%S %Z%z')

    # Write the formatted time to the log file
    with open(LOG_FILE_PATH, 'a') as f:
        f.write(f'{now}\n')

    # Return confirmation message
    return f'Logged time: {now}'

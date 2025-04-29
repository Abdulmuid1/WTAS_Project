from datetime import datetime, timedelta # Get current time
import logging
from app.utilities.helper import current_delays

# Configure logging
logging.basicConfig(
    filename="delay_log.txt",  # log will be saved in this file
    level=logging.INFO,        # only logs INFO and above
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_current_delays():
    """
    Return the current list of simulated transit delays.
    Each delay is represented as a DelayInfo object.
    """
    
    return current_delays


def check_delay(info, threshold=5):
    '''
    Check if the delay stored in the DelayInfo object exceeds the threshold.
    
    Parameters:
    - info (DelayInfo): An instance of DelayInfo containing delay data.
    - threshold (int): The delay time (in minutes)
    
    Returns:
    - dict: A dictionary showing delay status and how many minutes late
    '''
    
    if info._delay_minutes > threshold:
        logging.info(f"Delay detected for route {info._route}: {info._delay_minutes} minutes")
        return {
            "status": "delayed",
            "minutes_late": int(info._delay_minutes)
        }
    else:
        return {
            "status": "on time",
            "minutes_late": 0
        }
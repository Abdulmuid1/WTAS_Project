import logging
from app.models.transit import *
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
    result = []  # Create an empty list to hold the delay dictionaries
    for delay in current_delays:  # Loop through each actual delay
        result.append(delay.to_dict())  # Convert to dict and add to result
    return result

def check_delay(info, threshold=5):
    """
    Check if the delay stored in the DelayInfo object exceeds the threshold.
    
    Parameters:
    - info (DelayInfo): An instance of DelayInfo containing delay data.
    - threshold (int): The delay time (in minutes)
    
    Returns:
    - dict: A dictionary showing delay status and how many minutes late
    """
     
    if int(info["Delay time"]) > threshold:   
        logging.info(f"Delay detected for route {info['Route']}: {info['Delay time']} minutes")
        return {
            "status": "delayed",
            "minutes_late": int(info["Delay time"]) 
        }
    else:
        return {
            "status": "on time",
            "minutes_late": 0
        }
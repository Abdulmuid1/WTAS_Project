import random # Import random to simulate random delays
from datetime import datetime, timedelta # Get current time

import logging

# Configure logging
logging.basicConfig(
    filename="delay_log.txt",  # log will be saved in this file
    level=logging.INFO,        # only logs INFO and above
    format="%(asctime)s - %(levelname)s - %(message)s"
)



class DelayInfo():
    """
    A class to organize delay-related information in one object.
    """
    def __init__(self, route, station, reason, expected_arrival, delay_minutes):
        self._route = route
        self._station = station                
        self._reason = reason                  
        self._expected_arrival = expected_arrival 
        self._delay_minutes = delay_minutes
    
    def to_dict(self):
        """
        Converts the object's attributes into a dictionary
        """
        result = {}
        result["route"] = self._route
        result["station"] = self._station
        result["reason"] = self._reason
        result["expected_arrival"] = self._expected_arrival
        result["delay_minutes"] = self._delay_minutes
        return result




def get_current_delays():
    """
    Return a list of current mocked transit delays.
    Each delay is represented as a DelayInfo object.
    """
    # Get the current time
    current_time = datetime.now() 

    # Create a list of DelayInfo objects, with each representing a delay
    delays = [
        DelayInfo(
            route="Bus 12",
            station="Southgate",
            reason="Heavy snow",
            expected_arrival=(current_time + timedelta(minutes=5)).strftime("%H:%M"),
            delay_minutes=5
        ),
        DelayInfo(
            route="Train 4",
            station="University",
            reason="Signal issues",
            expected_arrival=(current_time + timedelta(minutes=12)).strftime("%H:%M"),
            delay_minutes=12
        ),
        DelayInfo(
            route="Bus 8",
            station="NAIT",
            reason="Mechanical issue",
            expected_arrival=(current_time + timedelta(minutes=8)).strftime("%H:%M"),
            delay_minutes=8
        )
    ]
    return delays 

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
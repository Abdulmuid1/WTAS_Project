import random # Import random to simulate random delays
from datetime import datetime # Get current time


class DelayInfo():
    '''
    A class to organize delay-related information in one object.
    '''
    def __init__(self, route, station, reason, expected_arrival, delay_minutes):
        self._route = route
        self._station = station                
        self._reason = reason                  
        self._expected_arrival = expected_arrival 
        self._delay_minutes = delay_minutes
    
    def to_dict(self):
        '''
        Converts the object's attributes into a dictionary
        '''
        result = {}
        result["route"] = self._route
        result["station"] = self._station
        result["reason"] = self._reason
        result["expected_arrival"] = self._expected_arrival
        result["delay_minutes"] = self._delay_minutes
        return result




def get_current_delays():
    """
    Simulates fetching real-time delay data.
    """
    # Simulate a delay happening randomly
    is_delayed = random.choice([True, False])
  
    if is_delayed: # If there's a delay
        # Simulate random delay information
        # Hardcoded data just for testing
        route = "Bus 12"
        station = "Southgate"
        reason = "Heavy snow"
        # Get the current time formatting it to show only hour and minute.
        current_time = datetime.now().replace(second=0, microsecond=0)
        expected_time = current_time.strftime("%H:%M")

        # Randomly choose how long the bus is delayed.
        delay_minutes = random.choice([5, 10, 15])

        # Create a DelayInfo object with this data
        delay_info = DelayInfo(route, station, reason, expected_time, delay_minutes)
        delay_dict = delay_info.to_dict()

    else: # If there's no delay, return none
        delay_dict = None    

    # Return as a dictionary structure so FastAPI can convert it to JSON
    return {
        "status": "ok", # status to tell us everything worked
        "data": delay_dict # data holds the delay info or None
    }    
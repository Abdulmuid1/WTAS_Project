

class DelayInfo():
    """
    A class to organize delay-related information in one object.
    """
    def __init__(self, route, station, reason, scheduled_arrival, delay_minutes, expected_arrival):
        self._route = route
        self._station = station                
        self._reason = reason         
        self._scheduled_arrival = scheduled_arrival         
        self._expected_arrival = expected_arrival 
        self._delay_minutes = delay_minutes
    
    def to_dict(self):
        """
        Converts the object's attributes into a dictionary
        """
        result = {}
        result["Route"] = self._route
        result["Destination"] = self._station
        result["Reason"] = self._reason
        result["Scheduled arrival"] = self._scheduled_arrival
        result["Delay time"] = self._delay_minutes
        result["Expected arrival"] = self._expected_arrival
        return result



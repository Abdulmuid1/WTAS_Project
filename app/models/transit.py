

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



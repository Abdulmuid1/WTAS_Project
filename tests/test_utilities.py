import unittest

from fastapi.testclient import TestClient
from app.main import app
from app.services.alerts import * 

# Create a client to simulate API requests
client = TestClient(app)

class TestRootEndpoint(unittest.TestCase):
    def test_root_status_code(self):
        # Make a GET request to "/"
        response = client.get("/")
        # Check if status code is 200
        self.assertEqual(response.status_code, 200)

    def test_root_response_message(self):
        # Make a GET request to "/"
        response = client.get("/")
        # Check if the message in the response is correct
        self.assertEqual(response.json(), {"message": "Welcome to the Winter Transit Alert System"})

    def test_delay_below_threshold(self):
        '''
        Test case where delay is acceptable
        '''
        info = DelayInfo("Bus 1", "Downtown", "Traffic", "08:10", 5)
        result = check_delay(info)  
        expected = {
            "status": "on time",
            "minutes_late": 0
        }
        self.assertEqual(result, expected)

    def test_delay_above_threshold(self):
        '''
        Test case where delay is above 10 minutes threshold
        '''
        info = DelayInfo("Bus 2", "Southside", "Snow", "08:30", 15)
        result = check_delay(info, threshold=10)  
        expected = {
            "status": "delayed",
            "minutes_late": 15
        }
        self.assertEqual(result, expected)    
        


if __name__ == "__main__":
    unittest.main()


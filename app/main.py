# Import FastAPI to buid the web API
from fastapi import FastAPI
# Import the function checking for delays
from app.services.alerts import *

# Create a FastAPI app object
app = FastAPI()

# Define a route the browser can visit to get the delay info
@app.get("/delays")
def get_delay_info():
    """
    Endpoint for retrieving simulated delay information.
    Returns: dict-> Contains the status and simulated delay data.
    """
    return get_current_delays()


@app.get("/")
def read_root():
    # This route handles the default home URL and returns a welcome message
    return {"message": "Welcome to the Winter Transit Alert System"}

@app.get("/delays")
def get_mocked_delays():
    """
    Endpoint to return a list of mocked transit delays.
    """
    # Create sample DelayInfo objects (you can later replace this with real data logic)
    delay1 = DelayInfo("Route 15", "Southgate Station", "Heavy snow", "08:30", 12)
    delay2 = DelayInfo("Route 30", "Century Park", "Mechanical issue", "09:15", 8)

    # Convert DelayInfo objects to dictionary format
    delay_list = [delay1.to_dict(), delay2.to_dict()]

    return {
        "status": "ok",
        "data": delay_list
    }
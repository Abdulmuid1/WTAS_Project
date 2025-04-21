# Import FastAPI to buid the web API
from fastapi import FastAPI
# Import the function checking for delays
from app.services.alerts import get_current_delays

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
    return f"Welcome to the WTAS Project API!"

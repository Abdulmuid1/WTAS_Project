# Import FastAPI to buid the web API
from fastapi import FastAPI
# Import the function checking for delays
from app.services.alerts import get_current_delays
from app.api import routes
from dotenv import load_dotenv
import os

import logging

load_dotenv() 
# Set default port to 8000
port = int(os.getenv("PORT", 8000))

# Create a FastAPI app object
app = FastAPI()

app.include_router(routes.router)


@app.get("/")
def read_root():
    # This route handles the default home URL and returns a welcome message
    return {"message": "Welcome to the Winter Transit Alert System"}

# Define a route the browser can visit to get the delay info
@app.get("/delays")
def get_delay_info():
    """
    Endpoint for retrieving simulated delay information.
    Returns: dict-> Contains the status and simulated delay data.
    """
    return {
        "status": "ok",
        "data": get_current_delays()
    }

@app.post("/sms")
def send_sms():
    delays = get_current_delays()
    for delay in delays:
        logging.info(f"Sending SMS: Delay on {delay._route} at {delay._station}: {delay._delay_minutes} minutes late")
    return {"message": "SMS alerts sent successfully"}    

@app.post("/speaker")
def speaker_announcement():
    delays = get_current_delays()
    for delay in delays:
        logging.info(f"Speaker Announcement: Attention! {delay._route} is delayed at {delay._station} by {delay._delay_minutes} minutes due to {delay._reason}.")
    return {"message": "Speaker announcements triggered successfully."}

# Temporary function to test .env setup
# @app.get("/env-check")
# def read_env():
#     port = os.getenv("PORT", "Not found")
#     return {"PORT": port}

# This is a temporary function to test mocked delay data
# @app.get("/delays")
# def get_mocked_delays():
#     """
#     Endpoint to return a list of mocked transit delays.
#     """
#     # Create sample DelayInfo objects (you can later replace this with real data logic)
#     delay1 = DelayInfo("Route 15", "Southgate Station", "Heavy snow", "08:30", 12)
#     delay2 = DelayInfo("Route 30", "Century Park", "Mechanical issue", "09:15", 8)

#     # Convert DelayInfo objects to dictionary format
#     delay_list = [delay1.to_dict(), delay2.to_dict()]

#     return {
#         "status": "ok",
#         "data": delay_list
#     }


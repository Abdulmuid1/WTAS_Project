# Import FastAPI to buid the web API
from fastapi import FastAPI, Response
# Import the function checking for delays
from fastapi.staticfiles import StaticFiles
from app.services.alerts import get_current_delays, check_delay
from app.api import routes
from app.core.config import settings
from app.utilities.helper import update_delays_periodically
import threading # Make infinite background tasks run in a seperate thread
import logging
from contextlib import asynccontextmanager  
from fastapi.middleware.cors import CORSMiddleware
import os

# Define the lifespan function for the background updater 
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event to start background updater when app launches.
    """
    updater_thread = threading.Thread(target=update_delays_periodically, args=(), daemon=True)
    updater_thread.start()
    yield  # Keeps the app running after startup


# Create a FastAPI app object
app = FastAPI(lifespan=lifespan) 

# CORS middleware to allow requests from your frontend domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the router at /api
app.include_router(routes.router, prefix="/api")

# Get the port from the environment settings
port = settings.PORT

# Mount static files under a dedicated subpath "/static"
app.mount("/static", StaticFiles(directory="client/build/static"), name="static")

# To support client side routing in a single-page application, serve index.html at "/"
@app.get("/")
async def serve_index():
    with open(os.path.join("client", "build", "index.html"), "r") as f:
        return Response(content=f.read(), media_type="text/html")


@app.get("/health") # Health check route to help ALB validate the service
def health_check():
    """
    Health check endpoint
    """
    return {"status": "ok"}

@app.get("/api/delays") # Route to get the real-time delay info
def get_delay_info():
    """
    Endpoint for retrieving simulated delay information.
    Returns: dict-> Contains the status and simulated delay data.
    """
    return {
        "status": "ok",
        "data": get_current_delays()
    }

@app.post("/api/sms") # Route to simulate sending SMS alerts
def send_sms():
    """
    Endpoint for simulating sending SMS alerts about delays
    """
    delays = get_current_delays()
    delay_list = []
    for delay in delays:
        delay_status = check_delay(delay)
        if delay_status["status"] == "delayed":
            message = {
                f"{delay['Route']} to {delay['Destination']} encountered an unexpected delay, "
                f"and will be {delay['Delay time']} minutes late. Scheduled arrival time: {delay['Scheduled arrival']}, "
                f"New arrival time: {delay['Expected arrival']}. "
                f"We apologize for any inconvenience caused."
            }
            delay_list.append({"type": "SMS", "message": message})
            logging.info(f"Sending SMS: {message}")
    return {"data": delay_list}  

@app.post("/api/speaker") # Route to simulate speaker announcements
def speaker_announcement():
    """
    Endpoint for simulating speaker announcements about delays
    """
    delays = get_current_delays()
    delay_list = []
    for delay in delays:
        delay_status = check_delay(delay)
        if delay_status["status"] == "delayed":
            message = {
                f"Attention! {delay['Route']} to {delay['Destination']} is delayed by "
                f"{delay['Delay time']} minutes due to {delay['Reason']}. "
                f"Scheduled arrival time: {delay['Scheduled arrival']}, New arrival time: {delay['Expected arrival']}. "
                f"We apologize for any inconvenience caused."
            }
            delay_list.append({"type": "Speaker", "message": message})
            logging.info(f"Speaker Announcement: {message}")
    return {"data": delay_list}

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
#     # Create sample DelayInfo objects
#     delay1 = DelayInfo("Route 15", "Southgate Station", "Heavy snow", "08:30", 12)
#     delay2 = DelayInfo("Route 30", "Century Park", "Mechanical issue", "09:15", 8)

#     # Convert DelayInfo objects to dictionary format
#     delay_list = [delay1.to_dict(), delay2.to_dict()]

#     return {
#         "status": "ok",
#         "data": delay_list
#     }


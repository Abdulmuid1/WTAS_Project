import time
from datetime import datetime, timedelta
import random
from app.models.transit import DelayInfo

# Global list that holds the current delays
current_delays = []

def load_routes():
    """
    Load all bus and train routes from routes.txt file
    """
    try:
        routes = [] # Create an empty list for routes
        with open("app/api/routes.txt", "r") as file:
            for line in file:
                line = line.strip()
                if line != "": # If the line isn't empty, append to routes list
                    routes.append(line)
        return routes
    except FileNotFoundError:
        return []


def extract_stations(routes):
    """
    Extract station names from routes.txt and return them paired with their full route line.
    Returns: 
        A list of tuples where each tuple contains:
        - the full route string (e.g., "Bus 53 Mill Woods")
        - the extracted station name (e.g., "Mill Woods")
    """
    paired_data = []  # Will hold tuples of (route, station)
    index = 0
    while index < len(routes): # Loop through all the routes
        route = routes[index]  # Get the current route line as a string
        parts = route.strip().split()  # Split the route into separate words

        if not parts:
             # If the route line is empty, skip it and go to the next one
            index += 1
            continue

        # If the route is a Bus and has enough words
        if parts[0] == "Bus" and len(parts) >= 3:
            station = parts[2] # Start with the third word as the station
            word_index = 3
            while word_index < len(parts): # Add any remaining words to the station
                station = station + " " + parts[word_index] 
                word_index += 1
            paired_data.append((route, station)) # Save the route and station as a tuple

        # If the route is a Train and has enough words
        elif parts[0] == "Train" and len(parts) >= 4:
            station = parts[3] # Start with the fourth word as station
            word_index = 4
            while word_index < len(parts): # Add any remaining words to the station
                station = station + " " + parts[word_index]
                word_index += 1
            paired_data.append((route, station)) # Save the route and station as a tuple

        index += 1 # Move to the next route in the list

    return paired_data # Return the final list of (route, station) pairs

def update_delays_periodically(refresh_interval=60):
    """
    Update the current_delays list every 'refresh_interval' seconds
    by simulating random delays for random routes.

    Note: This loop is intentionally infinite to simulate real-time updates
    during the lifetime of the application.
    """
    possible_routes = load_routes()
    route_station_pairs = extract_stations(possible_routes)
    # Possible delay reasons for buses
    bus_reasons = ["a heavy snow", "a mechanical issue", "a traffic jam", "an emergency maintenance"]
    # Possible delay reasons for trains
    train_reasons = ["a signal failure", "a track obstruction", "a power outage", "an emergency maintenance", "some frozen switches"]

    # Use an infinite loop that runs forever to simulate live real-time updates
    while True:

       # This is for debugging
       # print("Updating delays...")  

        current_delays.clear() # Clear out old delays prior to updating delays

        if not route_station_pairs:
            print("No routes available")
            time.sleep(refresh_interval)
            continue

        # Pick 3-5 random delays each cycle
        for _ in range(random.randint(3, 5)):
            selected = random.choice(route_station_pairs)
            route = selected[0]
            station = selected[1]

            # Determine if the selected route is a bus or train route to simulate specific delays
            if route.startswith("Bus"):
                reason = random.choice(bus_reasons)
            else:
                reason = random.choice(train_reasons)
                

            # Simulate a scheduled arrival time between 5 and 30 minutes from now
            scheduled_arrival_time = datetime.now() + timedelta(minutes=random.randint(5, 30)) 
            # Convert to readable format (e.g., "12:40")
            scheduled_arrival = scheduled_arrival_time.strftime("%H:%M")

            delay_minutes = random.randint(5, 20) # Simulate a delay between 5 and 20 minutes

            # Calculate the new expected arrival time after applying the delay
            expected_arrival_time = scheduled_arrival_time + timedelta(minutes=delay_minutes)
            expected_arrival = expected_arrival_time.strftime("%H:%M")

            # Create a DelayInfo object with all the simulated data
            delay = DelayInfo(route, station, reason, scheduled_arrival, delay_minutes, expected_arrival)

            current_delays.append(delay) # Append delay info to the list

            # This print statement is for debugging
            # print(f"{delay._route} to {delay._station} delayed by {delay._delay_minutes} minutes")


        time.sleep(refresh_interval) # Update delays

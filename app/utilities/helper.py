import time
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
    Extract station names from the routes.txt.
    """
    stations = [] # Create an empty list for stations
    for route in routes: # Loop over each line extracted from routes.txt
        parts = route.strip().split()
        if not parts:
            continue

        if parts[0] == "Bus" and len(parts) >= 3: # Extract the station name
            station = parts[2]
            for word in parts[3:]:
                station = station + " " + word
            stations.append(station)

        elif parts[0] == "Train" and len(parts) >= 4: #Extract the station name
            station = parts[3]
            for word in parts[4:]:
                station = station + " " + word
            stations.append(station) # Append extracted station names to stations list

    return stations

def update_delays_periodically(refresh_interval=60):
    """
    Update the current_delays list every 'refresh_interval' seconds
    by simulating random delays for random routes.

    Note: This loop is intentionally infinite to simulate real-time updates
    during the lifetime of the application.
    """
    possible_routes = load_routes()
    possible_stations = extract_stations(possible_routes)
    possible_reasons = ["Heavy snow", "Mechanical issue", "Traffic jam", "Signal failure", "Emergency maintenance"]

    # Use an infinite loop that runs forever to simulate live real-time updates
    while True:
        current_delays.clear() # Clear out old delays prior to updating delays

        if not possible_routes:
            print("No routes available")
            time.sleep(refresh_interval)
            continue

        # Pick 3-5 random delays each cycle
        for _ in range(random.randint(3, 5)):
            route = random.choice(possible_routes)
            station = random.choice(possible_stations)
            reason = random.choice(possible_reasons)
            expected_arrival = time.strftime("%H:%M")
            delay_minutes = random.randint(5, 20)

            delay = DelayInfo(route, station, reason, expected_arrival, delay_minutes)
            current_delays.append(delay) # Append delay info to the list

        time.sleep(refresh_interval) # Update delays

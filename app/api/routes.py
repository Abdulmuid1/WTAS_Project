from fastapi import APIRouter
from app.services.alerts import get_current_delays

router = APIRouter()

@router.get("/delays")
def read_delays():
    """
    API endpoint to return all current delays as a list of dictionaries. 
    """
    delays = get_current_delays() # list of DelayInfo objects
    data = []

    for delay in delays:
        data.append(delay) # Append it to the list

    return {
        "status": "ok", # Let API caller know it worked
        "data": data # The delay info
    }    
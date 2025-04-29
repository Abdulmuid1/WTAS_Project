import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Settings:
    APP_NAME = "Winter Transit Alert System"
    REFRESH_INTERVAL_SECONDS = int(os.getenv("REFRESH_INTERVAL_SECONDS", 60))  # how often to update delay data
    PORT = int(os.getenv("PORT", 8000)) # Set default port to 8000
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

settings = Settings()
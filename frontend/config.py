import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")
if not API_URL:
    raise ValueError("API_URL environment variable is not set. Please configure it in .env file.")

STREAMLIT_DEBUG = os.getenv("STREAMLIT_DEBUG", "false").lower() == "true"
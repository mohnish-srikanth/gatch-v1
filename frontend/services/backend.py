import requests

# CONFIG
BACKEND_URL = "http://backend:8000"

def get_insights():
    r = requests.get(f"{BACKEND_URL}/insights", timeout = 10)
    r.raise_for_status()
    return r.json().get("data")

def refresh_data():
    r = requests.get(f"{BACKEND_URL}/refresh", timeout = 120)
    r.raise_for_status()
import requests

BASE_URL = "https://www.thesportsdb.com/api/v1/json"

def get_pl_standings(api_key = "123"):
    url = f"{BASE_URL}/{api_key}/lookuptable.php?l=4328&s=2024-2025"
    return requests.get(url).json()

def get_pl_fixtures(api_key = "123"):
    url = f"{BASE_URL}/{api_key}/eventsnextleague.php?id=4328"
    return requests.get(url).json()

from datetime import datetime, timezone

CACHE = {
    "data": None,
    "updated_at": None
}

def save(data):
    CACHE["data"] = data
    CACHE["updated_at"] = datetime.now(timezone.utc)

def get():
    return CACHE
import os
from dotenv import load_dotenv

load_dotenv()

SPORTSDB_API_KEY = os.getenv("SPORTSDB_API_KEY", "1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

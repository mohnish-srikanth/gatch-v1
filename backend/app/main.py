from fastapi import FastAPI
from app.services.sportsdb import get_pl_standings, get_pl_fixtures
from app.insights import build_prompt
from app.openai_client import generate_insight
from app.store import save, get
from app.config import SPORTSDB_API_KEY

app = FastAPI(title = "Gatch API")

@app.post("/refresh")
def refresh():
    standings = get_pl_standings(SPORTSDB_API_KEY)
    fixtures = get_pl_fixtures(SPORTSDB_API_KEY)

    prompt = build_prompt(standings, fixtures)
    insight = generate_insight(prompt)

    save({
        "standings": standings,
        "fixtures": fixtures,
        "insight": insight
    })

    return {"status": "updated"}

@app.get("/insights")
def insights():
    return get()
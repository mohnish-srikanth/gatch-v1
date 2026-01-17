def build_prompt(standings, fixtures):
    return f"""
    You are a football analyst.
    Standings:
    {standings}
    Upcoming fixtures:
    {fixtures}
    Give 3 concise insights about:
    - Title race
    - Top 4 battle
    - Relagation risk
    """

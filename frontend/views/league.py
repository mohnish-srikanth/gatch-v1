import streamlit as st
import pandas as pd
import requests
from services.backend import get_insights, refresh_data

def render_league():
    # CONFIG
    BACKEND_URL = "http://backend:8000"

    st.set_page_config(
        page_title="Gatch ⚽",
        layout="wide"
    )


    # PREMIUM STYLES
    st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 2.5rem;
        max-width: 1200px;
    }

    .section-card {
        background-color: #111827;
        padding: 1.6rem 1.8rem;
        border-radius: 18px;
        margin-bottom: 1.8rem;
    }

    .insight-box {
        background: linear-gradient(135deg, #1f2937, #020617);
        padding: 2.2rem;
        border-radius: 22px;
        font-size: 1.05rem;
        line-height: 1.7;
    }

    .muted {
        color: #9ca3af;
        font-size: 0.9rem;
    }

    hr {
        border: none;
        height: 1px;
        background-color: #1f2937;
        margin: 2.2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)


    # HEADER
    left, right = st.columns([3, 1])

    with left:
        st.markdown("## ⚽ Gatch")
        st.markdown(
            "<p class='muted'>AI-powered Premier League insights</p>",
            unsafe_allow_html=True
        )

    with right:
        st.markdown("<div style='margin-top: 1.6rem'></div>", unsafe_allow_html=True)
        if st.button("🔄 Refresh Data"):
            with st.spinner("Fetching data & generating AI insights..."):
                try:
                    r = requests.post(f"{BACKEND_URL}/refresh", timeout=120)
                    if r.status_code == 200:
                        st.success("Data refreshed successfully!")
                    else:
                        st.error("Failed to refresh data")
                except Exception:
                    st.error("Backend not reachable")

    st.markdown("<hr/>", unsafe_allow_html=True)


    # FETCH DATA (SAFE)
    try:
        response = requests.get(f"{BACKEND_URL}/insights", timeout=10)
        response.raise_for_status()
        payload = response.json()
        data = payload.get("data")

        if not data:
            st.info("No data yet. Click **Refresh Data** to generate insights.")
            st.stop()

    except Exception:
        st.error("Backend not available yet. Please wait a few seconds.")
        st.stop()


    # AI INSIGHTS (HERO SECTION)
    st.markdown("### 🧠 This Week’s AI Insight")

    st.markdown(
        f"""
        <div class="insight-box">
            {data.get("insight", "No insight available")}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<hr/>", unsafe_allow_html=True)


    # STANDINGS
    st.markdown("### 🏆 League Standings")
    st.markdown(
        "<p class='muted'>Current Premier League table</p>",
        unsafe_allow_html=True
    )

    standings_raw = data.get("standings", {}).get("table", [])

    if not standings_raw:
        st.info("Standings not available")
        st.stop()

    COLUMN_MAP = {
        "idTeam": "idTeam",
        "intRank": "Rank",
        "strTeam": "Team",
        "intPlayed": "Played",
        "intWin": "Wins",
        "intDraw": "Draws",
        "intLoss": "Losses",
        "intGoalsFor": "Goals For",
        "intGoalsAgainst": "Goals Against",
        "intGoalDifference": "Goal Difference",
        "intPoints": "Points",
        "strForm": "Form",
    }

    rows = []
    for team in standings_raw:
        row = {new: team.get(old) for old, new in COLUMN_MAP.items()}
        row["Badge"] = team.get("strBadge")
        rows.append(row)

    df = pd.DataFrame(rows)

    numeric_cols = [
        "Rank", "Played", "Wins", "Draws",
        "Losses", "Goals For", "Goals Against",
        "Goal Difference", "Points"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.sort_values("Rank")

    # Header row
    header = st.columns([1, 4, 1, 1, 1, 1, 1, 2])
    header[0].markdown("**Logo**")
    header[1].markdown("**Team**")
    header[2].markdown("**Wins**")
    header[3].markdown("**Losses**")
    header[4].markdown("**Draws**")
    header[5].markdown("**Pts**")
    header[6].markdown("**GD**")
    header[7].markdown("**Form**")

    for _, row in df.iterrows():
        cols = st.columns([1, 4, 1, 1, 1, 1, 1, 2])

        with cols[0]:
            st.image(row["Badge"], width=38)

        with cols[1]:
            if st.button(
                row["Team"],
                key=f"team_{row['idTeam']}",
                help="View team details",
                use_container_width=True
            ):
                st.session_state.selected_team = {
                    "id": row["idTeam"],
                    "name": row["Team"]
                }
                st.rerun()

        with cols[2]:
            st.write(row["Wins"])

        with cols[3]:
            st.write(row["Losses"])

        with cols[4]:
            st.write(row["Draws"])

        with cols[5]:
            st.write(row["Points"])

        with cols[6]:
            st.write(row["Goal Difference"])

        with cols[7]:
            st.write(row["Form"])

    st.markdown("<hr/>", unsafe_allow_html=True)


    # FIXTURES
    st.markdown("### 📅 Upcoming Fixtures")
    st.markdown(
        "<p class='muted'>Next scheduled matches</p>",
        unsafe_allow_html=True
    )

    fixtures = data.get("fixtures", {}).get("events", [])

    if fixtures:
        for f in fixtures:
            st.markdown(
                f"""
                <div class="section-card">
                    <h4>{f['strHomeTeam']} vs {f['strAwayTeam']}</h4>
                    <p class="muted">
                        🗓 {f['dateEvent']} · ⏰ {f['strTime']} · 📍 {f['strVenue']}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("No fixtures available")


    # FOOTER
    st.markdown(
        "<p class='muted'>Powered by live Premier League data & AI analysis</p>",
        unsafe_allow_html=True
    )

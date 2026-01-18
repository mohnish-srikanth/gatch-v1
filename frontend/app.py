import streamlit as st
from views.league import render_league
from views.team import render_team

st.set_page_config(page_title = "Gatch", layout = "wide")

if "selected_team" not in st.session_state:
    st.session_state.selected_team = None

if st.session_state.selected_team is None:
    render_league()
else:
    render_team(st.session_state.selected_team)
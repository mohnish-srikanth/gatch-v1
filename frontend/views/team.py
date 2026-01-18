import streamlit as st

def render_team(team):
    if st.button("<- Back to League"):
        st.session_state.selected_team = None
        st.rerun()
    
    st.markdown(f"## {team['name']}")
    st.info("Team detail page coming next")
import streamlit as st

from utils import connect_to_db


def show_progress():
    progress_collection = st.session_state.db.progress
    st.markdown("**Progress**")

def add_progress():
    st.markdown("**Add progress**")
    progress_collection = st.session_state.db.progress
    injuries = progress_collection.distinct("injury")
    injuries.insert(0, "Add new")
    injury_selection = st.selectbox('Which injury do you want to add progress to?',injuries)
    if injury_selection == "Add new":
        injury = st.text_input("Please name your injury")
    else:
        injury = injury_selection

    date = st.date_input("For which date do you want to add progress?")
    pain = st.slider("On a scale from 1-10, how good does your injury feel?", min_value=1, max_value=10)    
    yesterday = st.text_input("What did you do yesterday?")
    today = st.text_input("What did you do today?")
    



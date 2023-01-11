from typing import Dict
import streamlit as st
from bson import ObjectId
from utils import connect_to_db 
from login import check_password

def add_progress(user: ObjectId) -> None:
    st.markdown("**Add progress**")
    st.sidebar.markdown("# Add progress ❄️")

    db = connect_to_db()
    collection = db.pain_tracker.progress
    injuries = collection.distinct("injury")
    injuries.insert(0, "Add new")
    injury_selection = st.selectbox('Which injury do you want to add progress to?',injuries)
    if injury_selection == "Add new":
        injury = st.text_input("Please name your injury")
    else:
        injury = injury_selection

    date = st.date_input("For which date do you want to add progress?")
    status = st.slider("On a scale from 1-10, how bad does your injury feel?", min_value=1, max_value=10)    
    yesterday = st.text_input("What did you do yesterday?")
    today = st.text_input("What did you do today?")
    doc = {
        "user": user,
        "injury": injury,
        "date": date.strftime("%Y-%m-%d"),
        "status": status,
        "activity_yesterday": yesterday,
        "activity_today": today
    }
    insert_document = st.button("Add progress")
    if insert_document:
        result = collection.insert_one(doc)
        if result.acknowledged:
            st.success("Successfully added information to your progress!")
        
if __name__ == "__main__":
    user = check_password()
    if user: 
        add_progress(user)

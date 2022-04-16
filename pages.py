from datetime import datetime
import streamlit as st
import plotly.express as px

from utils import connect_to_db, get_aggregated_progress


def show_progress():
    progress_collection = st.session_state.db.progress
    st.markdown("**Progress**")
    base_query = {"user": st.session_state.user["_id"]}
    injuries = progress_collection.find(base_query).distinct("injury")
    injury = st.selectbox("Choose your injury of interest", injuries)
    start_date_ = list(progress_collection.find(base_query).sort("date",+1).limit(1))[0]["date"]
    end_date_ = list(progress_collection.find(base_query).sort("date",-1).limit(1))[0]["date"]
    start_date_ = datetime.strptime(start_date_, "%Y-%m-%d")
    end_date_ = datetime.strptime(end_date_, "%Y-%m-%d")
    dates = st.date_input("Please choose a date range", value=(start_date_, end_date_), min_value=start_date_,
        max_value=end_date_,)
    try:
        data = get_aggregated_progress(progress_collection, st.session_state.user["_id"], injury, dates[0], dates[1])
        fig = px.scatter(data, x="dates", y="status", hover_data=["activity_yesterday", "activity_today"])
        st.plotly_chart(fig, use_container_width=True)
    except IndexError:
        pass
        # Two dates not yet chosen
    


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
    status = st.slider("On a scale from 1-10, how good does your injury feel?", min_value=1, max_value=10)    
    yesterday = st.text_input("What did you do yesterday?")
    today = st.text_input("What did you do today?")
    doc = {
        "user": st.session_state.user["_id"],
        "injury": injury,
        "date": date.strftime("%Y-%m-%d"),
        "status": status,
        "activity_yesterday": yesterday,
        "activity_today": today
    }
    insert_document = st.button("Add to progress")
    if insert_document:
        result = progress_collection.insert_one(doc)
        if result.acknowledged:
            st.success("Successfully added information to your progress!")
        
def login() -> None:
    user_placeholder = st.empty()
    pwd_placeholder = st.empty()
    username = user_placeholder.text_input("Please input username")
    pwd = pwd_placeholder.text_input("Please input password", type="password")
    if username != "":
        db = connect_to_db()
        user_collection = db.users
        user = user_collection.find_one({"username": username})
        if user is None:
            st.text("Sorry, that user does not exist!")
        else:
            if pwd != "":
                if pwd == user["password"]:
                    user_placeholder.empty()
                    pwd_placeholder.empty()
                    st.session_state.logged_in = True
                    st.session_state.user = user
                else:
                    st.text("Sorry, that is not correct")



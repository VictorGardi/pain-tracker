from datetime import datetime

import plotly.express as px
import streamlit as st
from bson import ObjectId

from login import check_password
from utils import connect_to_db, get_aggregated_progress


def show_progress(user: ObjectId):
    st.markdown("**Progress**")
    st.sidebar.markdown("# Show progress ❄️")
    db = connect_to_db()
    progress_collection = db.pain_tracker.progress
    base_query = {"user": user}
    injuries = progress_collection.find(base_query).distinct("injury")
    injury = st.selectbox("Choose your injury of interest", injuries)
    start_date_ = list(progress_collection.find(base_query).sort("date", +1).limit(1))[0]["date"]
    end_date_ = list(progress_collection.find(base_query).sort("date", -1).limit(1))[0]["date"]
    start_date_ = datetime.strptime(start_date_, "%Y-%m-%d")
    end_date_ = datetime.strptime(end_date_, "%Y-%m-%d")
    dates = st.date_input(
        "Please choose a date range",
        value=(start_date_, end_date_),
        min_value=start_date_,
        max_value=end_date_,
    )
    try:
        data = get_aggregated_progress(progress_collection, user, injury, dates[0], dates[1])
        fig = px.scatter(
            data, x="dates", y="status", hover_data=["activity_yesterday", "activity_today"]
        )
        st.plotly_chart(fig, use_container_width=True)
    except IndexError:
        pass
        # Two dates not yet chosen


if __name__ == "__main__":
    user = check_password()
    if user:
        show_progress(user)

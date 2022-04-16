import os

import streamlit as st
from pymongo import MongoClient


def connect_to_db() -> MongoClient:
    client = MongoClient(os.environ.get("DB_CONNECTION_STRING"))
    return client.pain_tracker

def login() -> None:
    user_placeholder = st.empty()
    pwd_placeholder = st.empty()
    username = user_placeholder.text_input("Please input Username")
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
                else:
                    st.text("Sorry, that is not correct")
        
    

import os
from typing import Union

import streamlit as st
from bson import ObjectId
from pymongo import MongoClient



def connect_to_db() -> MongoClient:
    client = MongoClient(os.environ.get("DB_CONNECTION_STRING"))
    return client

def login() -> Union[dict, None]:
    username = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    if username == "" and pw == "":
        return None 
    db = connect_to_db()
    user_collection = db.users.users
    user = user_collection.find_one({"username": username})
    if user is not None:
        if pw == user["password"]:
            st.success("Welcome!")
            return user
        st.error("Sorry, something went wrong..")

    else:
        st.error("Sorry, something went wrong..")
        return user


def get_aggregated_progress(collection, user_id, injury, start_date, end_date):
    result = collection.aggregate([
        {
            '$match': {
                'injury': injury, 
                'user': ObjectId(user_id), 
                'date': {
                    '$gte': start_date.strftime("%Y-%m-%d"), 
                    '$lte': end_date.strftime("%Y-%m-%d")
                }
            }
        }, {
            '$sort': {
                'date': 1
            }
        }, {
            '$group': {
                '_id': None, 
                'dates': {
                    '$push': '$date'
                }, 
                'status': {
                    '$push': '$status'
                }, 
                'activity_yesterday': {
                    '$push': '$activity_yesterday'
                }, 
                'activity_today': {
                    '$push': '$activity_today'
                }
            }
        }
    ])
    return list(result)[0]

        
    

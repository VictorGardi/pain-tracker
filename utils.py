import os
from datetime import datetime

from bson import ObjectId
from pymongo import MongoClient



def connect_to_db() -> MongoClient:
    client = MongoClient(os.environ.get("DB_CONNECTION_STRING"))
    return client.pain_tracker

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

        
    

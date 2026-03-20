from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

client = MongoClient(MONGO_URI)
db     = client["agriadvisor"]

users_col       = db["users"]
predictions_col = db["predictions"]

def create_user(user_data: dict):
    users_col.insert_one(user_data)

def get_user_by_email(email: str):
    return users_col.find_one({"email": email}, {"_id": 0})

def update_password(email: str, new_hashed_password: str):
    users_col.update_one(
        {"email": email},
        {"$set": {"password": new_hashed_password}}
    )

def save_prediction(user_email: str, inputs: dict, result: dict):
    predictions_col.insert_one({
        "user_email": user_email,
        "inputs":     inputs,
        "result":     result,
        "timestamp":  datetime.utcnow().isoformat()
    })

def get_user_predictions(user_email: str) -> list:
    cursor = predictions_col.find(
        {"user_email": user_email},
        {"_id": 0}
    ).sort("timestamp", -1)
    return list(cursor)
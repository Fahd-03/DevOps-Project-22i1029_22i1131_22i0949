# user-service/app.py
from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URI"))
# client = MongoClient("mongodb://localhost:27017")
# db = client["user_db"]
db = client[os.getenv("MONGO_DB_USER")]
collection = db["users"]

@app.route("/users", methods=["POST"])
def create_user():
    user_data = request.get_json()
    result = collection.insert_one(user_data)
    return jsonify({"id": str(result.inserted_id)}), 201

@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    user = collection.find_one({"id": int(user_id)})
    if user:
        user["_id"] = str(user["_id"])
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
# todo-service/app.py
from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

client = MongoClient(os.getenv("MONGO_URI"))
# client = MongoClient("mongodb://localhost:27017")
# db = client["todo_db"]
db = client[os.getenv("MONGO_DB_TODO")]
collection = db["todos"]

@app.route("/todos", methods=["POST"])
def create_todo():
    todo_data = request.get_json()
    result = collection.insert_one(todo_data)
    return jsonify({"id": str(result.inserted_id)}), 201

@app.route("/todos/<user_id>", methods=["GET"])
def get_todos(user_id):
    todos = list(collection.find({"user_id": int(user_id)}))
    for todo in todos:
        todo["_id"] = str(todo["_id"])
    return jsonify(todos)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
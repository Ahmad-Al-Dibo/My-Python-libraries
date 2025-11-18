from flask import Flask, jsonify, request
from pysessionmanager import *

app = Flask(__name__)
session_manager = SessionManager()

@app.route("/start", methods=["POST"])
def start():
    user_id = request.json.get("user_id", None)
    session_id = session_manager.add_session(user_id)
    return jsonify({"session_id": session_id})

@app.route("/status/<session_id>")
def status(session_id):
    active = session_manager.is_active(session_id)
    remaining = session_manager.get_time_remaining(session_id)
    return jsonify({"active": active, "remaining_seconds": remaining})


if __name__ == "__main__":
    app.run(debug=True)
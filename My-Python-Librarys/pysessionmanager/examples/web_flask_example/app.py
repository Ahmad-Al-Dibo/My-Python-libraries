from flask import Flask, jsonify, request, render_template
from pysessionmanager import SessionManager

app = Flask(__name__)
session_manager = SessionManager(protect_all=False)  # Set global protection to False by default

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start", methods=["POST"])
def start_session():
    data = request.get_json()
    user_id = data.get("user_id")
    password = data.get("password", None)
    
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    
    session_id = session_manager.add_session(user_id=user_id, password=password)
    return jsonify({"session_id": session_id})

@app.route("/status/<session_id>", methods=["GET"])
def session_status(session_id):
    try:
        active = session_manager.is_active(session_id)
        remaining = session_manager.get_time_remaining(session_id)
        return jsonify({
            "session_id": session_id,
            "active": active,
            "remaining_seconds": remaining
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 404

@app.route("/unlock", methods=["POST"])
def unlock_session():
    data = request.get_json()
    session_id = data.get("session_id")
    password = data.get("password")
    
    if not session_id or not password:
        return jsonify({"error": "session_id and password are required"}), 400

    try:
        session_manager.unlock_session(session_id, password)
        return jsonify({"message": "Session unlocked successfully"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 403

if __name__ == "__main__":
    app.run(debug=True)

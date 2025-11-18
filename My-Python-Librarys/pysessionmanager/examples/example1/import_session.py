from pysessionmanager.core import SessionManager
import time

# Initialiseer de SessionManager
sm = SessionManager(logging=True)
sm.load_sessions(filename="session.json", format="json", logging=True)
print(sm.get_all_sessions())
user_id = "cli_user2"  # Gebruik een bekend ID voor debugging
try:
    sm.unlock_session(user_id, password="SecurePass123")
except ValueError as e:
    print(f"Error unlocking session: {e}")
session = sm.get_session_id_by_session_name(user_id)
print(session)
if session:
    print("Session ID:", session)
    print("Session details:", session)
    print("Session started with ID:", session)
    
    while sm.is_active(session):
        print(f"Session is active. Time remaining: {sm.get_time_remaining(session)} seconds")
        time.sleep(2)
else:
    print("Session not found.")


from pysessionmanager.core import SessionManager
import time

sm = SessionManager()
session_id = sm.add_session("cli_user", 10)

print("Session started with ID:", session_id)
while sm.is_active(session_id):
    print("Session is active. Time remaining:", sm.get_time_remaining(session_id))
    time.sleep(2)

print("Session expired.")
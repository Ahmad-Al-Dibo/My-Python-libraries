from pysessionmanager.core import SessionManager
import time

sm = SessionManager(

)
session_user = sm.create_session("cli_user", 300, protected=True, password="SecurePass123")
session_user = sm.create_session("cli_user2", 600, protected=False)



sm.store_sessions("sessions.json", format="json")


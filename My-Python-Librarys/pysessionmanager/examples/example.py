from pysessionmanager import SessionManager as Session
from pysessionmanager.codes import SessionMessages as messages

admin_session = Session(
    name = "Admin-user",
    protect = False,
    auto_renew = True
).load("sessions.json")

def admin_login_session(value):  # here is to create the session in the correct place
    admin_session.create(
        unick_name = "logged_in",
        during_seconds = 60*60,
        value = value,
        password = None
    )
    return messages.SESSION_CREATE_SUCCESS


admin_logged_key = admin_session.get_key(admin_session, "admin-loggin")


loadend = admin_session.load_sessions('sessions.json')
print(f"Sessions loaded: {loadend}")
    



admin_active_time = admin_session.get_session_by_user_id(
    'admin',
)
print (f"Admin session active time: {admin_active_time}")

if loadend and admin_active_time is not None:
    print(admin_session.get_time_remaining(admin_active_time))

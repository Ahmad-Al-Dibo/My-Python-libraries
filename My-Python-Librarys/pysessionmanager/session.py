from pysessionmanager import SessionManager
from pysessionmanager.codes import SessionMessages as messages

admin_session = SessionManager(
    name = "Admin-user",
    protect = False,
    auto_renew = True
)
admin_session.load("sessions.json")



def admin_login_session(unick_name:str, value, during_seconds:int, password:str=None):  # here is to create the session in the correct place
    admin_session.create(
        unick_name = unick_name,
        during_seconds = during_seconds,
        value = value,
        password = password,
        custom_metadata={
            "role": "admin",
            "department": "engineering",
            "permissions": ["read", "write", "admin"]
        }
    )
    admin_session.save()
    return messages.SESSION_CREATE_SUCCESS

admin_login_session("admin-loggin", True, 60*60)

admin_logged_key = admin_session.get_key(admin_session, "admin-loggin")


loadend = admin_session.load('sessions.json')
print(f"Sessions loaded: {loadend}")
    



admin_active_time = admin_session.get_session_with_unick_name(
    'admin',
)
print (f"Admin session active time: {admin_active_time}")

if loadend and admin_active_time is not None:
    print(admin_session.get_time_remaining(admin_active_time))

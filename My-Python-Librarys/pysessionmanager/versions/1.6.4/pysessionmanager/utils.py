import os

def get_default_session_name() -> str:
    return os.getenv("DEFAULT_USER_ID", "default_user").lower()



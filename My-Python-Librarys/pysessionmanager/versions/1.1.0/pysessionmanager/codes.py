class SessionMessages:
    PROTECTED_SESSION = "PROTECTED_SESSION"
    ACTIVE_SESSION = "ACTIVE_SESSION"
    UNLOCK_SESSION= "UNLOCK_SESSION"
    LOCK_SESSION = "LOCK_SESSION"
    SESSION_NOT_FOUND = "SESSION_NOT_FOUND"
    SESSION_ALREADY_LOCKED = "SESSION_ALREADY_LOCKED"
    SESSION_ALREADY_UNLOCKED = "SESSION_ALREADY_UNLOCKED"
    SESSION_LOCKED = "SESSION_LOCKED"
    SESSION_UNLOCK_FAILED = "SESSION_UNLOCK_FAILED"
    SESSION_UNLOCK_SUCCESS = "SESSION_UNLOCK_SUCCESS"
    SESSION_LOCK_SUCCESS = "SESSION_LOCK_SUCCESS"
    SESSION_LOCK_FAILED = "SESSION_LOCK_FAILED"
    SESSION_CREATE_SUCCESS = "SESSION_CREATE_SUCCESS"
    SESSION_CREATE_FAILED = "SESSION_CREATE_FAILED"
    SESSION_DELETE_SUCCESS = "SESSION_DELETE_SUCCESS"
    SESSION_DELETE_FAILED = "SESSION_DELETE_FAILED"
    SESSION_LIST = "SESSION_LIST"
    SESSION_LIST_EMPTY = "SESSION_LIST_EMPTY"
    SESSION_LIST_NOT_FOUND = "SESSION_LIST_NOT_FOUND"
    SESSION_TIMEOUT = "SESSION_TIMEOUT"
    SESSION_RESTORE_SUCCESS = "SESSION_RESTORE_SUCCESS"
    SESSION_RESTORE_FAILED = "SESSION_RESTORE_FAILED"
    SESSION_ALREADY_EXISTS = "SESSION_ALREADY_EXISTS"
    INVALID_SESSION_ID = "INVALID_SESSION_ID"
    SESSION_ACCESS_DENIED = "SESSION_ACCESS_DENIED"
    SESSION_PASSWORD_REQUIRED = "SESSION_PASSWORD_REQUIRED"
    

    @staticmethod
    def protected_session_message(session_id):
        return f"Session {session_id} is protected. Please unlock it.", SessionMessages.PROTECTED_SESSION

    @staticmethod
    def session_message(session_id):
        return f"Session {session_id} is active.", SessionMessages.ACTIVE_SESSION

    @staticmethod
    def unlock_message(session_id):
        return f"Session {session_id} is unlocked.", SessionMessages.UNLOCK_SESSION

    @staticmethod
    def lock_message(session_id):
        return f"Session {session_id} is locked.", SessionMessages.LOCK_SESSION

    @staticmethod
    def session_not_found_message(session_id):
        return f"Session {session_id} not found.", SessionMessages.SESSION_NOT_FOUND

    @staticmethod
    def session_already_locked_message(session_id):
        return f"Session {session_id} is already locked.", SessionMessages.SESSION_ALREADY_LOCKED

    @staticmethod
    def session_already_unlocked_message(session_id):
        return f"Session {session_id} is already unlocked.", SessionMessages.SESSION_ALREADY_UNLOCKED

    @staticmethod
    def session_locked_message(session_id):
        return f"Session {session_id} is locked.", SessionMessages.SESSION_LOCKED

    @staticmethod
    def session_unlock_failed_message(session_id):
        return f"Failed to unlock session {session_id}.", SessionMessages.SESSION_UNLOCK_FAILED

    @staticmethod
    def session_unlock_success_message(session_id):
        return f"Session {session_id} unlocked successfully.", SessionMessages.SESSION_UNLOCK_SUCCESS

    @staticmethod
    def session_lock_success_message(session_id):
        return f"Session {session_id} locked successfully.", SessionMessages.SESSION_LOCK_SUCCESS

    @staticmethod
    def session_lock_failed_message(session_id):
        return f"Failed to lock session {session_id}.", SessionMessages.SESSION_LOCK_FAILED

    @staticmethod
    def session_create_success_message(session_id):
        return f"Session {session_id} created successfully.", SessionMessages.SESSION_CREATE_SUCCESS

    @staticmethod
    def session_create_failed_message(session_id):
        return f"Failed to create session {session_id}.",  SessionMessages.SESSION_CREATE_FAILED

    @staticmethod
    def session_delete_success_message(session_id):
        return f"Session {session_id} deleted successfully.", SessionMessages.SESSION_DELETE_SUCCESS

    @staticmethod
    def session_delete_failed_message(session_id):
        return f"Failed to delete session {session_id}.", SessionMessages.SESSION_DELETE_FAILED

    @staticmethod
    def session_list_message(sessions):
        return f"Active sessions: {', '.join(sessions)}", SessionMessages.SESSION_LIST

    @staticmethod
    def session_list_empty_message():
        return "No active sessions.", SessionMessages.SESSION_LIST_EMPTY

    @staticmethod
    def session_list_not_found_message(session_id):
        return f"Session {session_id} not found.", SessionMessages.SESSION_LIST_NOT_FOUND

    @staticmethod
    def session_timeout_message(session_id):
        return f"Session {session_id} has timed out due to inactivity.", SessionMessages.SESSION_TIMEOUT

    @staticmethod
    def session_restore_success_message(session_id):
        return f"Session {session_id} has been restored successfully.", SessionMessages.SESSION_RESTORE_SUCCESS

    @staticmethod
    def session_restore_failed_message(session_id):
        return f"Failed to restore session {session_id}.", SessionMessages.SESSION_RESTORE_FAILED

    @staticmethod
    def session_already_exists_message(session_id):
        return f"Session {session_id} already exists.", SessionMessages.SESSION_ALREADY_EXISTS

    @staticmethod
    def invalid_session_id_message(session_id):
        return f"The session ID '{session_id}' is invalid.", SessionMessages.INVALID_SESSION_ID

    @staticmethod
    def session_access_denied_message(session_id):
        return f"Access denied for session {session_id}.", SessionMessages.SESSION_ACCESS_DENIED
    
    @staticmethod
    def session_password_required_message(session_id):
        return f"Password is required for this session. SESSION_ID: {session_id}", SessionMessages.SESSION_PASSWORD_REQUIRED
    
    @staticmethod
    def session_password_incorrect_message(session_id):
        return f"Incorrect password for this session. SESSION_ID: {session_id}", SessionMessages.SESSION_PASSWORD_REQUIRED

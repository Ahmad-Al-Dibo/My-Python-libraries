import datetime
import json
from typing import Dict, Literal, Optional
import csv
import sqlite3
import psycopg2
import logging as log # type: ignore
from pysessionmanager.codes import SessionMessages  # Ensure this import is correct and the module exists
from .security import generate_session_id, hash_password, verify_password
from .utils import get_default_session_name
# this class is only example class to help as writing a new class
# for storing sessions in different formats
# it is not used in the main code
class SessionStoring:
    def __init__(self, filename: str = "sessions.json", db_name: str = "sessions.db"):
        self.filename = filename
        self.db_name = db_name
        self.logging = False


    def store_sessions_json(self, sessions: Dict[str, Dict], filename: str = "sessions.json", logging: bool = False):
        sessions_to_save = {
            session_id: {
                "session_name": session["session_name"],
                "start_time": session["start_time"].isoformat(),
                "end_time": session["end_time"].isoformat(),
                "protected": session["protected"],
                "password": session.get("password"),
                "value": session.get("value"),
            }
            for session_id, session in self.sessions.items()
        }
        with open(filename, 'w') as f:
            json.dump(sessions_to_save, f)
            if logging or self.logging:
                log.info(SessionMessages.sessions_as_json_added_message(filename)[0])
        return SessionMessages.sessions_as_json_added_message(filename)[1]

    def store_sessions_csv(self, sessions: Dict[str, Dict], filename: str = "sessions.csv"):
        with open(filename, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["session_id", "session_name", "start_time", "end_time", "protected", "password", "value"])
            for session_id, session in sessions.items():
                writer.writerow([
                    session_id,
                    session["session_name"],
                    session["start_time"].isoformat(),
                    session["end_time"].isoformat(),
                    session["protected"],
                    session["password"],
                    session.get("value", "")
                ])

    def load_sessions_csv(self, csv_filename: str = "sessions.csv") -> Dict[str, Dict]:
        sessions = {}
        try:
            with open(csv_filename, mode='r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    sessions[row["session_id"]] = {
                        "session_name": row["session_name"],
                        "start_time": datetime.datetime.fromisoformat(row["start_time"]),
                        "end_time": datetime.datetime.fromisoformat(row["end_time"]),
                        "protected": row["protected"] == 'True',
                        "password": row["password"],
                        "value": row["value"] if row["value"] else None
                    }
        except FileNotFoundError:
            return {}
        return sessions

    def store_sessions_sqlite(self, filename:str="sessions.db" ,sessions: Dict[str, Dict]=None):
        conn = sqlite3.connect(self.db_name if not filename else filename)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            session_name TEXT,
            start_time TEXT,
            end_time TEXT,
            protected INTEGER,
            password TEXT,
            value TEXT
        )""")
        cursor.execute('DELETE FROM sessions')
        for session_id, session in sessions.items():
            cursor.execute('''INSERT INTO sessions VALUES (?, ?, ?, ?, ?, ?, ?)''', (
                session_id,
                session["session_name"],
                session["start_time"].isoformat(),
                session["end_time"].isoformat(),
                int(session["protected"]),
                session["password"],
                session.get("value", None),
            ))
        conn.commit()
        conn.close()

    def load_sessions_sqlite(self, filename:str="sessions.db") -> Dict[str, Dict]:
        sessions = {}
        conn = sqlite3.connect(self.db_name if not filename else filename)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sessions')
        for row in cursor.fetchall():
            sessions[row[0]] = {
                "session_name": row[1],
                "start_time": datetime.datetime.fromisoformat(row[2]),
                "end_time": datetime.datetime.fromisoformat(row[3]),
                "protected": bool(row[4]),
                "password": row[5],
                "value": row[6] if len(row) > 6 else None
            }
        conn.close()
        return sessions

    def store_sessions_postgresql(self, filename:str="sessions.db", sessions: Dict[str, Dict]=None, conn_string:str=None):
        if not conn_string:
            raise ValueError("Connection string is required for PostgreSQL.")
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS sessions (
            session_id TEXT PRIMARY KEY,
            session_name TEXT,
            start_time TEXT,
            end_time TEXT,
            protected BOOLEAN,
            password TEXT,
            value TEXT
        )''')
        cursor.execute('DELETE FROM sessions')
        for session_id, session in sessions.items():
            cursor.execute('''INSERT INTO sessions VALUES (%s, %s, %s, %s, %s, %s)''', (
                session_id,
                session["session_name"],
                session["start_time"].isoformat(),
                session["end_time"].isoformat(),
                session["protected"],
                session["password"],
                session.get("value", None)
            ))
        conn.commit()
        conn.close()

    def load_sessions_postgresql(self, conn_string: str) -> Dict[str, Dict]:
        sessions = {}
        if not conn_string:
            raise ValueError("Connection string is required for PostgreSQL.")
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM sessions')
        for row in cursor.fetchall():
            sessions[row[0]] = {
                "session_name": row[1],
                "start_time": datetime.datetime.fromisoformat(row[2]),
                "end_time": datetime.datetime.fromisoformat(row[3]),
                "protected": row[4],
                "password": row[5],
                "value": row[6] if len(row) > 6 else None
            }
        conn.close()
        return sessions


class SessionManager:
    def __init__(self, protect_all: bool = False, logging: bool = False):
        self.sessions: Dict[str, Dict] = {}
        self.filename = "sessions.json"
        self.db_name = "sessions.db"
        self.protect_all = protect_all
        self.logging = logging
        self.storer = SessionStoring(self.filename, self.db_name)


    def create_session(
        self,
        session_name: str = None,
        duration_seconds: int = 3600,
        protected: bool = False,
        password: Optional[str] = None,
        value: str = None,
        password_length:int = 6
    ) -> str:
        """
        Add a new session.

        Args:
            session_name (str): Optional user identifier.
            duration_seconds (int): Lifetime of session in seconds.
            protected (bool): Whether this session is password-protected.
            password (str): Password to unlock the session if protected.

        Returns:
            str: The generated session ID.
        """
        session_id = generate_session_id()
        if session_name is None and not self.sessions:
            session_name = session_name or get_default_session_name()
        
        if protected and not password:
            raise ValueError("Password is required for protected sessions.")
        
        if self.protect_all and not password:
            raise ValueError("Password is required for all sessions due to global protection setting.")
        
        if protected and password or self.protect_all and password:
            if len(password) < password_length:
                raise ValueError(f"Password must be at least {password_length} characters long.")
            
        if protected and password or self.protect_all and password:
            new_password = hash_password(password) 
        else:
            new_password = None
        
        if value is not None:
            if not isinstance(value, str):
                raise ValueError("Value must be a string.")
            if len(value) < 1:
                raise ValueError("Value must be at least 1 character long.")

        now = datetime.datetime.now()
        self.sessions[session_id] = {
            "session_name": session_name,
            "start_time": now,
            "end_time": now + datetime.timedelta(seconds=duration_seconds),
            "protected": protected,
            "password": new_password,
            "value": value,
        }
        return session_id

    def remove_session(self, session_id: str):
        """
        Remove a session by ID.
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session ID {session_id} not found.")
        self.sessions.pop(session_id)

    def get_session(self, session_id: str) -> Optional[Dict]:
        """
        Get the session dictionary for a given session ID.
        """
        if session_id in self.sessions:
            return self.sessions[session_id]
        else:
            return SessionMessages.session_not_found_message(session_id)[1]

    def is_active(self, session_id: str) -> bool:
        """
        Check if the session is currently active.
        """
        session = self.get_session(session_id)
        now = datetime.datetime.now()
        return session["start_time"] <= now <= session["end_time"]

    def get_time_remaining(self, session_id: str) -> float:
        """
        Get the number of seconds remaining before the session expires.
        """
        session = self.get_session(session_id)
        return max((session["end_time"] - datetime.datetime.now()).total_seconds(), 0.0)

    def time_passed(self, session_id: str) -> float:
        """
        Get the number of seconds that have passed since the session started.
        """
        session = self.get_session(session_id)
        return max((datetime.datetime.now() - session["start_time"]).total_seconds(), 0.0)

    def get_all_sessions(self) -> Dict[str, Dict]:
        """
        Return all sessions.
        """
        removed_sessions = []
        protected_sessions = []
        for session_id, session in list(self.sessions.items()):
            if session["protected"]:
                if not session.get("password"):
                    protected_sessions.append(session_id)
                    continue
            if session ["end_time"] < datetime.datetime.now():
                removed_sessions.append(session_id)
                self.remove_session(session_id)
            
        return {
            session_id: {
                "session_name": session["session_name"],
                "start_time": session["start_time"].isoformat(),
                "end_time": session["end_time"].isoformat(),
                "protected": session["protected"],
                "password": session.get("password"),
                "value": session.get("value"),
            }
            for session_id, session in self.sessions.items()
        }, removed_sessions, protected_sessions

    def store_sessions(
    self,
    filename: Optional[str] = None,
    format: Optional[Literal["json", "csv", "sql", "postgresql"]] = None,
    logging: bool = False
):
        """
        Save sessions to a JSON file. Or to a CSV, SQLite, or PostgreSQL database.
        Args:
            filename (str): The name of the file to save the sessions to.
            format (str): The format to save the sessions in. Can be "json", "csv", "sql", or "postgresql".
            logging (bool): Whether to log the session saving process.
        raises:
            ValueError: If the format is not supported.

        """
        filename = filename
        split_filename = filename.split(".")
        if len(split_filename) > 1:
            pass
        else:
            raise ValueError("Filename must be in the format 'filename.extension'.")
        if format == "json" and split_filename[1] == "json":
            self.storer.store_sessions_json(self.sessions, filename)
            if logging or self.logging:
                log.info(SessionMessages.sessions_as_json_added_message(filename)[0])
            return SessionMessages.sessions_as_json_added_message(filename)[1]
        
        elif format == "csv" and split_filename[1] == "csv":
            self.storer.store_sessions_csv(self.sessions, filename)
            if logging or self.logging:
                log.info(SessionMessages.sessions_as_csv_added_message(filename)[0])
            return SessionMessages.sessions_as_csv_added_message(filename)[1]
        
        elif format == "sql" and  split_filename[1] == "db":
            self.storer.store_sessions_sqlite(filename, self.sessions)
            if logging or self.logging:
                log.info(SessionMessages.sessions_as_sqlite_added_message(filename)[0])
            return SessionMessages.sessions_as_sqlite_added_message(filename)[1]
        
        elif format == "postgresql" and  split_filename[1] == "db":
            self.storer.store_sessions_postgresql(self.sessions, filename)
            if logging or self.logging:
                log.info(SessionMessages.sessions_as_postgresql_added_message(filename)[0])
            return SessionMessages.sessions_as_postgresql_added_message(filename)[1]
        
        else:
            raise ValueError("Unsupported format. Supported formats are: json, csv, sql, postgresql. NOTE: filename must end with the correct file extension.")
        

    def load_sessions(self, filename: str = None, format: Optional[Literal["json", "csv", "sql", "postgresql"]] = "json", logging: bool = False):
        """
        Load sessions from a JSON file.
        """
        filename = str(filename)
        split_filename = filename.split(".")
        print(split_filename)
        if len(split_filename) > 1:
            pass
        else:
            raise ValueError("Filename must be in the format 'filename.extension'.")
        if format == "json" and split_filename[1] == "json":
            try:
                with open(filename, 'r') as f:
                    self.sessions = json.load(f)
                for session_id, session in self.sessions.items():
                    session["start_time"] = datetime.datetime.fromisoformat(session["start_time"])
                    session["end_time"] = datetime.datetime.fromisoformat(session["end_time"])
                    session["protected"] = session.get("protected", False)
                    session["password"] = session.get("password")
                    session["session_name"] = session.get("session_name", get_default_session_name())
                    session["value"] = session.get("value")
                    if logging or self.logging:
                        log.info(SessionMessages.session_as_json_loaded_message(filename)[0])
                    return SessionMessages.session_as_json_loaded_message(filename)[1]
            except json.JSONDecodeError:
                raise ValueError("Error loading sessions: Invalid JSON format.")
            except FileNotFoundError:
                self.sessions = {} 
        elif format == "csv" and split_filename[1] == "csv":
            self.sessions = self.storer.load_sessions_csv(filename)
            for session_id, session in self.sessions.items():
                session["start_time"] = datetime.datetime.fromisoformat(session["start_time"])
                session["end_time"] = datetime.datetime.fromisoformat(session["end_time"])
                session["protected"] = session.get("protected", False)
                session["password"] = session.get("password")
                session["session_name"] = session.get("session_name", get_default_session_name())
                session["value"] = session.get("value")
                if logging or self.logging:
                    log.info(SessionMessages.session_as_csv_loaded_message(filename)[0])
            return SessionMessages.session_as_csv_loaded_message(filename)[1]
        elif format == "sql" and split_filename[1] == "db":
            self.sessions = self.storer.load_sessions_sqlite(filename)
            for session_id, session in self.sessions.items():
                session["start_time"] = datetime.datetime.fromisoformat(session["start_time"])
                session["end_time"] = datetime.datetime.fromisoformat(session["end_time"])
                session["protected"] = session.get("protected", False)
                session["password"] = session.get("password")
                session["session_name"] = session.get("session_name", get_default_session_name())
                session["value"] = session.get("value")
                if logging or self.logging:
                    log.info(SessionMessages.session_as_sqlite_loaded_message(filename)[0])
            return SessionMessages.session_as_sqlite_loaded_message(filename)[1]
        elif format == "postgresql" and split_filename[1] == "db":
            self.sessions = self.storer.load_sessions_postgresql(filename)
            for session_id, session in self.sessions.items():
                session["start_time"] = datetime.datetime.fromisoformat(session["start_time"])
                session["end_time"] = datetime.datetime.fromisoformat(session["end_time"])
                session["protected"] = session.get("protected", False)
                session["password"] = session.get("password")
                session["session_name"] = session.get("session_name", get_default_session_name())
                session["value"] = session.get("value")
                if logging or self.logging:
                    log.info(SessionMessages.session_as_postgresql_loaded_message(filename)[0])
            return SessionMessages.session_as_postgresql_loaded_message(filename)[1]
        else:
            raise ValueError("Unsupported format. Supported formats are: json, csv, sql, postgresql. NOTE: filename must end with the correct file extension.")
        

    def clear_sessions(self):
        """
        Clear all sessions and overwrite the session file.
        """
        self.sessions.clear()
        with open(self.filename, 'w') as f:
            json.dump(self.sessions, f)

    def get_session_id_by_session_name(self, session_name: str, logging:bool=False) -> Optional[str]:
        """get_session_id_by_session_name
        Get the session ID for a given session name, if the session is not protected.
        """
        for session_id, session in self.sessions.items():
            if not session.get("protected") and session["session_name"] == session_name:
                return session_id
            if session.get("protected") and session["session_name"] == session_name:
                if logging or self.logging:
                    log.info(SessionMessages.protected_session_message(session_id)[0])
                    # Log the protected session message
                return SessionMessages.protected_session_message(session_id)[1]
        return None

    def unlock_session(self, session_name: str, password: str, logging:bool=False) -> Optional[str]:
        """
        Unlock a protected session for a given session_name by verifying the hashed password.
        """
        # Find the protected session by session_name
        for session_id, session in self.sessions.items():
            if session["session_name"] == session_name and session.get("protected"):
                if verify_password(password, session.get("password")):
                    session["protected"] = False
                    session["password"] = None
                    if logging or self.logging:
                        log.info(SessionMessages.unlock_message(session_id)[0])
                    return SessionMessages.unlock_message(session_id)[1]
                else:
                    return 
        if logging or self.logging:
            log.warning(SessionMessages.session_not_found_message(session_name)[0])
        return SessionMessages.session_not_found_message(session_name)[1]
    


    def lock_session(self, session_id: str, password: str, logging:bool=False) -> Optional[str]:
        """
        Lock a session by setting a password.
        """
        if session_id not in self.sessions:
            if logging or self.logging:
                log.warning(SessionMessages.session_not_found_message(session_id)[0])
            return SessionMessages.session_not_found_message(session_id)[1]
        if self.sessions[session_id].get("protected"):
            if logging or self.logging:
                log.warning(SessionMessages.session_already_locked_message(session_id)[0])
            return SessionMessages.session_already_locked_message(session_id)[1]
        if self.sessions[session_id].get("password"):
            if logging or self.logging:
                log.WARNING(SessionMessages.session_already_locked_message(session_id)[0])
            return SessionMessages.session_already_locked_message(session_id)[1]
        if not password:
            if logging or self.logging:
                log.error(SessionMessages.session_password_required_message(session_id)[0])
            raise ValueError("Password is required to lock the session.")
        if len(password) < 6:
            if logging or self.logging:
                log.error(SessionMessages.session_password_incorrect_message(session_id)[0])
            raise ValueError("Password must be at least 6 characters long.")
        
        self.sessions[session_id]["protected"] = True
        self.sessions[session_id]["password"] = hash_password(password)
        self.store_sessions(self.filename)
        self.load_sessions(self.filename)

        return self.sessions[session_id]
    

    def get_session_value(self, session_id: str) -> Optional[str]:
        """
        Get the value associated with a session.
        """
        if session_id in self.sessions:
            if self.sessions[session_id].get("protected"):
                return SessionMessages.session_locked_message(session_id)[1]
            return self.sessions[session_id].get("value")
        else:
            raise ValueError(f"Session ID {session_id} not found.")



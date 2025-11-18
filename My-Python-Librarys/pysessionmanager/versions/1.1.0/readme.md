# PySessionManager
PySessionManager is a Python library designed to simplify session management in your applications. It provides an easy-to-use interface for creating, managing, and persisting user sessions.

## Features

- Create and manage user sessions.
- Support for session persistence.
- Configurable session expiration.
- Lightweight and easy to integrate.

## Installation

Install the library using pip:

```bash
pip install pysessionmanager
```

## Usage

### Basic Example

```python
from pysessionmanager import SessionManager

# Initialize the session manager
session_manager = SessionManager()

# Create a new session
session_id = session_manager.create_session(user_id="12345")

# Retrieve session data
session_data = session_manager.get_session(session_id)

# End a session
session_manager.end_session(session_id)
```

### Advanced Examples

#### Example 1: Checking Session Activity

```python
# Check if a session is active
is_active = session_manager.is_session_active(session_id)
if is_active:
  print("Session is active.")
else:
  print("Session has expired or does not exist.")
```

#### Example 2: Custom Session Expiration

```python
# Initialize the session manager with a custom expiration time
session_manager = SessionManager(expiration_time=1800)  # 30 minutes

# Create a session with the custom expiration
session_id = session_manager.create_session(user_id="67890")
print(f"Session created with ID: {session_id}")
```

#### Example 3: Storing Additional Data in Sessions

```python
# Create a session with additional data
session_id = session_manager.create_session(user_id="54321", data={"role": "admin", "preferences": {"theme": "dark"}})

# Retrieve the session data
session_data = session_manager.get_session(session_id)
print(f"User Role: {session_data['role']}")
print(f"Theme Preference: {session_data['preferences']['theme']}")
```

## API Reference

### `SessionManager`

#### Methods:

- `create_session(user_id: str, data: Optional[dict] = None) -> str`: Creates a new session with optional additional data and returns the session ID.
- `get_session(session_id: str) -> dict`: Retrieves session data for the given session ID.
- `end_session(session_id: str) -> None`: Ends the session with the given session ID.
- `is_session_active(session_id: str) -> bool`: Checks if a session is still active.

## Example Projects

### 1. Web Application Authentication

Use PySessionManager to manage user sessions in a Flask or Django web application. Store user login states and preferences securely.

### 2. API Rate Limiting

Implement session-based rate limiting for APIs by tracking user requests and enforcing limits based on session data.

### 3. E-commerce Cart Management

Manage shopping cart sessions for users in an e-commerce application. Store cart items and retrieve them when users return.

### 4. Multiplayer Game Sessions

Use PySessionManager to manage player sessions in a multiplayer game, storing player stats and game states.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push the branch.
4. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback, please contact the maintainer at `ahmadaldibo212009@gmail.com`.
# PySessionManager

PySessionManager is a Python library for managing user sessions in your applications. It provides a simple API to create, store, retrieve, and manage session data, making it ideal for web and desktop projects.

## Features

- Create and manage user sessions
- Store session data securely
- Session expiration and cleanup
- Easy integration with web frameworks

## Installation

```bash
pip install pysessionmanager
```

## Usage

```python
from pysessionmanager import SessionManager

# Initialize session manager
manager = SessionManager()

# Create a new session
session_id = manager.create_session(user_id="user123")

# Set session data
manager.set_data(session_id, "key", "value")

# Get session data
value = manager.get_data(session_id, "key")

# End a session
manager.end_session(session_id)
```

## Example Project: session_web_manager

The [`session_web_manager`](../../../../testing/session_web_manager) project demonstrates how to use PySessionManager in a web application. Below are the main steps and example code to get started:

### How It Works

1. **Initialize PySessionManager** in your web app.
2. **Create sessions** when users log in.
3. **Store and retrieve session data** as users interact with your app.
4. **End sessions** when users log out.

### Example Code

```python
from pysessionmanager import SessionManager
from flask import Flask, request, redirect, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'
manager = SessionManager()

@app.route('/login', methods=['POST'])
def login():
    user_id = request.form['username']
    session_id = manager.create_session(user_id=user_id)
    session['session_id'] = session_id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    session_id = session.get('session_id')
    if session_id and manager.is_valid(session_id):
        user_data = manager.get_data(session_id, 'user_info')
        return f"Welcome! {user_data}"
    return redirect('/login')

@app.route('/logout')
def logout():
    session_id = session.get('session_id')
    if session_id:
        manager.end_session(session_id)
    session.pop('session_id', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
```

This example uses Flask, but you can adapt the logic to other frameworks.

## License

MIT License

## Contributing

Contributions are welcome! Please open issues or submit pull requests.

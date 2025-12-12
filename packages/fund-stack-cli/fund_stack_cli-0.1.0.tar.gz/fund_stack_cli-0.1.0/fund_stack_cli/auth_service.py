#========================
#FILE: auth_service.py
#========================

"""
Authentication Service Module.

This module handles user authentication operations including:
- User registration
- User login
- Session management (saving, retrieving, clearing session)
- User profile creation in the database
"""

import json, os, requests
from rich.console import Console
from rich.panel import Panel
from .firebase_config import FIREBASE_AUTH_LOGIN, FIREBASE_AUTH_SIGNUP, DATABASE_URL

console = Console()
SESSION_FILE = "session.json"

def save_session(data):
    """
    Saves the user session data to a local JSON file.

    Args:
        data (dict): The session data returned from Firebase Auth.
    """
    with open(SESSION_FILE, "w") as f:
        json.dump(data, f)

def get_session():
    """
    Retrieves the current user session if it exists.

    Returns:
        dict or None: The session data if the file exists, otherwise None.
    """
    if not os.path.exists(SESSION_FILE): return None
    with open(SESSION_FILE, "r") as f: return json.load(f)

def clear_session():
    """
    Clears the local session file, effectively logging the user out.
    """
    if os.path.exists(SESSION_FILE): os.remove(SESSION_FILE)


def register_user(email, password, name, age, phone, pan):
    """
    Registers a new user with Firebase Auth and creates a user profile in the database.

    Args:
        email (str): User's email address.
        password (str): User's password.
        name (str): User's full name.
        age (str): User's age.
        phone (str): User's phone number.
        pan (str): User's PAN card number.

    Returns:
        dict or None: The response data from Firebase if successful, None otherwise.
    """
    console.print(Panel("Creating your account...", style="cyan"))

    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(FIREBASE_AUTH_SIGNUP, json=payload)
    data = response.json()

    if "error" in data:
        console.print(Panel(f"❌ Registration failed: {data['error']['message']}", style="red"))
        return None

    uid = data["localId"]

    # Create user profile in Realtime Database
    profile = {"name": name, "age": age, "phone": phone, "pan": pan, "email": email}
    requests.put(f"{DATABASE_URL}/users/{uid}/profile.json", json=profile)

    console.print(Panel("✔ Account created successfully!", style="green"))
    return data


def login_user(email, password):
    """
    Authenticates a user with email and password.

    Args:
        email (str): User's email address.
        password (str): User's password.

    Returns:
        dict or None: The session data if login is successful, None otherwise.
    """
    console.print(Panel("🔐 Logging in...", style="cyan"))

    payload = {"email": email, "password": password, "returnSecureToken": True}
    response = requests.post(FIREBASE_AUTH_LOGIN, json=payload)
    data = response.json()

    if "error" in data:
        console.print(Panel(f"❌ Login failed: {data['error']['message']}", style="red"))
        return None

    save_session(data)
    console.print(Panel("✔ Logged in successfully!", style="green"))
    return data


def logout_user():
    """
    Logs out the current user by clearing the session file.
    """
    clear_session()
    console.print(Panel("✔ Logged out.", style="green"))
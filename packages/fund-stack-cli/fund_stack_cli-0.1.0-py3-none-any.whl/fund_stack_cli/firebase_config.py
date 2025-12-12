"""
Configuration settings for Firebase and Google Cloud services.

This module contains API keys and endpoints required for:
- Firebase Authentication (Sign up, Login)
- Firebase Realtime Database
"""

import requests

# Base Firebase project details
# API Key for Firebase project authentication
API_KEY = "AIzaSyB8MsAaONyO3MRyQWfw5Qque6iaVtK4fjg"

# Firebase Auth REST endpoints
# URL for creating a new user account
FIREBASE_AUTH_SIGNUP = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
# URL for signing in an existing user
FIREBASE_AUTH_LOGIN = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"

# Your Realtime Database URL
# Base URL for the Firebase Realtime Database
DATABASE_URL = "https://fundstack-cli-default-rtdb.firebaseio.com/"

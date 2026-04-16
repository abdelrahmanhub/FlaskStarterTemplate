"""Authentication service functions for user registration and login checks."""

import sqlite3

from werkzeug.security import generate_password_hash, check_password_hash
from app.database import execute_query

def register_user(name, username, password):
    """Create a new user with hashed password and return created row data."""
    hash_pw = generate_password_hash(password)
    try:
        execute_query("INSERT INTO users (name, username, hash) VALUES (?, ?, ?)", name, username, hash_pw)
    except sqlite3.IntegrityError:
        return None

    row = execute_query("SELECT * FROM users WHERE username = ?", username)
    if not row:
        return None

    return row[0]  # return tuple (id, name, username, hash)

def validate_login(username, password):
    """Validate user credentials and return user data when credentials are valid."""
    row = execute_query("SELECT * FROM users WHERE username = ?", username)
    if not row:
        return None
    if not check_password_hash(row[0]["hash"], password):
        return None
    return row[0]  # return tuple (id, name, username, hash)

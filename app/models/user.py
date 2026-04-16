"""User model wrapper compatible with Flask-Login session management."""

from flask_login import UserMixin
from app.database import execute_query

class User(UserMixin):
    """Represent a logged-in user and provide lookup helpers."""
    def __init__(self, id, name, username, password_hash):
        """Initialize a user object using values loaded from the database."""
        self.id = id
        self.name = name
        self.username = username
        self.password_hash = password_hash

    @staticmethod
    def get(user_id):
        """Fetch a user by id and return a User instance when found."""
        results = execute_query("SELECT * FROM users WHERE id = ?", user_id)
        if results:
            user_data = results[0]
            return User(
                user_data['id'], 
                user_data['name'], 
                user_data['username'], 
                user_data['hash']
            )
        return None
    

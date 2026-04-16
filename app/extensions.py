"""Initialize Flask extensions used by the application."""

from flask_login import LoginManager
from app.models.user import User

login_manager = LoginManager()
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    """Load and return the authenticated user object by its identifier."""
    return User.get(user_id)

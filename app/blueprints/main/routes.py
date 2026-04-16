"""Main application routes that render authenticated user pages."""

from flask import render_template
from flask_login import login_required, current_user
from . import main_bp

@main_bp.route("/")
@login_required
def index():
    """Render the main dashboard page for the signed-in user."""
    return render_template("main/index.html", user=current_user)

@main_bp.route("/profile")
@login_required
def profile():
    """Render the profile page showing the current user information."""
    return render_template("main/profile.html", user=current_user)

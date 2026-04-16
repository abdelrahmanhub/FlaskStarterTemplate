"""Authentication routes for login, registration, and secure logout flows."""

import re

from flask import current_app, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from . import auth_bp
from app.models.user import User
from app.services.auth_service import register_user, validate_login
from app.services.rate_limit_service import (
    build_login_identifier,
    clear_failed_logins,
    get_login_block_status,
    register_failed_login,
)

USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_.-]{3,30}$")
MAX_NAME_LENGTH = 80
MIN_PASSWORD_LENGTH = 8


def _normalize_text(value):
    """Return a trimmed string value and fallback to empty text when missing."""
    return (value or "").strip()


def _format_wait_time(seconds):
    """Convert remaining block seconds into a human-readable minute string."""
    minutes = (seconds + 59) // 60
    if minutes <= 1:
        return "1 minute"
    return f"{minutes} minutes"


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login with validation, rate limiting, and session creation."""
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        username = _normalize_text(request.form.get("username"))
        password = request.form.get("password") or ""
        login_identifier = build_login_identifier(username, request.remote_addr)

        if not username or not password:
            flash("Username and password are required", "error")
            return render_template("auth/login.html")

        is_blocked, remaining_seconds = get_login_block_status(login_identifier)
        if is_blocked:
            wait_time = _format_wait_time(remaining_seconds)
            flash(f"Too many failed login attempts. Try again in {wait_time}.", "error")
            return render_template("auth/login.html")

        user_data = validate_login(username, password)
        if not user_data:
            now_blocked, new_remaining = register_failed_login(login_identifier)
            if now_blocked:
                wait_time = _format_wait_time(new_remaining)
                flash(f"Too many failed login attempts. Try again in {wait_time}.", "error")
            else:
                flash("Invalid username or password", "error")
            return render_template("auth/login.html")

        clear_failed_logins(login_identifier)

        user = User(user_data["id"], user_data["name"], user_data["username"], user_data["hash"])
        login_user(user, remember=True)
        return redirect(url_for("main.index"))

    return render_template("auth/login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Handle user registration with input checks and automatic sign-in."""
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        name = _normalize_text(request.form.get("name"))
        username = _normalize_text(request.form.get("username"))
        password = request.form.get("password") or ""
        confirmation = request.form.get("confirmation") or ""

        if not name or not username or not password or not confirmation:
            flash("All fields are required", "error")
            return render_template("auth/register.html")

        if len(name) > MAX_NAME_LENGTH:
            flash(f"Name must be {MAX_NAME_LENGTH} characters or less", "error")
            return render_template("auth/register.html")

        if not USERNAME_PATTERN.fullmatch(username):
            flash("Username must be 3-30 chars and use letters, numbers, _, ., or -", "error")
            return render_template("auth/register.html")

        if len(password) < MIN_PASSWORD_LENGTH:
            flash(f"Password must be at least {MIN_PASSWORD_LENGTH} characters", "error")
            return render_template("auth/register.html")

        if password != confirmation:
            flash("Passwords do not match", "error")
            return render_template("auth/register.html")

        try:
            new_user = register_user(name, username, password)
        except Exception:
            current_app.logger.exception("Unexpected registration failure")
            flash("Registration failed due to a server error", "error")
            return render_template("auth/register.html")

        if not new_user:
            flash("Username already exists", "error")
            return render_template("auth/register.html")

        user = User(new_user["id"], new_user["name"], new_user["username"], new_user["hash"])
        login_user(user, remember=True)
        return redirect(url_for("main.index"))

    return render_template("auth/register.html")

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    """End the current authenticated session and redirect to login page."""
    logout_user()
    return redirect(url_for("auth.login"))

"""Provide CSRF token generation and validation utilities for request safety."""

import hmac
import secrets

from flask import abort, request, session

CSRF_TOKEN_KEY = "_csrf_token"
UNSAFE_HTTP_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


def generate_csrf_token():
    """Return a session-bound CSRF token, creating it once when missing."""
    token = session.get(CSRF_TOKEN_KEY)
    if not token:
        token = secrets.token_urlsafe(32)
        session[CSRF_TOKEN_KEY] = token
    return token


def validate_csrf_token():
    """Reject unsafe requests that do not include a valid CSRF token."""
    if request.method not in UNSAFE_HTTP_METHODS:
        return

    session_token = session.get(CSRF_TOKEN_KEY, "")
    request_token = request.form.get("csrf_token") or request.headers.get("X-CSRF-Token", "")

    if not session_token or not request_token:
        abort(400, description="Missing CSRF token.")

    if not hmac.compare_digest(session_token, request_token):
        abort(400, description="Invalid CSRF token.")

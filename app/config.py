"""Centralized application configuration loaded from environment variables."""

import os
import secrets
from dotenv import load_dotenv

load_dotenv()


def _to_bool(value, default=False):
    """Convert a string value to boolean with a fallback default."""
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def _to_int(value, default):
    """Convert a string value to integer with a fallback default."""
    if value is None:
        return default
    try:
        return int(str(value).strip())
    except ValueError:
        return default


class Config:
    """Store all runtime settings used by the Flask application."""
    APP_ENV = os.getenv("APP_ENV", "development").strip().lower()
    IS_PRODUCTION = APP_ENV == "production"

    SECRET_KEY = os.getenv("SECRET_KEY") or (None if IS_PRODUCTION else secrets.token_hex(32))
    DATABASE = os.path.join(os.path.dirname(__file__), "db", "app.db")
    TEMPLATES_AUTO_RELOAD = True

    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = _to_bool(os.getenv("SESSION_COOKIE_SECURE"), default=IS_PRODUCTION)
    SESSION_COOKIE_SAMESITE = "Lax"

    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = SESSION_COOKIE_SECURE
    REMEMBER_COOKIE_SAMESITE = "Lax"

    PREFERRED_URL_SCHEME = "https" if IS_PRODUCTION else "http"

    LOGIN_RATE_LIMIT_WINDOW_SECONDS = _to_int(os.getenv("LOGIN_RATE_LIMIT_WINDOW_SECONDS"), 900)
    LOGIN_RATE_LIMIT_MAX_ATTEMPTS = _to_int(os.getenv("LOGIN_RATE_LIMIT_MAX_ATTEMPTS"), 5)
    LOGIN_RATE_LIMIT_BLOCK_SECONDS = _to_int(os.getenv("LOGIN_RATE_LIMIT_BLOCK_SECONDS"), 900)

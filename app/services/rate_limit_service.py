"""Track failed login attempts and enforce temporary lockouts for abuse prevention."""

import time

from flask import current_app

from app.database import execute_query


def build_login_identifier(username, ip_address):
    """Create a stable key that groups failed attempts by IP and username."""
    safe_username = (username or "").strip().lower()
    safe_ip = (ip_address or "unknown").strip()
    return f"{safe_ip}:{safe_username}"


def _now():
    """Return the current Unix timestamp in seconds."""
    return int(time.time())


def _get_attempt_row(identifier):
    """Fetch a stored login-attempt row for the provided identifier."""
    rows = execute_query("SELECT * FROM login_attempts WHERE identifier = ?", identifier)
    if not rows:
        return None
    return rows[0]


def _get_rate_limit_settings():
    """Load rate-limit window, max-attempt, and block duration from config."""
    return {
        "window_seconds": int(current_app.config.get("LOGIN_RATE_LIMIT_WINDOW_SECONDS", 900)),
        "max_attempts": int(current_app.config.get("LOGIN_RATE_LIMIT_MAX_ATTEMPTS", 5)),
        "block_seconds": int(current_app.config.get("LOGIN_RATE_LIMIT_BLOCK_SECONDS", 900)),
    }


def get_login_block_status(identifier):
    """Return whether the identifier is blocked and how many seconds remain."""
    row = _get_attempt_row(identifier)
    if not row:
        return False, 0

    now = _now()
    blocked_until = int(row.get("blocked_until") or 0)
    if blocked_until > now:
        return True, blocked_until - now

    return False, 0


def register_failed_login(identifier):
    """Record a failed login attempt and return new block status details."""
    settings = _get_rate_limit_settings()
    now = _now()

    row = _get_attempt_row(identifier)
    if not row:
        execute_query(
            """
            INSERT INTO login_attempts (identifier, attempt_count, window_started_at, last_attempt_at, blocked_until)
            VALUES (?, ?, ?, ?, ?)
            """,
            identifier,
            1,
            now,
            now,
            0,
        )
        return False, 0

    blocked_until = int(row.get("blocked_until") or 0)
    if blocked_until > now:
        return True, blocked_until - now

    window_started_at = int(row["window_started_at"])
    if now - window_started_at > settings["window_seconds"]:
        attempt_count = 1
        window_started_at = now
    else:
        attempt_count = int(row["attempt_count"]) + 1

    new_blocked_until = 0
    if attempt_count >= settings["max_attempts"]:
        new_blocked_until = now + settings["block_seconds"]

    execute_query(
        """
        UPDATE login_attempts
        SET attempt_count = ?, window_started_at = ?, last_attempt_at = ?, blocked_until = ?
        WHERE identifier = ?
        """,
        attempt_count,
        window_started_at,
        now,
        new_blocked_until,
        identifier,
    )

    if new_blocked_until > now:
        return True, new_blocked_until - now

    return False, 0


def clear_failed_logins(identifier):
    """Remove stored failed-attempt records after a successful login."""
    execute_query("DELETE FROM login_attempts WHERE identifier = ?", identifier)

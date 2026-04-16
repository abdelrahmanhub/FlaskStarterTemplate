-- Database schema for core user data and login attempt rate limiting.
PRAGMA foreign_keys = ON;

-- Core users table for identity and password hash storage.
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    hash TEXT NOT NULL
);

-- Login attempts table for tracking failures and temporary blocks.
CREATE TABLE IF NOT EXISTS login_attempts (
    identifier TEXT PRIMARY KEY,
    attempt_count INTEGER NOT NULL DEFAULT 0,
    window_started_at INTEGER NOT NULL,
    last_attempt_at INTEGER NOT NULL,
    blocked_until INTEGER NOT NULL DEFAULT 0
);

# Flask Auth Starter Template

A clean, production-minded Flask starter template with:
- User registration and login
- Session management with `Flask-Login`
- SQLite database bootstrap on app startup
- Blueprint-based modular structure
- Reusable HTML layout with Bootstrap + custom CSS
- Example protected routes ready for extension

## Project Overview
This project is a **ready-to-extend Flask foundation** for building authenticated web applications quickly.

It gives you a full auth flow (register, login, logout), protected pages, and a clear structure so you can focus on business features instead of boilerplate setup.

## Tech Stack
- Python
- Flask
- Flask-Login
- Flask-Session (listed in requirements)
- SQLite
- Jinja2 templates + Bootstrap 5

## Architecture Overview
The project follows the **Application Factory pattern** via `create_app()` in `app/__init__.py`.

Key design points:
- Centralized app configuration (`app/config.py`) loaded from `.env`
- Login manager bootstrapped in `app/extensions.py`
- Database helpers in `app/database.py`
- Feature modules split into blueprints:
  - `auth` for authentication routes
  - `main` for core pages
  - `example` for sample protected routes
- Service layer (`app/services/auth_service.py`) separates auth logic from route handlers

## Request And Auth Flow
1. App starts from `run.py` and calls `create_app()`.
2. `create_app()` loads config, initializes Flask-Login, and executes `app/db/schema.sql`.
3. User registers from `/register`:
   - Password is hashed with Werkzeug.
   - User row is inserted into `users`.
   - User is auto-logged in.
4. User logs in from `/login`:
   - Username/password validated against stored hash.
   - `login_user(..., remember=True)` creates authenticated session.
5. Protected routes (`@login_required`) are available only for logged-in users.

## Project Structure
```text
FlaskTemplate/
├─ run.py
├─ requirements.txt
├─ .env.example
├─ README.md
├─ app/
   ├─ __init__.py            # App factory + blueprint registration + schema init
   ├─ config.py              # Environment-based settings
   ├─ extensions.py          # Flask-Login manager + user_loader
   ├─ database.py            # SQLite connection and query helpers
   ├─ db/
   │  ├─ app.db              # SQLite database file
   │  └─ schema.sql          # DB schema bootstrap script
   ├─ models/
   │  └─ user.py             # User model wrapper for Flask-Login
   ├─ services/
   │  ├─ auth_service.py     # Register/login business logic
   │  └─ rate_limit_service.py  # Login attempt tracking and lockouts
   ├─ security.py            # CSRF generation and verification
   ├─ blueprints/
   │  ├─ auth/
   │  │  ├─ __init__.py
   │  │  └─ routes.py        # /login, /register, /logout
   │  ├─ main/
   │  │  ├─ __init__.py
   │  │  └─ routes.py        # /, /profile
   │  └─ example/
   │     ├─ __init__.py
   │     └─ routes.py        # /route1 ... /route5
   ├─ templates/
   │  ├─ layout.html         # Shared layout, navbar, flash notices
   │  ├─ auth/
   │  │  ├─ login.html
   │  │  └─ register.html
   │  ├─ main/
   │  │  ├─ index.html
   │  │  └─ profile.html
   │  └─ examples/
   │     └─ example.html
   └─ static/
      ├─ css/style.css
      ├─ js/script.js
      ├─ images/icon.png
      └─ manifest.webmanifest
```

## Routes Map
| Route | Methods | Access | Purpose |
|---|---|---|---|
| `/login` | GET, POST | Public | Authenticate existing user |
| `/register` | GET, POST | Public | Create new account |
| `/logout` | POST | Authenticated | End session |
| `/` | GET | Authenticated | Home page |
| `/profile` | GET | Authenticated | Current user profile |
| `/route1` ... `/route5` | GET, POST | Authenticated | Sample feature routes |

## Database Schema
Current schema creates:
- `users(id, name, username UNIQUE, hash)`
- `login_attempts(identifier, attempt_count, window_started_at, last_attempt_at, blocked_until)`

This is defined in `app/db/schema.sql` and automatically applied at startup.

## Local Setup
```bash
# 1) Clone
git clone <your-repo-url>
cd FlaskTemplate

# 2) Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 3) Install dependencies
pip install -r requirements.txt

# 4) Create environment file
cp .env.example .env
```

Set `SECRET_KEY` in `.env`.

Generate one quickly:
```python
import secrets
print(secrets.token_hex(32))
```

Run the app:
```bash
python run.py
```

## Environment Variables
| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | Recommended | Flask secret key for sessions/CSRF-related security contexts (required in production) |
| `APP_ENV` | No | Use `development` or `production` |
| `SESSION_COOKIE_SECURE` | No | Set `True` in HTTPS production, keep `False` for local HTTP development |
| `FLASK_DEBUG` | No | Set `True` only during local debugging |
| `LOGIN_RATE_LIMIT_MAX_ATTEMPTS` | No | Maximum failed login attempts allowed inside the time window |
| `LOGIN_RATE_LIMIT_WINDOW_SECONDS` | No | Sliding window duration in seconds for failed login counting |
| `LOGIN_RATE_LIMIT_BLOCK_SECONDS` | No | Lockout duration in seconds after exceeding failed attempts |

## How To Reuse This Template
You can use this repository as a starter for most CRUD or dashboard-style apps:
1. Keep auth and user session flow as-is.
2. Add new blueprints under `app/blueprints/`.
3. Add new tables to `app/db/schema.sql`.
4. Add service modules under `app/services/` for business logic.
5. Build UI pages in `app/templates/` and `app/static/`.

## Notes
- CSRF protection is enabled for unsafe methods (`POST`, `PUT`, `PATCH`, `DELETE`) using per-session tokens.
- Logout now uses `POST` for safer session termination behavior.
- Login rate limiting is enabled by default and blocks repeated failed attempts.
- `Flask-Session` is listed in dependencies but not yet initialized in code; add it if server-side session storage is required.

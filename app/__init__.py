"""Create and configure the Flask application instance."""

import os
from flask import Flask
from .database import execute_script
from .config import Config
from .extensions import login_manager
from .security import generate_csrf_token, validate_csrf_token
from .blueprints.auth import auth_bp
from .blueprints.main import main_bp
from .blueprints.example import example_bp

def create_app(config_overrides=None):
    """Build the Flask app, load config, and register all integrations."""
    app = Flask(__name__, 
                template_folder="templates", 
                static_folder="static")

    app.config.from_object(Config)
    if config_overrides:
        app.config.update(config_overrides)

    if not app.config.get("SECRET_KEY"):
        raise RuntimeError("SECRET_KEY must be set when APP_ENV=production.")

    login_manager.init_app(app)

    @app.context_processor
    def inject_csrf_token():
        """Expose a CSRF token helper to all Jinja templates."""
        return {"csrf_token": generate_csrf_token}

    @app.before_request
    def protect_against_csrf():
        """Validate CSRF tokens before processing unsafe HTTP requests."""
        validate_csrf_token()

    with app.app_context():
        schema_path = os.path.join(os.path.dirname(__file__), "db", "schema.sql")
        if os.path.exists(schema_path):
            try:
                with open(schema_path, "r", encoding='utf-8') as f:
                    execute_script(f.read().strip())
            except Exception as e:
                print(f"Database Init Error: {e}")

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(example_bp)

    return app

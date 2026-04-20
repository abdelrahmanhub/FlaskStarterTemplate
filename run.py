"""Application entrypoint for running the Flask development server."""

import os

from app import create_app

if __name__ == '__main__':
    app = create_app()
    debug_mode = os.getenv("FLASK_DEBUG", "False").strip().lower() == "true"
    app.run(host='0.0.0.0', debug=debug_mode)
    

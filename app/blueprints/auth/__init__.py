"""Auth blueprint registration for authentication-related routes."""

from flask import Blueprint

auth_bp = Blueprint("auth", __name__, template_folder="templates", static_folder="static")
from . import routes

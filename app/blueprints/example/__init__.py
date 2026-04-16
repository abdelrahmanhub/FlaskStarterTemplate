"""Example blueprint registration for sample protected endpoints."""

from flask import Blueprint

example_bp = Blueprint("example", __name__, template_folder="templates", static_folder="static")
from . import routes

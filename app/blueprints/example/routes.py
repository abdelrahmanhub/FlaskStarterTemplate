"""Example protected routes used as placeholders for future features."""

from . import example_bp
from flask import render_template
from flask_login import login_required, current_user

@example_bp.route("/route1", methods=["GET", "POST"])
@login_required
def route1():
    """Render example page for sample route 1."""
    return render_template("examples/example.html", user=current_user)


@example_bp.route("/route2", methods=["GET", "POST"])
@login_required
def route2():
    """Render example page for sample route 2."""
    return render_template("examples/example.html", user=current_user)


@example_bp.route("/route3", methods=["GET", "POST"])
@login_required
def route3():
    """Render example page for sample route 3."""
    return render_template("examples/example.html", user=current_user)


@example_bp.route("/route4", methods=["GET", "POST"])
@login_required
def route4():
    """Render example page for sample route 4."""
    return render_template("examples/example.html", user=current_user)


@example_bp.route("/route5", methods=["GET", "POST"])
@login_required
def route5():
    """Render example page for sample route 5."""
    return render_template("examples/example.html", user=current_user)

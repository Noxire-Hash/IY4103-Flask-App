from functools import wraps

from flask import flash, redirect, session, url_for


# Add this to routes with login required
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            flash("You must be logged in to access this page", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


# Add this to routes with admin access required
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            flash("You must be logged in to access this page", "warning")
            return redirect(url_for("login"))
        if session.get("privilege_id") != 999:
            flash("Admin access required for this page", "warning")
            return redirect(url_for("home"))
        return f(*args, **kwargs)

    return decorated_function


# Add this to routes with moderator access required
def moderator_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            flash("You must be logged in to access this page", "warning")
            return redirect(url_for("login"))
        if session.get("privilege_id") <= 998:
            flash("Moderator access required for this page", "warning")
            return redirect(url_for("home"))
        return f(*args, **kwargs)

    return decorated_function

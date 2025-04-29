from flask import (
    Blueprint,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from models import User, db
from utils import Logger

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session["user_id"] = user.id
            session["username"] = user.username
            session["privilege_id"] = user.privilege_id
            flash("Login successful!", "success")
            Logger.info(f"Login successful: {user.id}")
            response = make_response(redirect(url_for("home")))
            response.set_cookie(
                key="user_id",
                value=str(user.id),
                max_age=2592000,  # 30 days in seconds
                path="/",
                httponly=True,
                samesite="Lax",
            )
            Logger.info(f"Direct cookie set for user_id: {user.id}")
            return response
        else:
            Logger.error(f"Invalid email or password: {email} {password}")
            flash("Invalid email or password!", "danger")
            return redirect(url_for("login"))

    return render_template("auth/login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        username = request.form.get("username")

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            Logger.error(f"User already exists: {email}")
            flash(
                "User already exists! if you forgot your password, please reset it.",
                "danger",
            )
            return redirect(url_for("register"))

        # Create new user
        new_user = User(
            email=email,
            password=password,
            username=username,
            privilege_id=1,
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful!", "success")
        Logger.info(f"Registration successful: {new_user.id}")
        session["user_id"] = new_user.id
        session["username"] = new_user.username
        session["privilege_id"] = new_user.privilege_id

        response = make_response(redirect(url_for("home")))
        response.set_cookie(
            key="user_id",
            value=str(new_user.id),
            max_age=2592000,  # 30 days in seconds
            path="/",
            httponly=True,
            samesite="Lax",
        )
        Logger.info(f"Direct cookie set for user_id: {new_user.id}")
        return response

    return render_template("auth/register.html")


@auth_bp.route("/logout")
def logout():
    response = make_response(redirect(url_for("home")))
    response.delete_cookie("user_id", path="/")
    session.clear()
    flash("You have been logged out.", "success")
    return response

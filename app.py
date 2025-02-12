import datetime
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask, send_from_directory, send_file, request, redirect, url_for, flash, render_template, session, make_response
from models import User, Privilege, Vendor, Purchase, Item, Subscription, db, ITEM_STATUS
from helper import find_user_from_id, json_interpreter


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def home():
    if session.get("user_id") == None:
        try:
            getCookie()
            print("Should work")
        except:
            print("No cookies found")
    print(session.get("user_id"))
    return render_template("index.html")


@app.route("/store")
def store():
    return render_template("store.html")


@app.route("/news")
def news():
    return send_from_directory("static/pages", "news.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Debug print
        print(f"Received: {username}, {email}, {password}")

        # Check if the email is already registered
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email is already registered.", "danger")
            return redirect(url_for("register"))

        # Add user to the database
        try:
            user = User(username=username, email=email,
                        password=password, privilege_id=1)
            db.session.add(user)
            db.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for("login"))
        except Exception as err:
            db.session.rollback()
            flash(f"An error occurred: {err}", "danger")
            print(f"Database Error: {err}")
            return redirect(url_for("register"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Query the user by email and plain-text password
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session["user_id"] = user.id
            session["username"] = user.username
            session["privilege_id"] = user.privilege_id
            flash("Login successful!", "success")
            setCookie()
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password!", "danger")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/account", methods=["GET", "POST"])
def send():
    return render_template("myaccount_template.html")


@app.route("/test_db")
def test_db():
    try:
        test_user = User(username="testuser", email="test@test.com",
                         password="1234", privilege_id=1)
        db.session.add(test_user)
        db.session.commit()
        print("User added successfully.")
        return "User added successfully."
    except Exception as e:
        db.session.rollback()
        print(f"Error: {e}")
        return f"Error: {e}"


@app.route("/test_flash")
def test_flash():
    flash("This is a success message!", "success")
    flash("This is a warning message!", "warning")
    flash("This is an error message!", "danger")
    return redirect(url_for("home"))


@app.route("/admin", methods=["GET", "POST"])
def admin_dashboard():
    # Restrict access to admin users
    if session.get("privilege_id") != 999:  # Assuming 2 is Admin privilege ID
        flash("Access denied! Admins only.", "danger")
        return redirect(url_for("home"))

    # Fetch all users and privileges
    users = User.query.all()
    privileges = Privilege.query.all()

    # Handle Create User
    if request.method == "POST" and "create_user" in request.form:
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        privilege_id = request.form.get("privilege_id")

        # Check if email is already registered
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("A user with this email already exists.", "danger")
        else:
            try:
                new_user = User(username=username, email=email,
                                password=password, privilege_id=privilege_id)
                db.session.add(new_user)
                db.session.commit()
                flash(f"User {username} created successfully!", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Error creating user: {e}", "danger")
        return redirect(url_for("admin_dashboard"))

    return render_template("admin.html", users=users, privileges=privileges)


@app.route("/admin/delete_user/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    # Restrict access to admin users
    if session.get("privilege_id") != 999:
        flash("Access denied! Admins only.", "danger")
        return redirect(url_for("home"))

    try:
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        flash(f"User {user.username} deleted successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting user: {e}", "danger")
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/update_user/<int:user_id>", methods=["POST"])
def update_user(user_id):
    # Restrict access to admin users
    if session.get("privilege_id") != 999:
        flash("Access denied! Admins only.", "danger")
        return redirect(url_for("home"))

    try:
        user = User.query.get(user_id)
        user.username = request.form.get("username")
        user.email = request.form.get("email")
        user.privilege_id = request.form.get("privilege_id")
        db.session.commit()
        flash(f"User {user.username} updated successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error updating user: {e}", "danger")
    return redirect(url_for("admin_dashboard"))


@app.route("/get_user_data", methods=["POST"])
def get_user_data():
    user_id = session.get("user_id")
    if user_id:
        print(find_user_from_id(user_id))
        print(type(find_user_from_id(user_id)))
        return find_user_from_id(user_id), 200
    else:
        return {"error": "User not logged in"}, 401


@app.route("/setCookie", methods=["POST", "GET"])
def setCookie():
    user_id = session.get("user_id")
    response = make_response(redirect(url_for("home")))
    response.set_cookie(key="user_id", value=str(user_id))
    return response


@app.route("/getCookie", methods=["POST", "GET"])
def getCookie():
    user_id = request.cookies.get("user_id")
    user = User.query.filter_by(id=user_id).first()
    session["user_id"] = user.id
    session["username"] = user.username
    session["privilege_id"] = user.privilege_id
    flash("Login successful!", "success")


@app.route("/vendor/dashboard", methods=["GET", "POST"])
def vendor_dashboard():
    items = Item.query.all()
    current_user_id = session.get("user_id")

    # Debug prints
    print(f"Current user ID: {current_user_id}")
    print("Items in database:")
    for item in items:
        print(
            f"Item ID: {item.id}, Name: {item.name}, Vendor ID: {item.vendor_id}")

    return render_template("vendor_dashboard.html", items=items)


@app.route("/vendor/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        name = request.form.get("product_name")
        description = request.form.get("product_description")
        price = request.form.get("product_price")
        category = request.form.get("product_category")
        tags = request.form.get("product_tags")
        vendor_id = session.get("user_id")

        # Validate required fields
        if not all([name, description, price, category, vendor_id]):
            flash("All fields except tags are required!", "danger")
            return redirect(url_for("vendor_dashboard"))

        try:
            new_item = Item(
                name=name,
                description=description,
                price=float(price),
                category=category,
                tags=tags,
                vendor_id=vendor_id
            )
            db.session.add(new_item)
            db.session.commit()
            flash("Item added successfully!", "success")
            return redirect(url_for("vendor_dashboard"))
        except ValueError:
            flash("Invalid price format!", "danger")
            return redirect(url_for("vendor_dashboard"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding item: {e}", "danger")
            return redirect(url_for("vendor_dashboard"))

    return render_template("vendor_dashboard.html")


@app.route("/vendor/delete_item/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    # Check if user is logged in and is the vendor of the item
    if not session.get("user_id"):
        flash("Please log in first!", "danger")
        return redirect(url_for("login"))

    try:
        item = Item.query.get(item_id)

        # Check if item exists
        if not item:
            flash("Item not found!", "danger")
            return redirect(url_for("vendor_dashboard"))

        # Check if the logged-in user is the vendor of this item
        if item.vendor_id != session.get("user_id"):
            flash("You don't have permission to delete this item!", "danger")
            return redirect(url_for("vendor_dashboard"))

        # Delete the item
        db.session.delete(item)
        db.session.commit()
        flash("Item deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting item: {e}", "danger")

    return redirect(url_for("vendor_dashboard"))


if __name__ == '__main__':
    app.run(debug=True)

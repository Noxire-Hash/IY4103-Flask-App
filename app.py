import os
from datetime import timedelta
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, send_from_directory, send_file, request, redirect, url_for, flash, render_template, session, make_response
from models import User, Privilege, Vendor, Purchase, Item, Subscription, db, ITEM_STATUS, SupportTicket, SupportTicketResponse, TICKET_CATEGORIES, TICKET_STATUS
from helper import find_user_from_id, json_interpreter

# App setup
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
migrate = Migrate(app, db)
db.init_app(app)

# Basic page routes


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


@app.route("/item_preview")
def item_preview():
    return render_template("item_preview.html")


@app.route("/news")
def news():
    return send_from_directory("static/pages", "news.html")


@app.route("/about")
def about():
    return render_template("about.html")

# Auth routes


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
                        password=password, privilege_id=999)
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
        test_user = User.query.filter_by(username="testuser", email="test@test.com",
                                         password="1234", privilege_id=1).first()
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

# Admin routes


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


@app.route("/get_item_data_from_id/<int:item_id>")
def get_item_data(item_id):
    pass


@app.route("/get_username_from_id/<int:user_id>")
def get_username_from_id(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user.username

# Cookie management


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


@app.route("/get_items", methods=["POST", "GET"])
def get_items():
    # May god forgive me for what about to do
    items = Item.query.all()
    item_dict = {}
    for item in items:
        vendor_name = get_username_from_id(item.vendor_id)
        item_dict[item.id] = {
            "name": item.name,
            "description": item.description,
            "price": item.price,
            "vendor_id": item.vendor_id,
            "vendor_name": vendor_name,
            "category": item.category,
            "tags": item.tags,
            "sales": item.sales,
            "status": item.status,
            "created_at": str(item.created_at)
        }
    return json_interpreter(item_dict)


@app.errorhandler(404)
def err_404(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def err_500():
    return render_template("500.html")


# Vendor routes


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


@app.route("/test_error")
def test_error():
    raise Exception("This is a test error!")

# Support ticket routes


@app.route("/support", methods=["GET", "POST"])
def support():
    if not session.get("user_id"):
        flash("Please log in to submit a support ticket.", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        category = request.form.get("category")
        subject = request.form.get("subject")
        message = request.form.get("message")

        if not all([category, subject, message]):
            flash("Please fill in all fields.", "danger")
            return redirect(url_for("support"))

        try:
            ticket = SupportTicket(
                user_id=session["user_id"],
                category=category,
                subject=subject,
                message=message
            )
            db.session.add(ticket)
            db.session.commit()
            flash("Your support ticket has been submitted successfully!", "success")
            return redirect(url_for("support"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error submitting ticket: {e}", "danger")
            return redirect(url_for("support"))

    # Get user's tickets for display
    tickets = SupportTicket.query.filter_by(user_id=session["user_id"]).order_by(
        SupportTicket.created_at.desc()).all()
    return render_template("support.html", tickets=tickets, categories=TICKET_CATEGORIES)


def reply_ticket():
    if not session.get("user_id"):
        flash("Please log in to reply a support ticket", "warning")
        return redirect(url_for("login"))
    return render_template("user_reply_ticket.html")


@app.route("/support/reply_ticket/<int:ticket_id>", methods=["GET", "POST"])
def user_reply_ticket(ticket_id):
    if not session.get("user_id"):
        flash("Please log in to reply to a support ticket", "warning")
        return redirect(url_for("login"))

    ticket = SupportTicket.query.get_or_404(ticket_id)

    # Check if the ticket belongs to the user
    if ticket.user_id != session.get("user_id"):
        flash("You don't have permission to view this ticket", "danger")
        return redirect(url_for("support"))

    if request.method == "POST":
        response = request.form.get("response")
        if response:
            try:
                ticket_response = SupportTicketResponse(
                    ticket_id=ticket.id,
                    responder_id=session["user_id"],
                    response=response,
                    is_user=True  # Use boolean instead of 1
                )
                db.session.add(ticket_response)
                db.session.commit()
                flash("Reply sent successfully!", "success")
            except Exception as e:
                db.session.rollback()
                flash(f"Error sending reply: {e}", "danger")

    # Get responses using the relationship
    responses = ticket.responses.all()

    return render_template("user_reply_ticket.html", ticket=ticket, responses=responses)


# Moderator routes
@app.route("/moderator/dashboard", methods=["GET", "POST"])
def moderator_dashboard():
    tickets = SupportTicket.query.all()
    return render_template("moderator_dashboard.html", tickets=tickets, get_username_from_id=get_username_from_id)


@app.route("/moderator/view_ticket/<int:ticket_id>", methods=["GET"])
def view_ticket(ticket_id):
    if session.get("privilege_id") < 998:
        flash("Access denied! Moderators only.", "danger")
        return redirect(url_for("home"))

    ticket = SupportTicket.query.get_or_404(ticket_id)
    user = User.query.get(ticket.user_id)
    purchases = Purchase.query.filter_by(user_id=ticket.user_id).all()

    # Get responses and convert to list
    responses = ticket.responses.all()  # This uses the relationship we defined

    return render_template(
        "moderator_view_ticket.html",
        ticket=ticket,
        user=user,
        purchases=purchases,
        responses=responses,  # Pass responses separately
        get_username_from_id=get_username_from_id,
        TICKET_STATUS=TICKET_STATUS
    )


@app.route("/moderator/respond/<int:ticket_id>", methods=["POST"])
def moderator_respond(ticket_id):
    if session.get("privilege_id") < 998:
        flash("Access denied! Moderators only.", "danger")
        return redirect(url_for("home"))

    ticket = SupportTicket.query.get_or_404(ticket_id)
    response = request.form.get("response")
    new_status = request.form.get("status")

    if response:
        try:
            # Create the response
            ticket_response = SupportTicketResponse(
                ticket_id=ticket.id,
                responder_id=session["user_id"],
                response=response,
                is_user=False  # This is a moderator response
            )

            # Update ticket status
            ticket.status = new_status

            db.session.add(ticket_response)
            db.session.commit()
            flash("Response sent successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error sending response: {e}", "danger")

    return redirect(url_for('view_ticket', ticket_id=ticket_id))

# Session management


@app.before_request
def make_session_permanent():
    if session.get("user_id"):
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=5)
    else:
        try:
            getCookie()

        except:
            print("No cookies found")


if __name__ == '__main__':
    app.run(debug=True)

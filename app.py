import os
from datetime import timedelta

from flask import (
    Flask,
    flash,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from flask_migrate import Migrate

import grindstone.main as grindstone
from models import (
    ITEM_STATUS,
    SYSTEM_ID,
    TICKET_CATEGORIES,
    TICKET_STATUS,
    Item,
    Privilege,
    Purchase,
    SupportTicket,
    SupportTicketResponse,
    SystemTransaction,
    User,
    db,
)
from utils import Logger
from utils import SystemTransactionHandler as sth

# App setup
app = Flask(
    __name__,
    static_url_path="/static",  # Change this line
    static_folder="static",
)
app.secret_key = os.urandom(24)
app.config.update(
    SESSION_COOKIE_SECURE=False,  # Set to True in production
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=60),
    SESSION_REFRESH_EACH_REQUEST=True,
)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = True
migrate = Migrate(app, db)
logger = Logger()
db.init_app(app)


@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store"
    return response


# Basic page routes


@app.route("/")
def home():
    try:
        if session.get("user_id") is None:
            try:
                getCookie()
            except Exception as e:
                print(f"No cookies found: {e}")
        return render_template("index.html")
    except OSError:
        session.clear()
        return render_template("index.html")


@app.route("/store")
def store():
    return render_template("store.html")


@app.route("/store/item/<int:item_id>")
def item_preview(item_id):
    if not session.get("user_id"):
        flash("Please log in to view items", "warning")
        return redirect(url_for("login"))

    try:
        # Get item data
        item = Item.query.get_or_404(item_id)
        vendor = User.query.get_or_404(
            item.vendor_id
        )  # Use get_or_404 to ensure vendor exists

        return render_template(
            "item_preview.html",
            item=item,
            vendor=vendor,
            similar_items=[],  # Simplified for now
        )

    except Exception as e:
        print(f"Error in item_preview: {e}")
        flash("Error loading item details", "danger")
        return redirect(url_for("store"))


@app.route("/news")
def news():
    return send_from_directory("static/pages", "news.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/lore")
def lore():
    return render_template("lore.html")


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
            user = User(
                username=username, email=email, password=password, privilege_id=999
            )
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
def account():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user = User.query.get(session.get("user_id"))
    if not user:
        session.clear()
        return redirect(url_for("login"))

    # Get recent purchases
    purchases = (
        Purchase.query.filter_by(user_id=user.id)
        .order_by(Purchase.purchase_date.desc())
        .limit(5)
        .all()
    )

    # Load item data for each purchase
    for purchase in purchases:
        purchase.item_name = (
            Item.query.get(purchase.item_id).name if purchase.item_id else "N/A"
        )
        purchase.item_status = (
            "Completed"  # Or get from the actual status field if available
        )

    # Get recent transactions
    transactions = (
        SystemTransaction.query.filter(
            (SystemTransaction.sender_id == user.id)
            | (SystemTransaction.receiver_id == user.id)
        )
        .order_by(SystemTransaction.created_at.desc())
        .limit(10)
        .all()
    )

    # For each transaction, manually get the sender and receiver usernames
    for transaction in transactions:
        # Get sender username if it's a user (not a system or payment provider)
        if transaction.sender_id > 0:
            sender = User.query.get(transaction.sender_id)
            transaction.sender_name = sender.username if sender else "Unknown"
        else:
            transaction.sender_name = (
                "System" if transaction.sender_id == SYSTEM_ID else "Payment Provider"
            )

        # Get receiver username
        receiver = User.query.get(transaction.receiver_id)
        transaction.receiver_name = receiver.username if receiver else "Unknown"

    return render_template(
        "myaccount_template.html",
        purchases=purchases,
        transactions=transactions,
        user=user,
    )


@app.route("/test_db")
def test_db():
    try:
        test_user = User.query.filter_by(
            username="testuser", email="test@test.com", password="1234", privilege_id=1
        ).first()
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
                new_user = User(
                    username=username,
                    email=email,
                    password=password,
                    privilege_id=privilege_id,
                )
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
def admin_update_user(user_id):
    if session.get("privilege_id") != 999:
        return jsonify({"error": "Access denied"}), 403

    try:
        user = User.query.get_or_404(user_id)

        # Update basic info if provided
        if "username" in request.form:
            user.username = request.form.get("username")
        if "email" in request.form:
            user.email = request.form.get("email")
        if "privilege_id" in request.form:
            user.privilege_id = request.form.get("privilege_id")

        # Update password if provided and not empty
        new_password = request.form.get("password")
        if new_password:
            user.password = new_password

        # Update balance if provided
        if "balance" in request.form:
            new_balance = float(request.form.get("balance"))
            if new_balance != user.balance:
                # Create a system transaction to adjust the balance
                difference = new_balance - float(user.balance)
                if difference > 0:
                    # Add funds
                    sth.create_and_process(
                        amount=difference,
                        sender_id=SYSTEM_ID,
                        receiver_id=user.id,
                        transaction_type="ADMIN_ADJUSTMENT",
                        logger=logger,
                    )
                else:
                    # Remove funds
                    sth.create_and_process(
                        amount=abs(difference),
                        sender_id=user.id,
                        receiver_id=SYSTEM_ID,
                        transaction_type="ADMIN_ADJUSTMENT",
                        logger=logger,
                    )

        db.session.commit()
        return jsonify({"success": True})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/admin/create_transaction", methods=["POST"])
def admin_create_transaction():
    if session.get("privilege_id") != 999:
        flash("Access denied! Admins only.", "danger")
        return redirect(url_for("admin_dashboard"))

    try:
        amount = float(request.form.get("amount"))
        transaction_type = request.form.get("transaction_type")
        sender_type = request.form.get("sender_type")
        receiver_id = int(request.form.get("receiver_id"))

        # Determine sender_id based on sender_type
        if sender_type == "payment_provider":
            sender_id = int(request.form.get("payment_provider"))
        elif sender_type == "system":
            sender_id = int(request.form.get("system_id", SYSTEM_ID))
        else:
            sender_id = int(request.form.get("sender_id"))

        success, message, receipt_id = sth.create_and_process(
            amount=amount,
            sender_id=sender_id,
            receiver_id=receiver_id,
            transaction_type=transaction_type,
            logger=logger,
        )

        if success:
            flash("Transaction created successfully!", "success")
        else:
            flash(f"Transaction failed: {message}", "danger")

    except Exception as e:
        flash(f"Error creating transaction: {str(e)}", "danger")

    return redirect(url_for("admin_dashboard"))


@app.route("/admin/get_user/<int:user_id>")
def admin_get_user(user_id):
    if session.get("privilege_id") != 999:
        return jsonify({"error": "Access denied"}), 403

    try:
        user = User.query.get_or_404(user_id)
        return jsonify(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "balance": int(user.balance),
                "privilege_id": user.privilege_id,
            }
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get_user_data", methods=["POST"])
def get_user_data():
    try:
        user_id = session.get("user_id")
        if user_id:
            user = User.query.get(user_id)
            if user:
                user_data = {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "privilege_id": user.privilege_id,
                    "created_at": user.created_at.strftime("%Y-%m-%d"),
                    "balance": user.balance,
                    "pending_balance": user.pending_balance,
                    "subscriptions": user.subscriptions,
                }
                return user_data, 200
            return {"error": "User not found"}, 404
        return {"error": "User not logged in"}, 401
    except Exception as e:
        print(f"Error in get_user_data: {e}")
        return {"error": "Server error"}, 500


@app.route("/get_item_data_from_id/<int:item_id>")
def get_item_data_from_id(item_id):
    try:
        item = Item.query.get_or_404(item_id)
        vendor = User.query.get(item.vendor_id)

        item_data = {
            "id": item.id,
            "name": item.name,
            "description": item.description,
            "price": item.price,
            "vendor_name": vendor.username,
            "sales": item.sales,
            "tags": item.tags,
            "status": item.status,
        }

        return jsonify(item_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


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
    try:
        user_id = request.cookies.get("user_id")
        if user_id is not None:
            user = User.query.filter_by(id=user_id).first()
            if user:
                session["user_id"] = user.id
                session["username"] = user.username
                session["privilege_id"] = user.privilege_id
                flash("Login successful!", "success")
    except Exception as e:
        print(f"Error getting cookie: {e}")
        session.clear()
    return redirect(url_for("home"))


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
            "created_at": str(item.created_at),
        }
    return jsonify(item_dict)


@app.errorhandler(404)
def err_404(error):
    return render_template("404.html"), 404


@app.errorhandler(500)
def err_500():
    return render_template("500.html")


# Vendor routes


@app.route("/vendor/dashboard", methods=["GET", "POST"])
def vendor_dashboard():
    try:
        # Check if user is logged in
        if not session.get("user_id"):
            flash("Please log in to access vendor dashboard", "warning")
            return redirect(url_for("login"))

        # Get vendor's items
        vendor_items = Item.query.filter_by(vendor_id=session.get("user_id")).all()

        return render_template(
            "vendor_dashboard.html", items=vendor_items, ITEM_STATUS=ITEM_STATUS
        )
    except Exception:
        flash("Error accessing vendor dashboard", "danger")
        return redirect(url_for("home"))


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
                vendor_id=vendor_id,
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


@app.route("/vendor/edit_item/<int:item_id>", methods=["GET", "POST"])
def edit_item(item_id):
    try:
        if not session.get("user_id"):
            flash("Please log in first!", "danger")
            return redirect(url_for("login"))

        item = Item.query.get_or_404(item_id)

        # Check if the logged-in user is the vendor of this item
        if item.vendor_id != session.get("user_id"):
            flash("You don't have permission to edit this item!", "danger")
            return redirect(url_for("vendor_dashboard"))

        if request.method == "POST":
            try:
                # Update item details
                item.name = request.form.get("product_name")
                item.description = request.form.get("product_description")
                item.price = float(request.form.get("product_price"))
                item.category = request.form.get("product_category")
                item.tags = request.form.get("product_tags")
                item.status = request.form.get("product_status")

                db.session.commit()
                flash("Item updated successfully!", "success")
                return redirect(url_for("vendor_dashboard"))
            except ValueError:
                flash("Invalid price format!", "danger")
            except Exception:
                db.session.rollback()
                flash("Error updating item", "danger")

        return render_template(
            "vendor_item_edit.html", item=item, ITEM_STATUS=ITEM_STATUS
        )

    except Exception:
        flash("Error accessing item", "danger")
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
                message=message,
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
    tickets = (
        SupportTicket.query.filter_by(user_id=session["user_id"])
        .order_by(SupportTicket.created_at.desc())
        .all()
    )
    return render_template(
        "support.html", tickets=tickets, categories=TICKET_CATEGORIES
    )


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
                    is_user=True,  # Use boolean instead of 1
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
    return render_template(
        "moderator_dashboard.html",
        tickets=tickets,
        get_username_from_id=get_username_from_id,
    )


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
        TICKET_STATUS=TICKET_STATUS,
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
                is_user=False,  # This is a moderator response
            )

            # Update ticket status
            ticket.status = new_status

            db.session.add(ticket_response)
            db.session.commit()
            flash("Response sent successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error sending response: {e}", "danger")

    return redirect(url_for("view_ticket", ticket_id=ticket_id))


# Session management


@app.before_request
def before_request():
    try:
        if session.get("user_id"):
            session.permanent = True
        else:
            getCookie()
    except Exception:
        session.clear()


@app.route("/deposit", methods=["GET", "POST"])
def deposit_funds():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            amount = float(data.get("amount", 0))
            payment_provider = data.get("payment_provider")

            if not session.get("user_id"):
                return jsonify(
                    {"success": False, "message": "Please log in to make a deposit"}
                )

            if amount < 10:
                return jsonify(
                    {"success": False, "message": "Minimum deposit amount is 10 AW"}
                )

            try:
                # Create and process transaction using SystemTransactionHandler
                success, message, receipt_id = sth.create_and_process(
                    amount=amount,
                    sender_id=payment_provider,
                    receiver_id=session["user_id"],
                    transaction_type="DEPOSIT",
                    logger=logger,
                )

                if success:
                    return jsonify(
                        {
                            "success": True,
                            "message": "Deposit successful!",
                            "redirect_url": url_for("account"),
                        }
                    )
                else:
                    return jsonify({"success": False, "message": message})

            except Exception as e:
                return jsonify({"success": False, "message": str(e)})
        else:
            # Handle form-based submission
            amount = float(request.form.get("amount", 0))
            payment_provider = request.form.get("payment_provider")

            if amount < 10:
                flash("Minimum deposit amount is 10 AW", "error")
                return redirect(url_for("deposit"))

            try:
                # Create and process transaction using SystemTransactionHandler
                success, message, receipt_id = sth.create_and_process(
                    amount=amount,
                    sender_id=payment_provider,
                    receiver_id=session["user_id"],
                    transaction_type="DEPOSIT",
                    logger=logger,
                )

                if success:
                    flash("Deposit successful!", "success")
                    return redirect(url_for("account"))
                else:
                    flash(f"Deposit failed: {message}", "danger")
                    return redirect(url_for("deposit"))

            except Exception as e:
                flash(str(e), "error")
                return redirect(url_for("deposit"))

    return render_template("checkout_deposit.html")


@app.route("/transfer", methods=["POST"])
def transfer_funds():
    try:
        amount = float(request.form.get("amount"))
        receiver_id = int(request.form.get("receiver_id"))
        sender_id = session.get("user_id")

        if not sender_id:
            flash("Please log in to make a transfer", "warning")
            return redirect(url_for("login"))

        # Use the new SystemTransactionHandler
        success, message, receipt_id = sth.create_and_process(
            amount=amount,
            sender_id=sender_id,
            receiver_id=receiver_id,
            transaction_type="TRANSFER",
            logger=logger,
        )

        if success:
            flash("Transfer successful!", "success")
        else:
            flash(f"Transfer failed: {message}", "danger")

        return redirect(url_for("account"))

    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for("account"))


@app.route("/check_static")
def check_static():
    import os

    static_path = os.path.join(app.static_folder, "scripts", "index.js")
    exists = os.path.exists(static_path)
    return f"Static file exists: {exists}, Path: {static_path}"


# Add this to ensure static files are served with correct paths
app.config["APPLICATION_ROOT"] = "/"


# Add a route specifically for JavaScript files
@app.route("/js/<path:filename>")
def serve_js(filename):
    return send_from_directory("static/scripts", filename)


@app.route("/checkout/<int:item_id>")
def checkout(item_id):
    print(f"Debug: Checkout called with item_id: {item_id}")  # Debug print
    print(f"Debug: User ID: {session.get('user_id')}")  # Debug print

    if not session.get("user_id"):
        flash("Please log in to continue", "warning")
        return redirect(url_for("login"))

    try:
        user = User.query.get_or_404(session.get("user_id"))
        item = Item.query.get_or_404(item_id)
        vendor = User.query.get_or_404(item.vendor_id)

        print(f"Debug: Found item: {item.name}")  # Debug print
        print(f"Debug: Found vendor: {vendor.username}")  # Debug print

        return render_template("checkout.html", user=user, item=item, vendor=vendor)
    except Exception as e:
        print(f"Debug: Error in checkout: {e}")  # Debug print
        flash("Error loading checkout", "danger")
        return redirect(url_for("store"))


@app.route("/process_payment", methods=["POST"])
def process_payment():
    try:
        item_id = request.form.get("item_id")
        if not item_id:
            flash("No item specified", "danger")
            return redirect(url_for("store"))

        item = Item.query.get_or_404(item_id)
        user_id = session.get("user_id")

        if not user_id:
            flash("Please log in to make a purchase", "warning")
            return redirect(url_for("login"))

        # Use the new SystemTransactionHandler
        success, message, receipt_id = sth.create_and_process(
            amount=item.price,
            sender_id=user_id,
            receiver_id=item.vendor_id,
            transaction_type="PURCHASE",
            item_id=item.id,
            quantity=1,
            logger=logger,
        )

        if success:
            flash("Purchase successful!", "success")
            return redirect(url_for("account"))
        else:
            flash(f"Purchase failed: {message}", "danger")
            return redirect(url_for("checkout", item_id=item_id))

    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for("store"))


@app.route("/checkout/deposit", methods=["GET", "POST"])
def deposit():
    return render_template("checkout_deposit.html")


@app.route("/debug")
def debug():
    return render_template("debug.html")


@app.route("/api/game_data")
def get_game_data():
    game_data = {
        "biomes": grindstone.BIOM_DATA,
        "equipment": {
            "starter_kit": grindstone.STARTER_KIT,
            "debug_kit": grindstone._DEBUG_KIT,
        },
        "tools": grindstone.TOOL_DATA,
        "inventory": grindstone.LOAD_INV_DATA,
    }
    return jsonify(game_data)


@app.route("/account/transactions", methods=["GET"])
def transaction_history():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    user = User.query.get(session.get("user_id"))
    if not user:
        session.clear()
        return redirect(url_for("login"))

    # Get all transactions for this user
    transactions = (
        SystemTransaction.query.filter(
            (SystemTransaction.sender_id == user.id)
            | (SystemTransaction.receiver_id == user.id)
        )
        .order_by(SystemTransaction.created_at.desc())
        .all()
    )

    # Calculate transaction statistics
    total_spent = 0
    total_received = 0

    for transaction in transactions:
        # For each transaction, manually get the sender and receiver usernames
        if transaction.sender_id > 0:
            sender = User.query.get(transaction.sender_id)
            transaction.sender_name = sender.username if sender else "Unknown"
        else:
            transaction.sender_name = (
                "System" if transaction.sender_id == SYSTEM_ID else "Payment Provider"
            )

        # Get receiver username
        receiver = User.query.get(transaction.receiver_id)
        transaction.receiver_name = receiver.username if receiver else "Unknown"

        # Calculate totals
        if transaction.sender_id == user.id:
            total_spent += transaction.amount
        if transaction.receiver_id == user.id:
            total_received += transaction.amount

        # Add default notes if none exist
        if not transaction.notes:
            if transaction.transaction_type == "DEPOSIT":
                transaction.notes = (
                    f"Deposit of {transaction.amount} AW from payment provider"
                )
            elif transaction.transaction_type == "PURCHASE":
                transaction.notes = f"Purchase transaction of {transaction.amount} AW"
            elif transaction.transaction_type == "TRANSFER":
                if transaction.sender_id == user.id:
                    transaction.notes = f"Transfer of {transaction.amount} AW to {transaction.receiver_name}"
                else:
                    transaction.notes = f"Transfer of {transaction.amount} AW from {transaction.sender_name}"
            elif transaction.transaction_type == "REFUND":
                transaction.notes = f"Refund of {transaction.amount} AW"
            else:
                transaction.notes = f"{transaction.transaction_type} transaction of {transaction.amount} AW"

    return render_template(
        "account_receipt_history.html",
        user=user,
        transactions=transactions,
        total_spent=total_spent,
        total_received=total_received,
        transaction_count=len(transactions),
    )


if __name__ == "__main__":
    app.run(debug=True)

from flask import render_template, redirect, url_for, flash, session, request, Blueprint
from wrapers import login_required
from models import Item, ITEM_STATUS, db

vendor_bp = Blueprint("vendor", __name__, url_prefix="/vendor")

@vendor_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
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
    except Exception as e:
        flash(f"Error accessing vendor dashboard: {str(e)}", "danger")
        return redirect(url_for("home"))


@vendor_bp.route("/add_product", methods=["GET", "POST"])
@login_required
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
            return redirect(url_for("vendor.vendor_dashboard"))

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
            return redirect(url_for("vendor.vendor_dashboard"))
        except ValueError:
            flash("Invalid price format!", "danger")
            return redirect(url_for("vendor.vendor_dashboard"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding item: {e}", "danger")
            return redirect(url_for("vendor.vendor_dashboard"))

    return render_template("vendor_dashboard.html")


@vendor_bp.route("/delete_item/<int:item_id>", methods=["POST"])
@login_required
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
            return redirect(url_for("vendor.vendor_dashboard"))

        # Check if the logged-in user is the vendor of this item
        if item.vendor_id != session.get("user_id"):
            flash("You don't have permission to delete this item!", "danger")
            return redirect(url_for("vendor.vendor_dashboard"))

        # Delete the item
        db.session.delete(item)
        db.session.commit()
        flash("Item deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting item: {e}", "danger")

    return redirect(url_for("vendor.vendor_dashboard"))


@vendor_bp.route("/edit_item/<int:item_id>", methods=["GET", "POST"])
@login_required
def edit_item(item_id):
    try:
        if not session.get("user_id"):
            flash("Please log in first!", "danger")
            return redirect(url_for("login"))

        item = Item.query.get_or_404(item_id)

        # Check if the logged-in user is the vendor of this item
        if item.vendor_id != session.get("user_id"):
            flash("You don't have permission to edit this item!", "danger")
            return redirect(url_for("vendor.vendor_dashboard"))

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
                return redirect(url_for("vendor.vendor_dashboard"))
            except ValueError:
                flash("Invalid price format!", "danger")
            except Exception as e:
                db.session.rollback()
                flash(f"Error updating item: {e}", "danger")

        return render_template(
            "vendor_item_edit.html", item=item, ITEM_STATUS=ITEM_STATUS
        )

    except Exception as e:
        flash(f"Error accessing item: {e}", "danger")
        return redirect(url_for("vendor.vendor_dashboard"))


@vendor_bp.route("/test_error")
def test_error():
    raise Exception("This is a test error!")

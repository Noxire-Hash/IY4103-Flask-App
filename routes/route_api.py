from flask import Blueprint, jsonify

from models import Item, User
from utils import Logger
from wrappers import login_required

api_bp = Blueprint("api", __name__, url_prefix="/api")


@login_required
@api_bp.route("/get_item/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = Item.query.get(item_id)
    if item:
        Logger.info(f"Item found: {item.to_dict()}")
        return jsonify(item.to_dict())
    else:
        Logger.error(f"Item not found: {item_id}")
        return jsonify({"error": "Item not found"}), 404


@login_required
@api_bp.route("/username/<int:user_id>", methods=["GET"])
def get_username(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({"username": user.username})
    else:
        return jsonify({"error": "User not found"}), 404


@login_required
@api_bp.route("/get_all_items", methods=["GET"])
def get_all_items():
    items = Item.query.all()
    items_list = []
    for item in items:
        vendor_name = get_username(item.vendor_id)
        items_list.append(
            {  # Append to list instead of dict
                "id": item.id,  # Make sure ID is included
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
        )
    Logger.info(f"Retrieved {len(items_list)} items")
    return jsonify(items_list)

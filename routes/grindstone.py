from flask import (
    Blueprint,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

import grindstone.main as grindstone
from models import (
    GrindStoneEquipment,
    GrindStoneInventoryItem,
    GrindStonePlayerSave,
    GrindStoneSkill,
    db,
)

# Create Blueprint
grindstone_bp = Blueprint("grindstone", __name__, url_prefix="/games/grindstone")


@grindstone_bp.route("/")
def index():
    if not session.get("user_id"):
        flash("Please log in to play Grindstone", "warning")
        return redirect(url_for("login"))

    # Check if player has a character
    player = GrindStonePlayerSave.query.filter_by(
        user_id=session.get("user_id")
    ).first()
    if not player:
        return redirect(url_for("grindstone.initialize_character"))

    return render_template("grindstone.html", player=player)


@grindstone_bp.route("/register")
def register():
    initialize_new_player(session.get("user_id"))
    return render_template("grindstone_register.html")


@grindstone_bp.route("/login")
def login():
    return render_template("grindstone_login.html")


@grindstone_bp.route("/api/state", methods=["GET"])
def get_game_state():
    if not session.get("user_id"):
        return jsonify({"error": "Not logged in"}), 401

    player = GrindStonePlayerSave.query.filter_by(
        user_id=session.get("user_id")
    ).first()
    if not player:
        return jsonify({"error": "No character found"}), 404

    return jsonify(
        {
            "character": {
                "name": player.character_name,
                "level": player.level,
                "exp": player.exp,
                "coins": player.coins,
                "current_biome": player.current_biome_id,
            }
        }
    )


@grindstone_bp.route("/api/action", methods=["POST"])
def perform_action():
    if not session.get("user_id"):
        return jsonify({"error": "Not logged in"}), 401

    data = request.json
    action_type = data.get("action_type")
    target_id = data.get("target_id")

    player = GrindStonePlayerSave.query.filter_by(
        user_id=session.get("user_id")
    ).first()
    if not player:
        return jsonify({"error": "No character found"}), 404

    # TODO: Implement action processing
    return jsonify(
        {"message": "Action received", "action": action_type, "target": target_id}
    )


@grindstone_bp.route("/api/inventory", methods=["GET"])
def get_inventory():
    if not session.get("user_id"):
        return jsonify({"error": "Not logged in"}), 401

    player = GrindStonePlayerSave.query.filter_by(
        user_id=session.get("user_id")
    ).first()
    if not player:
        return jsonify({"error": "No character found"}), 404

    inventory_items = GrindStoneInventoryItem.query.filter_by(
        player_save_id=player.id
    ).all()
    return jsonify(
        {
            "inventory": [
                {"item_id": item.item_id, "quantity": item.quantity}
                for item in inventory_items
            ]
        }
    )


@grindstone_bp.route("/api/skills", methods=["GET"])
def get_skills():
    if not session.get("user_id"):
        return jsonify({"error": "Not logged in"}), 401

    player = GrindStonePlayerSave.query.filter_by(
        user_id=session.get("user_id")
    ).first()
    if not player:
        return jsonify({"error": "No character found"}), 404

    skills = GrindStoneSkill.query.filter_by(player_save_id=player.id).all()
    return jsonify(
        {
            "skills": [
                {"name": skill.skill_name, "level": skill.level} for skill in skills
            ]
        }
    )


def initialize_new_player(user_id, character_name=None):
    """Create a new game save for a first-time player"""
    # Create player save record
    player_save = GrindStonePlayerSave(
        user_id=user_id,
        character_name=character_name or f"Player_{user_id}",
        current_biome_id="biom_dark_woods",
        level=1,
        exp=0,
        coins=1000,
    )
    db.session.add(player_save)
    db.session.flush()

    # Fix: Remove the extra comma and match the model fields
    sanitized_kit = {
        "head_armor_id": grindstone.STARTER_KIT.get("head_armor_id", 0),
        "chest_armor_id": grindstone.STARTER_KIT.get("chest_armor_id", 0),
        "leg_armor_id": grindstone.STARTER_KIT.get("leg_armor_id", 0),
        "woodcutting_tool_id": grindstone.STARTER_KIT.get("woodcutting_tool_id", 0),
        "mining_tool_id": grindstone.STARTER_KIT.get("mining_tool_id", 0),
        "hunting_tool_id": grindstone.STARTER_KIT.get("hunting_tool_id", 0),
        "melee_tool_id": grindstone.STARTER_KIT.get("melee_tool_id", 0),
    }

    # Add equipment
    equipment = GrindStoneEquipment(player_save_id=player_save.id, **sanitized_kit)
    db.session.add(equipment)

    # Add skills
    skills = [
        GrindStoneSkill(
            player_save_id=player_save.id, skill_name="woodcutting_skills", level=1
        ),
        GrindStoneSkill(
            player_save_id=player_save.id, skill_name="mining_skills", level=1
        ),
        GrindStoneSkill(
            player_save_id=player_save.id, skill_name="hunting_skills", level=1
        ),
        GrindStoneSkill(
            player_save_id=player_save.id, skill_name="crafting_skills", level=1
        ),
        GrindStoneSkill(
            player_save_id=player_save.id, skill_name="adventure_skills", level=1
        ),
        GrindStoneSkill(
            player_save_id=player_save.id, skill_name="cooking_skills", level=1
        ),
    ]
    db.session.add_all(skills)

    # Add starting inventory
    for category, items in grindstone.LOAD_INV_DATA.items():
        if isinstance(items, dict):
            for item_id, quantity in items.items():
                if not isinstance(item_id, str) or item_id.startswith("_"):
                    continue

                if isinstance(quantity, (int, float)) and quantity > 0:
                    inventory_item = GrindStoneInventoryItem(
                        player_save_id=player_save.id,
                        item_id=item_id,
                        quantity=quantity,
                    )
                    db.session.add(inventory_item)

    return player_save


@grindstone_bp.route("/initialize", methods=["GET", "POST"])
def initialize_character():
    if not session.get("user_id"):
        flash("Please log in to create a character", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        character_name = request.form.get("character_name")
        if not character_name:
            flash("Please provide a character name", "danger")
            return redirect(url_for("grindstone.initialize_character"))

        # Check if player already exists
        existing_player = GrindStonePlayerSave.query.filter_by(
            user_id=session.get("user_id")
        ).first()

        if existing_player:
            flash("You already have a character!", "warning")
            return redirect(url_for("grindstone.index"))

        # Initialize new player with character name
        try:
            player_save = initialize_new_player(
                user_id=session.get("user_id"), character_name=character_name
            )
            db.session.commit()
            flash("Character created successfully!", "success")
            return redirect(url_for("grindstone.index"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error creating character: {str(e)}", "danger")
            return redirect(url_for("grindstone.initialize_character"))

    return render_template("grindstone_init.html")


@grindstone_bp.route("/test_setup")
def test_setup():
    if not session.get("user_id"):
        return jsonify({"error": "Please log in first"}), 401

    try:
        # Test character creation
        character_name = f"Test_Character_{session.get('user_id')}"
        player = initialize_new_player(session.get("user_id"), character_name)
        db.session.commit()

        # Verify the data
        result = {
            "character": {
                "name": player.character_name,
                "level": player.level,
                "coins": player.coins,
            },
            "skills": [
                {"name": skill.skill_name, "level": skill.level}
                for skill in player.skills
            ],
            "inventory": [
                {"item_id": item.item_id, "quantity": item.quantity}
                for item in player.inventory
            ],
        }

        return jsonify(
            {
                "success": True,
                "message": "Test setup completed successfully",
                "data": result,
            }
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

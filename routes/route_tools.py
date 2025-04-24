from flask import Blueprint, jsonify, render_template

tools_bp = Blueprint("tools", __name__)


@tools_bp.route("/tools")
def tools():
    return render_template("tools/tools.html")


@tools_bp.route("/api/tools/init_tracker")
def init_tracker():
    return jsonify({"message": "Tracker initialized"})


@tools_bp.route("api/tools/notepad")
def notepad():
    return jsonify({"message": "Notepad initialized"})


@tools_bp.route("/api/tools/dice/<int:num_dice>/<int:num_sides>")
def dice_roll(num_dice, num_sides):
    import random

    total = 0
    rolls = []
    for _ in range(num_dice):
        roll = random.randint(1, num_sides)
        rolls.append(roll)
        total += roll
    return jsonify({"rolls": rolls, "total": total})

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from wrappers import login_required

loreteller_bp = Blueprint("loreteller", __name__, url_prefix="/loreteller")


@loreteller_bp.route("/")
@login_required
def index():
    if not session.get("user_id"):
        flash("Please log in to use LoreTeller", "warning")
        return redirect(url_for("login"))

    return render_template("loreteller.html")


@loreteller_bp.rotue("/init/new_adventure", methods=["GET"])
@login_required
def new_adventure():
    if not session.get("user_id"):
        flash("Please log in to use LoreTeller", "warning")
        return redirect(url_for("login"))
    try:
        ai_agent = request.form.get("ai_agent")
        adventure_name = request.form.get("adventure_name")
        genre = request.form.get("genre")
        sub_genre = request.form.get("sub_genre")
        setting = request.form.get("setting")
        custom_command_world = request.form.get("custom_command_world")
        players = request.form.get("players")

    except Exception as e:
        flash(f"An error occurred: {e}", "error")
    return render_template("new_adventure.html")


@loreteller_bp.route("/api/ai_agent")
@login_required
def ai_agent():
    pass

from flask import Blueprint, render_template

loremaker_bp = Blueprint("loremaker", __name__, url_prefix="/loremaker")


@loremaker_bp.route("/")
def index():
    return render_template("loremaker_index.html")

@loremaker_bp.route("/about")
def about():
    return render_template("loremaker_about.html")

@loremaker_bp.route("/contact")
def contact():
    return render_template("loremaker_contact.html")

@loremaker_bp.route("/terms")
def terms():
    return render_template("loremaker_terms.html")


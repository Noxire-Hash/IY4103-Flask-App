from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import User, Privilege
from app import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/', methods=['GET', 'POST'])
def admin_dashboard():
    if session.get('privilege_id') != 2:  # Admin check
        flash("Access denied! Admins only.", "danger")
        return redirect(url_for('home'))

    users = User.query.all()
    privileges = Privilege.query.all()

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        new_privilege_id = request.form.get('privilege_id')
        try:
            user = User.query.get(user_id)
            user.privilege_id = new_privilege_id
            db.session.commit()
            flash(f"Updated {user.username}'s privilege.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating privilege: {e}", "danger")
        return redirect(url_for('admin.admin_dashboard'))

    return render_template('admin.html', users=users, privileges=privileges)

@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if session.get('privilege_id') != 2:
        flash("Access denied! Admins only.", "danger")
        return redirect(url_for('home'))

    try:
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        flash(f"Deleted user {user.username}.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting user: {e}", "danger")
    return redirect(url_for('admin.admin_dashboard'))

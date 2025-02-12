from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
ITEM_STATUS = ["Active", "Pending", "Inactive", "Deleted"]


class Privilege(db.Model):
    __tablename__ = 'privileges'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.String(256))


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    privilege_id = db.Column(
        db.Integer, db.ForeignKey('privileges.id'), default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    purchases = db.relationship('Purchase', backref='user', lazy=True)
    subscriptions = db.relationship('Subscription', backref='user', lazy=True)


class Vendor(db.Model):
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, db.ForeignKey('users.id'),
                   primary_key=True)  # Vendor is also a User
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    items = db.relationship('Item', backref='vendor', lazy=True)


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey(
        'vendors.id'), nullable=False)
    category = db.Column(db.String(64), nullable=False)
    tags = db.Column(db.String(256))
    sales = db.Column(db.Integer, default=0)
    status = db.Column(db.String(64), default="Active")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Purchase(db.Model):
    __tablename__ = 'purchases'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey(
        'vendors.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_price = db.Column(db.Float, nullable=False)


class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subscription_type = db.Column(
        db.String(64), nullable=False)  # E.g., "Basic", "Premium"
    end_date = db.Column(db.DateTime, nullable=True)
    # start_date = db.Column(db.DateTime, default=datetime.utcnow)
    # Null if perpetual or inactive


class DndCharacter(db.Model):
    __tablename__ = "dnd_characters"
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    race = db.Column(db.String(300))
    bio = db.Column(db.String(300))
    skills = db.Column(db.Integer)
    picture = db.Column(db.Integer)

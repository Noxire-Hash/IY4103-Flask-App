from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Privilege(db.Model):
    __tablename__ = 'privileges'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String(256), nullable=True)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  
    privilege_id = db.Column(db.Integer, db.ForeignKey('privileges.id'), default=0)
    #created_at = db.Column(db.DateTime, default=datetime.utcnow)

    privilege = db.relationship('Privilege', backref='users')
    purchases = db.relationship('Purchase', backref='user', lazy=True)
    subscriptions = db.relationship('Subscription', backref='user', lazy=True)

class Vendor(db.Model):
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)  # Vendor is also a User
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    store_name = db.Column(db.String(128), nullable=True)

    items = db.relationship('Item', backref='vendor', lazy=True)

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    is_featured = db.Column(db.Boolean, default=False)

    purchases = db.relationship('Purchase', backref='item', lazy=True)

class Purchase(db.Model):
    __tablename__ = 'purchases'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    #purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    quantity = db.Column(db.Integer, default=1)

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    subscription_type = db.Column(db.String(64), nullable=False)  # E.g., "Basic", "Premium"
    #start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)  # Null if perpetual or inactive
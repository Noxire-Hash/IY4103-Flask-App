from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Constants
ITEM_STATUS = ["Active", "Pending", "Hidden", "Archived"]
TICKET_CATEGORIES = [
    "Game Problem",
    "Technical Issue",
    "Purchase Problem",
    "Account Problem",
    "Report User",
    "Feedback",
    "Billing Issue",
    "API Request",
    "Become Merchant",
    "Other",
]
TICKET_STATUS = ["Open", "In Progress", "Closed"]
PURCHASE_STATUS = ["Pending", "Completed", "Cancelled"]
TRANSACTION_TYPES = [
    "DEPOSIT",  # User adding money to system
    "WITHDRAWAL",  # User withdrawing money from system
    "TRANSFER",  # User to user transfer
    "PURCHASE",  # Store purchase
    "REFUND",  # Refund from purchase
]
SYSTEM_ID = -999  # Special ID for system
PAYMENT_PROVIDERS = {
    "SHOPIFY": -1,
    "APPLE_PAY": -2,
    "GOOGLE_PAY": -3,
    "PAYPAL": -4,
}  # Special IDs for payment providers


class Privilege(db.Model):
    __tablename__ = "privileges"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.String(256))


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, index=True)
    email = db.Column(db.String(128), unique=True, nullable=False, index=True)
    password = db.Column(db.String(128), nullable=False)
    privilege_id = db.Column(db.Integer, db.ForeignKey("privileges.id"), default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships with cascade delete
    purchases = db.relationship(
        "Purchase", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    subscriptions = db.relationship(
        "Subscription", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    receipts = db.relationship("Receipt", backref="user", lazy=True)

    # Balance fields
    balance = db.Column(db.Integer, default=0)
    pending_balance = db.Column(db.Integer, default=0)


class Vendor(db.Model):
    __tablename__ = "vendors"
    id = db.Column(
        db.Integer, db.ForeignKey("users.id"), primary_key=True
    )  # Vendor is also a User
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)

    # Relationships with cascade delete
    items = db.relationship(
        "Item", backref="vendor", lazy=True, cascade="all, delete-orphan"
    )

    # Balance fields
    balance = db.Column(db.Float, default=0)
    pending_balance = db.Column(db.Float, default=0)


class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    vendor_id = db.Column(
        db.Integer, db.ForeignKey("vendors.id"), nullable=False, index=True
    )
    reviews = db.relationship(
        "ReviewOfItem", backref="item", lazy=True, cascade="all, delete-orphan"
    )
    category = db.Column(db.String(64), nullable=False, index=True)
    tags = db.Column(db.String(256))
    sales = db.Column(db.Integer, default=0)
    status = db.Column(db.String(64), default="Active", index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ReviewOfItem(db.Model):
    __tablename__ = "reviews_of_items"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text)


class Purchase(db.Model):
    __tablename__ = "purchases"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey("vendors.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_price = db.Column(db.Float, nullable=False)


class Subscription(db.Model):
    __tablename__ = "subscriptions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    subscription_type = db.Column(
        db.String(64), nullable=False
    )  # E.g., "Basic", "Premium"
    end_date = db.Column(db.DateTime, nullable=True)
    # Null if perpetual or inactive


class DndCharacter(db.Model):
    __tablename__ = "dnd_characters"
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    race = db.Column(db.String(300))
    bio = db.Column(db.String(300))
    skills = db.Column(db.Integer)
    picture = db.Column(db.Integer)


class SupportTicket(db.Model):
    __tablename__ = "support_tickets"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="Open", index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to responses - with cascade delete
    responses = db.relationship(
        "SupportTicketResponse",
        back_populates="ticket",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    user = db.relationship("User", backref="tickets")


class SupportTicketResponse(db.Model):
    __tablename__ = "support_ticket_responses"
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(
        db.Integer, db.ForeignKey("support_tickets.id"), nullable=False
    )
    responder_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_user = db.Column(db.Boolean, default=False)
    ticket = db.relationship("SupportTicket", back_populates="responses")
    responder = db.relationship("User", backref="responses")


class Receipt(db.Model):
    __tablename__ = "receipts"
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(
        db.Integer, nullable=False, index=True
    )  # Can be negative for payment providers
    receiver_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"), nullable=True)
    quantity = db.Column(db.Integer, default=1)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(64), default="Pending", index=True)
    transaction_type = db.Column(db.String(64), nullable=False, index=True)

    # Add relationship to receiver
    receiver = db.relationship(
        "User", foreign_keys=[receiver_id], backref="received_transactions"
    )


class SystemTransaction(db.Model):
    __tablename__ = "system_transactions"
    id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.String(64), nullable=False, index=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(64), default="Pending", index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    # For payment verification
    reference_code = db.Column(db.String(128), unique=True)
    notes = db.Column(db.Text, nullable=True)


class TransactionLog(db.Model):
    """Simple transaction log for balance changes"""

    __tablename__ = "transaction_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    receipt_id = db.Column(
        db.Integer, db.ForeignKey("receipts.id"), nullable=True, index=True
    )
    old_balance = db.Column(db.Float, nullable=False)
    new_balance = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship("User", backref="balance_logs")
    receipt = db.relationship("Receipt", backref="logs")

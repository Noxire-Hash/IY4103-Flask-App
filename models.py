from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Constants
ITEM_STATUS = ["Active", "Pending", "Hidden", "Archived"]
TICKET_CATEGORIES = [
    "Game Problem",
    "Technical Problem",
    "Purchase Problem",
    "Account Problem",
    "Report User",
    "Feedback",
    "Billing Issue",
    "API Request",
    "Become Vendor",
    "Other",
]
COMMUNITY_LEVELS = ["Lost Soul", "Wanderer", "Chronicler", "Sage", "Elder"]
MERCHANT_LEVELS = [
    "Street Padddler",
    "Bazaar Trader",
    "Guild Merchant",
    "The Gilded Baron",
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
ACCOUNT_STATUS = [
    "Active",
    "Inactive",
    "Banned",
    "Game Ban",
    "Community Suspended",
    "Community Ban",
    "Vendor Ban",
]

SUBSCRIPTION_MAPPING = {
    "basic": 0,
    "premium": 1,
    "exclusive": 2,
}


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
    bio = db.Column(db.String(256), default="")
    privilege_id = db.Column(db.Integer, db.ForeignKey("privileges.id"), default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(64), default="Active", index=True)
    balance = db.Column(db.Integer, default=0)
    pending_balance = db.Column(db.Integer, default=0)
    purchases = db.relationship(
        "Purchase", back_populates="user", lazy=True, cascade="all, delete-orphan"
    )
    subscription = db.relationship(
        "Subscription", back_populates="user", lazy=True, cascade="all, delete-orphan"
    )
    received_transactions = db.relationship(
        "Receipt", foreign_keys="Receipt.receiver_id", back_populates="receiver"
    )
    tickets = db.relationship("SupportTicket", back_populates="user")
    responses = db.relationship("SupportTicketResponse", back_populates="responder")
    balance_logs = db.relationship("TransactionLog", back_populates="user")
    game_states = db.relationship("GameState", back_populates="user")
    grindstone_items = db.relationship("GrindStoneItem", back_populates="user")
    community_posts = db.relationship("CommunityPost", back_populates="creator")
    community_replies = db.relationship("CommunityReply", back_populates="creator")


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

    # Add the user relationship
    user = db.relationship("User", back_populates="purchases")


class Subscription(db.Model):
    __tablename__ = "subscriptions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    subscription_type = db.Column(db.Integer, nullable=False, default=0)
    end_date = db.Column(db.DateTime, nullable=True)
    # Add the user relationship to match User.subscriptions
    user = db.relationship("User", back_populates="subscription")


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

    # Update relationships to use back_populates consistently
    responses = db.relationship(
        "SupportTicketResponse",
        back_populates="ticket",
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    user = db.relationship("User", back_populates="tickets")


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

    # Update relationships to use back_populates
    ticket = db.relationship("SupportTicket", back_populates="responses")
    responder = db.relationship("User", back_populates="responses")


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

    # Define relationships
    receiver = db.relationship(
        "User", foreign_keys=[receiver_id], back_populates="received_transactions"
    )
    transaction_logs = db.relationship(
        "TransactionLog",
        back_populates="receipt",
        lazy=True,
        cascade="all, delete-orphan",
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

    # Update relationships
    user = db.relationship("User", back_populates="balance_logs")
    receipt = db.relationship("Receipt", back_populates="transaction_logs")


class CommunityPost(db.Model):
    __tablename__ = "community_posts"
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(255), nullable=False)
    parent_id = db.Column(
        db.Integer, db.ForeignKey("community_posts.id"), nullable=True
    )
    tags = db.Column(db.String(255))
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Only keep one relationship for replies
    replies = db.relationship(
        "CommunityReply", back_populates="post", lazy=True, cascade="all, delete-orphan"
    )
    creator = db.relationship("User", back_populates="community_posts")


class CommunityReply(db.Model):
    __tablename__ = "community_replys"
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    post_id = db.Column(
        db.Integer, db.ForeignKey("community_posts.id"), nullable=False, index=True
    )
    content = db.Column(db.Text, nullable=False)
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Update relationships
    post = db.relationship("CommunityPost", back_populates="replies")
    creator = db.relationship("User", back_populates="community_replies")


class GameState(db.Model):
    __tablename__ = "game_states"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    game_id = db.Column(db.Integer, nullable=False)
    state_data = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Add relationship
    user = db.relationship("User", back_populates="game_states")


class GrindStoneItem(db.Model):
    __tablename__ = "grindstone_items"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    generic_id = db.Column(db.Integer, nullable=False, index=True)
    unique_id = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Add relationship
    user = db.relationship("User", back_populates="grindstone_items")


class GrindStonePlayerSave(db.Model):
    __tablename__ = "grindstone_player_saves"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    character_name = db.Column(db.String(50), nullable=False)
    current_biome_id = db.Column(
        db.String(50), nullable=False, default="biom_dark_woods"
    )
    level = db.Column(db.Integer, default=1)
    exp = db.Column(db.Integer, default=0)
    coins = db.Column(db.Integer, default=1000)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships with explicit foreign key naming
    equipment = db.relationship(
        "GrindStoneEquipment",
        backref="player_save",
        lazy=True,
        cascade="all, delete-orphan",
        foreign_keys="GrindStoneEquipment.player_save_id",
    )

    skills = db.relationship(
        "GrindStoneSkill",
        backref="player_save",
        lazy=True,
        cascade="all, delete-orphan",
        foreign_keys="GrindStoneSkill.player_save_id",
    )

    inventory = db.relationship(
        "GrindStoneInventoryItem",
        backref="player_save",
        lazy=True,
        cascade="all, delete-orphan",
        foreign_keys="GrindStoneInventoryItem.player_save_id",
    )


class GrindStoneEquipment(db.Model):
    __tablename__ = "grindstone_equipment"
    id = db.Column(db.Integer, primary_key=True)
    player_save_id = db.Column(
        db.Integer,
        db.ForeignKey("grindstone_player_saves.id", name="fk_equipment_player_save"),
        nullable=False,
    )

    # Equipment slots
    chest_armor_id = db.Column(db.Integer, default=0)
    head_armor_id = db.Column(db.Integer, default=0)
    leg_armor_id = db.Column(db.Integer, default=0)
    woodcutting_tool_id = db.Column(db.Integer, default=0)
    mining_tool_id = db.Column(db.Integer, default=0)
    hunting_tool_id = db.Column(db.Integer, default=0)
    melee_tool_id = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class GrindStoneSkill(db.Model):
    __tablename__ = "grindstone_skills"
    id = db.Column(db.Integer, primary_key=True)
    player_save_id = db.Column(
        db.Integer,
        db.ForeignKey("grindstone_player_saves.id", name="fk_skill_player_save"),
        nullable=False,
    )
    skill_name = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer, default=1)
    exp = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class GrindStoneInventoryItem(db.Model):
    __tablename__ = "grindstone_inventory_items"
    id = db.Column(db.Integer, primary_key=True)
    player_save_id = db.Column(
        db.Integer,
        db.ForeignKey("grindstone_player_saves.id", name="fk_inventory_player_save"),
        nullable=False,
    )
    item_id = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class LoreTellerAiAgent(db.Model):
    __tablename__ = "loreteller_ai_agents"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.String(256))
    api_key = db.Column(db.String(128), nullable=False)
    secret = db.Column(db.String(128), nullable=False)


class LoreTellerPlayers(db.Model):
    __tablename__ = "loreteller_players"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    description = db.Column(db.String(256))
    adventure_id = db.Column(
        db.Integer, db.ForeignKey("LoreTellerAdventures.id"), nullable=False
    )
    custom_command = db.Column(db.String(256), nullable=False)


class LoreTellerAdventures(db.Model):
    __tablename__ = "loreteller_adventures"
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(64), nullable=False, unique=True)
    genre = db.Column(db.String(64), nullable=False)
    sub_genre = db.Column(db.String(64), nullable=False)
    setting = db.Column(db.String(64), nullable=False)
    custom_command_world = db.Column(db.String(256), nullable=False)
    metadata = db.Column(db.Text, nullable=False)

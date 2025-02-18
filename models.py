from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import uuid
import time

db = SQLAlchemy()
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
    "Other"
]
TICKET_STATUS = ["Open", "In Progress", "Closed"]
PURCHASE_STATUS = ["Pending", "Completed", "Cancelled"]
TRANSACTION_TYPES = [
    "DEPOSIT",      # User adding money to system
    "WITHDRAWAL",   # User withdrawing money from system
    "TRANSFER",     # User to user transfer
    "PURCHASE",     # Store purchase
    "REFUND"        # Refund from purchase
]
SYSTEM_ID = 0  # Special ID for system transactions


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
    receipts = db.relationship('Receipt', backref='user', lazy=True)
    balance = db.Column(db.Float, default=0)
    pending_balance = db.Column(db.Float, default=0)


class Vendor(db.Model):
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, db.ForeignKey('users.id'),
                   primary_key=True)  # Vendor is also a User
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    items = db.relationship('Item', backref='vendor', lazy=True)
    balance = db.Column(db.Float, default=0)
    pending_balance = db.Column(db.Float, default=0)


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey(
        'vendors.id'), nullable=False)
    reviews = db.relationship('ReviewOfItem', backref='item', lazy=True)
    category = db.Column(db.String(64), nullable=False)
    tags = db.Column(db.String(256))
    sales = db.Column(db.Integer, default=0)
    status = db.Column(db.String(64), default="Active")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ReviewOfItem(db.Model):
    __tablename__ = 'reviews_of_items'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text)


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


class SupportTicket(db.Model):
    __tablename__ = 'support_tickets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='Open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to responses
    responses = db.relationship(
        'SupportTicketResponse', back_populates='ticket', lazy='dynamic')
    user = db.relationship('User', backref='tickets')


class SupportTicketResponse(db.Model):
    __tablename__ = 'support_ticket_responses'
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey(
        'support_tickets.id'), nullable=False)
    responder_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)
    response = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_user = db.Column(db.Boolean, default=False)
    ticket = db.relationship('SupportTicket', back_populates='responses')
    responder = db.relationship('User', backref='responses')


class Receipt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey(
        'vendors.id'), nullable=False)
    # Nullable for system transactions
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    quantity = db.Column(db.Integer, default=1)
    purchase_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(64), default="Pending")
    transaction_type = db.Column(
        db.String(64), nullable=True)  # For system transactions


class SystemTransaction(db.Model):
    __tablename__ = 'system_transactions'
    id = db.Column(db.Integer, primary_key=True)
    transaction_type = db.Column(db.String(64), nullable=False)
    sender_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey(
        'users.id'), nullable=True)  # Null for deposits
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(64), default="Pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    # For payment verification
    reference_code = db.Column(db.String(128), unique=True)


class SystemTransactionHandler:
    def __init__(self, receipt_id):
        if not isinstance(receipt_id, int) or receipt_id <= 0:
            raise ValueError("Invalid receipt ID")
        self.receipt_id = receipt_id
        self._receipt = None
        self._transaction = None

    def read_receipt(self):
        """Safely fetch and cache the receipt."""
        if self._receipt is None:
            self._receipt = Receipt.query.get_or_404(self.receipt_id)
        return self._receipt

    def validate_receipt(self):
        """Validate receipt before processing."""
        receipt = self.read_receipt()

        if receipt.status != "Pending":
            return False, "Receipt is not in pending status"

        if receipt.transaction_type not in TRANSACTION_TYPES:
            return False, "Invalid transaction type"

        if receipt.total_price <= 0:
            return False, "Invalid amount"

        return True, "Receipt is valid"

    def process_receipt(self):
        """Process the transaction based on receipt type."""
        try:
            is_valid, message = self.validate_receipt()
            if not is_valid:
                return False, message

            receipt = self.read_receipt()

            if receipt.transaction_type == "DEPOSIT":
                return self._process_deposit()
            elif receipt.transaction_type == "TRANSFER":
                return self._process_transfer()
            else:
                return False, "Unsupported transaction type"

        except Exception as e:
            db.session.rollback()
            return False, str(e)

    def _process_deposit(self):
        """Internal method to process deposit."""
        try:
            receipt = self.read_receipt()
            # In deposit, seller is the user receiving money
            user = User.query.get(receipt.seller_id)

            if not user:
                return False, "User not found"

            db.session.begin_nested()
            try:
                # Update user balance
                user.balance += receipt.total_price

                # Update receipt status
                receipt.status = "Completed"

                db.session.commit()
                return True, "Deposit completed successfully"

            except Exception as e:
                db.session.rollback()
                raise ValueError(f"Deposit failed: {str(e)}")

        except Exception as e:
            db.session.rollback()
            return False, str(e)

    def _process_transfer(self):
        """Internal method to process transfer."""
        try:
            receipt = self.read_receipt()
            sender = User.query.get(receipt.buyer_id)
            receiver = User.query.get(receipt.seller_id)

            if not all([sender, receiver]):
                return False, "Invalid sender or receiver"

            if sender.balance < receipt.total_price:
                return False, "Insufficient funds"

            db.session.begin_nested()
            try:
                # Update balances
                sender.balance -= receipt.total_price
                receiver.balance += receipt.total_price

                # Update receipt status
                receipt.status = "Completed"

                db.session.commit()
                return True, "Transfer completed successfully"

            except Exception as e:
                db.session.rollback()
                raise ValueError(f"Transfer failed: {str(e)}")

        except Exception as e:
            db.session.rollback()
            return False, str(e)


class CashReceipt:
    def __init__(self, amount, buyer_id, seller_id, transaction_type):
        self.amount = amount
        self.buyer_id = buyer_id
        self.seller_id = seller_id
        self.transaction_type = transaction_type
        self._receipt = None

    def create(self):
        """Create a pending receipt."""
        try:
            receipt = Receipt(
                buyer_id=self.buyer_id,
                seller_id=self.seller_id,
                total_price=self.amount,
                transaction_type=self.transaction_type,
                status="Pending"
            )
            db.session.add(receipt)
            db.session.commit()
            self._receipt = receipt
            return True, receipt.id
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    def cash(self):
        """Process the receipt and complete the transaction."""
        try:
            handler = SystemTransactionHandler(self._receipt.id)
            return handler.process_receipt()
        except Exception as e:
            return False, str(e)

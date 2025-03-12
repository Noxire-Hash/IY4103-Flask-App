from datetime import datetime

from models import (
    PAYMENT_PROVIDERS,
    SYSTEM_ID,
    TRANSACTION_TYPES,
    Item,
    Purchase,
    Receipt,
    SystemTransaction,
    TransactionLog,
    User,
    Vendor,
    db,
)


class Logger:
    # Log levels
    INFO = "INFO"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

    # Source identifiers
    PLAYER = "PLAYER"
    GAME = "GAME"
    SERVER = "SERVER"
    SYSTEM = "SYSTEM"

    def __init__(
        self, log_to_console=True, log_to_file=False, log_file="grindstone.log"
    ):
        self.log_to_console = log_to_console
        self.log_to_file = log_to_file
        self.log_file = log_file
        self.logs = []

    def log(self, source, level, message, data=None):
        """Create a formatted log entry

        Args:
            source: Who triggered the action (PLAYER, GAME, SERVER, SYSTEM)
            level: Status level (INFO, SUCCESS, WARNING, ERROR, CRITICAL)
            message: Main log message
            data: Optional dictionary of additional relevant data
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Format: [TIMESTAMP] [SOURCE] [LEVEL] Message {Data if present}
        log_entry = f"[{timestamp}] [{source}] [{level}] {message}"

        # Add data if provided
        if data:
            data_str = " ".join([f"{k}={v}" for k, v in data.items()])
            log_entry += f" {{{data_str}}}"

        # Store log
        self.logs.append(log_entry)

        # Output to console if enabled
        if self.log_to_console:
            print(log_entry)

        # Write to file if enabled
        if self.log_to_file:
            with open(self.log_file, "a") as f:
                f.write(log_entry + "\n")

        return log_entry

    # Convenience methods for different log types
    def info(self, source, message, data=None):
        return self.log(source, self.INFO, message, data)

    def player_action(self, action, message, data=None):
        return self.log(self.PLAYER, self.INFO, f"{action}: {message}", data)

    def game_event(self, event, message, data=None):
        return self.log(self.GAME, self.INFO, f"{event}: {message}", data)

    def server_event(self, event, message, data=None):
        return self.log(self.SERVER, self.INFO, f"{event}: {message}", data)

    def system_event(self, event, message, data=None):
        return self.log(self.SYSTEM, self.INFO, f"{event}: {message}", data)

    def success(self, source, message, data=None):
        return self.log(source, self.SUCCESS, message, data)

    def warning(self, source, message, data=None):
        return self.log(source, self.WARNING, message, data)

    def error(self, source, message, data=None):
        return self.log(source, self.ERROR, message, data)

    def critical(self, source, message, data=None):
        return self.log(source, self.CRITICAL, message, data)

    def get_logs(self):
        """Return all stored logs"""
        return self.logs.copy()

    def clear_logs(self):
        """Clear stored logs"""
        self.logs = []


# Utility functions can be added here as needed
class SystemTransactionHandler:
    """Handles creation and processing of system transactions."""

    # Transaction status codes for clearer error handling
    TRANSACTION_STATUS = {
        "SUCCESS": 0,
        "INVALID_AMOUNT": 1,
        "INSUFFICIENT_FUNDS": 2,
        "INVALID_SENDER": 3,
        "INVALID_RECEIVER": 4,
        "INVALID_TRANSACTION_TYPE": 5,
        "INVALID_PAYMENT_PROVIDER": 6,
        "PROCESSING_ERROR": 7,
        "INVALID_ITEM": 8,
        "RECEIPT_ALREADY_PROCESSED": 9,
    }

    # Map status codes to human-readable messages
    STATUS_MESSAGES = {
        0: "Transaction completed successfully",
        1: "Invalid amount: Amount must be positive",
        2: "Insufficient funds to complete transaction",
        3: "Invalid sender account",
        4: "Invalid receiver account",
        5: "Invalid transaction type",
        6: "Invalid payment provider",
        7: "Error processing transaction",
        8: "Invalid or unavailable item",
        9: "Receipt has already been processed",
    }

    @classmethod
    def create_and_process(
        cls,
        amount: float,
        sender_id: int,
        receiver_id: int,
        transaction_type: str,
        item_id=None,
        quantity=1,
        logger=None,
    ):
        """
        Creates and processes a transaction in one step.

        Args:
            amount: The amount to transfer
            sender_id: ID of the sender (can be payment provider ID)
            receiver_id: ID of the receiver (must be valid user ID)
            transaction_type: Type of transaction (from TRANSACTION_TYPES)
            item_id: Optional ID of item for purchases
            quantity: Optional quantity for purchases
            logger: Optional Logger instance for transaction logging

        Returns:
            tuple: (success: bool, message: str, receipt_id: int or None)
        """
        try:
            # Log the transaction request
            if logger:
                logger.info(
                    logger.SYSTEM,
                    f"Transaction request: {transaction_type}",
                    {
                        "amount": amount,
                        "sender_id": sender_id,
                        "receiver_id": receiver_id,
                        "item_id": item_id,
                        "quantity": quantity,
                    },
                )

            # Validate inputs
            if amount <= 0:
                if logger:
                    logger.error(
                        logger.SYSTEM,
                        "Transaction validation failed",
                        {"error": "Amount must be positive"},
                    )
                return (
                    False,
                    cls.STATUS_MESSAGES[cls.TRANSACTION_STATUS["INVALID_AMOUNT"]],
                    None,
                )

            if transaction_type not in TRANSACTION_TYPES:
                if logger:
                    logger.error(
                        logger.SYSTEM,
                        "Transaction validation failed",
                        {"error": "Invalid transaction type"},
                    )
                return (
                    False,
                    cls.STATUS_MESSAGES[
                        cls.TRANSACTION_STATUS["INVALID_TRANSACTION_TYPE"]
                    ],
                    None,
                )

            # Additional validation based on transaction type
            if transaction_type == "DEPOSIT" and sender_id >= 0:
                if logger:
                    logger.error(
                        logger.SYSTEM,
                        "Transaction validation failed",
                        {"error": "Deposit must come from a payment provider"},
                    )
                return False, "Deposit must come from a payment provider", None

            if transaction_type == "TRANSFER" and sender_id < 0:
                if logger:
                    logger.error(
                        logger.SYSTEM,
                        "Transaction validation failed",
                        {"error": "Transfer must be between users"},
                    )
                return False, "Transfer must be between users", None

            # For purchases, validate the item
            if transaction_type == "PURCHASE" and not item_id:
                if logger:
                    logger.error(
                        logger.SYSTEM,
                        "Transaction validation failed",
                        {"error": "Purchase requires an item_id"},
                    )
                return False, "Purchase requires an item_id", None

            # Create receipt
            receipt = Receipt(
                sender_id=sender_id,
                receiver_id=receiver_id,
                item_id=item_id,
                quantity=quantity,
                total_price=amount,
                transaction_type=transaction_type,
                status="Pending",
            )

            db.session.add(receipt)
            db.session.commit()

            if logger:
                logger.info(
                    logger.SYSTEM, "Receipt created", {"receipt_id": receipt.id}
                )

            # Process the transaction
            handler = cls(receipt.id, logger=logger)
            success, message = handler.process_receipt()

            return success, message, receipt.id if success else None

        except Exception as e:
            db.session.rollback()
            error_msg = f"Failed to create transaction: {str(e)}"
            if logger:
                logger.error(
                    logger.SYSTEM, "Transaction creation failed", {"error": str(e)}
                )
            return False, error_msg, None

    def __init__(self, receipt_id: int, logger=None):
        """Initialize with a receipt ID and optional logger."""
        if not isinstance(receipt_id, int) or receipt_id <= 0:
            raise ValueError("Invalid receipt ID")
        self.receipt_id = receipt_id
        self._receipt = None
        self.logger = logger

    def read_receipt(self):
        """Safely fetch and cache the receipt."""
        if self._receipt is None:
            self._receipt = Receipt.query.get_or_404(self.receipt_id)
        return self._receipt

    def validate_receipt(self):
        """Validate receipt before processing."""
        receipt = self.read_receipt()

        if receipt.status != "Pending":
            if self.logger:
                self.logger.warning(
                    self.logger.SYSTEM,
                    "Receipt validation failed",
                    {"receipt_id": self.receipt_id, "error": "Not in pending status"},
                )
            return False, "Receipt is not in pending status"

        if receipt.transaction_type not in TRANSACTION_TYPES:
            if self.logger:
                self.logger.error(
                    self.logger.SYSTEM,
                    "Receipt validation failed",
                    {
                        "receipt_id": self.receipt_id,
                        "error": "Invalid transaction type",
                    },
                )
            return False, "Invalid transaction type"

        if receipt.total_price <= 0:
            if self.logger:
                self.logger.error(
                    self.logger.SYSTEM,
                    "Receipt validation failed",
                    {"receipt_id": self.receipt_id, "error": "Invalid amount"},
                )
            return False, "Invalid amount"

        # Validate receiver exists
        receiver = User.query.get(receipt.receiver_id)
        if not receiver:
            if self.logger:
                self.logger.error(
                    self.logger.SYSTEM,
                    "Receipt validation failed",
                    {"receipt_id": self.receipt_id, "error": "Invalid receiver"},
                )
            return False, "Invalid receiver"

        # Validate based on transaction type
        if receipt.transaction_type == "DEPOSIT":
            if receipt.sender_id >= 0:
                if self.logger:
                    self.logger.error(
                        self.logger.SYSTEM,
                        "Receipt validation failed",
                        {
                            "receipt_id": self.receipt_id,
                            "error": "Deposit must come from a payment provider",
                        },
                    )
                return False, "Deposit must come from a payment provider"

        elif receipt.transaction_type == "TRANSFER":
            if receipt.sender_id < 0:
                if self.logger:
                    self.logger.error(
                        self.logger.SYSTEM,
                        "Receipt validation failed",
                        {
                            "receipt_id": self.receipt_id,
                            "error": "Transfer must be between users",
                        },
                    )
                return False, "Transfer must be between users"

        # For purchases and refunds, validate item
        if receipt.transaction_type in ["PURCHASE", "REFUND"] and receipt.item_id:
            item = Item.query.get(receipt.item_id)
            if not item:
                if self.logger:
                    self.logger.error(
                        self.logger.SYSTEM,
                        "Receipt validation failed",
                        {"receipt_id": self.receipt_id, "error": "Invalid item"},
                    )
                return False, "Invalid item"

        if self.logger:
            self.logger.info(
                self.logger.SYSTEM,
                "Receipt validation successful",
                {"receipt_id": self.receipt_id},
            )
        return True, "Receipt is valid"

    def process_receipt(self):
        """Process the transaction based on receipt type."""
        try:
            if self.logger:
                self.logger.info(
                    self.logger.SYSTEM,
                    "Processing receipt",
                    {"receipt_id": self.receipt_id},
                )

            is_valid, message = self.validate_receipt()
            if not is_valid:
                return False, message

            return self._process_transaction()

        except Exception as e:
            db.session.rollback()
            error_msg = f"Failed to process receipt: {str(e)}"
            if self.logger:
                self.logger.error(
                    self.logger.SYSTEM,
                    "Receipt processing failed",
                    {"receipt_id": self.receipt_id, "error": str(e)},
                )
            return False, error_msg

    def _create_transaction_log(self, user_id, old_balance, new_balance, description):
        """Create a transaction log entry for a balance change."""
        receipt = self.read_receipt()

        log = TransactionLog(
            user_id=user_id,
            receipt_id=receipt.id,
            old_balance=old_balance,
            new_balance=new_balance,
            description=description,
        )

        db.session.add(log)

        if self.logger:
            self.logger.info(
                self.logger.SYSTEM,
                "Transaction log created",
                {
                    "user_id": user_id,
                    "receipt_id": receipt.id,
                    "old_balance": old_balance,
                    "new_balance": new_balance,
                },
            )

        return log

    def _process_transaction(self):
        """Process the actual transaction with improved handling."""
        receipt = self.read_receipt()

        # Start a transaction - this creates a savepoint
        db.session.begin_nested()

        try:
            # For payment provider transactions, only check receiver
            if receipt.sender_id < 0:
                sender = None
                if receipt.sender_id not in [v for v in PAYMENT_PROVIDERS.values()]:
                    db.session.rollback()
                    if self.logger:
                        self.logger.error(
                            self.logger.SYSTEM,
                            "Invalid payment provider",
                            {
                                "receipt_id": self.receipt_id,
                                "provider_id": receipt.sender_id,
                            },
                        )
                    return False, self.STATUS_MESSAGES[
                        self.TRANSACTION_STATUS["INVALID_PAYMENT_PROVIDER"]
                    ]
            else:
                sender = User.query.get(receipt.sender_id)
                if not sender:
                    db.session.rollback()
                    if self.logger:
                        self.logger.error(
                            self.logger.SYSTEM,
                            "Invalid sender",
                            {
                                "receipt_id": self.receipt_id,
                                "sender_id": receipt.sender_id,
                            },
                        )
                    return False, self.STATUS_MESSAGES[
                        self.TRANSACTION_STATUS["INVALID_SENDER"]
                    ]

                # Check funds for transfers, purchases, etc.
                if receipt.transaction_type in ["TRANSFER", "PURCHASE"]:
                    if sender.balance < receipt.total_price:
                        db.session.rollback()
                        if self.logger:
                            self.logger.warning(
                                self.logger.SYSTEM,
                                "Insufficient funds",
                                {
                                    "receipt_id": self.receipt_id,
                                    "sender_id": receipt.sender_id,
                                    "required": receipt.total_price,
                                    "available": sender.balance,
                                },
                            )
                        return False, self.STATUS_MESSAGES[
                            self.TRANSACTION_STATUS["INSUFFICIENT_FUNDS"]
                        ]

            receiver = User.query.get(receipt.receiver_id)
            if not receiver:
                db.session.rollback()
                if self.logger:
                    self.logger.error(
                        self.logger.SYSTEM,
                        "Invalid receiver",
                        {
                            "receipt_id": self.receipt_id,
                            "receiver_id": receipt.receiver_id,
                        },
                    )
                return False, self.STATUS_MESSAGES[
                    self.TRANSACTION_STATUS["INVALID_RECEIVER"]
                ]

            # Process based on transaction type
            if receipt.transaction_type == "DEPOSIT":
                # Track old balance for logging
                old_balance = receiver.balance
                receiver.balance += receipt.total_price

                # Create transaction log
                self._create_transaction_log(
                    user_id=receiver.id,
                    old_balance=old_balance,
                    new_balance=receiver.balance,
                    description=f"Deposit from payment provider: {receipt.total_price} AW",
                )

                if self.logger:
                    self.logger.success(
                        self.logger.SYSTEM,
                        "Deposit processed",
                        {
                            "receipt_id": self.receipt_id,
                            "user_id": receiver.id,
                            "amount": receipt.total_price,
                            "old_balance": old_balance,
                            "new_balance": receiver.balance,
                        },
                    )

            elif receipt.transaction_type == "TRANSFER":
                # Track old balances for logging
                if sender:
                    old_sender_balance = sender.balance
                    sender.balance -= receipt.total_price

                    # Create transaction log for sender
                    self._create_transaction_log(
                        user_id=sender.id,
                        old_balance=old_sender_balance,
                        new_balance=sender.balance,
                        description=f"Transfer to {receiver.username}: {receipt.total_price} AW",
                    )

                old_receiver_balance = receiver.balance
                receiver.balance += receipt.total_price

                # Create transaction log for receiver
                self._create_transaction_log(
                    user_id=receiver.id,
                    old_balance=old_receiver_balance,
                    new_balance=receiver.balance,
                    description=f"Transfer from {sender.username if sender else 'System'}: {receipt.total_price} AW",
                )

                if self.logger:
                    self.logger.success(
                        self.logger.SYSTEM,
                        "Transfer processed",
                        {
                            "receipt_id": self.receipt_id,
                            "sender_id": sender.id,
                            "receiver_id": receiver.id,
                            "amount": receipt.total_price,
                            "sender_old_balance": old_sender_balance,
                            "sender_new_balance": sender.balance,
                            "receiver_old_balance": old_receiver_balance,
                            "receiver_new_balance": receiver.balance,
                        },
                    )

            elif receipt.transaction_type == "WITHDRAWAL":
                # Check if user has sufficient funds for withdrawal
                if receiver.balance < receipt.total_price:
                    db.session.rollback()
                    if self.logger:
                        self.logger.warning(
                            self.logger.SYSTEM,
                            "Insufficient funds for withdrawal",
                            {
                                "receipt_id": self.receipt_id,
                                "user_id": receiver.id,
                                "required": receipt.total_price,
                                "available": receiver.balance,
                            },
                        )
                    return False, "Insufficient funds for withdrawal"

                old_balance = receiver.balance
                receiver.balance -= receipt.total_price

                # Create transaction log
                self._create_transaction_log(
                    user_id=receiver.id,
                    old_balance=old_balance,
                    new_balance=receiver.balance,
                    description=f"Withdrawal: {receipt.total_price} AW",
                )

                if self.logger:
                    self.logger.success(
                        self.logger.SYSTEM,
                        "Withdrawal processed",
                        {
                            "receipt_id": self.receipt_id,
                            "user_id": receiver.id,
                            "amount": receipt.total_price,
                            "old_balance": old_balance,
                            "new_balance": receiver.balance,
                        },
                    )

            elif receipt.transaction_type == "PURCHASE":
                # Handle item purchase
                if not receipt.item_id:
                    db.session.rollback()
                    if self.logger:
                        self.logger.error(
                            self.logger.SYSTEM,
                            "Missing item for purchase",
                            {"receipt_id": self.receipt_id},
                        )
                    return False, "Missing item information for purchase"

                # Find the item
                item = Item.query.get(receipt.item_id)
                if not item:
                    db.session.rollback()
                    if self.logger:
                        self.logger.error(
                            self.logger.SYSTEM,
                            "Invalid item",
                            {"receipt_id": self.receipt_id, "item_id": receipt.item_id},
                        )
                    return False, "Invalid item"

                # Process the purchase
                if sender:
                    old_sender_balance = sender.balance
                    sender.balance -= receipt.total_price

                    # Create transaction log
                    self._create_transaction_log(
                        user_id=sender.id,
                        old_balance=old_sender_balance,
                        new_balance=sender.balance,
                        description=f"Purchase: {item.name} ({receipt.quantity}x) for {receipt.total_price} AW",
                    )

                # Find the vendor and update their pending balance
                vendor = Vendor.query.get(item.vendor_id)
                if vendor:
                    old_vendor_balance = vendor.pending_balance
                    vendor.pending_balance += receipt.total_price

                    # Create transaction log for vendor's pending balance
                    self._create_transaction_log(
                        user_id=vendor.id,
                        old_balance=old_vendor_balance,
                        new_balance=vendor.pending_balance,
                        description=f"Sale: {item.name} ({receipt.quantity}x) for {receipt.total_price} AW (pending)",
                    )

                    if self.logger:
                        self.logger.info(
                            self.logger.SYSTEM,
                            "Vendor pending balance updated",
                            {
                                "receipt_id": self.receipt_id,
                                "vendor_id": vendor.id,
                                "old_pending_balance": old_vendor_balance,
                                "new_pending_balance": vendor.pending_balance,
                            },
                        )

                # Update item sales count
                item.sales += receipt.quantity

                # Create a Purchase record
                purchase = Purchase(
                    user_id=sender.id,
                    item_id=item.id,
                    vendor_id=item.vendor_id,
                    quantity=receipt.quantity,
                    total_price=receipt.total_price,
                )
                db.session.add(purchase)

                if self.logger:
                    self.logger.success(
                        self.logger.SYSTEM,
                        "Purchase processed",
                        {
                            "receipt_id": self.receipt_id,
                            "user_id": sender.id,
                            "item_id": item.id,
                            "vendor_id": item.vendor_id,
                            "amount": receipt.total_price,
                            "quantity": receipt.quantity,
                            "old_balance": old_sender_balance,
                            "new_balance": sender.balance,
                        },
                    )

            elif receipt.transaction_type == "REFUND":
                # Handle refund process
                if not receipt.item_id:
                    db.session.rollback()
                    if self.logger:
                        self.logger.error(
                            self.logger.SYSTEM,
                            "Missing item for refund",
                            {"receipt_id": self.receipt_id},
                        )
                    return False, "Missing item information for refund"

                item = Item.query.get(receipt.item_id)
                if not item:
                    db.session.rollback()
                    if self.logger:
                        self.logger.error(
                            self.logger.SYSTEM,
                            "Invalid item for refund",
                            {"receipt_id": self.receipt_id, "item_id": receipt.item_id},
                        )
                    return False, "Invalid item for refund"

                old_receiver_balance = receiver.balance
                receiver.balance += receipt.total_price

                # Create transaction log for customer receiving refund
                self._create_transaction_log(
                    user_id=receiver.id,
                    old_balance=old_receiver_balance,
                    new_balance=receiver.balance,
                    description=f"Refund for: {item.name} ({receipt.quantity}x) for {receipt.total_price} AW",
                )

                # If vendor exists, update their balance
                if item:
                    vendor = Vendor.query.get(item.vendor_id)
                    if vendor:
                        old_vendor_balance = vendor.pending_balance
                        vendor.pending_balance -= receipt.total_price

                        # Create transaction log for vendor's pending balance
                        self._create_transaction_log(
                            user_id=vendor.id,
                            old_balance=old_vendor_balance,
                            new_balance=vendor.pending_balance,
                            description=f"Refund: {item.name} ({receipt.quantity}x) for {receipt.total_price} AW (from pending)",
                        )

                        if self.logger:
                            self.logger.info(
                                self.logger.SYSTEM,
                                "Vendor pending balance updated for refund",
                                {
                                    "receipt_id": self.receipt_id,
                                    "vendor_id": vendor.id,
                                    "old_pending_balance": old_vendor_balance,
                                    "new_pending_balance": vendor.pending_balance,
                                },
                            )

                if self.logger:
                    self.logger.success(
                        self.logger.SYSTEM,
                        "Refund processed",
                        {
                            "receipt_id": self.receipt_id,
                            "user_id": receiver.id,
                            "item_id": receipt.item_id,
                            "amount": receipt.total_price,
                            "old_balance": old_receiver_balance,
                            "new_balance": receiver.balance,
                        },
                    )

            else:
                db.session.rollback()
                if self.logger:
                    self.logger.error(
                        self.logger.SYSTEM,
                        "Unsupported transaction type",
                        {
                            "receipt_id": self.receipt_id,
                            "type": receipt.transaction_type,
                        },
                    )
                return (
                    False,
                    f"Unsupported transaction type: {receipt.transaction_type}",
                )

            # Update receipt status
            receipt.status = "Completed"

            # Create a record in the SystemTransaction table
            transaction_log = SystemTransaction(
                transaction_type=receipt.transaction_type,
                sender_id=receipt.sender_id if receipt.sender_id > 0 else SYSTEM_ID,
                receiver_id=receipt.receiver_id,
                amount=receipt.total_price,
                status="Completed",
                created_at=receipt.purchase_date,
                completed_at=datetime.utcnow(),
                reference_code=f"R{receipt.id}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            )
            db.session.add(transaction_log)

            # Commit all changes
            db.session.commit()

            if self.logger:
                self.logger.success(
                    self.logger.SYSTEM,
                    "Transaction completed successfully",
                    {
                        "receipt_id": self.receipt_id,
                        "transaction_id": transaction_log.id,
                        "reference_code": transaction_log.reference_code,
                    },
                )

            return True, "Transaction completed successfully"

        except Exception as e:
            db.session.rollback()
            if self.logger:
                self.logger.error(
                    self.logger.SYSTEM,
                    "Transaction processing failed",
                    {"receipt_id": self.receipt_id, "error": str(e)},
                )
            return False, f"Transaction failed: {str(e)}"

    def generate_confirmation(self):
        """Generate a transaction confirmation summary."""
        receipt = self.read_receipt()

        # Get user names for better readability
        sender_name = "Payment Provider"
        if receipt.sender_id > 0:
            sender = User.query.get(receipt.sender_id)
            if sender:
                sender_name = sender.username
        elif receipt.sender_id == SYSTEM_ID:
            sender_name = "System"

        receiver = User.query.get(receipt.receiver_id)
        receiver_name = receiver.username if receiver else "Unknown User"

        # Format transaction amount
        formatted_amount = f"{receipt.total_price:.2f} AW"

        # Create confirmation details
        confirmation = {
            "receipt_id": receipt.id,
            "timestamp": receipt.purchase_date.strftime("%Y-%m-%d %H:%M:%S"),
            "transaction_type": receipt.transaction_type,
            "sender": sender_name,
            "receiver": receiver_name,
            "amount": formatted_amount,
            "status": receipt.status,
            "reference_code": f"TX-{receipt.id}-{receipt.purchase_date.strftime('%Y%m%d%H%M')}",
        }

        # Add item details for purchases and refunds
        if receipt.transaction_type in ["PURCHASE", "REFUND"] and receipt.item_id:
            item = Item.query.get(receipt.item_id)
            if item:
                confirmation["item"] = item.name
                confirmation["quantity"] = receipt.quantity
                confirmation["unit_price"] = f"{item.price:.2f} AW"

        return confirmation

import random
from datetime import datetime, timedelta

from app import app, db
from models import (
    PAYMENT_PROVIDERS,
    Item,
    Privilege,
    Purchase,
    Receipt,
    SupportTicket,
    SupportTicketResponse,
    User,
)


def create_dummy_users(privileges):
    """Create dummy users for each privilege level"""
    users = []

    # Create admin users
    admin = User(
        username="LoreKeeper",
        email="lorekeeper@lorekeeper.com",
        password="lorekeeper",
        privilege_id=privileges["Admin"].id,
        balance=1000000,
    )
    users.append(admin)

    # Create moderators
    mod1 = User(
        username="ModMaster",
        email="mod@example.com",
        password="moderator123",
        privilege_id=privileges["Moderator"].id,
        balance=5000,
    )
    users.append(mod1)

    # Create vendors
    vendor_names = ["GameMaster", "PixelArtist", "LootMaster"]
    for i, name in enumerate(vendor_names):
        vendor = User(
            username=name,
            email=f"{name.lower()}@example.com",
            password="vendor123",
            privilege_id=privileges["Vendor"].id,
            balance=1000 * (i + 1),
        )
        users.append(vendor)

    # Create regular users
    user_names = ["Player1", "Player2", "Player3", "Tester1", "Tester2"]
    for i, name in enumerate(user_names):
        user = User(
            username=name,
            email=f"{name.lower()}@example.com",
            password="user123",
            privilege_id=privileges["User"].id,
            balance=100 * (i + 1),
        )
        users.append(user)

    # Create promo users
    promo = User(
        username="PromoKing",
        email="promo@example.com",
        password="promo123",
        privilege_id=privileges["Promo Account"].id,
        balance=2500,
    )
    users.append(promo)

    return users


def create_dummy_items(vendors):
    """Create dummy items for testing"""
    items = []
    categories = ["Weapon", "Armor", "Potion", "Spell", "Mount"]
    statuses = ["Active", "Pending", "Hidden", "Archived"]
    prices = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000]  # Fixed price points

    for vendor in vendors:
        for i in range(3):  # 3 items per vendor
            item = Item(
                name=f"{random.choice(['Epic', 'Rare', 'Common'])} {random.choice(categories)}",
                description=f"A fantastic item created by {vendor.username}",
                price=random.choice(prices),
                vendor_id=vendor.id,
                category=random.choice(categories),
                tags=f"tag1,tag2,{random.choice(categories).lower()}",
                sales=random.randint(0, 100),
                status=random.choice(statuses),
                created_at=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
            )
            items.append(item)

    return items


def create_dummy_transactions(users, items):
    """Create dummy transactions and purchases"""
    receipts = []
    purchases = []

    # Create deposits from payment providers
    deposit_amounts = [50, 100, 200, 500, 1000]  # Fixed deposit amounts
    for user in users:
        if random.random() > 0.5:  # 50% chance for each user
            receipt = Receipt(
                sender_id=random.choice(list(PAYMENT_PROVIDERS.values())),
                receiver_id=user.id,
                total_price=random.choice(deposit_amounts),
                status="Completed",
                transaction_type="DEPOSIT",
            )
            receipts.append(receipt)

    # Create transfers between users
    transfer_amounts = [10, 25, 50, 100, 200]  # Fixed transfer amounts
    for _ in range(5):
        sender = random.choice(users)
        receiver = random.choice([u for u in users if u != sender])
        receipt = Receipt(
            sender_id=sender.id,
            receiver_id=receiver.id,
            total_price=random.choice(transfer_amounts),
            status="Completed",
            transaction_type="TRANSFER",
        )
        receipts.append(receipt)

    # Create purchases
    for user in users:
        if random.random() > 0.3:  # 70% chance for each user
            item = random.choice(items)
            quantity = random.randint(1, 3)
            purchase = Purchase(
                user_id=user.id,
                item_id=item.id,
                vendor_id=item.vendor_id,
                quantity=quantity,
                total_price=item.price * quantity,
            )
            purchases.append(purchase)

    return receipts, purchases


def create_dummy_support_tickets(users):
    """Create dummy support tickets and responses"""
    tickets = []
    responses = []

    for user in random.sample(users, 5):  # Create tickets for 5 random users
        ticket = SupportTicket(
            user_id=user.id,
            category=random.choice(
                ["Game Problem", "Technical Issue", "Purchase Problem"]
            ),
            subject=f"Issue with {random.choice(['game', 'purchase', 'account'])}",
            message=f"This is a test ticket from {user.username}",
            status=random.choice(["Open", "In Progress", "Closed"]),
        )
        tickets.append(ticket)

        # Add responses to tickets
        response = SupportTicketResponse(
            ticket=ticket,
            responder_id=user.id,
            response="Test response to ticket",
            is_user=True,
        )
        responses.append(response)

    return tickets, responses


def populate_database():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Create privileges
        privileges = {
            "User": Privilege(
                id=1, name="User", description="Regular user with basic access"
            ),
            "Vendor": Privilege(
                id=2, name="Vendor", description="User with vendor access"
            ),
            "Promo Account": Privilege(
                id=3, name="Promo Account", description="User with promotional access"
            ),
            "Moderator": Privilege(
                id=998, name="Moderator", description="User with moderator access"
            ),
            "Admin": Privilege(
                id=999, name="Admin", description="Admin with full access"
            ),
        }

        # Add privileges
        for privilege in privileges.values():
            db.session.add(privilege)
        db.session.commit()

        # Create and add users
        users = create_dummy_users(privileges)
        for user in users:
            db.session.add(user)
        db.session.commit()

        # Create and add items
        vendors = [u for u in users if u.privilege_id == privileges["Vendor"].id]
        items = create_dummy_items(vendors)
        for item in items:
            db.session.add(item)
        db.session.commit()

        # Create and add transactions
        receipts, purchases = create_dummy_transactions(users, items)
        for receipt in receipts:
            db.session.add(receipt)
        for purchase in purchases:
            db.session.add(purchase)
        db.session.commit()

        # Create and add support tickets
        tickets, responses = create_dummy_support_tickets(users)
        for ticket in tickets:
            db.session.add(ticket)
        for response in responses:
            db.session.add(response)
        db.session.commit()

        print("Database populated successfully with test data!")
        print(f"Created {len(users)} users")
        print(f"Created {len(items)} items")
        print(f"Created {len(receipts)} receipts")
        print(f"Created {len(purchases)} purchases")
        print(f"Created {len(tickets)} support tickets")


if __name__ == "__main__":
    populate_database()

import random
from datetime import datetime, timedelta

from app import app, db
from models import (
    PAYMENT_PROVIDERS,
    CommunityPost,
    CommunityReply,
    GrindStoneEquipment,
    GrindStoneInventoryItem,
    GrindStonePlayerSave,
    GrindStoneSkill,
    Item,
    Privilege,
    Purchase,
    Receipt,
    ReviewOfItem,
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

    # Create regular users with Grindstone characters
    user_names = [
        "Adventurer1",
        "DragonSlayer",
        "MysticMage",
        "WoodCutter",
        "MinerKing",
    ]
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


def create_item_reviews(users, items):
    """Create reviews for items"""
    reviews = []
    review_texts = [
        "Great item, totally worth the price!",
        "Not as good as I expected, but still decent.",
        "Amazing quality, will definitely buy again!",
        "The item arrived quickly, but it's not as described.",
        "Very useful, exactly what I needed.",
        "Decent quality for the price.",
        "Excellent craftsmanship!",
        "Not recommended, doesn't work as advertised.",
        "Good value for money.",
        "Could be better but works for now.",
    ]

    # Create reviews for some items
    for item in items:
        # Each item gets 0-3 reviews
        num_reviews = random.randint(0, 3)
        reviewers = random.sample(users, min(num_reviews, len(users)))

        for user in reviewers:
            # Skip if user is the vendor
            if user.id == item.vendor_id:
                continue

            rating = random.randint(1, 5)
            review_text = random.choice(review_texts)
            created_date = datetime.utcnow() - timedelta(days=random.randint(0, 20))

            review = ReviewOfItem(
                user_id=user.id,
                item_id=item.id,
                rating=rating,
                review=review_text,
                created_at=created_date,
            )
            reviews.append(review)

    return reviews


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


def create_grindstone_characters(users):
    """Create Grindstone characters for regular users"""
    characters = []
    skills = [
        "woodcutting_skills",
        "mining_skills",
        "hunting_skills",
        "crafting_skills",
        "adventure_skills",
        "cooking_skills",
    ]

    for user in users:
        if user.privilege_id == 1:  # Regular users only
            # Create player save
            character = GrindStonePlayerSave(
                user_id=user.id,
                character_name=f"{user.username}'s Character",
                current_biome_id="biom_dark_woods",
                level=random.randint(1, 10),
                exp=random.randint(0, 1000),
                coins=random.randint(100, 5000),
            )
            characters.append(character)
            db.session.add(character)
            db.session.flush()  # Get ID without committing

            # Add equipment
            equipment = GrindStoneEquipment(
                player_save_id=character.id,
                chest_armor_id=random.randint(0, 3),  # Fixed equipment slots
                head_armor_id=random.randint(0, 3),
                leg_armor_id=random.randint(0, 3),
                woodcutting_tool_id=random.randint(0, 3),
                mining_tool_id=random.randint(0, 3),
                hunting_tool_id=random.randint(0, 3),
                melee_tool_id=random.randint(0, 3),
            )
            db.session.add(equipment)

            # Add skills
            for skill_name in skills:
                skill = GrindStoneSkill(
                    player_save_id=character.id,
                    skill_name=skill_name,
                    level=random.randint(1, 5),
                    exp=random.randint(0, 500),
                )
                db.session.add(skill)

            # Add inventory items
            items = ["wood", "stone", "iron_ore", "food", "potion"]
            for item in items:
                inventory_item = GrindStoneInventoryItem(
                    player_save_id=character.id,
                    item_id=item,
                    quantity=random.randint(1, 50),
                )
                db.session.add(inventory_item)

    return characters


def create_community_content(users):
    """Create community posts and replies"""
    posts = []
    replies = []

    categories = ["Guide", "Discussion", "Question", "Showcase", "News"]
    tags = ["gameplay", "tips", "grindstone", "community", "help", "update"]

    # Create and commit posts first
    for _ in range(10):  # Create 10 posts
        creator = random.choice(users)
        post = CommunityPost(
            creator_id=creator.id,
            title=f"A post about {random.choice(categories)}",
            content=f"This is a sample post content by {creator.username}",
            category=random.choice(categories),
            tags=",".join(random.sample(tags, 3)),
            upvotes=random.randint(0, 100),
            downvotes=random.randint(0, 20),
        )
        db.session.add(post)
        db.session.flush()  # Get the post ID

        # Create replies for this post
        for _ in range(random.randint(1, 5)):
            reply = CommunityReply(
                creator_id=random.choice(users).id,
                post_id=post.id,  # Now we have the post ID
                content=f"This is a reply to the post '{post.title}'",
                upvotes=random.randint(0, 20),
                downvotes=random.randint(0, 5),
            )
            replies.append(reply)

        posts.append(post)

    return posts, replies


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
                id=999, name="Admin", description="User with full access"
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

        # Create Grindstone characters
        create_grindstone_characters(users)
        db.session.commit()

        # Create community content
        posts, replies = create_community_content(users)
        # Posts are already added and flushed in create_community_content
        db.session.commit()

        # Now add replies
        for reply in replies:
            db.session.add(reply)
        db.session.commit()

        # Create and add items
        vendors = [u for u in users if u.privilege_id == privileges["Vendor"].id]
        items = create_dummy_items(vendors)
        for item in items:
            db.session.add(item)
        db.session.commit()

        # Create and add item reviews
        reviews = create_item_reviews(users, items)
        for review in reviews:
            db.session.add(review)
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
        print(
            f"Created {len([u for u in users if u.privilege_id == 1])} Grindstone characters"
        )
        print(f"Created {len(posts)} community posts")
        print(f"Created {len(replies)} community replies")
        print(f"Created {len(items)} items")
        print(f"Created {len(reviews)} item reviews")
        print(f"Created {len(receipts)} receipts")
        print(f"Created {len(purchases)} purchases")


if __name__ == "__main__":
    populate_database()

# Adjust the import based on your app structure
from app import app, db
from models import Privilege, User

# Create a function to populate the privileges table


def populate_privileges():
    with app.app_context():
        # Check if the privileges already exist to avoid duplicates
        if Privilege.query.count() == 0:
            # Create privilege instances
            user_privilege = Privilege(
                id=1, name='User', description='Regular user with basic access')
            vendor_privilege = Privilege(
                id=2, name='Vendor', description='User with vendor access')
            promo_privilege = Privilege(
                id=3, name='Promo Account', description='User with promotional access')
            moderator_privilege = Privilege(
                id=998, name='Moderator', description='User with moderator access, can delete posts and comments, and approve or reject vendor applications, look support tickets')
            admin_privilege = Privilege(
                id=999, name='Admin', description="Admins or Grand Wizards that can do anything")
            lorekeeper_account = User(
                id=1, username='LoreKeeper', email='lorekeeper@lorekeeper.com', password='lorekeeper', privilege_id=999)

            # Add privileges to the session
            db.session.add(user_privilege)
            db.session.add(vendor_privilege)
            db.session.add(promo_privilege)
            db.session.add(moderator_privilege)
            db.session.add(admin_privilege)
            db.session.add(lorekeeper_account)
            # Commit the session to save the privileges to the database
            db.session.commit()
            print("Privileges populated successfully.")
        else:
            print("Privileges already exist in the database.")


if __name__ == '__main__':
    populate_privileges()

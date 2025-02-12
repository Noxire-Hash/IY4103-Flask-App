# Adjust the import based on your app structure
from app import app, db
from models import Privilege

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
            admin_privilege = Privilege(
                id=999, name='Admin', description='Administrator with full access')

            # Add privileges to the session
            db.session.add(user_privilege)
            db.session.add(vendor_privilege)
            db.session.add(promo_privilege)
            db.session.add(admin_privilege)

            # Commit the session to save the privileges to the database
            db.session.commit()
            print("Privileges populated successfully.")
        else:
            print("Privileges already exist in the database.")


if __name__ == '__main__':
    populate_privileges()

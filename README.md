# IY4103-Flask-App: Lorekeeper

A comprehensive digital marketplace platform developed with Flask for the IY4103 Web Development course at the University of Essex. Lorekeeper enables users to trade virtual items, manage transactions, and participate in a community-driven marketplace.

## Features

### Core Features

- 🔐 **User Authentication**
  - Secure login/registration
  - Session management with cookies
  - Role-based access (Admin, Moderator, Vendor, User)

- 🏪 **Marketplace**
  - Browse and search items
  - Detailed product listings
  - Category filtering
  - Review system

- 💰 **Transaction System**
  - Virtual currency (AW) management
  - User-to-user transfers
  - Purchase processing
  - Transaction history

- 🎫 **Support System**
  - Ticket creation and tracking
  - Moderator response interface
  - Category-based organization

- 💬 **Community Features**
  - Discussion boards
  - User profiles
  - Item reviews
  - Community posts

### Admin Features

- User management
- Transaction monitoring
- System-wide controls
- Support ticket management

## Tech Stack

- **Backend**: Python 3.12, Flask
- **Database**: SQLite, SQLAlchemy, Flask-Migrate
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Template Engine**: Jinja2

## Setup Instructions

1. **Clone the repository**

```bash
git clone [repository-url]
cd IY4103-Flask-App
```

2. **Create and activate virtual environment**

```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/MacOS
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Initialize database**

```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

5. **Run the application**

```bash
python run.py
```

6. **Access the application**

- Open browser and go to `http://127.0.0.1:5000`

## Test Accounts

| Role      | Email                     | Password      |
|-----------|---------------------------|---------------|
| Admin     | <lorekeeper@lorekeeper.com> | lorekeeper   |
| Moderator | <mod@example.com>          | moderator123  |
| Vendor    | <gamemaster@example.com>    | vendor123     |
| User      | <player1@example.com>      | user123       |

## Project Structure

- **app.py**: Main application file with route definitions and core logic
- **models.py**: Database models and relationships
- **utils.py**: Utility functions for transaction handling and logging
- **templates/**: HTML templates organized by functionality
- **static/**: CSS, JavaScript, and image assets
- **migrations/**: Database migration scripts
- **populate_db.py**: Script to populate the database with test data

## Database Schema

The application uses several key models with complex relationships:

- **User**: Account information and authentication
- **Privilege**: Role-based permission system
- **Item**: Marketplace products with metadata
- **Purchase**: Transaction records for items
- **SystemTransaction**: Financial transaction tracking
- **SupportTicket/Response**: Customer support system
- **Receipt**: Purchase receipts and documentation

## Development Process

This project was developed following a structured software development lifecycle:

1. **Requirement Analysis**: Identified user needs and defined core functionality
2. **Planning**: Created project timeline and milestone targets
3. **Design**: Developed wireframes and UI/UX mockups
4. **Implementation**: Built the application incrementally with regular testing
5. **Testing**: Conducted thorough testing across all features
6. **Deployment**: Prepared for production environment

## Future Development Plans

This project continues to evolve with plans for:

- **Enhanced Analytics Dashboard**: More comprehensive data visualization
- **User Profile Customization**: Avatar uploads and profile personalization
- **Notification System**: Real-time alerts for transactions and system events
- **Community Forums**: Interactive discussion boards where users can communicate with each other, share experiences, post questions, and exchange knowledge about marketplace items and game strategies
- **Mobile Application**: Companion app using the existing API endpoints

---

University of Essex - IY4103 Web Development

# IY4103-Flask-App: Lorekeeper

A comprehensive digital marketplace platform developed with Flask for the IY4103 Web Development course at the University of Essex. Lorekeeper enables users to trade virtual items, manage transactions, and participate in a community-driven marketplace with integrated mini-games and interactive features.

## Project Overview

This application demonstrates the implementation of a full-stack web application using Python Flask, focusing on secure user management, virtual marketplace operations, and community engagement features. The project showcases database design, authentication systems, and interactive web interfaces.

## Features

### Core Features (Fully Implemented)

- 🔐 **User Authentication & Account Management**
  - Secure login/registration system
  - Role-based access control (Admin, Moderator, Vendor, User)
  - User profiles with balance management
  - Account status monitoring

- 🏪 **Marketplace System**
  - Browse and search virtual items
  - Category filtering and tag-based organization
  - Detailed product listings with user reviews
  - Purchase processing with virtual currency

- 💰 **Transaction System**
  - Virtual currency (AW) management
  - User-to-user transfers
  - Transaction history tracking
  - Receipt generation and storage

- 🎫 **Support System**
  - Ticket creation with categories
  - Staff response interface
  - Ticket status tracking
  - Resolution workflow

### Beta Features

- 💬 **Taverns (Community Forums)**
  - Discussion boards organized by topics
  - Post creation and reply system
  - User reputation through up/downvotes
  - Community post management
  - *Note: Currently in beta testing phase with core functionality working*

### Work in Progress Features

- 🎮 **GrindStone Mini-Game**
  - Resource gathering simulation
  - Character progression system
  - Inventory management
  - *Note: Basic implementation complete, further development ongoing*

- 🎲 **LoreTeller Interactive Storytelling**
  - AI-driven narrative experiences
  - Player choice-based adventures
  - Custom adventure creation tools
  - *Note: Framework established, content development in progress*

### Admin Features

- Comprehensive user management dashboard
- Transaction monitoring and intervention tools
- System-wide parameter controls
- Support ticket oversight and moderation tools

## Tech Stack

- **Backend**: Python 3.12, Flask
- **Database**: SQLite, SQLAlchemy, Flask-Migrate
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Template Engine**: Jinja2
- **Auxiliary Tools**: Python data analysis libraries for admin analytics

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

5. **Populate database with test data (optional)**

```bash
python populate_db.py
```

6. **Run the application**

```bash
python run.py
```

7. **Access the application**

- Open browser and go to `http://127.0.0.1:5000`

## Test Accounts

| Role      | Email                     | Password      |
|-----------|---------------------------|---------------|
| Admin     | <lorekeeper@lorekeeper.com> | lorekeeper    |
| Moderator | <mod@example.com>          | moderator123  |
| Vendor    | <gamemaster@example.com>    | vendor123     |
| User      | <player1@example.com>      | user123       |

## Project Structure

- **app.py**: Main application file with route definitions and core logic
- **models.py**: Database models and relationships
- **utils.py**: Utility functions for transaction handling and data processing
- **wrapers.py**: Wrappers to better handle login state and user privileges
- **routes/**: Modularized route handlers
- **templates/**: HTML templates organized by functionality
  - **taverns/**: Community forum templates
  - **loremaker/**: Interactive storytelling templates
  - **vendor/**: Vendor dashboard templates
- **static/**: CSS, JavaScript, and image assets
- **migrations/**: Database migration scripts
- **grindstone/**: Mini-game implementation files
- **populate_db.py**: Test data generation script

## Database Schema

The application implements a relational database with the following key models:

- **User**: Account information and authentication
- **Privilege**: Role-based permission system
- **Item/Vendor**: Marketplace product management
- **Purchase/Receipt**: Transaction records
- **SystemTransaction/TransactionLog**: Financial tracking
- **SupportTicket/Response**: Customer support system
- **CommunityPost/Reply**: Forum functionality
- **GrindStone/LoreTeller models**: Game state management

## Academic Context

This project was developed as part of the IY4103 Web Development course at the University of Essex. It demonstrates the application of web development principles including:

- Full-stack application architecture
- Database design and implementation
- Authentication and authorization systems
- User interface design principles
- RESTful API design
- Session management and security practices

## Future Development Roadmap

Planned enhancements for future iterations include:

- Integration of real-time notifications using WebSockets
- Expanded analytics dashboard for vendors and administrators
- Enhanced mobile responsiveness for all interfaces
- Completion of the LoreTeller AI storytelling system
- Full deployment of the GrindStone mini-game with expanded content
- Implementation of achievement and badge systems

---

University of Essex - IY4103 Web Development

# Lorekeeper: A Digital Marketplace for Virtual Items

A comprehensive digital marketplace platform developed with Flask for the IY4103 Web Development course at the University of Essex. Lorekeeper enables users to trade virtual items, manage transactions, and participate in a community-driven marketplace with integrated mini-games and interactive features.

<img src="static/svg/lorekeeper_team_logo.svg" alt="Lorekeeper Logo" width="300" height="auto">

## Overview

Lorekeeper is a full-stack web application that demonstrates advanced concepts in web development, focusing on:

- Digital marketplace functionality
- User authentication and role management
- Virtual currency systems
- Community interaction
- Mini-games and storytelling features

## Features

### Core Marketplace Features

- **User Authentication System**
  - Secure login/registration with role-based access control
  - User profiles with customizable bios
  - Session management with cookies

- **Virtual Item Marketplace**
  - Browse and filter items by category and tags
  - Detailed product listings with reviews
  - Vendor management system

- **Transaction System**
  - Virtual currency (AW) management
  - User-to-user transfers
  - Purchase processing
  - Transaction history tracking

- **Support Ticketing**
  - User ticket creation and management
  - Staff response interface
  - Categorized support requests

### Community Features

- **Taverns (Forums)**
  - Discussion boards by topic
  - Post and reply system
  - Upvote/downvote functionality
  - User reputation tracking

### Gaming Features(In development)

- **GrindStone Mini-Game**
  - Resource gathering simulation
  - Character progression
  - Skill development
  - Inventory management

- **LoreTeller Interactive Storytelling**
  - AI-driven narrative experiences
  - Player choice-based adventures
  - Custom adventure creation

### Administration Features

- **Admin Dashboard**
  - User management and privilege control
  - Transaction monitoring
  - System parameter configuration
  - Support ticket oversight

- **Moderator Tools**
  - Content moderation
  - Support ticket handling
  - Community management

## Tech Stack

- **Backend**: Python 3.x, Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Authentication**: Flask session management
- **Template Engine**: Jinja2

## Project Structure

```
IY4103-Flask-App/
├── app.py                 # Main application file
├── models.py              # Database models
├── utils.py               # Utility functions
├── wrappers.py            # Authentication wrappers
├── config.py              # Configuration settings
├── routes/                # Route modules
│   ├── grindstone.py      # Mini-game routes
│   ├── route_loremaker.py # Storytelling routes
│   ├── route_subs.py      # Subscription routes
│   ├── route_taverns.py   # Forum routes
│   └── route_vendor.py    # Vendor dashboard routes
├── templates/             # HTML templates
│   ├── taverns/           # Forum templates
│   ├── loremaker/         # Storytelling templates
│   └── vendor/            # Vendor templates
├── static/                # Static assets
│   ├── css/               # Stylesheets
│   ├── scripts/           # JavaScript files
│   └── svg/               # SVG assets
├── migrations/            # Database migrations
├── grindstone/            # Mini-game implementation
└── populate_db.py         # Test data generation
```

## Setup Instructions

> **Note:** This application requires Python 3.7 or higher.

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/IY4103-Flask-App.git
cd IY4103-Flask-App
```

2. **Create and activate virtual environment**

```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/MacOS
python3 -m venv venv
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
# Windows
python app.py

# Linux/MacOS
python3 app.py
```

7. **Access the application**

Open your browser and navigate to `http://127.0.0.1:5000`

## Test Accounts

| Role      | Email                       | Password      |
|-----------|----------------------------|---------------|
| Admin     | <lorekeeper@lorekeeper.com> | lorekeeper    |
| Teacher   | <essexuniversity@essex.ac.uk> | essexuniversity |
| Moderator | <mod@example.com>           | moderator123  |
| Vendor    | <gamemaster@example.com>     | vendor123     |
| User      | <adventurer1@example.com>    | user123       |

## Database Schema

The application implements a relational database with the following key models:

- **User**: Account information and authentication
- **Privilege**: Role-based permission system
- **Item**: Marketplace product management
- **Purchase/Receipt**: Transaction records
- **SystemTransaction/TransactionLog**: Financial tracking
- **SupportTicket/Response**: Customer support system
- **CommunityPost/Reply**: Forum functionality
- **GrindStone models**: Game state management
- **LoreTeller models**: Storytelling system

## Contribution Guidelines

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## Future Development

Planned enhancements include:

- Real-time notifications with WebSockets
- Enhanced analytics dashboard
- Mobile responsive design improvements
- AI-driven content recommendation system
- Expanded mini-game system
- Achievement and badge systems

## License

This project was developed for educational purposes as part of the IY4103 Web Development course at the University of Essex.

## Acknowledgments

- IY4103 Web Development course faculty
- University of Essex
- Flask and related package developers
- Bootstrap team

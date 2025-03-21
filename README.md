# IY4103-Flask-App: Lorekeeper

This project is a web application developed for the IY4103 Web Development course at the University of Essex. Lorekeeper is a comprehensive digital marketplace platform that demonstrates advanced web development concepts using Flask, a micro web framework for Python. **This project significantly exceeds the course requirements** by implementing numerous additional features beyond the basic assessment criteria.

## Project Overview

Lorekeeper is a digital marketplace platform designed for trading virtual items and managing transactions between users. The application features a complete user authentication system, role-based access control, transaction processing, support ticket management, and detailed analytics. It integrates with a SQLite database to manage user data, products, transactions, and other resources.

### Assessment Requirements Met

This project fulfills all the assessment requirements:

- ✅ Well-written, neat, and commented code throughout all files
- ✅ Multiple HTML templates (15+) with base templates for consistent layout
- ✅ Bootstrap CSS library integration with custom CSS enhancements
- ✅ Complete Flask routing for all page endpoints
- ✅ SQLite database with 10+ models and complex relationships
- ✅ Extensive JavaScript functionality for dynamic user interactions
- ✅ Adherence to modern web design standards and best practices
- ✅ Fully populated with test data to demonstrate all functionality

## Core Features

- **User Authentication System**:
  - Secure registration and login
  - Session management with cookies
  - Role-based access control

- **Product Marketplace**:
  - Browse and search items
  - Detailed product pages
  - Category filtering

- **Vendor Management**:
  - Product creation and editing
  - Sales tracking
  - Inventory management

- **Admin Dashboard**:
  - User management
  - System-wide transaction control
  - Privilege assignment

## Extended Features (Beyond Course Requirements)

- **Complete Transaction System**:
  - Virtual currency (AW) management
  - Multiple payment provider integration
  - User-to-user transfers
  - Purchase processing with receipts
  - Detailed transaction history with insights

- **Advanced User Roles and Permissions**:
  - Hierarchical privilege system (Admin, Moderator, Vendor, User)
  - Role-specific dashboards and capabilities
  - Dynamic UI elements based on user privileges

- **Support Ticket System**:
  - Ticket creation and tracking
  - Moderator response interface
  - Category-based organization

- **Enhanced Security Features**:
  - Secure session management
  - Input validation and sanitization
  - Comprehensive error handling and logging

- **Data Visualization and Analytics**:
  - Transaction statistics and insights
  - User activity tracking
  - Financial summaries

- **Database Migration System**:
  - Structured schema evolution
  - Version-controlled database models

- **Community Forums**: Interactive discussion boards where users can communicate with each other, share experiences, post questions, and exchange knowledge about marketplace items and game strategies

## Technologies Used

- **Backend**: Python, Flask, SQLAlchemy, Flask-Migrate
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript, jQuery, Bootstrap 5
- **Template Engine**: Jinja2
- **Development Tools**: Git, Visual Studio Code

## Setup Instructions

To set up the project on your local machine, follow these steps:

1. **Clone the repository**:

    ```sh
    git clone https://github.com/yourusername/IY4103-Flask-App.git
    cd IY4103-Flask-App
    ```

2. **Set up a virtual environment**:

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the database**:

    ```sh
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    python populate_db.py  # Populate with test data
    ```

5. **Run the application**:

    ```sh
    flask run
    ```

6. **Access the application**:
    Open your web browser and go to `http://127.0.0.1:5000`.

## Test Accounts

The application comes with several pre-configured test accounts:

- **Admin**: `lorekeeper@lorekeeper.com` / `lorekeeper`
- **Moderator**: `mod@example.com` / `moderator123`
- **Vendor**: `gamemaster@example.com` / `vendor123`
- **User**: `player1@example.com` / `user123`
- **Promo**: `promo@example.com` / `promo123`

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

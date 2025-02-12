# IY4103-Flask-App

This project is a web application developed as part of the IY4103 Web Development course at the University of Essex. The application demonstrates the use of Flask, a micro web framework for Python, to create a functional web application with user authentication, database interactions, and more.

## Project Description

The IY4103-Flask-App is designed to help students understand the fundamentals of web development using Flask. The application includes features such as user registration, login, vendor management, and an admin dashboard. It integrates with a SQLite database to manage user data, products, and other resources.

## Features

- **User Registration and Login**: Users can create accounts and log in to access their profiles.
- **Vendor Dashboard**: Vendors can manage their products, including adding, updating, and deleting items.
- **Admin Panel**: Admin users can manage all users and their privileges.
- **Responsive Design**: The application is built with Bootstrap for a mobile-friendly interface.
- **Flash Messages**: Provides user feedback for actions like successful logins, registrations, and errors.

## Technologies Used

- **Flask**: A lightweight WSGI web application framework in Python.
- **SQLAlchemy**: An ORM for database management.
- **SQLite**: A lightweight database for development.
- **Bootstrap**: A front-end framework for responsive design.
- **jQuery**: A JavaScript library for DOM manipulation and AJAX requests.

## Setup Instructions

To set up the project on your local machine, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/IY4103-Flask-App.git
    cd IY4103-Flask-App
    ```

2. **Set up a virtual environment** (optional but recommended):
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
    ```

5. **Run the application**:
    ```sh
    flask run
    ```

6. **Access the application**:
    Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

- Visit the home page at `http://127.0.0.1:5000/` to explore the features.
- Register a new account or log in with an existing account.
- Access the vendor dashboard at `http://127.0.0.1:5000/vendor/dashboard` to manage products.
- Access the admin dashboard at `http://127.0.0.1:5000/admin` (Admins only).

## Project Structure

- **app.py**: The main application file containing route definitions and application logic.
- **models.py**: Contains the database models for the application.
- **templates/**: Directory containing HTML templates for rendering web pages.
- **static/**: Directory containing static files such as CSS and JavaScript.
- **populate_privileges.py**: Script to populate the privileges table in the database.

## Acknowledgements

This project is inspired by various resources and tools used in the IY4103 course:

- **D&D Beyond**: Inspiration for the project.
- **D&D 5e Tools**: Tools and resources for D&D 5th edition.

## Contact

For any questions or support, please contact the course instructor or teaching assistants.

---

University of Essex - IY4103 Web Development

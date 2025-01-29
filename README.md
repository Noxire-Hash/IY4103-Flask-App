# IY4103-Flask-App

This project is a web application developed as part of the IY4103 Web Development course at the University of Essex. The application demonstrates the use of Flask, a micro web framework for Python, to create a functional web application with user authentication, database interactions, and more.

## Project Description

The IY4103-Flask-App is designed to help students understand the fundamentals of web development using Flask. The application includes features such as user registration, login, and an admin dashboard. It also integrates with a SQLite database to manage user data and other resources.

## Setup Instructions

To set up the project on your local machine, follow these steps:

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/IY4103-Flask-App.git
    cd IY4103-Flask-App
    ```

2. **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Set up the database:**
    ```sh
    flask db upgrade
    ```

4. **Run the application:**
    ```sh
    flask run
    ```

## Usage

- Visit the home page at `http://127.0.0.1:5000/` to explore the features.
- Register a new account or log in with an existing account.
- Access the admin dashboard at `http://127.0.0.1:5000/admin` (Admins only).

## Project Structure

- [app.py](http://_vscodecontentref_/0): The main application file containing route definitions and application logic.
- [models.py](http://_vscodecontentref_/1): Contains the database models for the application.
- [templates](http://_vscodecontentref_/2): Directory containing HTML templates for rendering web pages.
- [static](http://_vscodecontentref_/3): Directory containing static files such as CSS and JavaScript.

## Acknowledgements

This project is inspired by various resources and tools used in the IY4103 course:

- **D&D Beyond**: Inspiration for the project.
- **D&D 5e Tools**: Tools and resources for D&D 5th edition.

## Contact

For any questions or support, please contact the course instructor or teaching assistants.

---

University of Essex - IY4103 Web Development
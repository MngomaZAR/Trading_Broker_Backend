Description:
Backend.py - Flask User Authentication and Order Management

This Flask application serves as a backend system for user authentication and order management. It provides a simple yet powerful foundation for applications that require user registration, login, and the ability to manage orders.

Key Features:

User Registration: Users can register with a unique username and password.
User Authentication: Secure login functionality to authenticate users.
User Management: Log out the currently logged-in user.
Order Creation: Create new orders associated with the logged-in user.
Order Retrieval: Retrieve all orders for the currently logged-in user.
Order Updates: Update the status of specific orders (limited to the order owner).
Order Deletion: Delete specific orders (limited to the order owner).
Technologies Used:

Flask: A lightweight web framework for Python.
Flask-SQLAlchemy: Integration with SQLAlchemy for database support.
Flask-Migrate: Simple database migrations for Flask applications.
Flask-Login: User session management.
Flask-Marshmallow: Integration for object serialization and deserialization.
Installation and Usage:

Clone the Repository:

bash
Copy code
git clone https://github.com/MngomaZAR/backend.py.git
cd backend.py
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Set Up the Database:

bash
Copy code
flask db init
flask db migrate
flask db upgrade
Run the Application:

bash
Copy code
flask run
Explore Endpoints:

Register a new user: http://localhost:5000/register
Log in: http://localhost:5000/login
Log out: http://localhost:5000/logout
Create an order: http://localhost:5000/orders
Get all orders: http://localhost:5000/orders
Update an order: http://localhost:5000/orders/1
Delete an order: http://localhost:5000/orders/1
License:
This project is licensed under the MIT License - see the LICENSE file for details.
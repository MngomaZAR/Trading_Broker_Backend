from flask import Flask, request, jsonify, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Initialize app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Add a secret key for the app
app.config['SECRET_KEY'] = 'mysecretkey'

# Initialize database and migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize Marshmallow
ma = Marshmallow(app)

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    orders = db.relationship('Order', backref='user', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)

# Order model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(16), nullable=False, default='open')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Order {}>'.format(self.id)

# User schema
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'password_hash', 'orders')

# Order schema
class OrderSchema(ma.Schema):
    class Meta:
        fields = ('id', 'quantity', 'status')

# Initialize schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

# Create a user
@app.route('/register', methods=['POST'])
def register():
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Username is required')
    parser.add_argument('password', type=str, required=True, help='Password is required')
    args = parser.parse_args()

    user = User.query.filter_by(username=args['username']).first()
    if user:
        abort(400, message="Username already exists")

    new_user = User(
        username=args['username'],
        password_hash=generate_password_hash(args['password'])
    )

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)

# Login a user
@app.route('/login', methods=['POST'])
def login():
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Username is required')
    parser.add_argument('password', type=str, required=True, help='Password is required')
    args = parser.parse_args()

    user = User.query.filter_by(username=args['username']).first()
    if not user or not check_password_hash(user.password_hash, args['password']):
        abort(401, message="Invalid username or password")

    login_user(user)

    return user_schema.jsonify(user)

# Logout a user
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return '', 204

# Create an order
@app.route('/orders', methods=['POST'])
@login_required
def create_order():
    parser = reqparse.RequestParser()
    parser.add_argument('quantity', type=int, required=True, help='Quantity is required')
    args = parser.parse_args()

    new_order = Order(
        quantity=args['quantity'],
        user_id=current_user.id
    )

    db.session.add(new_order)
    db.session.commit()

    return order_schema.jsonify(new_order)

# Get all orders
@app.route('/orders', methods=['GET'])
@login_required
def get_orders():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    return orders_schema.jsonify(orders)

# Update an order
@app.route('/orders/<int:order_id>', methods=['PUT'])
@login_required
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        abort(403)

    parser = reqparse.RequestParser()
    parser.add_argument('status', type=str, required=True, help='Status is required')
    args = parser.parse_args()

    order.status = args['status']
    db.session.commit()

    return order_schema.jsonify(order)

# Delete an order
@app.route('/orders/<int:order_id>', methods=['DELETE'])
@login_required
def delete_order(order_id):
        order = Order.query.get_or_404(order_id)
    if order.user_id != current_user.id:
        abort(403)

    db.session.delete(order)
    db.session.commit()

    return '', 204

# User loader callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app.run(debug=True)
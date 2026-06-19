from flask import Blueprint
from app.controllers.cart_controller import CartController
from app.classes.Authentication import Authentication

# Create shopping cart blueprint
cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/add', methods=['POST'])
@Authentication.login_required
def add():
    """Endpoint to add items to cart via POST requests"""
    return CartController.add_to_cart()

@cart_bp.route('/count', methods=['GET'])
@Authentication.login_required
def get_count():
    """Endpoint to fetch the user's current live cart quantity count"""
    return CartController.get_cart_count()
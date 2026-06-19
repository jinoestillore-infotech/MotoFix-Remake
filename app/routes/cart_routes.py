from flask import Blueprint
from app.controllers.cart_controller import CartController
from app.classes.Authentication import Authentication

cart_bp = Blueprint('cart', __name__)

# Ensure all cart operations are restricted strictly to registered clients
@cart_bp.before_request
@Authentication.role_required('Client')
def restrict_to_clients():
    pass

@cart_bp.route('/', methods=['GET'])
def view():
    """Renders Cart template UI"""
    return CartController.view_cart()

@cart_bp.route('/add', methods=['POST'])
def add():
    """AJAX API endpoint adding item to cart"""
    return CartController.add_to_cart_api()

@cart_bp.route('/update', methods=['POST'])
def update():
    """AJAX API modifying item quantity"""
    return CartController.update_quantity_api()

@cart_bp.route('/remove', methods=['POST'])
def remove():
    """AJAX API deleting item from user pool"""
    return CartController.remove_item_api()

@cart_bp.route('/count', methods=['GET'])
def count():
    """Retrieves dynamic cart quantity summary count"""
    return CartController.get_cart_count_api()
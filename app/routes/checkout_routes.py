from flask import Blueprint
from app.controllers.checkout_controller import CheckoutController
from app.classes.Authentication import Authentication

checkout_bp = Blueprint('checkout', __name__)

# Checkout is exclusive to clients
@checkout_bp.before_request
@Authentication.role_required('Client')
def restrict_to_clients():
    pass

@checkout_bp.route('/', methods=['GET'])
def view():
    """Renders payment checkout options list"""
    return CheckoutController.show_checkout_page()

@checkout_bp.route('/place-order', methods=['POST'])
def place():
    """POST Route completing transaction order items placement"""
    return CheckoutController.place_order()

@checkout_bp.route('/success/<int:order_id>', methods=['GET'])
def success(order_id):
    """Renders Invoice details page upon transaction success"""
    return CheckoutController.show_success_page(order_id)

@checkout_bp.route('/orders', methods=['GET'])
def list_orders():
    """Renders the Client-side orders tracking view"""
    return CheckoutController.view_orders()

@checkout_bp.route('/order-count', methods=['GET'])
def order_count():
    """Retrieves live active orders count for badge display"""
    return CheckoutController.get_order_count_api()
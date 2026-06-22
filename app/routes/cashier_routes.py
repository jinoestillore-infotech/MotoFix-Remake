# project/app/routes/cashier_routes.py
from flask import Blueprint
from app.controllers.cashier_controller import CashierController
from app.classes.Authentication import Authentication

cashier_bp = Blueprint('cashier', __name__)

# Restrict the entire cashier/POS pipeline exclusively to Owners
@cashier_bp.before_request
@Authentication.role_required('Owner')
def restrict_to_owners():
    pass

@cashier_bp.route('/', methods=['GET'])
def view_terminal():
    """Renders the primary Jinja-powered cashier POS interface"""
    return CashierController.show_cashier_panel()

@cashier_bp.route('/search', methods=['GET'])
def search_parts():
    """Real-time parts query retrieval API"""
    return CashierController.search_parts_api()

@cashier_bp.route('/add/<int:part_id>', methods=['POST'])
def add_to_ticket(part_id):
    """POST Route adding an item to cashier session draft"""
    return CashierController.add_to_ticket(part_id)

@cashier_bp.route('/update-qty/<int:part_id>/<string:delta>', methods=['POST'])
def update_qty(part_id, delta):
    """POST Route adjusting target quantities inside cashier draft (allows negative values)"""
    return CashierController.update_ticket_qty(part_id, delta)

@cashier_bp.route('/clear', methods=['POST'])
def clear_ticket():
    """POST Route purging active POS ticket queue"""
    return CashierController.clear_ticket()

@cashier_bp.route('/checkout', methods=['POST'])
def process_checkout():
    """POST Route executing final backend checkout verification, database write, and receipt generation"""
    return CashierController.process_checkout_api()
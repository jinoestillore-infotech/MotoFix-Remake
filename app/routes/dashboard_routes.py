# project/app/routes/dashboard_routes.py
from flask import Blueprint
from app.controllers.dashboard_controller import DashboardController
from app.classes.Authentication import Authentication

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/owner/dashboard', methods=['GET'])
@Authentication.role_required('Owner')
def owner_dashboard():
    """Renders administrative dashboard overview"""
    return DashboardController.owner_dashboard()

@dashboard_bp.route('/mechanic/dashboard', methods=['GET'])
@Authentication.role_required('Mechanic')
def mechanic_dashboard():
    """Renders shop mechanic diagnostic dashboard"""
    return DashboardController.mechanic_dashboard()

@dashboard_bp.route('/shop', methods=['GET'])
@Authentication.role_required('Client')
def client_index():
    """Renders active storefront parts catalog for clients"""
    return DashboardController.client_index()

@dashboard_bp.route('/owner/orders', methods=['GET'])
@Authentication.role_required('Owner')
def owner_orders():
    """Renders management queue of incoming customer orders"""
    return DashboardController.view_owner_orders()

@dashboard_bp.route('/owner/orders/update-status/<int:order_id>', methods=['POST'])
@Authentication.role_required('Owner')
def update_order_status(order_id):
    """Saves workflow status edits to order data records"""
    return DashboardController.update_order_status(order_id)

@dashboard_bp.route('/owner/orders/mark-paid/<int:order_id>', methods=['POST'])
@Authentication.role_required('Owner')
def mark_order_as_paid(order_id):
    """Locks a completed order record into Paid state"""
    return DashboardController.mark_order_as_paid(order_id)

@dashboard_bp.route('/owner/orders/transaction-history', methods=['GET'])
@Authentication.role_required('Owner')
def transaction_history():
    """Renders archived log sheet of fully completed and paid transactions"""
    return DashboardController.view_transaction_history()
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

# --- NEW WORKFLOWS FOR APPOINTMENTS & SCHEDULING ---

@dashboard_bp.route('/owner/appointments', methods=['GET'])
@Authentication.role_required('Owner')
def owner_appointments():
    """Renders Owner appointments console list"""
    return DashboardController.view_owner_appointments()

@dashboard_bp.route('/owner/appointments/assign', methods=['POST'])
@Authentication.role_required('Owner')
def owner_assign_mechanic():
    """Processes assigning a mechanic and resolving schedule overlaps"""
    return DashboardController.owner_assign_mechanic()

@dashboard_bp.route('/mechanic/appointments/complete', methods=['POST'])
@Authentication.role_required('Mechanic')
def mechanic_complete_appointment():
    """Processes mechanics filing repair logs and completing jobs"""
    return DashboardController.mechanic_complete_appointment()

# --- CUSTOMER ORDER ADMINISTRATIVE WORKFLOWS ---

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

@dashboard_bp.route('/owner/history/clear', methods=['POST'])
def owner_clear_transaction_history():
    """Route handling safe deletion processing requests to wipe out history"""
    return DashboardController.owner_clear_transaction_history_post()

@dashboard_bp.route('/owner/payment-settings', methods=['GET'])
@Authentication.role_required('Owner')
def payment_settings():
    """Renders interface to update owner GCash billing details"""
    return DashboardController.view_payment_settings()

@dashboard_bp.route('/owner/payment-settings/update', methods=['POST'])
@Authentication.role_required('Owner')
def update_payment_settings():
    """Handles post request saving owner payment details"""
    return DashboardController.update_payment_settings()
from flask import Blueprint
from app.controllers.dashboard_controller import DashboardController
from app.classes.Authentication import Authentication

# Create dashboard blueprint
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/owner/dashboard', methods=['GET'])
@Authentication.role_required('Owner')
def owner_dashboard():
    return DashboardController.owner_dashboard()

@dashboard_bp.route('/mechanic/dashboard', methods=['GET'])
@Authentication.role_required('Mechanic')
def mechanic_dashboard():
    return DashboardController.mechanic_dashboard()

@dashboard_bp.route('/client/home', methods=['GET'])
@Authentication.role_required('Client')
def client_index():
    return DashboardController.client_index()

@dashboard_bp.route('/owner/orders', methods=['GET'])
@Authentication.role_required('Owner')
def owner_orders():
    """Allows Owner to view all client customer orders"""
    return DashboardController.owner_orders()

@dashboard_bp.route('/owner/orders/update-status/<int:order_id>', methods=['POST'])
@Authentication.role_required('Owner')
def update_order_status(order_id):
    """Allows Owner to approve, process, complete, or cancel an order"""
    return DashboardController.update_order_status(order_id)
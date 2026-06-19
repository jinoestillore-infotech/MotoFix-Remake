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
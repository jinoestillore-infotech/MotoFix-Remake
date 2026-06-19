from flask import Blueprint
from app.controllers.auth_controller import AuthController
from app.classes.Authentication import Authentication

# Create authentication blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET'])
def login():
    return AuthController.show_login()

@auth_bp.route('/login', methods=['POST'])
def login_post():
    return AuthController.handle_login()

@auth_bp.route('/register', methods=['GET'])
def register():
    return AuthController.show_register()

@auth_bp.route('/register', methods=['POST'])
def register_post():
    return AuthController.handle_register()

@auth_bp.route('/onboard-mechanic', methods=['POST'])
@Authentication.role_required('Owner')
def onboard_mechanic():
    """Secure endpoint for Owners to onboard professional Mechanics"""
    return AuthController.handle_mechanic_onboard()

@auth_bp.route('/logout', methods=['GET'])
def logout():
    return AuthController.logout()
from flask import Blueprint
from app.controllers.auth_controller import AuthController

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

@auth_bp.route('/logout', methods=['GET'])
def logout():
    return AuthController.logout()
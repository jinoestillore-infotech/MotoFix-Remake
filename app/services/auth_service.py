from app.models.user import User
from app.models.role import Role
from app.classes.Helpers import Helpers
import re

class AuthService:
    """Business Logic for Authentication & Registration Layer"""

    @staticmethod
    def register_user(role_id: int, first_name: str, last_name: str, email: str, phone: str, password: str, confirm_password: str):
        """Processes checks and registers new accounts"""
        # Validate Inputs
        if not first_name or not last_name or not email or not password:
            return {"success": False, "message": "All mandatory fields must be filled out."}

        # Check Email Format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return {"success": False, "message": "Invalid email format choice."}

        # Validate Passwords match
        if password != confirm_password:
            return {"success": False, "message": "Passwords do not match."}

        if len(password) < 6:
            return {"success": False, "message": "Password must be at least 6 characters long."}

        # Ensure Role ID exists
        selected_role = Role.find_by_id(role_id)
        if not selected_role:
            return {"success": False, "message": "Invalid system role assignment selected."}

        # Ensure email uniqueness
        existing_user = User.find_by_email(email)
        if existing_user:
            return {"success": False, "message": "Email is already registered in the system."}

        # Generate Secure Hash & Create
        hashed_password = Helpers.hash_password(password)
        try:
            new_user_id = User.create(
                role_id=role_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                password_hash=hashed_password
            )
            return {"success": True, "message": "Account registered successfully!", "user_id": new_user_id}
        except Exception as e:
            return {"success": False, "message": f"Database failure on write: {str(e)}"}

    @staticmethod
    def authenticate_user(email: str, password: str):
        """Handles authentication verification for credentials"""
        if not email or not password:
            return {"success": False, "message": "Please enter both Email and Password."}

        user = User.find_by_email(email)
        if not user:
            return {"success": False, "message": "Invalid credentials. Please try again."}

        if user['status'] != 'active':
            return {"success": False, "message": f"This account is currently {user['status']}."}

        # Verify password via Crypt helper
        if Helpers.check_password(password, user['password_hash']):
            return {"success": True, "user": user}
        
        return {"success": False, "message": "Invalid credentials. Please try again."}
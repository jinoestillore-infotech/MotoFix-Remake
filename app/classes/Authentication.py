from functools import wraps
from flask import session, redirect, url_for, flash

class Authentication:
    """Handles session guards, login session states, and role clearances"""

    @staticmethod
    def login_user(user_data):
        """Stores key security claims in active session"""
        session.clear()  # Flush session before writing new login
        session['user_id'] = user_data['id']
        session['email'] = user_data['email']
        session['first_name'] = user_data['first_name']
        session['last_name'] = user_data['last_name']
        session['role_name'] = user_data['role_name']
        session['role_id'] = user_data['role_id']

    @staticmethod
    def logout_user():
        """Destroys current session"""
        session.clear()

    @staticmethod
    def is_authenticated() -> bool:
        """Verifies if the current user session is populated and valid"""
        return 'user_id' in session

    @staticmethod
    def login_required(f):
        """Route decorator ensuring authentication is met before page access"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not Authentication.is_authenticated():
                flash("Please log in to access this page.", "warning")
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return decorated_function

    @staticmethod
    def role_required(*allowed_roles):
        """Route decorator restricting route access by Roles"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if not Authentication.is_authenticated():
                    flash("Please log in to access this page.", "warning")
                    return redirect(url_for('auth.login'))
                
                user_role = session.get('role_name')
                if user_role not in allowed_roles:
                    flash("Access denied. You do not have permissions for this action.", "danger")
                    # Fall back to user's perspective dashboard
                    if user_role == 'Owner':
                        return redirect(url_for('dashboard.owner_dashboard'))
                    elif user_role == 'Mechanic':
                        return redirect(url_for('dashboard.mechanic_dashboard'))
                    else:
                        return redirect(url_for('dashboard.client_index'))
                return f(*args, **kwargs)
            return decorated_function
        return decorator
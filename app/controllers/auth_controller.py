from flask import render_template, request, redirect, url_for, flash, session
from app.services.auth_service import AuthService
from app.classes.Authentication import Authentication

class AuthController:
    """Controller navigating user credential verification requests"""

    @staticmethod
    def show_login():
        """Renders login interface if user isn't logged in"""
        if Authentication.is_authenticated():
            return AuthController.redirect_by_role()
        return render_template('auth/login.html')

    @staticmethod
    def handle_login():
        """Post controller validating user credentials"""
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        result = AuthService.authenticate_user(email, password)
        
        if result['success']:
            Authentication.login_user(result['user'])
            flash(f"Welcome back, {result['user']['first_name']}!", "success")
            return AuthController.redirect_by_role()
        else:
            flash(result['message'], "danger")
            return redirect(url_for('auth.login'))

    @staticmethod
    def show_register():
        """Renders signup template for clients only"""
        if Authentication.is_authenticated():
            return AuthController.redirect_by_role()
        
        return render_template('auth/register.html')

    @staticmethod
    def handle_register():
        """POST handler writing new accounts. Securely hardcoded to Client role (ID: 3)"""
        # Hardcoded to Client (ID 3) to prevent role manipulation attacks
        role_id = 3 
        
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        result = AuthService.register_user(
            role_id=role_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=password,
            confirm_password=confirm_password
        )

        if result['success']:
            flash(result['message'], "success")
            return redirect(url_for('auth.login'))
        else:
            flash(result['message'], "danger")
            return redirect(url_for('auth.register'))

    @staticmethod
    def logout():
        """Logout controller session flush"""
        Authentication.logout_user()
        flash("You have logged out successfully.", "info")
        return redirect(url_for('auth.login'))

    @staticmethod
    def redirect_by_role():
        """Helper router that routes authenticated users directly to distinct panels"""
        role_name = session.get('role_name')
        
        if role_name == 'Owner':
            return redirect(url_for('dashboard.owner_dashboard'))
        elif role_name == 'Mechanic':
            return redirect(url_for('dashboard.mechanic_dashboard'))
        else:
            return redirect(url_for('dashboard.client_index'))
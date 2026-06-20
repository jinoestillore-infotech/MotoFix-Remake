# project/app/__init__.py
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from app.config import Config
from app.database import Database

# Initialize CSRF protection globally
csrf = CSRFProtect()

def create_app():
    """Application factory for the Flask app with CSRF security enabled"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize connection pool
    Database.initialize()

    # Initialize CSRF protection on the app instance
    csrf.init_app(app)

    # Import blueprints inside factory to prevent circular imports
    from app.routes.auth_routes import auth_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.inventory_routes import inventory_bp
    from app.routes.cart_routes import cart_bp
    from app.routes.checkout_routes import checkout_bp
    from app.routes.appointment_routes import appointment_bp

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(cart_bp, url_prefix='/cart')
    app.register_blueprint(checkout_bp, url_prefix='/checkout')
    app.register_blueprint(appointment_bp, url_prefix='/appointments')
    
    # Default index path logic fallback
    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect(url_for('auth.login'))

    return app
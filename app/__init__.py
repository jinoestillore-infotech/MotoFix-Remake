from flask import Flask
from app.config import Config
from app.database import Database

def create_app():
    """Application factory for the Flask app"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize connection pool
    Database.initialize()

    # Import blueprints inside factory to prevent circular imports
    from app.routes.auth_routes import auth_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.inventory_routes import inventory_bp
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')

    # Default index path logic fallback
    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect(url_for('auth.login'))

    return app
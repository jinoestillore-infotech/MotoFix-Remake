from flask import render_template, session
from app.database import Database
from app.models.user import User

class DashboardController:
    """Controller navigating authorized dashboard sessions"""

    @staticmethod
    def owner_dashboard():
        """Aggregates metrics and renders Owner Dashboard panel"""
        # Fetch initial dashboard metrics
        stats = {
            'total_clients': 0,
            'total_mechanics': 0,
            'total_appointments': 0,
            'low_stock_parts': 0
        }
        
        # Pull counts from database to present real-time dashboard data
        try:
            # Count Clients (Role ID: 3)
            res_clients = Database.execute_query("SELECT COUNT(*) as count FROM users WHERE role_id = 3")
            stats['total_clients'] = res_clients[0]['count'] if res_clients else 0

            # Count Mechanics (Role ID: 2)
            res_mechanics = Database.execute_query("SELECT COUNT(*) as count FROM users WHERE role_id = 2")
            stats['total_mechanics'] = res_mechanics[0]['count'] if res_mechanics else 0
            
            # Fetch mechanics list to display on dashboard
            mechanics = Database.execute_query(
                "SELECT id, first_name, last_name, email, phone, status FROM users WHERE role_id = 2 ORDER BY created_at DESC"
            )
        except Exception as e:
            print(f"Error fetching dashboard statistics: {e}")
            mechanics = []

        return render_template('owner-page/dashboard.html', stats=stats, mechanics=mechanics)

    @staticmethod
    def mechanic_dashboard():
        """Renders Mechanic specific workspace"""
        return render_template('mechanic-page/dashboard.html')

    @staticmethod
    def client_index():
        """Renders client storefront and appointment portal"""
        return render_template('client-page/index.html')
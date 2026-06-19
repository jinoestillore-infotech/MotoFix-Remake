from flask import render_template, request, redirect, url_for, flash, session
from app.database import Database
from app.models.user import User
from app.models.part import Part
from app.models.order import Order

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
            'low_stock_parts': 0,
            'pending_orders': 0
        }
        
        # Pull counts from database to present real-time dashboard data
        try:
            # Count Clients (Role ID: 3)
            res_clients = Database.execute_query("SELECT COUNT(*) as count FROM users WHERE role_id = 3")
            stats['total_clients'] = res_clients[0]['count'] if res_clients else 0

            # Count Mechanics (Role ID: 2)
            res_mechanics = Database.execute_query("SELECT COUNT(*) as count FROM users WHERE role_id = 2")
            stats['total_mechanics'] = res_mechanics[0]['count'] if res_mechanics else 0
            
            # Count Pending Orders
            res_orders = Database.execute_query("SELECT COUNT(*) as count FROM orders WHERE status = 'Pending'")
            stats['pending_orders'] = res_orders[0]['count'] if res_orders else 0
            
            # Fetch low-stock parts using our Part model method
            stats['low_stock_parts'] = Part.get_low_stock_count()
            
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
        try:
            parts = Part.find_all()
        except Exception as e:
            print(f"Error fetching client parts catalog: {e}")
            parts = []
            
        categories = ['Engine', 'Brakes', 'Suspension', 'Tires & Wheels', 'Electrical', 'Body & Frame', 'Fluids & Lubes', 'Accessories']
        return render_template('client-page/index.html', parts=parts, categories=categories)

    @staticmethod
    def owner_orders():
        """Renders the administrative customer orders management list view"""
        try:
            orders = Order.find_all_orders()
            orders_list = []
            for order in orders:
                order_dict = dict(order)
                # Attach order items
                order_dict['order_items'] = Order.get_order_items(order['id'])
                orders_list.append(order_dict)
        except Exception as e:
            print(f"Error compiling administrative orders: {e}")
            orders_list = []

        return render_template('owner-page/orders.html', orders=orders_list)

    @staticmethod
    def update_order_status(order_id):
        """Processes administrative status adjustments for client transactions"""
        new_status = request.form.get('status')
        valid_statuses = ['Pending', 'Processing', 'Completed', 'Cancelled']
        
        if new_status not in valid_statuses:
            flash("Invalid status transition requested.", "danger")
            return redirect(url_for('dashboard.owner_orders'))

        try:
            Order.update_status(order_id, new_status)
            flash(f"Order has been updated to '{new_status}' successfully!", "success")
        except Exception as e:
            flash(f"Failed to update status: {str(e)}", "danger")

        return redirect(url_for('dashboard.owner_orders'))
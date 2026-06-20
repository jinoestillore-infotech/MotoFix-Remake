from flask import render_template, request, session, redirect, url_for, flash
from app.models.user import User
from app.models.part import Part
from app.models.order import Order

class DashboardController:
    """Controller navigating business matrices, appointment logs, and order status cycles"""

    @staticmethod
    def owner_dashboard():
        """Aggregates active analytics for stats grid blocks"""
        total_clients_query = "SELECT COUNT(*) as count FROM users WHERE role_id = 3"
        total_mechanics_query = "SELECT COUNT(*) as count FROM users WHERE role_id = 2"
        total_appointments_query = "SELECT COUNT(*) as count FROM orders WHERE status = 'Pending'" # Placeholder for appointment count

        try:
            total_clients = User.Database.execute_query(total_clients_query)[0]['count']
            total_mechanics = User.Database.execute_query(total_mechanics_query)[0]['count']
            total_appointments = User.Database.execute_query(total_appointments_query)[0]['count']
            low_stock = Part.get_low_stock_count()
        except Exception:
            total_clients = 0
            total_mechanics = 0
            total_appointments = 0
            low_stock = 0

        stats = {
            'total_clients': total_clients,
            'total_mechanics': total_mechanics,
            'total_appointments': total_appointments,
            'low_stock_parts': low_stock
        }
        return render_template('owner-page/dashboard.html', stats=stats)

    @staticmethod
    def mechanic_dashboard():
        return render_template('mechanic-page/dashboard.html')

    @staticmethod
    def client_index():
        parts = Part.find_all()
        categories = ['Engine', 'Brakes', 'Suspension', 'Tires & Wheels', 'Electrical', 'Body & Frame', 'Fluids & Lubes', 'Accessories']
        return render_template('client-page/index.html', parts=parts, categories=categories)

    @staticmethod
    def view_owner_orders():
        """Lists active customer orders that are not yet marked as Paid"""
        orders = Order.find_all_orders()
        orders_list = []
        for order in orders:
            order_dict = dict(order)
            order_dict['order_items'] = Order.get_order_items(order['id'])
            orders_list.append(order_dict)
        return render_template('owner-page/orders.html', orders=orders_list)

    @staticmethod
    def update_order_status(order_id):
        """Allows Owners to change the status of an active client order"""
        status = request.form.get('status')
        if status:
            Order.update_status(order_id, status)
            flash(f"Order status successfully updated to '{status}'!", "success")
        else:
            flash("Invalid status selected.", "danger")
        return redirect(url_for('dashboard.owner_orders'))

    @staticmethod
    def mark_order_as_paid(order_id):
        """Performs transactional shift of completed orders to Paid state"""
        order = Order.find_by_id(order_id)
        if not order:
            flash("Order not found.", "danger")
            return redirect(url_for('dashboard.owner_orders'))

        if order['status'] != 'Completed':
            flash("Only completed orders can be flagged as paid.", "warning")
            return redirect(url_for('dashboard.owner_orders'))

        Order.mark_as_paid(order_id)
        flash(f"Order has been fully settled and moved to transaction history!", "success")
        return redirect(url_for('dashboard.owner_orders'))

    @staticmethod
    def view_transaction_history():
        """Lists completed and fully paid transactions for ledger summary analyses"""
        paid_orders = Order.find_paid_transactions()
        orders_list = []
        total_profit = 0.0

        for order in paid_orders:
            order_dict = dict(order)
            order_dict['order_items'] = Order.get_order_items(order['id'])
            total_profit += float(order['total_amount'])
            orders_list.append(order_dict)

        return render_template(
            'owner-page/transaction_history.html', 
            orders=orders_list, 
            total_profit=total_profit
        )
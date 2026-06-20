# project/app/controllers/dashboard_controller.py
import os
from flask import render_template, request, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from app.database import Database
from app.models.user import User
from app.models.part import Part
from app.models.order import Order
from app.models.payment_setting import PaymentSetting

# Configuration guidelines for valid payment QR uploads
ALLOWED_PAYMENT_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'gif'}

def allowed_file(filename):
    """Checks if the uploaded file has a valid image extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_PAYMENT_EXTENSIONS

class DashboardController:
    """Controller navigating business matrices, appointment logs, and order status cycles"""

    @staticmethod
    def owner_dashboard():
        """Aggregates active analytics for stats grid blocks"""
        total_clients_query = "SELECT COUNT(*) as count FROM users WHERE role_id = 3"
        total_mechanics_query = "SELECT COUNT(*) as count FROM users WHERE role_id = 2"
        pending_orders_query = "SELECT COUNT(*) as count FROM orders WHERE status = 'Pending'"

        try:
            # Resolved User.Database error by executing queries via direct Database class
            total_clients = Database.execute_query(total_clients_query)[0]['count']
            total_mechanics = Database.execute_query(total_mechanics_query)[0]['count']
            pending_orders = Database.execute_query(pending_orders_query)[0]['count']
            low_stock = Part.get_low_stock_count()
        except Exception as e:
            # Standard error logging to console
            print(f"Error loading dashboard metrics: {str(e)}")
            total_clients = 0
            total_mechanics = 0
            pending_orders = 0
            low_stock = 0

        # Aligned keys with the 'dashboard.html' requirements ('pending_orders')
        stats = {
            'total_clients': total_clients,
            'total_mechanics': total_mechanics,
            'pending_orders': pending_orders,
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
            flash(f"Order #{order_id} status successfully updated to '{status}'!", "success")
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
        flash(f"Order #{order_id} has been fully settled and moved to transaction history!", "success")
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

    @staticmethod
    def view_payment_settings():
        """Loads payment credentials manager dashboard"""
        settings = PaymentSetting.get()
        return render_template('owner-page/payment_settings.html', settings=settings)

    @staticmethod
    def update_payment_settings():
        """Processes edits to the GCash details and secures uploaded QR code picture files"""
        gcash_name = request.form.get('gcash_name', '').strip()
        gcash_phone = request.form.get('gcash_phone', '').strip()

        if not gcash_name or not gcash_phone:
            flash("GCash Name and Phone Number are required fields.", "danger")
            return redirect(url_for('dashboard.payment_settings'))

        image_filename = None
        if 'gcash_qr' in request.files:
            file = request.files['gcash_qr']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_folder = os.path.join('app', 'static', 'uploads', 'payments')
                os.makedirs(upload_folder, exist_ok=True)
                
                # Prefix filename with unique key
                unique_filename = f"gcash_qr_{filename}"
                file.save(os.path.join(upload_folder, unique_filename))
                image_filename = unique_filename

        try:
            PaymentSetting.update(gcash_name, gcash_phone, image_filename)
            flash("Payment method configuration updated successfully!", "success")
        except Exception as e:
            flash(f"Update failed: {str(e)}", "danger")
            
        return redirect(url_for('dashboard.payment_settings'))
from app.database import Database

class Order:
    """Model mapping database operations on 'orders' and 'order_items'"""

    @staticmethod
    def create_order(user_id: int, full_name: str, phone: str, fulfillment_method: str, address: str, payment_method: str, total_amount: float, notes: str = None):
        """Creates a new order record and returns the inserted ID"""
        query = """
            INSERT INTO orders (user_id, full_name, phone, fulfillment_method, address, payment_method, total_amount, notes, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Pending')
        """
        params = (user_id, full_name, phone, fulfillment_method, address, payment_method, total_amount, notes)
        return Database.execute_query(query, params, commit=True)

    @staticmethod
    def add_order_item(order_id: int, part_id: int, quantity: int, price: float):
        """Saves a single purchased item record connected to an order"""
        query = """
            INSERT INTO order_items (order_id, part_id, quantity, price)
            VALUES (%s, %s, %s, %s)
        """
        return Database.execute_query(query, (order_id, part_id, quantity, price), commit=True)

    @staticmethod
    def find_by_id(order_id: int):
        """Fetches order details by ID"""
        query = "SELECT * FROM orders WHERE id = %s"
        results = Database.execute_query(query, (order_id,))
        return results[0] if results else None

    @staticmethod
    def get_order_items(order_id: int):
        """Fetches all items associated with an order, joined with part details"""
        query = """
            SELECT oi.*, p.name, p.sku, p.image_filename
            FROM order_items oi
            JOIN parts p ON oi.part_id = p.id
            WHERE oi.order_id = %s
        """
        return Database.execute_query(query, (order_id,))

    @staticmethod
    def find_by_user_id(user_id: int):
        """Fetches all orders made by a specific customer, sorted newest to oldest"""
        query = "SELECT * FROM orders WHERE user_id = %s ORDER BY id DESC"
        return Database.execute_query(query, (user_id,))

    @staticmethod
    def find_all_orders():
        """Fetches all customer transactions across all shop users for administrative dashboards (excluding Paid ones to keep active dashboard clean)"""
        query = """
            SELECT o.*, u.first_name AS user_first, u.last_name AS user_last, u.email AS user_email
            FROM orders o
            JOIN users u ON o.user_id = u.id
            WHERE o.is_paid = 0
            ORDER BY o.id DESC
        """
        return Database.execute_query(query)

    @staticmethod
    def update_status(order_id: int, status: str):
        """Modifies status workflow state for client orders"""
        query = "UPDATE orders SET status = %s WHERE id = %s"
        return Database.execute_query(query, (status, order_id), commit=True)

    @staticmethod
    def get_active_count(user_id: int) -> int:
        """Counts orders that are currently active (Pending or Processing) for dynamic badge notifications"""
        query = "SELECT COUNT(*) as active_count FROM orders WHERE user_id = %s AND status IN ('Pending', 'Processing')"
        result = Database.execute_query(query, (user_id,))
        return result[0]['active_count'] if result else 0

    @staticmethod
    def mark_as_paid(order_id: int):
        """Flags an order as permanently paid"""
        query = "UPDATE orders SET is_paid = 1 WHERE id = %s"
        return Database.execute_query(query, (order_id,), commit=True)

    @staticmethod
    def clear_paid_history():
        """Permanently deletes all orders that have been paid and settled (is_paid = 1)"""
        query = "DELETE FROM orders WHERE is_paid = 1"
        return Database.execute_query(query, commit=True)
    
    @staticmethod
    def find_paid_transactions():
        """Fetches historical sales transactions which are flagged as is_paid = 1"""
        query = """
            SELECT o.*, u.first_name AS user_first, u.last_name AS user_last, u.email AS user_email
            FROM orders o
            JOIN users u ON o.user_id = u.id
            WHERE o.is_paid = 1
            ORDER BY o.id DESC
        """
        return Database.execute_query(query)
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
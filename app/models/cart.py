# project/app/models/cart.py
from app.database import Database

class Cart:
    """Model mapping database operations on 'cart_items' table"""

    @staticmethod
    def get_by_user_id(user_id: int):
        """Fetches all items in a user's cart along with live product prices, SKU codes, images, and stock balances"""
        query = """
            SELECT c.id, c.user_id, c.part_id, c.quantity, 
                   p.name, p.sku, p.price, p.image_filename, p.quantity AS stock_quantity
            FROM cart_items c
            JOIN parts p ON c.part_id = p.id
            WHERE c.user_id = %s
            ORDER BY c.created_at DESC
        """
        return Database.execute_query(query, (user_id,))

    @staticmethod
    def find_by_user_and_part(user_id: int, part_id: int):
        """Finds if a part is already added to a user's cart"""
        query = "SELECT * FROM cart_items WHERE user_id = %s AND part_id = %s"
        results = Database.execute_query(query, (user_id, part_id))
        return results[0] if results else None

    @staticmethod
    def add_item(user_id: int, part_id: int, quantity: int):
        """Inserts a new item into the cart database"""
        query = "INSERT INTO cart_items (user_id, part_id, quantity) VALUES (%s, %s, %s)"
        return Database.execute_query(query, (user_id, part_id, quantity), commit=True)

    @staticmethod
    def update_quantity(item_id: int, quantity: int):
        """Updates the quantity of an item in the cart"""
        query = "UPDATE cart_items SET quantity = %s WHERE id = %s"
        return Database.execute_query(query, (quantity, item_id), commit=True)

    @staticmethod
    def delete_item(item_id: int, user_id: int):
        """Securely removes an item from the cart of a specific user"""
        query = "DELETE FROM cart_items WHERE id = %s AND user_id = %s"
        return Database.execute_query(query, (item_id, user_id), commit=True)

    @staticmethod
    def get_total_count(user_id: int) -> int:
        """Sums up the total item quantities inside a user's cart"""
        query = "SELECT SUM(quantity) as total_count FROM cart_items WHERE user_id = %s"
        result = Database.execute_query(query, (user_id,))
        return result[0]['total_count'] if result and result[0]['total_count'] is not None else 0

    @staticmethod
    def find_by_id_and_user(item_id: int, user_id: int):
        """Verifies ownership of a cart item"""
        query = "SELECT * FROM cart_items WHERE id = %s AND user_id = %s"
        results = Database.execute_query(query, (item_id, user_id))
        return results[0] if results else None
from app.database import Database

class Cart:
    """Model mapping database operations on the 'cart_items' table"""

    @staticmethod
    def add_or_update(user_id: int, part_id: int, quantity: int):
        """Inserts a new item or updates the quantity of an existing item in the cart"""
        query = """
            INSERT INTO cart_items (user_id, part_id, quantity)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE quantity = quantity + VALUES(quantity)
        """
        params = (user_id, part_id, quantity)
        return Database.execute_query(query, params, commit=True)

    @staticmethod
    def get_user_cart(user_id: int):
        """Fetches all cart items for a specific user, joined with the parts table for details"""
        query = """
            SELECT c.id AS cart_item_id, c.quantity AS cart_quantity, 
                   p.id AS part_id, p.name, p.sku, p.price, p.brand, p.category, 
                   p.image_filename, p.quantity AS available_stock
            FROM cart_items c
            JOIN parts p ON c.part_id = p.id
            WHERE c.user_id = %s
            ORDER BY c.created_at DESC
        """
        return Database.execute_query(query, (user_id,))

    @staticmethod
    def get_cart_count(user_id: int) -> int:
        """Returns the total number of items currently in the user's cart"""
        query = "SELECT SUM(quantity) AS total_count FROM cart_items WHERE user_id = %s"
        results = Database.execute_query(query, (user_id,))
        if results and results[0]['total_count'] is not None:
            return int(results[0]['total_count'])
        return 0

    @staticmethod
    def get_item_in_cart(user_id: int, part_id: int):
        """Finds a specific cart record to inspect currently added volumes"""
        query = "SELECT * FROM cart_items WHERE user_id = %s AND part_id = %s"
        results = Database.execute_query(query, (user_id, part_id))
        return results[0] if results else None

    @staticmethod
    def update_quantity(user_id: int, part_id: int, quantity: int):
        """Directly overrides the quantity of a product in the cart"""
        query = "UPDATE cart_items SET quantity = %s WHERE user_id = %s AND part_id = %s"
        return Database.execute_query(query, (quantity, user_id, part_id), commit=True)

    @staticmethod
    def remove(user_id: int, part_id: int):
        """Removes an item from the user's cart"""
        query = "DELETE FROM cart_items WHERE user_id = %s AND part_id = %s"
        return Database.execute_query(query, (user_id, part_id), commit=True)
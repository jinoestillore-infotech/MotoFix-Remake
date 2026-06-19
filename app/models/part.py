from app.database import Database

class Part:
    """Model mapping database CRUD operations on the 'parts' table"""

    @staticmethod
    def create(name: str, sku: str, description: str, price: float, quantity: int, low_stock_threshold: int):
        """Inserts a new part into the inventory database"""
        query = """
            INSERT INTO parts (name, sku, description, price, quantity, low_stock_threshold)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (name, sku, description, price, quantity, low_stock_threshold)
        return Database.execute_query(query, params, commit=True)

    @staticmethod
    def find_all():
        """Fetches all items from parts catalog ordered by name"""
        query = "SELECT * FROM parts ORDER BY name ASC"
        return Database.execute_query(query)

    @staticmethod
    def find_by_id(part_id: int):
        """Fetches a single part by its primary ID"""
        query = "SELECT * FROM parts WHERE id = %s"
        results = Database.execute_query(query, (part_id,))
        return results[0] if results else None

    @staticmethod
    def find_by_sku(sku: str):
        """Fetches a single part by its unique Stock Keeping Unit (SKU)"""
        query = "SELECT * FROM parts WHERE sku = %s"
        results = Database.execute_query(query, (sku,))
        return results[0] if results else None

    @staticmethod
    def update(part_id: int, name: str, sku: str, description: str, price: float, quantity: int, low_stock_threshold: int):
        """Updates metadata and stock variables of a specific part"""
        query = """
            UPDATE parts 
            SET name = %s, sku = %s, description = %s, price = %s, quantity = %s, low_stock_threshold = %s
            WHERE id = %s
        """
        params = (name, sku, description, price, quantity, low_stock_threshold, part_id)
        return Database.execute_query(query, params, commit=True)

    @staticmethod
    def delete(part_id: int):
        """Removes a part entirely from inventory list"""
        query = "DELETE FROM parts WHERE id = %s"
        return Database.execute_query(query, (part_id,), commit=True)

    @staticmethod
    def get_low_stock_count():
        """Counts how many items reside below their low stock threshold levels"""
        query = "SELECT COUNT(*) as count FROM parts WHERE quantity <= low_stock_threshold"
        res = Database.execute_query(query)
        return res[0]['count'] if res else 0
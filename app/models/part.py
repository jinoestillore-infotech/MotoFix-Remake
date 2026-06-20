from app.database import Database

class Part:
    """Model mapping database operations on the enhanced 'parts' table"""

    @staticmethod
    def create(sku: str, name: str, brand: str, category: str, description: str, price: float, quantity: int, low_stock_threshold: int, image_filename: str = None):
        """Creates a new motorcycle part item"""
        query = """
            INSERT INTO parts (sku, name, brand, category, description, price, quantity, low_stock_threshold, image_filename)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (sku, name, brand, category, description, price, quantity, low_stock_threshold, image_filename)
        return Database.execute_query(query, params, commit=True)

    @staticmethod
    def find_all():
        """Fetches all items in the inventory"""
        query = "SELECT * FROM parts ORDER BY name ASC"
        return Database.execute_query(query)

    @staticmethod
    def find_by_id(part_id: int):
        """Finds a single part by ID"""
        query = "SELECT * FROM parts WHERE id = %s"
        results = Database.execute_query(query, (part_id,))
        return results[0] if results else None

    @staticmethod
    def find_by_sku(sku: str):
        """Finds a part by SKU"""
        query = "SELECT * FROM parts WHERE sku = %s"
        results = Database.execute_query(query, (sku,))
        return results[0] if results else None

    @staticmethod
    def update(part_id: int, sku: str, name: str, brand: str, category: str, description: str, price: float, quantity: int, low_stock_threshold: int, image_filename: str = None):
        """Updates an existing part's details including category, brand, and image"""
        if image_filename:
            query = """
                UPDATE parts 
                SET sku = %s, name = %s, brand = %s, category = %s, description = %s, price = %s, quantity = %s, low_stock_threshold = %s, image_filename = %s
                WHERE id = %s
            """
            params = (sku, name, brand, category, description, price, quantity, low_stock_threshold, image_filename, part_id)
        else:
            # Maintain previous image if a new one is not uploaded
            query = """
                UPDATE parts 
                SET sku = %s, name = %s, brand = %s, category = %s, description = %s, price = %s, quantity = %s, low_stock_threshold = %s
                WHERE id = %s
            """
            params = (sku, name, brand, category, description, price, quantity, low_stock_threshold, part_id)
        
        return Database.execute_query(query, params, commit=True)

    @staticmethod
    def delete(part_id: int):
        """Removes a part item from database"""
        query = "DELETE FROM parts WHERE id = %s"
        return Database.execute_query(query, (part_id,), commit=True)

    @staticmethod
    def get_low_stock_count():
        """Counts items whose stock is less than or equal to their low stock warning threshold"""
        query = "SELECT COUNT(*) as count FROM parts WHERE quantity <= low_stock_threshold"
        results = Database.execute_query(query)
        return results[0]['count'] if results else 0
from app.database import Database

class Role:
    """Model mapping database operations on 'roles' table"""

    @staticmethod
    def find_all():
        query = "SELECT * FROM roles ORDER BY id ASC"
        return Database.execute_query(query)

    @staticmethod
    def find_by_id(role_id: int):
        query = "SELECT * FROM roles WHERE id = %s"
        results = Database.execute_query(query, (role_id,))
        return results[0] if results else None

    @staticmethod
    def find_by_name(name: str):
        query = "SELECT * FROM roles WHERE name = %s"
        results = Database.execute_query(query, (name,))
        return results[0] if results else None
from app.database import Database

class User:
    """Model mapping database operations on 'users' table"""

    @staticmethod
    def create(role_id: int, first_name: str, last_name: str, email: str, phone: str, password_hash: str):
        """Inserts a new user record into the DB"""
        query = """
            INSERT INTO users (role_id, first_name, last_name, email, phone, password_hash, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'active')
        """
        params = (role_id, first_name, last_name, email, phone, password_hash)
        return Database.execute_query(query, params, commit=True)

    @staticmethod
    def find_by_email(email: str):
        """Fetches a single user join with their system Role"""
        query = """
            SELECT u.*, r.name AS role_name 
            FROM users u
            JOIN roles r ON u.role_id = r.id
            WHERE u.email = %s
        """
        results = Database.execute_query(query, (email,))
        return results[0] if results else None

    @staticmethod
    def find_by_id(user_id: int):
        """Fetches standard user information by user ID"""
        query = """
            SELECT u.*, r.name AS role_name 
            FROM users u
            JOIN roles r ON u.role_id = r.id
            WHERE u.id = %s
        """
        results = Database.execute_query(query, (user_id,))
        return results[0] if results else None
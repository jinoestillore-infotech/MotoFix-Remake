import bcrypt

class Helpers:
    """Security utilities for encryption and verification"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a clear-text password using bcrypt."""
        if not password:
            raise ValueError("Password cannot be empty")
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    @staticmethod
    def check_password(password: str, hashed_password: str) -> bool:
        """Verify standard password match with bcrypt hash."""
        if not password or not hashed_password:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
# project/app/models/payment_setting.py
from app.database import Database

class PaymentSetting:
    """Model mapping database operations on 'payment_settings' configuration table"""

    @staticmethod
    def get():
        """Retrieves active shop settings parameters"""
        query = "SELECT * FROM payment_settings WHERE id = 1 LIMIT 1"
        results = Database.execute_query(query)
        if results:
            return results[0]
        # Robust fallback dict in case table row seeding hasn't completed yet
        return {
            'id': 1,
            'gcash_name': 'MotoShop Parts Admin',
            'gcash_phone': '0917-888-2918',
            'gcash_qr_filename': None
        }

    @staticmethod
    def update(gcash_name: str, gcash_phone: str, gcash_qr_filename: str = None):
        """Updates payment collection configurations dynamically or inserts them if missing"""
        if gcash_qr_filename:
            query = """
                INSERT INTO payment_settings (id, gcash_name, gcash_phone, gcash_qr_filename)
                VALUES (1, %s, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    gcash_name = VALUES(gcash_name), 
                    gcash_phone = VALUES(gcash_phone), 
                    gcash_qr_filename = VALUES(gcash_qr_filename)
            """
            params = (gcash_name, gcash_phone, gcash_qr_filename)
        else:
            query = """
                INSERT INTO payment_settings (id, gcash_name, gcash_phone)
                VALUES (1, %s, %s)
                ON DUPLICATE KEY UPDATE 
                    gcash_name = VALUES(gcash_name), 
                    gcash_phone = VALUES(gcash_phone)
            """
            params = (gcash_name, gcash_phone)
        return Database.execute_query(query, params, commit=True)
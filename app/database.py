import mysql.connector
from mysql.connector import pooling
from app.config import Config

class Database:
    """Thread-Safe Connection Pool implementation for MySQL"""
    _pool = None

    @classmethod
    def initialize(cls):
        if cls._pool is None:
            try:
                cls._pool = mysql.connector.pooling.MySQLConnectionPool(
                    pool_name="moto_pool",
                    pool_size=10,  # Max connections in pool
                    host=Config.DB_HOST,
                    user=Config.DB_USER,
                    password=Config.DB_PASSWORD,
                    database=Config.DB_NAME
                )
            except mysql.connector.Error as err:
                print(f"Database Initialization Error: {err}")
                raise err

    @classmethod
    def get_connection(cls):
        if cls._pool is None:
            cls.initialize()
        return cls._pool.get_connection()

    @classmethod
    def execute_query(cls, query, params=None, commit=False):
        """Helper to run a query and manage connections cleanly"""
        conn = cls.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = None
        try:
            cursor.execute(query, params or ())
            if commit:
                conn.commit()
                result = cursor.lastrowid
            else:
                result = cursor.fetchall()
        except mysql.connector.Error as err:
            conn.rollback()
            print(f"Query execution error: {err}")
            raise err
        finally:
            cursor.close()
            conn.close()
        return result
# app/database.py
import urllib.parse
import os
import mysql.connector
from mysql.connector import pooling
from app.config import Config

class Database:
    """Thread-Safe Connection Pool implementation for MySQL with URI and SSL support"""
    _pool = None

    @classmethod
    def initialize(cls):
        if cls._pool is None:
            try:
                # Safely check for DATABASE_URL attribute to avoid AttributeError conflicts with config.py
                db_url = getattr(Config, 'DATABASE_URL', os.environ.get('DATABASE_URL'))

                if db_url and db_url.startswith("mysql://"):
                    # Parse the URI cleanly (Aiven URI flow)
                    url = urllib.parse.urlparse(db_url)
                    db_user = url.username
                    db_password = url.password
                    db_host = url.hostname
                    db_port = url.port
                    db_name = url.path[1:] if url.path else getattr(Config, 'DB_NAME', 'defaultdb')

                    cls._pool = mysql.connector.pooling.MySQLConnectionPool(
                        pool_name="moto_pool",
                        pool_size=10,
                        host=db_host,
                        port=db_port,
                        user=db_user,
                        password=db_password,
                        database=db_name,
                        ssl_disabled=False  # Tells the driver to negotiate SSL securely with Aiven
                    )
                else:
                    # Fallback to separate configuration parameters (Matches your .env & config.py setup)
                    db_host = getattr(Config, 'DB_HOST', 'localhost')
                    db_user = getattr(Config, 'DB_USER', 'root')
                    db_password = getattr(Config, 'DB_PASSWORD', '')
                    db_name = getattr(Config, 'DB_NAME', 'defaultdb')
                    
                    # Safely handle custom ports if provided in host string (e.g., host:port) or environment
                    db_port = 3306
                    if ":" in db_host:
                        db_host, port_str = db_host.split(":", 1)
                        db_port = int(port_str)
                    else:
                        db_port = int(os.environ.get('DB_PORT', 3306))

                    # Automatically enforce SSL parameters if connecting to an external cloud database
                    is_cloud_db = 'aivencloud.com' in db_host or 'render.com' in db_host
                    ssl_args = {'ssl_disabled': False} if is_cloud_db else {}

                    cls._pool = mysql.connector.pooling.MySQLConnectionPool(
                        pool_name="moto_pool",
                        pool_size=10,
                        host=db_host,
                        port=db_port,
                        user=db_user,
                        password=db_password,
                        database=db_name,
                        **ssl_args
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
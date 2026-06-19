import os
from dotenv import load_dotenv

# Load environmental variables from .env file
load_dotenv()

class Config:
    """Base Configuration Class"""
    SECRET_KEY = os.getenv("SECRET_KEY", "your_highly_secure_secret_key_12345")
    
    # Database Configurations
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "moto_db")
    
    # Session Configuration
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
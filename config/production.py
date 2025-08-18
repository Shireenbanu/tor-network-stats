import os
from dotenv import load_dotenv

class ProductionConfig:
    def __init__(self):
        # Load production environment variables (optional, AWS Lambda sets env vars directly)
        if os.path.exists('.env.production'):
            load_dotenv('.env.production')
        
        # Required database credentials - will fail if not set
        self.DB_HOST = self._require_env('DB_HOST')
        self.DB_USER = self._require_env('DB_USER')
        self.DB_PASSWORD = self._require_env('DB_PASSWORD')
        self.DB_NAME = self._require_env('DB_NAME')
        
        # Optional with sensible defaults
        self.DB_PORT = int(os.getenv('DB_PORT', '5432'))


    def get_database_url(self):
        """Return database URL string with SSL for production"""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}?sslmode=require"
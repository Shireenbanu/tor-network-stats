import os
from dotenv import load_dotenv

class DevelopmentConfig:
    def __init__(self):
        # Load development environment variables
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print(f"Project Root: {project_root}")
        env_path = os.path.join(project_root, '.env.development')
        print(f"Env Path: {env_path}")

        load_dotenv(env_path)
        
        # Required database credentials - will fail if not set
        self.DB_HOST = self._require_env('DB_HOST')
        self.DB_USER = self._require_env('DB_USER')
        self.DB_PASSWORD = self._require_env('DB_PASSWORD')
        self.DB_NAME = self._require_env('DB_NAME')
        
        # Optional with sensible defaults
        self.DB_PORT = int(os.getenv('DB_PORT', '5432'))

    def _require_env(self, var_name):
        """Get required environment variable or raise error"""
        value = os.getenv(var_name)
        if not value:
            raise ValueError(f"Environment variable {var_name} is required but not set in .env.development")
        return value


    def get_database_url(self):
        """Return database URL string"""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
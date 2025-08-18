
"""Configuration loader - determines which config to use based on ENVIRONMENT variable"""
import os

def get_config():
    """
    Load configuration based on ENVIRONMENT variable
    Returns the appropriate configuration class instance
    """
    
    # Get environment from system environment variable
    environment = os.getenv('ENVIRONMENT', 'development')
    
    print(f"Loading configuration for environment: {environment}")
    
    if environment == 'production':
        from .production import ProductionConfig
        return ProductionConfig()
    elif environment == 'staging':
        # You can add staging config later if needed
        from .production import ProductionConfig
        return ProductionConfig()
    else:  # development (default)
        from .development import DevelopmentConfig
        return DevelopmentConfig()
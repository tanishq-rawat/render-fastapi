"""
Configuration settings for the application.
Loads environment variables and provides application settings.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = os.getenv("APP_NAME", "Expense Tracker API")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
    
    # Security - JWT Configuration
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./expense_tracker.db")
    
    def __init__(self):
        """Validate required settings on initialization."""
        if not self.SECRET_KEY:
            raise ValueError(
                "SECRET_KEY is not set. Please set it in your .env file. "
                "Generate one using: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
            )


# Create settings instance
settings = Settings()

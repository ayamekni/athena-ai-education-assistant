"""
Configuration module for ATHENA backend
Handles environment variables and application settings
"""
from pydantic_settings import BaseSettings
from typing import Optional, List
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "ATHENA - AI EdTech Platform"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # MongoDB
    MONGO_URI: str
    DATABASE_NAME: str = "athena"
    
    # JWT Settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS - will be parsed from comma-separated string in .env
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173,http://localhost:8080,http://localhost:8081,http://127.0.0.1:8080,http://127.0.0.1:8081"
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse ALLOWED_ORIGINS from comma-separated string"""
        if isinstance(self.ALLOWED_ORIGINS, str):
            return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(',') if origin.strip()]
        return self.ALLOWED_ORIGINS
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Ignore extra fields in .env


# Global settings instance
settings = Settings()

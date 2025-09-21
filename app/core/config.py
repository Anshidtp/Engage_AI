import os
from typing import List, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = "LinkedIn Post Generator"
    app_version: str = "1.0.0"
    debug: bool = False
    log_level: str = "INFO"
    
    # API Keys
    google_api_key: str
    serpapi_api_key: Optional[str] = None

    
    
    # News search settings
    max_news_results: int = 5
    news_search_days: int = 7
    
    # AI Generation settings
    max_post_length: int = 3000
    temperature: float = 0.7
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False


settings = Settings()
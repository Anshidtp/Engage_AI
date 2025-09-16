import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator


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
    google_cse_id: Optional[str] = None
    
    # # CORS
    # ALLOWED_ORIGINS: List[str] = ["*"]
    
    # Rate limiting
    rate_limit_per_minute: int = 10
    
    # News search settings
    max_news_results: int = 5
    news_search_days: int = 7
    
    # AI Generation settings
    max_post_length: int = 3000
    temperature: float = 0.7
    
    # @validator("allowed_origins", pre=True)
    # def assemble_cors_origins(cls, v):
    #     """Parse CORS origins from string."""
    #     if isinstance(v, str) and not v.startswith("["):
    #         return [i.strip() for i in v.split(",")]
    #     elif isinstance(v, (list, str)):
    #         return v
    #     raise ValueError(v)
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False


settings = Settings()
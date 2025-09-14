from typing import Any, Dict, Optional


class AppException(Exception):
    """Base application exception."""
    
    def __init__(
        self,
        message: str,
        code: str = "APP_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)


class APIKeyError(AppException):
    """API key related errors."""
    
    def __init__(self, message: str = "Invalid or missing API key"):
        super().__init__(message, "API_KEY_ERROR")


class NewsSearchError(AppException):
    """News search related errors."""
    
    def __init__(self, message: str = "Failed to search news"):
        super().__init__(message, "NEWS_SEARCH_ERROR")


class AIGenerationError(AppException):
    """AI generation related errors."""
    
    def __init__(self, message: str = "Failed to generate content"):
        super().__init__(message, "AI_GENERATION_ERROR")


class RateLimitError(AppException):
    """Rate limiting errors."""
    
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, "RATE_LIMIT_ERROR")
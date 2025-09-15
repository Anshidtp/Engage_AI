from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class NewsSource(BaseModel):
    """News source information."""
    
    title: str
    url: str
    published_date: Optional[datetime] = None
    source_name: Optional[str] = None
    snippet: Optional[str] = None


class GeneratePostResponse(BaseModel):
    """Response model for generated LinkedIn post."""
    
    topic: str = Field(description="Original topic requested")
    
    linkedin_post: str = Field(description="Generated LinkedIn post content")
    
    news_sources: List[NewsSource] = Field(
        description="List of news sources used for generation"
    )
    
    image_suggestion: Optional[str] = Field(
        default=None,
        description="Suggested image URL or search query"
    )
    
    hashtags: List[str] = Field(
        default_factory=list,
        description="Suggested hashtags for the post"
    )
    
    generated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Timestamp when post was generated"
    )
    
    word_count: int = Field(description="Word count of generated post")
    
    character_count: int = Field(description="Character count of generated post")


class ErrorResponse(BaseModel):
    """Error response model."""
    
    error: str = Field(description="Error message")
    code: str = Field(description="Error code")
    details: dict = Field(default_factory=dict, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
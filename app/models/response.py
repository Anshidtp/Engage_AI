from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class NewsSource(BaseModel):
    """News source information."""
    
    title: str
    url: str
    published_date: Optional[datetime] = None
    source_name: Optional[str] = None
    snippet: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

class ProcessingMetadata(BaseModel):
    """Metadata about the LangGraph workflow processing."""
    
    search_attempts: int = Field(description="Number of news search attempts")
    generation_attempts: int = Field(description="Number of content generation attempts")
    error_messages: List[str] = Field(default_factory=list, description="Any error messages during processing")
    news_analysis: Optional[Dict[str, Any]] = Field(description="News analysis results")
    content_outline: Optional[Dict[str, Any]] = Field(description="Content outline used")


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

    # Enhanced LangGraph-specific fields
    quality_score: Optional[float] = Field(
        default=None,
        description="AI-assessed quality score (1-10)",
        ge=1.0,
        le=10.0
    )
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class ErrorResponse(BaseModel):
    error: str = Field(description="Error message")
    code: str = Field(description="Error code")
    details: dict = Field(default_factory=dict, description="Additional error details")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
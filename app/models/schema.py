from typing import List
from pydantic import BaseModel, Field
from app.models.response import NewsSource

class PostRequest(BaseModel):
    """Request model for post generation."""
    topic: str = Field(..., min_length=1, max_length=100, description="Topic for LinkedIn post")


class PostResponse(BaseModel):
    """Response model for generated post."""
    topic: str
    news_sources: List[NewsSource] = Field(
        description="List of news sources used for generation"
    )
    linkedin_post: str
    image_suggestion: str = None
from typing import Optional
from pydantic import BaseModel, Field, validator


class GeneratePostRequest(BaseModel):
    """Request model for generating LinkedIn post."""
    
    topic: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Topic to search news for and generate post about"
    )
    
    style: Optional[str] = Field(
        default="professional",
        description="Post style: professional, casual, thought-leadership"
    )
    
    include_hashtags: bool = Field(
        default=True,
        description="Whether to include relevant hashtags"
    )
    
    max_length: Optional[int] = Field(
        default=2000,
        ge=100,
        le=3000,
        description="Maximum post length in characters"
    )
    
    @validator("topic")
    def validate_topic(cls, v):
        """Validate topic field."""
        if not v.strip():
            raise ValueError("Topic cannot be empty")
        return v.strip()
    
    @validator("style")
    def validate_style(cls, v):
        """Validate style field."""
        allowed_styles = ["professional", "casual", "thought-leadership"]
        if v and v not in allowed_styles:
            raise ValueError(f"Style must be one of: {', '.join(allowed_styles)}")
        return v
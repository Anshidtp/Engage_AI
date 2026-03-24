from typing import List, Dict, Any, Optional, TypedDict, Annotated
from datetime import datetime
from pydantic import BaseModel
from operator import add

from app.models.response import NewsSource


class WorkflowState(TypedDict):
    """State for the LinkedIn post generation workflow."""
    
    # Input parameters
    topic: str
    style: str
    max_length: int
    include_hashtags: bool
    
    # Intermediate results
    news_sources: Annotated[List[NewsSource], add]
    news_analysis: Optional[Dict[str, Any]]
    content_outline: Optional[Dict[str, Any]]
    
    # Generated content
    draft_post: Optional[str]
    refined_post: Optional[str]
    hashtags: Annotated[List[str], add]
    image_suggestion: Optional[str]
    
    # Metadata
    processing_stage: str
    error_messages: Annotated[List[str], add]
    quality_score: Optional[float]
    word_count: Optional[int]
    character_count: Optional[int]
    
    # Tool results
    search_attempts: int
    generation_attempts: int


class NewsAnalysisResult(BaseModel):
    """Result from news analysis step."""
    
    key_themes: List[str]
    sentiment: str  # positive, negative, neutral
    industry_impact: str
    trend_direction: str  # rising, declining, stable
    credibility_score: float
    summary: str


class ContentOutline(BaseModel):
    """Content outline for LinkedIn post."""
    
    hook: str
    main_points: List[str]
    call_to_action: str
    tone_keywords: List[str]
    target_audience: str
    estimated_engagement_score: float


class QualityMetrics(BaseModel):
    """Quality assessment metrics for generated content."""
    
    readability_score: float
    engagement_potential: float
    professional_tone: float
    linkedin_best_practices: float
    overall_score: float
    improvement_suggestions: List[str]
from typing import Dict, Any
from app.services.langraph_workflow import LinkedInPostWorkflow
from app.models.requests import GeneratePostRequest
from app.models.response import GeneratePostResponse, NewsSource
from app.core.logging import get_logger
from app.core.exceptions import AppException

logger = get_logger(__name__)


class LangGraphPostGeneratorService:
    """Enhanced post generator service using LangGraph workflow."""
    
    def __init__(self):
        self.workflow = LinkedInPostWorkflow()
    
    async def generate_post(self, request: GeneratePostRequest) -> GeneratePostResponse:
        """
        Generate a LinkedIn post using LangGraph workflow.
        
        Args:
            request: Post generation request
            
        Returns:
            Generated post response with enhanced metadata
            
        Raises:
            AppException: If generation fails
        """
        try:
            logger.info(f"Starting LangGraph post generation for topic: {request.topic}")
            
            # Run LangGraph workflow
            workflow_result = await self.workflow.generate_post(
                topic=request.topic,
                style=request.style or "professional",
                max_length=request.max_length or 2000,
                include_hashtags=request.include_hashtags
            )
            
            # Convert news sources if available
            news_sources = []
            for source_data in workflow_result.get("news_sources", []):
                if isinstance(source_data, dict):
                    news_sources.append(NewsSource(**source_data))
                else:
                    news_sources.append(source_data)
            
            # Create enhanced response
            response = GeneratePostResponse(
                topic=request.topic,
                linkedin_post=workflow_result["post_content"],
                news_sources=news_sources,
                image_suggestion=workflow_result.get("image_suggestion"),
                hashtags=workflow_result.get("hashtags", []),
                word_count=workflow_result.get("word_count", 0),
                character_count=workflow_result.get("character_count", 0),
                quality_score=workflow_result.get("quality_score", 0.0)
            )
            
            
            logger.info(f"LangGraph post generation completed successfully. Quality: {response.quality_score:.1f}/10")
            return response
            
        except Exception as e:
            logger.error(f"LangGraph post generation failed: {str(e)}")
            if isinstance(e, AppException):
                raise
            else:
                raise AppException(f"Enhanced post generation failed: {str(e)}")
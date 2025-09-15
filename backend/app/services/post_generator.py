from typing import Dict, Any
from app.services.linkedin_agent import AIAgent
from app.services.news_agent import NewsSearchAgent
from app.models.requests import GeneratePostRequest
from app.models.response import GeneratePostResponse, NewsSource
from app.core.logging import get_logger
from app.core.exceptions import AppException

logger = get_logger(__name__)


class PostGeneratorService:
    """Main service for orchestrating post generation."""
    
    def __init__(self):
        self.ai_agent = AIAgent()
        self.news_service = NewsSearchAgent()
    
    async def generate_post(self, request: GeneratePostRequest) -> GeneratePostResponse:
        """
        Generate a LinkedIn post based on request parameters.
        
        Args:
            request: Post generation request
            
        Returns:
            Generated post response
            
        Raises:
            AppException: If generation fails
        """
        try:
            logger.info(f"Starting post generation for topic: {request.topic}")
            
            # Step 1: Search for recent news
            news_sources = await self.news_service.search_news(
                topic=request.topic,
                limit=5
            )
            
            if not news_sources:
                logger.warning(f"No news sources found for topic: {request.topic}")
                # Create a fallback news source
                news_sources = [
                    NewsSource(
                        title=f"Industry insights on {request.topic}",
                        url=f"https://example.com/{request.topic.lower().replace(' ', '-')}",
                        source_name="Industry Report",
                        snippet=f"Latest trends and developments in {request.topic}"
                    )
                ]
            
            # Step 2: Generate LinkedIn post using AI
            generation_result = await self.ai_agent.generate_linkedin_post(
                topic=request.topic,
                news_sources=news_sources,
                style=request.style or "professional",
                max_length=request.max_length or 2000,
                include_hashtags=request.include_hashtags
            )
            
            # Step 3: Create response
            response = GeneratePostResponse(
                topic=request.topic,
                linkedin_post=generation_result["post_content"],
                news_sources=news_sources,
                image_suggestion=generation_result["image_suggestion"],
                hashtags=generation_result["hashtags"],
                word_count=generation_result["word_count"],
                character_count=generation_result["character_count"]
            )
            
            logger.info("Post generation completed successfully")
            return response
            
        except Exception as e:
            logger.error(f"Post generation failed: {str(e)}")
            if isinstance(e, AppException):
                raise
            else:
                raise AppException(f"Unexpected error during post generation: {str(e)}")
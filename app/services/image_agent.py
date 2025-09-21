import asyncio
from typing import Optional
from serpapi import GoogleSearch

from backend.app.core.config import settings
from backend.app.core.logging import get_logger

logger = get_logger(__name__)


class ImageAgent:
    """Service for generating image suggestions using SerpAPI."""
    
    def __init__(self):
        self.serpapi_key = settings.serpapi_api_key
    
    async def get_image_suggestion(self, topic: str) -> Optional[str]:
        """
        Get image suggestion URL for the topic using SerpAPI.
        
        Args:
            topic: The topic to find images for
            
        Returns:
            Image URL or fallback suggestion
        """
        try:
            logger.info(f"Searching images for topic: {topic}")
            
            if self.serpapi_key:
                return await self._search_with_serpapi(topic)
            else:
                return self._get_fallback_suggestion(topic)
                
        except Exception as e:
            logger.error(f"Image search failed: {str(e)}")
            return self._get_fallback_suggestion(topic)
    
    async def _search_with_serpapi(self, topic: str) -> Optional[str]:
        """Search Google Images using SerpAPI."""
        try:
            # Create search query for professional business images
            search_query = f"{topic} professional business"
            
            search_params = {
                "engine": "google",
                "q": search_query,
                "api_key": self.serpapi_key,
                "tbm": "isch",  # Images search
                "imgsz": "l",   # Large images
                "imgtype": "photo",  # Photo type
                "safe": "active",  # Safe search
                "num": 3  # Get top 3 results
            }
            
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            search = await loop.run_in_executor(None, lambda: GoogleSearch(search_params))
            results = await loop.run_in_executor(None, search.get_dict)
            
            # Extract image URLs
            if "images_results" in results and results["images_results"]:
                # Get the first high-quality image
                for image in results["images_results"]:
                    if "original" in image:
                        logger.info(f"Found image: {image['original']}")
                        return image["original"]
                    elif "thumbnail" in image:
                        logger.info(f"Using thumbnail: {image['thumbnail']}")
                        return image["thumbnail"] 
            
            logger.warning(f"No images found for topic: {topic}")
            return self._get_fallback_suggestion(topic)
            
        except Exception as e:
            logger.error(f"SerpAPI image search failed: {str(e)}")
            return self._get_fallback_suggestion(topic)
    
    def _get_fallback_suggestion(self, topic: str) -> str:
        """Fallback image suggestion when SerpAPI is unavailable."""
        topic_encoded = topic.replace(" ", "%20")
        logger.info(f"Using fallback image suggestion for: {topic}")
        return f"https://source.unsplash.com/1200x630/?{topic_encoded},business,professional"
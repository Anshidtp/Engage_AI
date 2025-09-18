import aiohttp
from typing import Optional

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


class ImageService:
    """Service for generating image suggestions."""
    
    def __init__(self):
        self.unsplash_key = settings.unsplash_access_key
    
    async def get_image_suggestion(self, topic: str) -> Optional[str]:
        """
        Get image suggestion URL for the topic.
        
        Args:
            topic: The topic to find images for
            
        Returns:
            Image URL or None
        """
        try:
            if self.unsplash_key:
                return await self._search_unsplash(topic)
            else:
                return self._get_fallback_suggestion(topic)
                
        except Exception as e:
            logger.error(f"Image search failed: {str(e)}")
            return self._get_fallback_suggestion(topic)
    
    async def _search_unsplash(self, topic: str) -> Optional[str]:
        """Search Unsplash for relevant images."""
        try:
            async with aiohttp.ClientSession() as session:
                url = "https://api.unsplash.com/search/photos"
                headers = {"Authorization": f"Client-ID {self.unsplash_key}"}
                params = {
                    "query": topic,
                    "page": 1,
                    "per_page": 1,
                    "orientation": "landscape"
                }
                
                async with session.get(url, headers=headers, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("results"):
                            return data["results"][0]["urls"]["regular"]
            
            return self._get_fallback_suggestion(topic)
            
        except Exception as e:
            logger.error(f"Unsplash search failed: {str(e)}")
            return self._get_fallback_suggestion(topic)
    
    def _get_fallback_suggestion(self, topic: str) -> str:
        """Fallback image suggestion."""
        topic_encoded = topic.replace(" ", "%20")
        return f"https://source.unsplash.com/1200x630/?{topic_encoded},business,professional"
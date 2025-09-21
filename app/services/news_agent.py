import asyncio
from typing import List, Optional
from datetime import datetime, timedelta
from serpapi import GoogleSearch

from app.core.config import settings
from app.core.logging import get_logger
from app.models.response import NewsSource
from app.core.exceptions import NewsSearchError

logger = get_logger(__name__)

class NewsSearchAgent:
    """Agent to handle news searching using Google Custom Search or SerpAPI."""
    def __init__(self):
        self.serp_api_key = settings.serpapi_api_key

    async def search_news(self, topic: str, limit: int = 5) -> List[NewsSource]:
        """
        Search for recent news articles on a topic.
        
        Args:
            topic: The topic to search for
            limit: Maximum number of results to return
            
        Returns:
            List of news sources
            
        Raises:
            NewsSearchError: If search fails
            APIKeyError: If API key is invalid
        """
        try:
            logger.info(f"Searching news for topic: {topic}")
            
            if self.serp_api_key:
                return await self._search_with_serpapi(topic, limit)
            else:
                # Fallback to a simple web scraping approach
                return await self._get_fallback_urls(topic, limit)
                
        except Exception as e:
            logger.error(f"News search failed: {str(e)}")
            raise NewsSearchError(f"Failed to search news: {str(e)}")
        
    async def _search_with_serpapi(self, topic: str, limit: int) -> List[str]:
        """Search using SerpAPI."""
        try:
            # Calculate date range for recent news
            end_date = datetime.now()
            start_date = end_date - timedelta(days=settings.news_search_days)
            
            search_params = {
                "engine": "google",
                "q": f"{topic} news",
                "api_key": self.serp_api_key,
                "num": limit,
                "tbm": "nws",  # News search
                "tbs": f"cdr:1,cd_min:{start_date.strftime('%m/%d/%Y')},cd_max:{end_date.strftime('%m/%d/%Y')}"
            }
            
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            search = await loop.run_in_executor(
                None, lambda: GoogleSearch(search_params)
            )
            results = await loop.run_in_executor(None, search.get_dict)
            
            news_sources = []

            
            if "news_results" in results:
                for result in results["news_results"][:limit]:
                    source = NewsSource(
                        title=result.get("title", ""),
                        url=result.get("link", ""),
                        source_name=result.get("source", ""),
                        snippet=result.get("snippet", ""),
                        published_date=self._parse_date(result.get("date"))
                    )
                    news_sources.append(source)
            
            logger.info(f"Found {len(news_sources)} news articles")
            return news_sources if news_sources else self._get_fallback_urls(topic)
            
        except Exception as e:
            logger.error(f"SerpAPI search failed: {str(e)}")
            raise NewsSearchError(f"SerpAPI search failed: {str(e)}")
        
    def _get_fallback_urls(self, topic: str) -> List[str]:
        """Return fallback URLs if no news found."""
        logger.info("Using fallback news URLs")
        return [
            f"https://news.google.com/search?q={topic.replace(' ', '%20')}",
            f"https://www.bing.com/news/search?q={topic.replace(' ', '%20')}",
            f"https://www.reuters.com/search/news?blob={topic.replace(' ', '%20')}"
        ]
    
    # async def _search_fallback(self, topic: str, limit: int) -> List[NewsSource]:
    #     """Fallback search method using NewsAPI or similar free service."""
    #     logger.warning("Using fallback news search method")
        
    #     # This is a simplified fallback - you might want to integrate with
    #     # other free news APIs like NewsAPI, or implement web scraping
    #     news_sources = []
        
    #     try:
    #         # Example using a free news aggregator API
    #         # You can replace this with any other free news API
            
    #         async with aiohttp.ClientSession() as session:
    #             # Using a hypothetical free news API endpoint
    #             url = f"https://api.example-news.com/search"
    #             params = {
    #                 "q": topic,
    #                 "limit": limit,
    #                 "category": "general"
    #             }
                
    #             async with session.get(url, params=params) as response:
    #                 if response.status == 200:
    #                     data = await response.json()
                        
    #                     for article in data.get("articles", [])[:limit]:
    #                         source = NewsSource(
    #                             title=article.get("title", ""),
    #                             url=article.get("url", ""),
    #                             source_name=article.get("source", ""),
    #                             snippet=article.get("description", ""),
    #                             published_date=self._parse_date(article.get("publishedAt"))
    #                         )
    #                         news_sources.append(source)
            
    #     except Exception as e:
    #         logger.warning(f"Fallback search failed: {str(e)}")
            
    #         # Last resort: return mock data for demo purposes
    #         news_sources = [
    #             NewsSource(
    #                 title=f"Latest developments in {topic}",
    #                 url=f"https://example.com/news/{topic.lower().replace(' ', '-')}",
    #                 source_name="Tech News Daily",
    #                 snippet=f"Recent updates and trends in {topic} that are shaping the industry...",
    #                 published_date=datetime.now() - timedelta(hours=2)
    #             )
    #         ]
            
    #         logger.info("Using fallback mock news data")
        
    #     return news_sources
    
    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse date string to datetime object."""
        if not date_str:
            return None
            
        try:
            # Handle various date formats
            for fmt in ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%SZ"]:
                try:
                    return datetime.strptime(date_str, fmt)
                except ValueError:
                    continue
                    
            # If no format matches, return None
            return None
            
        except Exception:
            return None
import asyncio
from typing import List, Dict, Any, Optional
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate

from app.core.config import settings
from app.core.exceptions import AIGenerationError, APIKeyError
from app.core.logging import get_logger
from app.models.response import NewsSource

logger = get_logger(__name__)


class AIAgent:
    """AI Agent for generating LinkedIn posts using Google Gemini."""
    
    def __init__(self):
        try:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                google_api_key=settings.google_api_key,
                temperature=settings.temperature
            )
            logger.info("AI Agent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize AI Agent: {str(e)}")
            raise APIKeyError(f"Failed to initialize Gemini API: {str(e)}")
    
    async def generate_linkedin_post(
        self,
        topic: str,
        news_sources: List[NewsSource],
        style: str = "professional",
        max_length: int = 2000,
        include_hashtags: bool = True
    ) -> Dict[str, Any]:
        """
        Generate a LinkedIn post based on news sources.
        
        Args:
            topic: The main topic
            news_sources: List of news sources
            include_hashtags: Whether to include hashtags
            
        Returns:
            Dictionary containing post content, hashtags
        """
        try:
            logger.info(f"Generating LinkedIn post for topic: {topic}")
            
            # Create prompt for post generation
            post_prompt = self._create_post_prompt(
                topic, news_sources, style, max_length, include_hashtags
            )
            
            messages = HumanMessage(content = post_prompt) 

            # Generate post content
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, lambda: self.llm.invoke([messages])
            )
            
            post_content = response.content.strip()
            
            # Extract hashtags and image suggestion
            hashtags = await self._extract_hashtags(post_content, topic)
            
            
            # Clean up the post content (remove hashtags section if present)
            clean_post = self._clean_post_content(post_content)
            
            result = {
                "post_content": clean_post,
                "hashtags": hashtags,
                "word_count": len(clean_post.split()),
                "character_count": len(clean_post)
            }
            
            logger.info("LinkedIn post generated successfully")
            return result
            
        except Exception as e:
            logger.error(f"Failed to generate LinkedIn post: {str(e)}")
            raise AIGenerationError(f"Failed to generate post: {str(e)}")
    
    def _create_post_prompt(
        self,
        topic: str,
        news_sources: List[NewsSource],
        style: str,
        max_length: int,
        include_hashtags: bool
    ) -> str:
        """Create prompt for LinkedIn post generation."""
        
        # Prepare news sources text
        news_text = ""
        for i, source in enumerate(news_sources[:3], 1):  # Use top 3 sources
            news_text += f"\n{i}. {source.title}\n"
            if source.snippet:
                news_text += f"   Summary: {source.snippet}\n"
            news_text += f"   Source: {source.source_name or 'Unknown'}\n"
        
        # Style-specific instructions
        style_instructions = {
            "professional": "Use a formal, business-appropriate tone. Focus on industry insights and professional implications.",
            "casual": "Use a conversational, approachable tone. Make it feel like a friendly discussion.",
            "thought-leadership": "Position the content as expert analysis. Share strategic insights and future implications."
        }
        
        prompt_text = f"""
        You are a professional LinkedIn content creator. Create an engaging LinkedIn post about "{topic}" based on the following recent news:

        {news_text}

        REQUIREMENTS:
        - Style: {style_instructions.get(style, style_instructions['professional'])}
        - Maximum length: {max_length} characters
        - Make it engaging and likely to get comments/shares
        - Include a compelling hook in the first line
        - Structure with proper paragraphs and line breaks
        - End with a thought-provoking question or call to action
        - {'Include 3-5 relevant hashtags at the end' if include_hashtags else 'Do not include hashtags'}
        
        CONTENT GUIDELINES:
        - Start with an attention-grabbing opening
        - Provide valuable insights, not just news summary
        - Use LinkedIn-appropriate language
        - Make it conversation-starting
        - Include specific examples or data points when possible
        - Maintain authenticity and avoid overly promotional tone
        
        Generate the LinkedIn post now:
        """
        
        return prompt_text
    
    async def _extract_hashtags(self, post_content: str, topic: str) -> List[str]:
        """Extract or generate relevant hashtags."""
        try:
            # First, try to extract hashtags from the generated content
            lines = post_content.split('\n')
            hashtags = []
            
            for line in lines:
                if line.strip().startswith('#'):
                    tags = [tag.strip() for tag in line.split() if tag.startswith('#')]
                    hashtags.extend(tags)
            
            # If no hashtags found, generate some
            if not hashtags:
                hashtag_prompt = SystemMessage(content=f"""
                Generate 5 relevant LinkedIn hashtags for a post about "{topic}". 
                Return only the hashtags, one per line, starting with #.
                Focus on professional, industry-relevant tags.
                """)
                
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None, lambda: self.llm.invoke([hashtag_prompt])
                )
                
                hashtag_lines = response.content.strip().split('\n')
                hashtags = [line.strip() for line in hashtag_lines if line.strip().startswith('#')]
            
            return hashtags[:5]  # Limit to 5 hashtags
            
        except Exception as e:
            logger.warning(f"Failed to extract hashtags: {str(e)}")
            # Return some generic hashtags based on topic
            return [f"#{topic.replace(' ', '')}", "#LinkedIn", "#Industry", "#Business"]
    
    
    
    def _clean_post_content(self, content: str) -> str:
        """Clean up the generated post content."""
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Remove hashtag-only lines (they'll be handled separately)
            if line.strip() and not line.strip().startswith('#'):
                cleaned_lines.append(line)
            elif line.strip().startswith('#'):
                # Stop processing when we hit hashtags
                break
        
        return '\n'.join(cleaned_lines).strip()
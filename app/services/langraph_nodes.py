import asyncio
import json
from typing import Dict, Any, List
from datetime import datetime
import re

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import PromptTemplate

from app.core.config import settings
from app.core.logging import get_logger
from app.core.exceptions import AIGenerationError
from app.models.langraph_state import (
    WorkflowState, NewsAnalysisResult, ContentOutline, QualityMetrics
)
from app.models.response import NewsSource
from app.services.news_agent import NewsSearchAgent
from app.services.image_agent import ImageAgent

logger = get_logger(__name__)


style_instructions = {
        "professional": "Use a formal, business-appropriate tone. Focus on industry insights and professional implications.",
        "casual": "Use a conversational, approachable tone. Make it feel like a friendly discussion.",
        "thought-leadership": "Position the content as expert analysis. Share strategic insights and future implications."
    }

class LangGraphNodes:
    """Collection of LangGraph nodes for LinkedIn post generation."""
    
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=settings.google_api_key,
            temperature=settings.temperature
        )
        self.news_service = NewsSearchAgent()
        self.image_agent = ImageAgent()
        self.style_instructions = style_instructions
    
    async def search_news_node(self, state: WorkflowState) -> WorkflowState:
        """Node to search for recent news articles."""
        logger.info(f"Searching news for topic: {state['topic']}")
        
        try:
            state["processing_stage"] = "searching_news"
            state["search_attempts"] = state.get("search_attempts", 0) + 1
            
            # Search for news with retry logic
            max_attempts = 2
            news_sources = []
            
            for attempt in range(max_attempts):
                try:
                    news_sources = await self.news_service.search_news(
                        topic=state["topic"],
                        limit=5
                    )
                    if news_sources:
                        break
                except Exception as e:
                    logger.warning(f"News search attempt {attempt + 1} failed: {e}")
                    if attempt == max_attempts - 1:
                        # Use fallback news
                        news_sources = self._create_fallback_news(state["topic"])
            
            state["news_sources"] = news_sources
            logger.info(f"Found {len(news_sources)} news sources")
            
        except Exception as e:
            error_msg = f"News search failed: {str(e)}"
            logger.error(error_msg)
            state["error_messages"] = state.get("error_messages", []) + [error_msg]
            state["news_sources"] = self._create_fallback_news(state["topic"])
        
        return state
    
    async def analyze_news_node(self, state: WorkflowState) -> WorkflowState:
        """Node to analyze news content and extract insights."""
        logger.info("Analyzing news content for insights")
        
        try:
            state["processing_stage"] = "analyzing_news"
            
            news_sources = state.get("news_sources", [])
            if not news_sources:
                raise AIGenerationError("No news sources available for analysis")
            
            # Create analysis prompt
            analysis_prompt = self._create_news_analysis_prompt(
                state["topic"], news_sources
            )
            
            # Get analysis from AI
            response = await self.llm.ainvoke([
                SystemMessage(content="You are an expert news analyst."),
                HumanMessage(content=analysis_prompt.content)
            ])
            
            # Parse analysis result
            analysis_result = self._parse_news_analysis(response.content)
            state["news_analysis"] = analysis_result.dict()
            
            logger.info("News analysis completed successfully")
            
        except Exception as e:
            error_msg = f"News analysis failed: {str(e)}"
            logger.error(error_msg)
            state["error_messages"] = state.get("error_messages", []) + [error_msg]
            state["news_analysis"] = self._create_fallback_analysis(state["topic"])
        
        return state
    
    async def create_content_outline_node(self, state: WorkflowState) -> WorkflowState:
        """Node to create content outline for LinkedIn post."""
        logger.info("Creating content outline")
        
        try:
            state["processing_stage"] = "creating_outline"
            
            # Create outline prompt
            outline_prompt = self._create_outline_prompt(
                state["topic"],
                state.get("news_analysis", {}),
                state["style"]
            )
            
            # Generate outline
            response = await self.llm.ainvoke([
                SystemMessage(content="You are an expert news analyst."),
                HumanMessage(content=outline_prompt.content)
            ])
            
            # Parse outline
            outline = self._parse_content_outline(response.content, state["style"])
            state["content_outline"] = outline.dict()
            
            logger.info("Content outline created successfully")
            
        except Exception as e:
            error_msg = f"Outline creation failed: {str(e)}"
            logger.error(error_msg)
            state["error_messages"] = state.get("error_messages", []) + [error_msg]
            state["content_outline"] = self._create_fallback_outline(state["topic"])
        
        return state
    
    async def generate_draft_post_node(self, state: WorkflowState) -> WorkflowState:
        """Node to generate initial draft of LinkedIn post."""
        logger.info("Generating draft LinkedIn post")
        
        try:
            state["processing_stage"] = "generating_draft"
            state["generation_attempts"] = state.get("generation_attempts", 0) + 1
            
            # Create generation prompt
            generation_prompt = self._create_post_generation_prompt(
                state["topic"],
                state.get("content_outline", {}),
                state.get("news_analysis", {}),
                state["style"],
                state["max_length"]
            )
            
            # Generate draft post
            response = await self.llm.ainvoke([
                SystemMessage(content="You are a professional LinkedIn content writer."),
                HumanMessage(content=generation_prompt.content)
            ])
            
            draft_post = self._clean_generated_content(response.content)
            state["draft_post"] = draft_post
            
            # Update counts
            state["word_count"] = len(draft_post.split())
            state["character_count"] = len(draft_post)
            
            logger.info(f"Draft post generated: {state['word_count']} words")
            
        except Exception as e:
            error_msg = f"Draft generation failed: {str(e)}"
            logger.error(error_msg)
            state["error_messages"] = state.get("error_messages", []) + [error_msg]
            state["draft_post"] = f"Professional insights on {state['topic']} based on recent developments..."
        
        return state
    
    async def quality_check_node(self, state: WorkflowState) -> WorkflowState:
        """Node to assess content quality and suggest improvements."""
        logger.info("Performing quality check on draft post")
        
        try:
            state["processing_stage"] = "quality_checking"
            
            draft_post = state.get("draft_post", "")
            if not draft_post:
                raise AIGenerationError("No draft post available for quality check")
            
            # Create quality assessment prompt
            quality_prompt = self._create_quality_check_prompt(
                draft_post, state["topic"], state["style"]
            )
            
            # Get quality assessment
            response = await self.llm.ainvoke([
                SystemMessage(content="You are a professional LinkedIn content writer."),
                HumanMessage(content=quality_prompt.content)
            ])
            
            # Parse quality metrics
            quality_metrics = self._parse_quality_metrics(response.content)
            state["quality_score"] = quality_metrics.overall_score
            
            logger.info(f"Quality check completed: {quality_metrics.overall_score:.2f}/10")
            
        except Exception as e:
            error_msg = f"Quality check failed: {str(e)}"
            logger.error(error_msg)
            state["error_messages"] = state.get("error_messages", []) + [error_msg]
            state["quality_score"] = 7.0  # Default acceptable score
        
        return state
    
    async def refine_post_node(self, state: WorkflowState) -> WorkflowState:
        """Node to refine post based on quality assessment."""
        logger.info("Refining LinkedIn post")
        
        try:
            state["processing_stage"] = "refining_content"
            
            quality_score = state.get("quality_score", 7.0)
            draft_post = state.get("draft_post", "")
            
            # Only refine if quality score is below threshold
            if quality_score >= 8.0:
                logger.info("Draft quality is good, skipping refinement")
                state["refined_post"] = draft_post
            else:
                # Create refinement prompt
                refinement_prompt = self._create_refinement_prompt(
                    draft_post, state["topic"], state["style"], quality_score
                )
                
                # Generate refined post
                response = await self.llm.ainvoke([
                SystemMessage(content="You are a professional LinkedIn content writer."),
                HumanMessage(content=refinement_prompt.content)
            ])
                
                refined_post = self._clean_generated_content(response.content)
                state["refined_post"] = refined_post
                
                # Update counts
                state["word_count"] = len(refined_post.split())
                state["character_count"] = len(refined_post)
                
                logger.info("Post refinement completed")
        
        except Exception as e:
            error_msg = f"Post refinement failed: {str(e)}"
            logger.error(error_msg)
            state["error_messages"] = state.get("error_messages", []) + [error_msg]
            state["refined_post"] = state.get("draft_post", "")
        
        return state
    
    async def generate_hashtags_node(self, state: WorkflowState) -> WorkflowState:
        """Node to generate relevant hashtags."""
        logger.info("Generating hashtags")
        
        try:
            state["processing_stage"] = "generating_hashtags"
            
            if not state["include_hashtags"]:
                state["hashtags"] = []
                return state
            
            # Create hashtag generation prompt
            hashtag_prompt = self._create_hashtag_prompt(
                state["topic"],
                state.get("refined_post", state.get("draft_post", "")),
                state.get("news_analysis", {})
            )
            logger.info(f"Generated prompt: {hashtag_prompt.content}")
            
            # Generate hashtags
            response = await self.llm.ainvoke([
                SystemMessage(content="You are a professional LinkedIn content writer."),
                HumanMessage(content=hashtag_prompt.content)
            ])
            logger.info(f"Generated hashtags: {response.content}")
            
            hashtags = self._extract_hashtags(response.content)
            state["hashtags"] = hashtags[:8]  # Limit to 8 hashtags
            
            logger.info(f"Generated {len(state['hashtags'])} hashtags")
            
        except Exception as e:
            error_msg = f"Hashtag generation failed: {str(e)}"
            logger.error(error_msg)
            state["error_messages"] = state.get("error_messages", []) + [error_msg]
            # Fallback hashtags
            state["hashtags"] = [
                f"#{state['topic'].replace(' ', '')}",
                "#LinkedIn",
                "#Industry",
                "#Business"
            ][:4]
        
        return state
    
    async def generate_image_node(self, state: WorkflowState) -> WorkflowState:
        """Node to generate image suggestion using existing ImageAgent."""
        logger.info("[LangGraph] Generating image suggestion")
        
        try:
            state["processing_stage"] = "generating_image"
            
            # Use existing ImageAgent
            image_suggestion = await self.image_agent.get_image_suggestion(
                topic=state["topic"]
            )

            state["image_suggestion"] = image_suggestion
            logger.info("[LangGraph] Image suggestion generated")
            
        except Exception as e:
            error_msg = f"Image suggestion failed: {str(e)}"
            logger.error(error_msg)
            state["error_messages"] = state.get("error_messages", []) + [error_msg]
            state["image_suggestion"] = f"Professional image related to {state['topic']}"
        
        return state
    
    # Helper methods for prompt creation and parsing
    
    def _create_news_analysis_prompt(self, topic: str, news_sources: List[NewsSource]) -> SystemMessage:
        """Create prompt for news analysis."""
        news_text = "\n".join([
            f"Title: {source.title}\nSummary: {source.snippet or 'No summary'}\nSource: {source.source_name}"
            for source in news_sources[:3]
        ])
        
        prompt = f"""
        Analyze the following news about "{topic}" and provide structured insights:

        NEWS CONTENT:
        {news_text}

        Please provide analysis in this JSON format:
        {{
            "key_themes": ["theme1", "theme2", "theme3"],
            "sentiment": "positive/negative/neutral",
            "industry_impact": "description of industry impact",
            "trend_direction": "rising/declining/stable",
            "credibility_score": 0.8,
            "summary": "2-sentence summary of key insights"
        }}
        
        Focus on business implications and trends that would be relevant for LinkedIn professionals.
        """
        return SystemMessage(content=prompt)
    
    # Style-specific instructions
    
    def _create_outline_prompt(self, topic: str, analysis: Dict, style: str) -> SystemMessage:
        """Create prompt for content outline."""
        prompt = f"""
        Create a LinkedIn post outline for "{topic}" based on this analysis:
        {json.dumps(analysis, indent=2)}

        Style: {self.style_instructions.get(style, self.style_instructions['professional'])}
        
        Provide outline in this JSON format:
        {{
            "hook": "attention-grabbing opening line",
            "main_points": ["point1", "point2", "point3"],
            "call_to_action": "engaging question or CTA",
            "tone_keywords": ["professional", "insightful", "engaging"],
            "target_audience": "description of target audience",
            "estimated_engagement_score": 8.5
        }}
        
        Make it compelling and LinkedIn-appropriate.
        """
        return SystemMessage(content=prompt)
    
    def _create_post_generation_prompt(
        self, topic: str, outline: Dict, analysis: Dict, style: str, max_length: int
    ) -> SystemMessage:
        """Create prompt for LinkedIn post generation."""
        prompt = f"""
        Write a compelling LinkedIn post about "{topic}" using this outline and analysis:

        OUTLINE: {json.dumps(outline, indent=2)}
        ANALYSIS: {json.dumps(analysis, indent=2)}

        REQUIREMENTS:
        - Style: {self.style_instructions.get(style, self.style_instructions['professional'])}
        - Maximum {max_length} characters
        - Start with an engaging hook
        - Include 2-3 key insights
        - End with a question or call to action
        - Use proper LinkedIn formatting with line breaks
        - Be conversational yet professional
        - Include specific examples or data points
        
        Generate the complete LinkedIn post now:
        """
        return SystemMessage(content=prompt)
    
    def _create_quality_check_prompt(self, post: str, topic: str, style: str) -> SystemMessage:
        """Create prompt for quality assessment."""
        prompt = f"""
        Assess the quality of this LinkedIn post about "{topic}" (style: {self.style_instructions.get(style, self.style_instructions['professional'])}):

        POST:
        {post}

        Rate each aspect from 1-10 and provide in JSON format:
        {{
            "readability_score": 8.5,
            "engagement_potential": 9.0,
            "professional_tone": 8.0,
            "linkedin_best_practices": 7.5,
            "overall_score": 8.25,
            "improvement_suggestions": ["suggestion1", "suggestion2"]
        }}
        
        Consider: clarity, engagement, professionalism, LinkedIn best practices, and relevance.
        """
        return SystemMessage(content=prompt)
    
    def _create_refinement_prompt(
        self, draft: str, topic: str, style: str, quality_score: float
    ) -> SystemMessage:
        """Create prompt for post refinement."""
        prompt = f"""
        Improve this LinkedIn post about "{topic}" (current quality: {quality_score}/10):

        CURRENT POST:
        {draft}

        IMPROVEMENTS NEEDED:
        - Enhance engagement potential
        - Improve clarity and flow
        - Add more compelling insights
        - Optimize for LinkedIn best practices
        - Maintain {self.style_instructions.get(style, self.style_instructions['professional'])} style

        Provide the improved version:
        """
        return SystemMessage(content=prompt)
    
    def _create_hashtag_prompt(self, topic: str, post: str, analysis: Dict) -> SystemMessage:
        """Create prompt for hashtag generation."""
        prompt = f"""
        Generate "8" relevant LinkedIn hashtags for this post about "{topic}":

        POST: {post}
        ANALYSIS: {json.dumps(analysis, indent=2)}

        Requirements:
        - Professional and industry-relevant
        - Mix of broad and specific tags
        - High engagement potential
        - LinkedIn best practices

        Return hashtags one per line, starting with #:
        """
        return SystemMessage(content=prompt)
    
    def _create_image_suggestion_prompt(
        self, topic: str, analysis: Dict, outline: Dict
    ) -> SystemMessage:
        """Create prompt for image suggestions."""
        prompt = f"""
        Suggest a professional image or visual for a LinkedIn post about "{topic}":

        CONTENT CONTEXT:
        Analysis: {json.dumps(analysis, indent=2)}
        Outline: {json.dumps(outline, indent=2)}

        Provide a specific, actionable image suggestion that would:
        - Complement the post content
        - Be professional and LinkedIn-appropriate
        - Increase engagement
        - Be easy to source or create

        Describe the ideal image in 1-2 sentences:
        """
        return SystemMessage(content=prompt)
    
    # Parsing and utility methods
    
    def _parse_news_analysis(self, content: str) -> NewsAnalysisResult:
        """Parse news analysis response."""
        try:
            # Try to extract JSON from response
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return NewsAnalysisResult(**data)
        except Exception as e:
            logger.warning(f"Failed to parse news analysis: {e}")
        
        # Fallback parsing
        return NewsAnalysisResult(
            key_themes=["innovation", "technology", "industry"],
            sentiment="positive",
            industry_impact="Significant positive impact on industry development",
            trend_direction="rising",
            credibility_score=0.8,
            summary="Recent developments show positive trends in the industry."
        )
    
    def _parse_content_outline(self, content: str, style: str) -> ContentOutline:
        """Parse content outline response."""
        try:
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return ContentOutline(**data)
        except Exception as e:
            logger.warning(f"Failed to parse content outline: {e}")
        
        # Fallback outline
        return ContentOutline(
            hook="🚀 Exciting developments are reshaping our industry",
            main_points=[
                "Key insight from recent research",
                "Impact on professional practices",
                "Future implications and opportunities"
            ],
            call_to_action="What's your experience with these changes?",
            tone_keywords=["professional", "insightful", "engaging"],
            target_audience="Industry professionals and thought leaders",
            estimated_engagement_score=8.0
        )
    
    def _parse_quality_metrics(self, content: str) -> QualityMetrics:
        """Parse quality assessment response."""
        try:
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return QualityMetrics(**data)
        except Exception as e:
            logger.warning(f"Failed to parse quality metrics: {e}")
        
        # Fallback metrics
        return QualityMetrics(
            readability_score=8.0,
            engagement_potential=7.5,
            professional_tone=8.5,
            linkedin_best_practices=7.0,
            overall_score=7.75,
            improvement_suggestions=["Add more specific examples", "Enhance call to action"]
        )
    
    def _extract_hashtags(self, content: str) -> List[str]:
        """Extract hashtags from response."""
        hashtags = re.findall(r'#\w+', content)
        return list(set(hashtags)) if hashtags else []  # Remove duplicates
    
    def _clean_generated_content(self, content: str) -> str:
        """Clean up generated content."""
        # Remove extra whitespace
        content = re.sub(r'\n\s*\n', '\n\n', content)
        content = content.strip()
        
        # Remove any JSON or prompt artifacts
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Skip lines that look like JSON or prompts
            if line.strip().startswith(('{', '}', '"', 'POST:', 'ANALYSIS:')) or line.strip().endswith(':'):
                continue
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines).strip()
    
    def _create_fallback_news(self, topic: str) -> List[NewsSource]:
        """Create fallback news sources."""
        return [
            NewsSource(
                title=f"Latest developments in {topic}",
                url=f"https://example.com/news/{topic.lower().replace(' ', '-')}",
                source_name="Industry Report",
                snippet=f"Recent insights and trends in {topic} are reshaping the landscape...",
                published_date=datetime.now()
            )
        ]
    
    def _create_fallback_analysis(self, topic: str) -> Dict[str, Any]:
        """Create fallback analysis."""
        return {
            "key_themes": ["innovation", "growth", "industry"],
            "sentiment": "positive",
            "industry_impact": f"Positive developments in {topic}",
            "trend_direction": "rising",
            "credibility_score": 0.7,
            "summary": f"Recent developments in {topic} show promising trends."
        }
    
    def _create_fallback_outline(self, topic: str) -> Dict[str, Any]:
        """Create fallback outline."""
        return {
            "hook": f"🚀 {topic} is transforming how we work",
            "main_points": [
                "Key industry developments",
                "Professional implications",
                "Future opportunities"
            ],
            "call_to_action": "What's your take on these changes?",
            "tone_keywords": ["professional", "engaging"],
            "target_audience": "Industry professionals",
            "estimated_engagement_score": 7.5
        }
from typing import Dict, Any, List
import asyncio
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import InMemorySaver

from app.core.logging import get_logger
from app.models.langraph_state import WorkflowState
from app.services.langraph_nodes import LangGraphNodes

logger = get_logger(__name__)


class LinkedInPostWorkflow:
    """LangGraph workflow for generating LinkedIn posts."""
    
    def __init__(self):
        self.nodes = LangGraphNodes()
        self.memory = InMemorySaver()
        self.workflow = self._build_workflow()
        
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow."""
        
        workflow = StateGraph(WorkflowState)
        
        # Add nodes
        workflow.add_node("search_news", self.nodes.search_news_node)
        workflow.add_node("analyze_news", self.nodes.analyze_news_node)
        workflow.add_node("create_outline", self.nodes.create_content_outline_node)
        workflow.add_node("generate_draft", self.nodes.generate_draft_post_node)
        workflow.add_node("quality_check", self.nodes.quality_check_node)
        workflow.add_node("refine_post", self.nodes.refine_post_node)
        workflow.add_node("generate_hashtags", self.nodes.generate_hashtags_node)
        workflow.add_node("generate_image_suggestion", self.nodes.generate_image_node)
        
        # Define workflow edges
        workflow.set_entry_point("search_news")
        
        # Linear flow with conditional branching
        workflow.add_edge("search_news", "analyze_news")
        workflow.add_edge("analyze_news", "create_outline")
        workflow.add_edge("create_outline", "generate_draft")
        workflow.add_edge("generate_draft", "quality_check")
        
        # Conditional refinement
        workflow.add_conditional_edges(
            "quality_check",
            self._should_refine_post,
            {
                "refine": "refine_post",
                "continue": "generate_hashtags"
            }
        )
        
        workflow.add_edge("refine_post", "generate_hashtags")
        workflow.add_edge("generate_hashtags", "generate_image_suggestion")
        workflow.add_edge("generate_image_suggestion", END)
        
        return workflow.compile(checkpointer=self.memory)
    
    def _should_refine_post(self, state: WorkflowState) -> str:
        """Determine if post should be refined based on quality score."""
        quality_score = state.get("quality_score", 7.0)
        generation_attempts = state.get("generation_attempts", 0)
        
        # Refine if quality is low and we haven't tried too many times
        if quality_score < 8.0 and generation_attempts < 2:
            return "refine"
        else:
            return "continue"
    
    async def generate_post(
        self,
        topic: str,
        style: str = "professional",
        max_length: int = 2000,
        include_hashtags: bool = True
    ) -> Dict[str, Any]:
        """
        Generate LinkedIn post using LangGraph workflow.
        
        Args:
            topic: The topic to generate post about
            style: Writing style (professional, casual, thought-leadership)
            max_length: Maximum post length in characters
            include_hashtags: Whether to include hashtags
            
        Returns:
            Complete post generation result
        """
        logger.info(f"Starting LangGraph workflow for topic: {topic}")
        
        # Initialize state
        initial_state: WorkflowState = {
            "topic": topic,
            "style": style,
            "max_length": max_length,
            "include_hashtags": include_hashtags,
            "news_sources": [],
            "news_analysis": None,
            "content_outline": None,
            "draft_post": None,
            "refined_post": None,
            "hashtags": [],
            "image_suggestion": None,
            "processing_stage": "initializing", 
            "error_messages": [],
            "quality_score": None,
            "word_count": None,
            "character_count": None,
            "search_attempts": 0,
            "generation_attempts": 0
        }
        
        try:
            # Run the workflow
            config = {"configurable": {"thread_id": f"linkedin_post_{topic}_{int(asyncio.get_event_loop().time())}"}}
            
            final_state = await self.workflow.ainvoke(initial_state, config)
            
            # Extract final post content
            final_post = final_state.get("refined_post") or final_state.get("draft_post", "")
            
            result = {
                "post_content": final_post,
                "hashtags": final_state.get("hashtags", []),
                "image_suggestion": final_state.get("image_suggestion"),
                "news_sources": final_state.get("news_sources", []),
                "word_count": final_state.get("word_count", 0),
                "character_count": final_state.get("character_count", 0),
                "quality_score": final_state.get("quality_score", 0.0),
                "processing_metadata": {
                    "search_attempts": final_state.get("search_attempts", 0),
                    "generation_attempts": final_state.get("generation_attempts", 0),
                    "error_messages": final_state.get("error_messages", []),
                    "news_analysis": final_state.get("news_analysis"),
                    "content_outline": final_state.get("content_outline")
                }
            }
            
            logger.info(f"LangGraph workflow completed successfully. Quality score: {result['quality_score']}")
            return result
            
        except Exception as e:
            logger.error(f"LangGraph workflow failed: {str(e)}", exc_info=True)
            
            # Return fallback result
            fallback_post = f"""🚀 Exciting developments in {topic} are reshaping our industry landscape.

                Recent trends show significant growth and innovation in this space. Key insights from industry analysis:

                • Enhanced capabilities and performance improvements
                • Growing adoption across major organizations  
                • Positive impact on productivity and efficiency

                These changes present new opportunities for professionals to:
                ✓ Expand skill sets and expertise
                ✓ Drive innovation in their organizations
                ✓ Stay ahead of industry trends

                What trends are you seeing in {topic}? Share your thoughts below! 👇

                #{topic.replace(' ', '')} #Innovation #Industry #ProfessionalDevelopment"""

            return {
                "post_content": fallback_post,
                "hashtags": [f"#{topic.replace(' ', '')}", "#Innovation", "#Industry", "#ProfessionalDevelopment"],
                "image_suggestion": f"Professional infographic showing trends and statistics related to {topic}",
                "news_sources": [],
                "word_count": len(fallback_post.split()),
                "character_count": len(fallback_post),
                "quality_score": 7.0,
                "processing_metadata": {
                    "search_attempts": 1,
                    "generation_attempts": 1,
                    "error_messages": [f"Workflow failed: {str(e)}"],
                    "news_analysis": None,
                    "content_outline": None
                }
            }
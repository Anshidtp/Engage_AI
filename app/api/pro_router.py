from fastapi import APIRouter, HTTPException, Depends, Request, BackgroundTasks
from typing import Dict, Any
from datetime import datetime

from app.models.requests import GeneratePostRequest
from app.models.response import GeneratePostResponse, ErrorResponse
from app.services.pro_post_generator import LangGraphPostGeneratorService
\
from app.core.exceptions import AppException, APIKeyError, NewsSearchError, AIGenerationError
from app.core.logging import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/posts", tags=["pro"])

# Initialize enhanced service
post_service = LangGraphPostGeneratorService()


@router.post(
    "/generate-post-pro",
    response_model=GeneratePostResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        429: {"model": ErrorResponse, "description": "Rate Limit Exceeded"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
    summary="Generate Enhanced LinkedIn Post with LangGraph",
    description="""
    Generate a professional LinkedIn post using advanced LangGraph workflow.
    
    This enhanced endpoint provides:
    - Multi-step content analysis and generation
    - Quality assessment and automatic refinement
    - Structured workflow with error recovery
    - Detailed processing metadata
    - Higher quality content generation
    
    The LangGraph workflow includes:
    1. News search and analysis
    2. Content outline creation
    3. Draft post generation
    4. Quality assessment
    5. Content refinement (if needed)
    6. Hashtag and image suggestion generation
    """
)
async def generate_enhanced_post(
    request: GeneratePostRequest,
    background_tasks: BackgroundTasks
) -> GeneratePostResponse:
    """
    Generate an enhanced LinkedIn post using LangGraph workflow.
    
    - **topic**: The main topic to search news for (required)
    - **style**: Post style - professional, casual, or thought-leadership
    - **include_hashtags**: Whether to include relevant hashtags
    - **max_length**: Maximum post length in characters
    
    Returns a complete LinkedIn post with enhanced metadata including:
    - Quality score assessment
    - Processing workflow metadata
    - Multi-step content refinement
    - Comprehensive news analysis
    """
    try:
        # Log request metadata
        # metadata = get_request_metadata(http_request)
        # logger.info(f"Enhanced post generation request: {request.topic} from {metadata['client_ip']}")
        
        # Generate post using LangGraph workflow
        result = await post_service.generate_post(request)
        
        # Log success metrics in background
        background_tasks.add_task(
            log_enhanced_success_metrics,
            request.topic,
            len(result.linkedin_post),
            len(result.news_sources),
            result.quality_score or 0.0,

        )
        
        return result
        
    except APIKeyError as e:
        logger.error(f"API key error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error="Service configuration error",
                code=e.code,
                details=e.details
            ).dict()
        )
        
    except NewsSearchError as e:
        logger.error(f"News search error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=ErrorResponse(
                error="Failed to search for recent news",
                code=e.code,
                details=e.details
            ).dict()
        )
        
    except AIGenerationError as e:
        logger.error(f"AI generation error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error="Failed to generate post content",
                code=e.code,
                details=e.details
            ).dict()
        )
        
    except AppException as e:
        logger.error(f"Application error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=ErrorResponse(
                error=e.message,
                code=e.code,
                details=e.details
            ).dict()
        )
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error="An unexpected error occurred",
                code="INTERNAL_ERROR",
                details={"message": str(e)}
            ).dict()
        )


@router.get(
    "/workflow-status/{thread_id}",
    summary="Get Workflow Status",
    description="Get the status of a running LangGraph workflow (if implemented with persistence)."
)
async def get_workflow_status(thread_id: str) -> Dict[str, Any]:
    """Get workflow execution status (placeholder for future enhancement)."""
    return {
        "thread_id": thread_id,
        "status": "This endpoint can be enhanced to provide real-time workflow status",
        "message": "Consider implementing workflow persistence for production use"
    }


async def log_enhanced_success_metrics(
    topic: str, 
    post_length: int, 
    news_count: int, 
    quality_score: float
):
    """Log enhanced success metrics in background."""
    logger.info(
        f"Enhanced success metrics - Topic: {topic}, "
        f"Post length: {post_length}, News sources: {news_count}, "
        f"Quality score: {quality_score:.1f}/10, Time: {datetime.utcnow().isoformat()}"
    )
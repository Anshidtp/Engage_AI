from fastapi import APIRouter, HTTPException,Request,BackgroundTasks
from typing import Dict, Any
from datetime import datetime

from app.models.response import ErrorResponse
from app.models.schema import PostRequest, PostResponse
from app.services.post_generator import PostGeneratorService
from app.core.exceptions import AppException,APIKeyError,NewsSearchError
from app.core.logging import get_logger


logger = get_logger(__name__)

router = APIRouter(prefix="/posts", tags=["posts"])

#initialize the PostGeneratorService
post_service = PostGeneratorService()

@router.post(
    "/generate-post",
    response_model=PostResponse,)
async def generate_post(
    request: PostRequest,
    background_tasks: BackgroundTasks,
) -> PostResponse:
    '''Endpoint to generate a LinkedIn post based on the provided request parameters.'''

    try:
        # # Log request metadata
        # metadata = get_request_metadata(http_request)
        logger.info(f"Post generation request: {request.topic} ")
        
        # Generate post
        result = await post_service.generate_post(request)
        
        # Log success in background
        background_tasks.add_task(
            log_success_metrics,
            request.topic,
            len(result.linkedin_post),
            len(result.news_sources)
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
        
        
    except AppException as e:
        logger.error(f"Application error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=ErrorResponse(
                error=e.message,
                code=e.code,
                details=e.details,
                timestamp=datetime.utcnow().isoformat()  # Convert to ISO format string
            ).dict()
        )
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=ErrorResponse(
                error="An unexpected error occurred",
                code="INTERNAL_ERROR",
                details={"message": str(e)},
                timestamp=datetime.utcnow().isoformat()  # Convert to ISO format string
            ).dict()
        )


@router.get(
    "/health",
    summary="Health Check",
    description="Check if the service is healthy and all dependencies are working."
)
async def health_check() -> Dict[str, Any]:
    """Health check endpoint."""
    try:
        # Basic health check
        # await validate_api_keys()
        
        return {
            "status": "healthy",
            "service": "LinkedIn Post Generator",
            "version": "1.0.0",
            "timestamp": "2023-12-01T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": "2023-12-01T00:00:00Z"
            }
        )


async def log_success_metrics(topic: str, post_length: int, news_count: int):
    """Log success metrics in background."""
    logger.info(f"Success metrics - Topic: {topic}, Post length: {post_length}, News sources: {news_count}")
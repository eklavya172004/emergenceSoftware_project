"""Chat API routes."""
from fastapi import APIRouter, HTTPException
from typing import List
import logging
from ..models.chat import ChatRequest, ChatResponse, Message, ResumeRequest
from ..services.openrouter_service import openrouter_service
from ..config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/message", response_model=ChatResponse)
async def send_message(request: ChatRequest) -> ChatResponse:
    """
    Send a message to the AI assistant.
    
    Args:
        request: ChatRequest containing the user message and conversation history
        
    Returns:
        ChatResponse with the assistant's reply
        
    Raises:
        HTTPException: If API key is not configured or API call fails
    """
    try:
        # Validate input
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Build messages list for OpenRouter
        messages: List[dict] = []
        
        # Add conversation history
        if request.conversation_history:
            for msg in request.conversation_history:
                messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        # Add current message
        messages.append({
            "role": "user",
            "content": request.message
        })
        
        # Get system prompt with resume context
        system_prompt = openrouter_service.build_system_prompt(settings.resume_context)
        
        # Prepare messages with system prompt
        full_messages = [
            {"role": "system", "content": system_prompt},
            *messages
        ]
        
        # Get response from OpenRouter
        response_text = await openrouter_service.chat_completion(
            messages=full_messages,
            temperature=0.7,
            max_tokens=512
        )
        
        if response_text is None:
            raise HTTPException(
                status_code=500,
                detail="Failed to get response from AI service"
            )
        
        return ChatResponse(message=response_text)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in send_message: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/start-conversation")
async def start_conversation():
    """
    Start a new conversation.
    
    Returns:
        Conversation metadata
    """
    try:
        return {
            "status": "success",
            "message": "Conversation started",
            "conversation_id": None  # Can be extended with database later
        }
    except Exception as e:
        logger.error(f"Error in start_conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resume")
async def get_resume():
    """
    Get the current resume context.
    
    Returns:
        Current resume content
    """
    return {
        "status": "success",
        "resume_content": settings.resume_context
    }


@router.post("/update-resume")
async def update_resume(request: ResumeRequest):
    """
    Update the resume context used for AI responses.
    
    Args:
        request: ResumeRequest containing the resume content
        
    Returns:
        Success status
    """
    try:
        if not request.resume_content.strip():
            raise HTTPException(status_code=400, detail="Resume content cannot be empty")
        
        # Update the settings
        settings.resume_context = request.resume_content
        
        logger.info("Resume context updated successfully")
        
        return {
            "status": "success",
            "message": "Resume context updated"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_resume: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def chat_health():
    """Health check for chat service."""
    return {
        "status": "healthy",
        "service": "chat_api",
        "openrouter_configured": bool(settings.openrouter_api_key)
    }


@router.post("/test-openrouter")
async def test_openrouter():
    """
    Test OpenRouter API connection and API key validity.
    
    Returns:
        Status of OpenRouter connection
    """
    try:
        if not settings.openrouter_api_key:
            return {
                "status": "error",
                "message": "OpenRouter API key not configured"
            }
        
        # Make a simple test request
        response_text = await openrouter_service.chat_completion(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Respond with exactly: Connected"
                },
                {
                    "role": "user",
                    "content": "Are you working?"
                }
            ],
            temperature=0.1,
            max_tokens=50
        )
        
        if response_text.startswith("Error:"):
            return {
                "status": "error",
                "message": response_text,
                "model": settings.openrouter_model
            }
        
        return {
            "status": "success",
            "message": "OpenRouter API is working",
            "model": settings.openrouter_model,
            "response": response_text[:100]  # First 100 chars
        }
    except Exception as e:
        logger.error(f"Error testing OpenRouter: {str(e)}")
        return {
            "status": "error",
            "message": str(e),
            "model": settings.openrouter_model
        }

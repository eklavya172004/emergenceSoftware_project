"""Database and conversation management API routes."""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import logging
from typing import List
from ..database import get_db
from ..models.chat import (
    ChatRequest, ChatResponse, ConversationStartRequest, 
    ConversationResponse, ConversationHistoryResponse,
    ConversationListResponse
)
from ..services.database_service import ConversationService, ResumeService
from ..services.openrouter_service import openrouter_service
from ..config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.options("/start")
@router.options("")
async def options_handler():
    """Handle CORS preflight requests."""
    return {"status": "ok"}


@router.post("/start", response_model=ConversationResponse)
async def start_conversation(
    request: ConversationStartRequest,
    db: Session = Depends(get_db)
) -> ConversationResponse:
    """
    Start a new conversation.
    
    Args:
        request: ConversationStartRequest with user info
        db: Database session
        
    Returns:
        ConversationResponse with new conversation details
    """
    try:
        conversation = ConversationService.create_conversation(
            db=db,
            user_name=request.user_name or "User",
            user_email=request.user_email
        )
        
        logger.info(f"New conversation started: {conversation.id}")
        
        return ConversationResponse(
            conversation_id=conversation.id,
            user_name=conversation.user_name,
            created_at=conversation.created_at
        )
    except Exception as e:
        logger.error(f"Error starting conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/message-with-history", response_model=ChatResponse)
async def send_message_with_history(
    request: ChatRequest,
    db: Session = Depends(get_db)
) -> ChatResponse:
    """
    Send a message with conversation history saved to database.
    
    Args:
        request: ChatRequest with message and conversation_id
        db: Database session
        
    Returns:
        ChatResponse with assistant's reply
    """
    try:
        # Validate input
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        conversation_id = request.conversation_id
        
        # If no conversation_id, create new one
        if not conversation_id:
            conversation = ConversationService.create_conversation(
                db=db,
                user_name="User"
            )
            conversation_id = conversation.id
        
        # Save user message
        ConversationService.add_message(
            db=db,
            conversation_id=conversation_id,
            role="user",
            content=request.message
        )
        
        # Build messages list for OpenRouter
        messages = []
        
        # Get conversation history from database
        db_messages = ConversationService.get_conversation_history(db, conversation_id)
        for msg in db_messages:
            messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Get system prompt
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
        
        if response_text is None or response_text.startswith("Error:"):
            error_msg = response_text or "Failed to get response from AI service"
            logger.error(f"AI service error: {error_msg}")
            raise HTTPException(
                status_code=500,
                detail=error_msg
            )
        
        # Save assistant message
        ConversationService.add_message(
            db=db,
            conversation_id=conversation_id,
            role="assistant",
            content=response_text
        )
        
        logger.info(f"Message processed in conversation: {conversation_id}")
        
        return ChatResponse(
            message=response_text,
            conversation_id=conversation_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in send_message_with_history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_name}", response_model=ConversationListResponse)
async def get_user_conversations(
    user_name: str,
    limit: int = 10,
    db: Session = Depends(get_db)
) -> ConversationListResponse:
    """
    Get all conversations for a user.
    
    Args:
        user_name: Name of the user
        limit: Maximum conversations to return
        db: Database session
        
    Returns:
        List of user's conversations
    """
    try:
        conversations = ConversationService.get_user_conversations(
            db=db,
            user_name=user_name,
            limit=limit
        )
        
        return ConversationListResponse(
            total=len(conversations),
            conversations=[
                ConversationResponse(
                    conversation_id=conv.id,
                    user_name=conv.user_name,
                    created_at=conv.created_at
                )
                for conv in conversations
            ]
        )
    except Exception as e:
        logger.error(f"Error getting user conversations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversation/{conversation_id}", response_model=ConversationHistoryResponse)
async def get_conversation_history(
    conversation_id: str,
    db: Session = Depends(get_db)
) -> ConversationHistoryResponse:
    """
    Get full history of a conversation.
    
    Args:
        conversation_id: ID of the conversation
        db: Database session
        
    Returns:
        Conversation history with all messages
    """
    try:
        conversation = ConversationService.get_conversation(db, conversation_id)
        
        if not conversation:
            raise HTTPException(
                status_code=404,
                detail=f"Conversation {conversation_id} not found"
            )
        
        messages = ConversationService.get_conversation_history(db, conversation_id)
        
        return ConversationHistoryResponse(
            conversation_id=conversation.id,
            user_name=conversation.user_name,
            messages=[
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.created_at
                }
                for msg in messages
            ],
            created_at=conversation.created_at,
            updated_at=conversation.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conversation history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/conversation/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a conversation (soft delete).
    
    Args:
        conversation_id: ID of the conversation to delete
        db: Database session
        
    Returns:
        Success status
    """
    try:
        success = ConversationService.delete_conversation(db, conversation_id)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Conversation {conversation_id} not found"
            )
        
        return {
            "status": "success",
            "message": f"Conversation {conversation_id} deleted"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/conversation/{conversation_id}/archive")
async def archive_conversation(
    conversation_id: str,
    db: Session = Depends(get_db)
):
    """
    Archive a conversation.
    
    Args:
        conversation_id: ID of the conversation to archive
        db: Database session
        
    Returns:
        Success status
    """
    try:
        success = ConversationService.archive_conversation(db, conversation_id)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Conversation {conversation_id} not found"
            )
        
        return {
            "status": "success",
            "message": f"Conversation {conversation_id} archived"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error archiving conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/db-health")
async def database_health(db: Session = Depends(get_db)):
    """
    Check database health.
    
    Args:
        db: Database session
        
    Returns:
        Database status
    """
    try:
        from ..models.db.models import Conversation
        
        # Try a simple query to check connection
        db.query(Conversation).first()
        
        return {
            "status": "healthy",
            "database": "connected",
            "type": "sqlite" if "sqlite" in settings.DATABASE_URL else "postgresql"
        }
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Database connection failed")

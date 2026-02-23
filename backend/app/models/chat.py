"""Data models for chat functionality."""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Message(BaseModel):
    """Individual message model."""
    role: str = Field(..., description="Role of the message sender: 'user' or 'assistant'")
    content: str = Field(..., description="Content of the message")
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., description="User's message/question")
    conversation_id: Optional[str] = Field(None, description="Conversation ID (optional)")
    conversation_history: Optional[List[Message]] = Field(
        default_factory=list,
        description="Previous messages in the conversation"
    )


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    message: str = Field(..., description="Assistant's response")
    role: str = Field(default="assistant", description="Role of the responder")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    conversation_id: Optional[str] = Field(None, description="Associated conversation ID")


class ConversationStartRequest(BaseModel):
    """Request model to start a new conversation."""
    user_name: Optional[str] = Field(default="User", description="Name of the user")
    user_email: Optional[str] = Field(None, description="Email of the user")


class ConversationResponse(BaseModel):
    """Response for conversation creation."""
    conversation_id: str = Field(..., description="ID of the created conversation")
    user_name: str = Field(..., description="User name")
    created_at: datetime = Field(..., description="Creation timestamp")


class ConversationHistoryResponse(BaseModel):
    """Response for conversation history."""
    conversation_id: str = Field(..., description="Conversation ID")
    messages: List[Message] = Field(..., description="List of messages")
    user_name: str = Field(..., description="User name")
    created_at: datetime = Field(..., description="Conversation creation time")
    updated_at: datetime = Field(..., description="Last update time")


class ResumeRequest(BaseModel):
    """Request model to update resume context."""
    resume_content: str = Field(..., description="The resume content")


class ResumeResponse(BaseModel):
    """Response for resume operations."""
    resume_id: str = Field(..., description="Resume ID")
    version: int = Field(..., description="Resume version")
    created_at: datetime = Field(..., description="Creation timestamp")


class HealthCheckResponse(BaseModel):
    """Health check response model."""
    status: str = Field(default="healthy", description="Status of the service")
    version: str = Field(default="1.0.0", description="API version")
    database: Optional[str] = Field(None, description="Database status")


class GetConversationsRequest(BaseModel):
    """Request to get user conversations."""
    user_name: str = Field(..., description="User name")
    limit: Optional[int] = Field(10, description="Maximum conversations to return")


class ConversationListResponse(BaseModel):
    """Response for list of conversations."""
    total: int = Field(..., description="Total number of conversations")
    conversations: List[ConversationResponse] = Field(..., description="List of conversations")


"""SQLAlchemy ORM models for database."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

Base = declarative_base()


class Conversation(Base):
    """Conversation model storing user conversations."""
    
    __tablename__ = "conversations"
    
    # Primary key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # User information
    user_name = Column(String(255), nullable=False, default="User")
    user_email = Column(String(255), nullable=True)
    
    # Metadata
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Status
    is_active = Column(String(20), default="active", nullable=False)  # active, archived, deleted
    
    # Relationship
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, user={self.user_name}, created_at={self.created_at})>"


class Message(Base):
    """Message model storing individual messages in conversations."""
    
    __tablename__ = "messages"
    
    # Primary key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Foreign key
    conversation_id = Column(String(36), ForeignKey("conversations.id"), nullable=False)
    
    # Message content
    role = Column(String(50), nullable=False)  # user or assistant
    content = Column(Text, nullable=False)
    
    # Metadata
    tokens_used = Column(Integer, nullable=True)  # Track API usage
    model_used = Column(String(255), nullable=True)  # Which model generated the response
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Status
    is_deleted = Column(String(20), default="false", nullable=False)  # true or false
    
    # Relationship
    conversation = relationship("Conversation", back_populates="messages")
    
    def __repr__(self):
        return f"<Message(id={self.id}, role={self.role}, created_at={self.created_at})>"


class ResumeData(Base):
    """Store resume versions for context."""
    
    __tablename__ = "resume_data"
    
    # Primary key
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Content
    content = Column(Text, nullable=False)
    
    # Metadata
    version = Column(Integer, default=1, nullable=False)
    is_active = Column(String(20), default="active", nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<ResumeData(id={self.id}, version={self.version})>"

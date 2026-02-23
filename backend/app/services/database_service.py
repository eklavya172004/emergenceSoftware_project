"""Service for managing conversations in the database."""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime
import logging
from ..models.db.models import Conversation, Message, ResumeData
from ..models.chat import Message as MessageSchema

logger = logging.getLogger(__name__)


class ConversationService:
    """Service to handle conversation database operations."""
    
    @staticmethod
    def create_conversation(db: Session, user_name: str, user_email: Optional[str] = None) -> Conversation:
        """
        Create a new conversation.
        
        Args:
            db: Database session
            user_name: Name of the user
            user_email: Email of the user (optional)
            
        Returns:
            Created Conversation object
        """
        try:
            conversation = Conversation(
                user_name=user_name,
                user_email=user_email,
                title=f"Conversation with {user_name}",
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
            logger.info(f"Conversation created: {conversation.id}")
            return conversation
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating conversation: {str(e)}")
            raise
    
    @staticmethod
    def get_conversation(db: Session, conversation_id: str) -> Optional[Conversation]:
        """
        Get a conversation by ID.
        
        Args:
            db: Database session
            conversation_id: ID of the conversation
            
        Returns:
            Conversation object or None
        """
        try:
            return db.query(Conversation).filter(
                Conversation.id == conversation_id,
                Conversation.is_active == "active"
            ).first()
        except Exception as e:
            logger.error(f"Error getting conversation: {str(e)}")
            return None
    
    @staticmethod
    def get_user_conversations(db: Session, user_name: str, limit: int = 10) -> List[Conversation]:
        """
        Get all conversations for a user.
        
        Args:
            db: Database session
            user_name: Name of the user
            limit: Maximum number of conversations to return
            
        Returns:
            List of Conversation objects
        """
        try:
            return db.query(Conversation).filter(
                Conversation.user_name == user_name,
                Conversation.is_active == "active"
            ).order_by(desc(Conversation.updated_at)).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting user conversations: {str(e)}")
            return []
    
    @staticmethod
    def add_message(
        db: Session,
        conversation_id: str,
        role: str,
        content: str,
        tokens_used: Optional[int] = None,
        model_used: Optional[str] = None
    ) -> Message:
        """
        Add a message to a conversation.
        
        Args:
            db: Database session
            conversation_id: ID of the conversation
            role: Role of the sender (user or assistant)
            content: Message content
            tokens_used: Tokens used by the API (optional)
            model_used: Model used to generate response (optional)
            
        Returns:
            Created Message object
        """
        try:
            message = Message(
                conversation_id=conversation_id,
                role=role,
                content=content,
                tokens_used=tokens_used,
                model_used=model_used,
            )
            db.add(message)
            
            # Update conversation timestamp
            conversation = db.query(Conversation).filter(
                Conversation.id == conversation_id
            ).first()
            if conversation:
                conversation.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(message)
            logger.info(f"Message added to conversation: {conversation_id}")
            return message
        except Exception as e:
            db.rollback()
            logger.error(f"Error adding message: {str(e)}")
            raise
    
    @staticmethod
    def get_conversation_history(db: Session, conversation_id: str) -> List[Message]:
        """
        Get all messages in a conversation.
        
        Args:
            db: Database session
            conversation_id: ID of the conversation
            
        Returns:
            List of Message objects ordered by creation time
        """
        try:
            return db.query(Message).filter(
                Message.conversation_id == conversation_id,
                Message.is_deleted == "false"
            ).order_by(Message.created_at).all()
        except Exception as e:
            logger.error(f"Error getting conversation history: {str(e)}")
            return []
    
    @staticmethod
    def delete_conversation(db: Session, conversation_id: str) -> bool:
        """
        Soft delete a conversation (mark as deleted).
        
        Args:
            db: Database session
            conversation_id: ID of the conversation
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conversation = db.query(Conversation).filter(
                Conversation.id == conversation_id
            ).first()
            
            if not conversation:
                return False
            
            conversation.is_active = "deleted"
            db.commit()
            logger.info(f"Conversation deleted: {conversation_id}")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting conversation: {str(e)}")
            return False
    
    @staticmethod
    def archive_conversation(db: Session, conversation_id: str) -> bool:
        """
        Archive a conversation.
        
        Args:
            db: Database session
            conversation_id: ID of the conversation
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conversation = db.query(Conversation).filter(
                Conversation.id == conversation_id
            ).first()
            
            if not conversation:
                return False
            
            conversation.is_active = "archived"
            db.commit()
            logger.info(f"Conversation archived: {conversation_id}")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error archiving conversation: {str(e)}")
            return False


class ResumeService:
    """Service to manage resume data versions."""
    
    @staticmethod
    def save_resume(db: Session, content: str) -> ResumeData:
        """
        Save a new resume version.
        
        Args:
            db: Database session
            content: Resume content
            
        Returns:
            Created ResumeData object
        """
        try:
            # Set previous resume as inactive
            previous = db.query(ResumeData).filter(
                ResumeData.is_active == "active"
            ).first()
            
            if previous:
                previous.is_active = "inactive"
            
            # Create new version
            version = (db.query(ResumeData).count() or 0) + 1
            resume = ResumeData(
                content=content,
                version=version,
                is_active="active"
            )
            
            db.add(resume)
            db.commit()
            db.refresh(resume)
            logger.info(f"Resume saved: version {version}")
            return resume
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving resume: {str(e)}")
            raise
    
    @staticmethod
    def get_active_resume(db: Session) -> Optional[ResumeData]:
        """
        Get the current active resume.
        
        Args:
            db: Database session
            
        Returns:
            ResumeData object or None
        """
        try:
            return db.query(ResumeData).filter(
                ResumeData.is_active == "active"
            ).first()
        except Exception as e:
            logger.error(f"Error getting active resume: {str(e)}")
            return None
    
    @staticmethod
    def get_resume_history(db: Session, limit: int = 10) -> List[ResumeData]:
        """
        Get resume history.
        
        Args:
            db: Database session
            limit: Maximum number of versions to return
            
        Returns:
            List of ResumeData objects
        """
        try:
            return db.query(ResumeData).order_by(
                desc(ResumeData.created_at)
            ).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting resume history: {str(e)}")
            return []

"""
Database Integration Examples
"""

# Example 1: React frontend using database API

from typing import Optional
import asyncio

# Frontend code (React/TypeScript - ChatComponent.tsx)
REACT_EXAMPLE = """
import React, { useState, FC } from 'react';

const ChatWithDB: FC = () => {
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  // Start a new conversation
  const startConversation = async () => {
    const response = await fetch(
      'http://localhost:8000/api/v1/conversations/start',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_name: 'User' })
      }
    );
    const data = await response.json();
    setConversationId(data.conversation_id);
  };

  // Send message and save to database
  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!conversationId) {
      await startConversation();
      return;
    }

    const response = await fetch(
      'http://localhost:8000/api/v1/conversations/message-with-history',
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: input,
          conversation_id: conversationId
        })
      }
    );

    const data = await response.json();
    setMessages(prev => [
      ...prev,
      { role: 'user', content: input },
      { role: 'assistant', content: data.message }
    ]);
    setInput('');
  };

  // Load conversation history
  const loadConversation = async (convId: string) => {
    const response = await fetch(
      'http://localhost:8000/api/v1/conversations/conversation/' +convId
    );
    const data = await response.json();
    setConversationId(convId);
    setMessages(data.messages);
  };

  return (
    <div>
      <button onClick={startConversation}>New Chat</button>
      <form onSubmit={sendMessage}>
        <input value={input} onChange={e => setInput(e.target.value)} />
        <button type="submit">Send</button>
      </form>
      {messages.map((msg, i) => (
        <div key={i} className={msg.role}>
          {msg.content}
        </div>
      ))}
    </div>
  );
};

export default ChatWithDB;
"""

# Example 2: Python script to manage conversations

PYTHON_EXAMPLE = """
from app.database import SessionLocal
from app.services.database_service import ConversationService, ResumeService

db = SessionLocal()

# Create new conversation
conv = ConversationService.create_conversation(
    db, 
    user_name="Alice",
    user_email="alice@example.com"
)

# Add messages
ConversationService.add_message(
    db, 
    conversation_id=conv.id,
    role="user",
    content="Tell me about React"
)

ConversationService.add_message(
    db,
    conversation_id=conv.id,
    role="assistant", 
    content="React is a JavaScript library..."
)

# Get conversation history
history = ConversationService.get_conversation_history(db, conv.id)

for msg in history:
    print(f"{msg.role}: {msg.content}")

# Get all user conversations
conversations = ConversationService.get_user_conversations(db, "Alice", limit=5)
print(f"Total conversations: {len(conversations)}")

# Archive a conversation
ConversationService.archive_conversation(db, conv.id)

db.close()
"""

# Example 3: cURL commands for database APIs

CURL_EXAMPLE = """
# 1. Start a new conversation
curl -X POST http://localhost:8000/api/v1/conversations/start \\
  -H "Content-Type: application/json" \\
  -d '{
    "user_name": "John",
    "user_email": "john@example.com"
  }'

# Response:
# {
#   "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
#   "user_name": "John",
#   "created_at": "2024-02-22T10:30:00"
# }

# 2. Send message with database saving
curl -X POST http://localhost:8000/api/v1/conversations/message-with-history \\
  -H "Content-Type: application/json" \\
  -d '{
    "message": "What are your skills?",
    "conversation_id": "550e8400-e29b-41d4-a716-446655440000"
  }'

# 3. Get all conversations for a user
curl http://localhost:8000/api/v1/conversations/john

# 4. Get conversation history
curl http://localhost:8000/api/v1/conversations/conversation/550e8400-e29b-41d4-a716-446655440000

# 5. Delete a conversation
curl -X DELETE http://localhost:8000/api/v1/conversations/conversation/550e8400-e29b-41d4-a716-446655440000

# 6. Archive a conversation
curl -X POST http://localhost:8000/api/v1/conversations/conversation/550e8400-e29b-41d4-a716-446655440000/archive

# 7. Check database health
curl http://localhost:8000/api/v1/conversations/db-health
"""

# Example 4: Environment variables for different databases

ENV_EXAMPLES = """
# .env - SQLite (default, no setup needed)
DATABASE_URL=sqlite:///./portfolio.db

# .env - PostgreSQL (local)
DATABASE_URL=postgresql://user:password@localhost:5432/portfolio

# .env - PostgreSQL (Railway)
DATABASE_URL=postgresql://user:password@your-railway-domain.up.railway.app:5432/portfolio

# .env - PostgreSQL (AWS RDS)
DATABASE_URL=postgresql://admin:password@portfolio.c9akciq32.us-east-1.rds.amazonaws.com:5432/portfolio
"""

if __name__ == "__main__":
    print("=== Database Integration Examples ===\n")
    print("1. React Frontend Example:")
    print(REACT_EXAMPLE)
    print("\n2. Python Script Example:")
    print(PYTHON_EXAMPLE)
    print("\n3. cURL Commands:")
    print(CURL_EXAMPLE)
    print("\n4. Environment Variables:")
    print(ENV_EXAMPLES)

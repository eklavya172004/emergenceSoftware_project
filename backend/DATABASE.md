# Database Setup & Configuration Guide

## ✅ Database Integration Complete!

Your backend now has full database support for storing conversation history with SQLite (default) and support for PostgreSQL.

---

## 🗄️ What's Included

### Database Features:
- ✅ **Conversation Storage** - Save and retrieve conversations
- ✅ **Message History** - Store all user and AI messages
- ✅ **Resume Versioning** - Track resume changes
- ✅ **Automatic Timestamps** - Track when conversations happen
- ✅ **Soft Deletes** - Archive/delete conversations safely
- ✅ **SQLite Default** - Zero configuration needed!
- ✅ **PostgreSQL Ready** - Easy upgrade for production

---

## 🚀 Quick Start

### 1️⃣ Install Database Dependencies

```bash
cd backend
source venv/Scripts/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt  # This now includes SQLAlchemy
```

### 2️⃣ Initialize Database

```bash
python init_db.py
```

You should see:
```
✅ Database initialized successfully!
Database file: portfolio.db
Tables created: conversations, messages, resume_data
```

### 3️⃣ Run the Server

```bash
python main.py
```

Your database is ready! 🎉

---

## 📊 Database Schema

### Tables

#### **conversations**
Stores conversation metadata
```
- id (UUID) - Primary key
- user_name (String) - User identifier
- user_email (String) - Optional email
- title (String) - Conversation title
- description (Text) - Optional description
- created_at (DateTime) - When conversation started
- updated_at (DateTime) - Last activity time
- is_active (String) - active/archived/deleted status
```

#### **messages**
Stores individual messages in conversations
```
- id (UUID) - Primary key
- conversation_id (FK) - References conversations.id
- role (String) - 'user' or 'assistant'
- content (Text) - Message content
- tokens_used (Integer) - API tokens (optional)
- model_used (String) - Which model generated it
- created_at (DateTime) - Message timestamp
- updated_at (DateTime) - Last update time
- is_deleted (String) - true/false soft delete flag
```

#### **resume_data**
Stores resume versions
```
- id (UUID) - Primary key
- content (Text) - Resume content
- version (Integer) - Version number
- is_active (String) - active/inactive status
- created_at (DateTime) - Creation time
- updated_at (DateTime) - Update time
```

---

## 🔌 New API Endpoints

### Conversation Management

```
POST /api/v1/conversations/start
- Start a new conversation
- Returns: conversation_id

POST /api/v1/conversations/message-with-history
- Send message and save to database
- Returns: assistant response + conversation_id

GET /api/v1/conversations/{user_name}
- Get all conversations for a user
- Returns: List of conversations

GET /api/v1/conversations/conversation/{conversation_id}
- Get full history of a conversation
- Returns: All messages in conversation

DELETE /api/v1/conversations/conversation/{conversation_id}
- Soft delete a conversation
- Returns: Success status

POST /api/v1/conversations/conversation/{conversation_id}/archive
- Archive a conversation
- Returns: Success status

GET /api/v1/conversations/db-health
- Check database connection
- Returns: Database status
```

---

## 💾 Database Types

### SQLite (Default)

**Pros:**
- ✅ Zero configuration
- ✅ File-based (easy backup)
- ✅ Perfect for development
- ✅ No server needed

**Cons:**
- Limited concurrent users
- Not ideal for production with many users

**Setup:**
```env
DATABASE_URL=sqlite:///./portfolio.db
```

File location: `backend/portfolio.db`

### PostgreSQL (Production)

**Pros:**
- ✅ Production-ready
- ✅ Handles many concurrent users
- ✅ Better performance
- ✅ Advanced features

**Cons:**
- Requires server setup
- More configuration

**Setup:**

1. Install PostgreSQL
2. Create database:
   ```bash
   createdb portfolio
   ```

3. Update `.env`:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/portfolio
   ```

4. Install driver:
   ```bash
   pip install psycopg2-binary
   ```

---

## 🔄 Using the Database in Code

### Example: Save and Retrieve Conversations

```python
from app.database import SessionLocal
from app.services.database_service import ConversationService

# Get database session
db = SessionLocal()

# Start a conversation
conversation = ConversationService.create_conversation(
    db=db,
    user_name="John Doe",
    user_email="john@example.com"
)
print(f"Conversation ID: {conversation.id}")

# Add messages
ConversationService.add_message(
    db=db,
    conversation_id=conversation.id,
    role="user",
    content="What skills do you have?"
)

ConversationService.add_message(
    db=db,
    conversation_id=conversation.id,
    role="assistant",
    content="I have experience with React, Python, and more..."
)

# Get conversation history
messages = ConversationService.get_conversation_history(
    db=db,
    conversation_id=conversation.id
)

for msg in messages:
    print(f"{msg.role}: {msg.content}")

db.close()
```

---

## 🧪 Test the Database

### Using API Docs

1. Start server: `python main.py`
2. Open: http://localhost:8000/docs
3. Try these endpoints:
   - `POST /api/v1/conversations/start`
   - `POST /api/v1/conversations/message-with-history`
   - `GET /api/v1/conversations/{user_name}`
   - `GET /api/v1/conversations/db-health`

### Using Python

```python
import httpx
import asyncio

async def test_db():
    async with httpx.AsyncClient() as client:
        # Start conversation
        conv = await client.post(
            "http://localhost:8000/api/v1/conversations/start",
            json={"user_name": "TestUser"}
        )
        conv_id = conv.json()["conversation_id"]
        
        # Send message
        response = await client.post(
            "http://localhost:8000/api/v1/conversations/message-with-history",
            json={
                "message": "Tell me about your experience",
                "conversation_id": conv_id
            }
        )
        print(response.json())
        
        # Get history
        history = await client.get(
            f"http://localhost:8000/api/v1/conversations/conversation/{conv_id}"
        )
        print(history.json())

asyncio.run(test_db())
```

---

## 🔧 Troubleshooting

### Issue: "No such table: conversations"

**Solution:**
```bash
python init_db.py
```

### Issue: "Database is locked"

**Reason:** Multiple processes accessing SQLite

**Solutions:**
- Close all connections
- Use PostgreSQL for multiple connections
- Restart the server

### Issue: Can't connect to PostgreSQL

**Check:**
1. PostgreSQL running: `psql --version`
2. Database exists: `createdb portfolio`
3. Credentials correct in .env
4. Driver installed: `pip install psycopg2-binary`

### Issue: "ImportError: No module named sqlalchemy"

**Solution:**
```bash
pip install -r requirements.txt
```

---

## 📈 Performance Tips

### SQLite
- Use for development and testing
- Single-server deployments
- Low-traffic applications

### PostgreSQL
- Use for production
- Multiple servers
- High-traffic applications
- Better for concurrent users

### Optimization
- Add indexes on frequently queried columns
- Archive old conversations
- Regular backups
- Monitor query performance

---

## 🔒 Security

### Best Practices

1. **Backup regularly:**
   ```bash
   cp portfolio.db portfolio.db.backup
   ```

2. **Use environment variables:**
   ```env
   DATABASE_URL=postgresql://user:password@host/db
   ```

3. **Never commit database files:**
   ```
   *.db
   *.db-*
   ```

4. **Validate user input**:
   - Pydantic validates all inputs
   - Use prepared statements (SQLAlchemy does this)

5. **Access control:**
   - Authenticate users before saving conversations
   - Only allow users to see their own conversations

---

## 🚀 Production Deployment

### Railway (Recommended)

Railway provides free PostgreSQL database:

1. Connect GitHub repo to Railway
2. Add PostgreSQL service
3. Railway creates DATABASE_URL automatically
4. Set in backend environment variables

### Render

Render offers free PostgreSQL:

1. Create PostgreSQL service
2. Get connection string
3. Add to environment variables

### AWS RDS

For larger applications:

```env
DATABASE_URL=postgresql://user:pw@rds.amazonaws.com:5432/portfolio
```

### Local PostgreSQL

1. Install: `brew install postgresql` (Mac) or `apt-get install postgresql` (Linux)
2. Create DB: `createdb portfolio`
3. Update .env with local credentials

---

## 📝 Next Steps

1. ✅ Database setupcomplete
2. 🎯 Connect frontend to new endpoints
3. 📊 Add conversation statistics
4. 🔐 Add user authentication
5. 🚀 Deploy to production

---

## 🔗 Resources

- **SQLAlchemy Docs:** https://docs.sqlalchemy.org
- **PostgreSQL Setup:** https://www.postgresql.org/download
- **Railway:** https://railway.app
- **Render:** https://render.com

---

## 💡 Example: Full Conversation Workflow

```python
# 1. User visits portfolio
# Frontend button: "Start Chat"

# 2. Frontend calls:
POST /api/v1/conversations/start
{
  "user_name": "Visitor",
  "user_email": "visitor@example.com"
}
# Response: { "conversation_id": "uuid-123" }

# 3. User asks question
# Frontend calls:
POST /api/v1/conversations/message-with-history
{
  "message": "What projects have you built?",
  "conversation_id": "uuid-123"
}
# Response: { "message": "I've built...", "conversation_id": "uuid-123" }

# 4. Messages are saved automatically to:
# - conversations table
# - messages table (both user and assistant messages)

# 5. User later returns and wants to see old chats
# Frontend calls:
GET /api/v1/conversations/{user_name}
# Response: [{ conversation_id: "uuid-123", created_at: "...", ... }]

# 6. User opens old conversation
# Frontend calls:
GET /api/v1/conversations/conversation/uuid-123
# Response: Complete conversation history with all messages
```

---

**Your database is production-ready! 🎉**

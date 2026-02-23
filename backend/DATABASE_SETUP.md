# 🗄️ Database Integration - Complete Guide

Your backend now has **full database support** for storing conversation history!

## ⚡ Quick Start (2 Minutes)

### Windows
```bash
cd backend
python venv\Scripts\activate.bat
pip install -r requirements.txt
python init_db.py
python main.py
```

### Mac/Linux
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
python init_db.py
python main.py
```

### Or use the quick start script:
```bash
bash backend/quickstart.sh          # Mac/Linux
backend\quickstart.bat              # Windows
```

Then open: **http://localhost:8000/docs**

---

## 📋 What You Get

### ✅ Included Files

```
backend/
├── app/
│   ├── database.py                 # SQLAlchemy setup
│   ├── models/db/
│   │   ├── models.py              # 3 ORM models (Conversation, Message, ResumeData)
│   │   └── __init__.py
│   ├── services/
│   │   └── database_service.py    # Business logic layer
│   ├── api/
│   │   └── database.py            # 7 new API endpoints
│   ├── config.py                  # Database configuration
│   └── main.py                    # Updated with database initialization
├── init_db.py                      # Database initialization script
├── migrate.py                      # Migration tools
├── DATABASE.md                     # Full documentation
├── DATABASE_EXAMPLES.py            # Code examples
├── FRONTEND_INTEGRATION.py         # React integration guide
├── quickstart.sh / quickstart.bat  # Quick start scripts
└── requirements.txt                # Updated with SQLAlchemy
```

### 📊 Database Tables

| Table | Purpose |
|-------|---------|
| **conversations** | Stores conversation metadata |
| **messages** | Stores individual messages (user & assistant) |
| **resume_data** | Stores resume versions |

### 🔌 New API Endpoints (7 Total)

```
POST   /conversations/start                          # New conversation
POST   /conversations/message-with-history           # Send & save message
GET    /conversations/{user_name}                    # List user conversations
GET    /conversations/conversation/{conversation_id} # Get conversation history
DELETE /conversations/conversation/{conversation_id} # Delete conversation
POST   /conversations/conversation/{conversation_id}/archive # Archive conversation
GET    /conversations/db-health                      # Database status
```

---

## 🚀 Next Steps

### 1️⃣ Initialize Database
```bash
python init_db.py
```
Creates `portfolio.db` with 3 tables ready to use.

### 2️⃣ Test API Endpoints
Start server: `python main.py`
Visit: http://localhost:8000/docs

### 3️⃣ Try an Endpoint
```bash
curl -X POST http://localhost:8000/api/v1/conversations/start \
  -H "Content-Type: application/json" \
  -d '{"user_name": "John"}'
```

### 4️⃣ Connect Frontend
See [FRONTEND_INTEGRATION.py](FRONTEND_INTEGRATION.py) for React setup

### 5️⃣ Deploy
Switch to PostgreSQL in production using [migrate.py](migrate.py)

---

## 🎯 Key Features

### Database Options
- **SQLite** (default, zero config) - Perfect for development
- **PostgreSQL** (production) - Handles more users, better performance

### Auto-Initialization
Database creates tables automatically when app starts - just run `init_db.py` once!

### Type Safety
All models use Pydantic for validation - ensures data quality

### Service Layer
Clean separation between API routes and database logic - easy to test and maintain

### Soft Deletes
Archive/delete conversations safely - no data loss, can restore if needed

---

## 📚 Documentation

### For Detailed Setup
→ Read [DATABASE.md](DATABASE.md)
- Schema details
- Configuration options
- Troubleshooting
- Production deployment

### For Code Examples  
→ Read [DATABASE_EXAMPLES.py](DATABASE_EXAMPLES.py)
- React component examples
- Python usage examples
- cURL commands
- Environment variables

### For Frontend Integration
→ Read [FRONTEND_INTEGRATION.py](FRONTEND_INTEGRATION.py)
- Complete React component (styled)
- API client setup
- Deployment configuration
- CORS setup

### For Database Migration
→ Read [migrate.py](migrate.py)
- How to switch from SQLite to PostgreSQL
- Docker setup for PostgreSQL
- Data migration scripts
- Verification tools

---

## 🔒 Default Configuration

### Database
```
SQLite file: portfolio.db
Location: backend/portfolio.db
Size: ~1MB initially, grows with conversations
Backup: Use your file system or cp portfolio.db portfolio.db.backup
```

### API
```
Base URL: http://localhost:8000/api/v1
Docs: http://localhost:8000/docs
CORS: Allows localhost:3000 (React frontend)
```

---

## ⚙️ Environment Variables

### Default (.env)
```
DATABASE_URL=sqlite:///./portfolio.db
```

### Production (.env)
```
DATABASE_URL=postgresql://user:password@host:5432/db
```

---

## 🐛 Troubleshooting

### "No such table: conversations"
```bash
python init_db.py
```

### "Database is locked"
SQLite issue - close all connections and restart server

### Can't install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### More help?
See [DATABASE.md](DATABASE.md) Troubleshooting section

---

## 🔄 Common Workflows

### Deleting Old Conversations
```python
from app.database import SessionLocal
from app.services.database_service import ConversationService

db = SessionLocal()
ConversationService.delete_conversation(db, conversation_id)
db.close()
```

### Backing Up Database
```bash
cp backend/portfolio.db backend/portfolio.db.backup
```

### Switching to PostgreSQL
```bash
python migrate.py --docker      # See Docker setup
python migrate.py --migrate     # See migration guide
```

---

## 📈 Production Checklist

- [ ] Backup SQLite database
- [ ] Setup PostgreSQL on production
- [ ] Update DATABASE_URL environment variable
- [ ] Run `python init_db.py` on production server
- [ ] Test all endpoints
- [ ] Enable CORS for your domain
- [ ] Setup database backups
- [ ] Monitor query performance
- [ ] Consider adding user authentication

---

## 💡 Pro Tips

1. **Conversations auto-save** - Just use `/message-with-history` endpoint
2. **No migrations needed** - Tables created automatically on startup
3. **Export conversations** - Get JSON from `/conversation/{id}` endpoint
4. **Archive instead of delete** - Use soft deletes for audit trail
5. **Monitor performance** - Use PostgreSQL for 100+ concurrent users

---

## 🎓 Learning Resources

- **SQLAlchemy:** https://docs.sqlalchemy.org
- **FastAPI Database:** https://fastapi.tiangolo.com/tutorial/sql-databases
- **PostgreSQL:** https://www.postgresql.org/docs
- **Vercel Deployment:** https://vercel.com/docs
- **Railway Deployment:** https://docs.railway.app

---

## 📊 Project Status

✅ **Complete Features:**
- SQLAlchemy ORM models
- Database service layer
- 7 API endpoints
- Auto-initialization
- SQLite & PostgreSQL support
- Type-safe Pydantic models
- Full error handling

🚀 **Ready to Deploy:**
- Frontend integration guide provided
- Migration tools included
- Production setup documented
- Quick start scripts included

---

## 🤝 Support

**Need help?**
1. Check [DATABASE.md](DATABASE.md) for detailed guide
2. Look at [DATABASE_EXAMPLES.py](DATABASE_EXAMPLES.py) for code samples
3. Review [FRONTEND_INTEGRATION.py](FRONTEND_INTEGRATION.py) for React setup
4. Run `python migrate.py --help` for migration options

---

**Database integration complete! 🎉 Your backend is now production-ready with full conversation history storage.**

Happy coding! 🚀

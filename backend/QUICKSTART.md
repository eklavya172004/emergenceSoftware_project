"""
BACKEND SETUP & QUICK START GUIDE
===================================

This is a FastAPI-based Python backend for your AI portfolio with chat functionality.

## ✅ COMPLETED SETUP

Your backend structure is now ready with:
- ✅ FastAPI application
- ✅ Virtual environment (venv/)
- ✅ All dependencies installed
- ✅ Chat API endpoints with OpenRouter integration
- ✅ CORS configured for frontend connection
- ✅ Environment configuration system
- ✅ Type-safe Pydantic models

## 🚀 NEXT STEPS: GET YOUR API KEY

1. Go to https://openrouter.ai
2. Sign up / Log in (it's free!)
3. Get your API key from: https://openrouter.ai/account/api-keys
4. Copy your API key

## ⚙️ CONFIGURE YOUR API KEY

1. Open: backend/.env
2. Replace this line:
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   
   With your actual key:
   OPENROUTER_API_KEY=sk-or-xxxxxxxxxxxxxxxxxx

3. Save the file

## 🏃 RUN THE SERVER

### Windows:
```bash
cd backend
venv\Scripts\activate
python main.py
```

### Linux/Mac:
```bash
cd backend
source venv/bin/activate
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## 📚 API DOCUMENTATION

Once server is running, visit:
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 🧪 TEST THE API

### Option 1: Using Python
```bash
# In another terminal, from backend folder:
source venv/Scripts/activate  # On Windows: venv\Scripts\activate
python test_api.py
```

### Option 2: Using cURL
```bash
# Check health
curl http://localhost:8000/health

# Check chat service
curl http://localhost:8000/api/v1/chat/health

# Send a message (requires API key configured)
curl -X POST "http://localhost:8000/api/v1/chat/message" \\
  -H "Content-Type: application/json" \\
  -d {
    "message": "What projects have you worked on?",
    "conversation_history": []
  }
```

### Option 3: Visit Swagger UI
Open http://localhost:8000/docs and test endpoints directly in the browser!

## 📁 PROJECT STRUCTURE

```
backend/
├── app/
│   ├── __init__.py           # Package initialization
│   ├── main.py               # FastAPI app factory
│   ├── config.py             # Config & environment variables
│   ├── api/
│   │   ├── __init__.py
│   │   └── chat.py           # Chat API routes
│   ├── models/
│   │   ├── __init__.py
│   │   └── chat.py           # Pydantic data models
│   └── services/
│       ├── __init__.py
│       └── openrouter_service.py  # OpenRouter API client
├── main.py                   # Entry point
├── requirements.txt          # Python dependencies
├── .env.example              # Example env variables
├── .env                      # Your actual configuration (not in git)
├── test_api.py              # API testing script
├── setup.sh                 # Linux/Mac setup script
├── setup.bat                # Windows setup script
└── README.md                # Full documentation

## 🔗 API ENDPOINTS

### Chat Endpoints
- POST /api/v1/chat/message           - Send a message to AI
- POST /api/v1/chat/start-conversation - Start new conversation
- POST /api/v1/chat/update-resume     - Update resume context
- GET  /api/v1/chat/health            - Chat service health check

### General Endpoints
- GET  /health                        - Overall health check
- GET  /                              - API info

## 🎯 EXAMPLE: SEND A MESSAGE

```python
import httpx
import asyncio

async def chat_with_ai():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/chat/message",
            json={
                "message": "Tell me about your experience with React",
                "conversation_history": []
            }
        )
        print(response.json())

asyncio.run(chat_with_ai())
```

## 🔑 ENVIRONMENT VARIABLES

Edit .env to customize:
- OPENROUTER_API_KEY    - Your API key
- OPENROUTER_MODEL      - Model to use
- SERVER_HOST           - Server host (default: 0.0.0.0)
- SERVER_PORT           - Server port (default: 8000)
- DEBUG                 - Debug mode (default: True)
- RESUME_CONTEXT        - Your resume information

## 📝 UPDATING RESUME CONTENT

Update the resume context dynamically via API:

```bash
curl -X POST "http://localhost:8000/api/v1/chat/update-resume" \\
  -H "Content-Type: application/json" \\
  -d '{
    "resume_content": "Your updated resume here..."
  }'
```

## ⚠️ TROUBLESHOOTING

### Issue: "Module not found"
- Make sure venv is activated
- Run: pip install -r requirements.txt

### Issue: "Port 8000 already in use"
- Change PORT in .env or use: python main.py --port 8001

### Issue: "API key not found"
- Edit .env and add your OpenRouter API key
- Restart the server

### Issue: "CORS error from frontend"
- Check CORS_ORIGINS in .env
- Ensure your frontend URL is in the list

## 🚀 NEXT: CONNECT FRONTEND

After testing the backend, update your frontend to call these endpoints.
See the React integration guide in the main portfolio README.

## 💡 TIPS

- Keep .env safe - don't commit it to git
- Use DEBUG=False in production
- Monitor API usage at openrouter.ai
- Test with Swagger UI at /docs

---

Questions? Check README.md for more details!
"""

print(__doc__)

# Portfolio Backend - Complete Setup & Deployment Guide

## ✅ Backend Setup Complete!

Your FastAPI backend is ready with:
- ✅ **FastAPI Framework** - Modern, fast, async Python framework
- ✅ **OpenRouter Integration** - Connect to free AI models
- ✅ **Chat API Endpoints** - Full chat with conversation history
- ✅ **CORS Configuration** - Ready for frontend connection
- ✅ **Type Safety** - Pydantic models for all requests/responses
- ✅ **Error Handling** - Proper error messages and logging
- ✅ **API Documentation** - Auto-generated Swagger UI at /docs

---

## 🎯 QUICK START

### 1️⃣ Get Your API Key
1. Go to https://openrouter.ai
2. Sign up (free tier available)
3. Get your API key from: https://openrouter.ai/account/api-keys

### 2️⃣ Configure Backend
```bash
cd backend
# Edit .env and add your API key
# OPENROUTER_API_KEY=sk-or-xxxxx
```

### 3️⃣ Run Server
```bash
# Windows
venv\Scripts\activate
python main.py

# Linux/Mac
source venv/bin/activate
python main.py
```

### 4️⃣ Test It
Visit: **http://localhost:8000/docs** - Interactive API documentation

---

## 📚 Backend Structure

```
backend/
├── app/
│   ├── main.py               ← FastAPI app
│   ├── config.py             ← Configuration
│   ├── api/
│   │   └── chat.py           ← Chat routes
│   ├── models/
│   │   └── chat.py           ← Data models
│   └── services/
│       └── openrouter_service.py  ← OpenRouter API
├── main.py                   ← Entry point
├── requirements.txt          ← Dependencies
├── .env                      ← Your configuration
└── README.md                 ← Full docs
```

---

## 🔌 API ENDPOINTS

### Chat API
```
POST /api/v1/chat/message
Content-Type: application/json

{
  "message": "What are your skills?",
  "conversation_history": []
}

Response:
{
  "message": "I have experience with...",
  "role": "assistant",
  "timestamp": "2024-02-22T..."
}
```

### Other Endpoints
- `POST /api/v1/chat/start-conversation` - New conversation
- `POST /api/v1/chat/update-resume` - Update resume context
- `GET /api/v1/chat/health` - Chat service status
- `GET /health` - Overall health check
- `GET /docs` - Interactive API docs

---

## 🌐 Frontend Integration

The backend is CORS-enabled for your React frontend.

### Using in React (TypeScript)

```typescript
// .env
REACT_APP_API_URL=http://localhost:8000

// ChatComponent.tsx
const [messages, setMessages] = useState([]);
const [input, setInput] = useState('');

const sendMessage = async () => {
  const response = await fetch(
    `${process.env.REACT_APP_API_URL}/api/v1/chat/message`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: input,
        conversation_history: messages
      })
    }
  );
  
  const data = await response.json();
  setMessages([...messages, { role: 'assistant', content: data.message }]);
};
```

See **ChatComponent.example.tsx** for full example!

---

## 🚀 Deployment Options

### Option 1: Cloudflare Tunnel (Recommended for Free Tier)
```bash
# Install Cloudflare CLI
# Run your backend
python main.py

# In another terminal, expose it
cloudflared tunnel --url http://localhost:8000
```

Your backend will be accessible at a public URL!

### Option 2: Railway (Free Tier)
1. Push code to GitHub
2. Connect GitHub to Railway
3. Set environment variables
4. Deploy!

### Option 3: Render (Free Tier)
1. Create account at render.com
2. Connect GitHub repo
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python main.py`
5. Add environment variables
6. Deploy!

### Option 4: PythonAnywhere (Free Tier)
1. Upload files to pythonanywhere.com
2. Configure web app
3. Set Python version to 3.9+
4. Deploy!

---

## 🔒 Production Checklist

Before deploying:

- [ ] Set `DEBUG=False` in .env
- [ ] Use environment variables for API key
- [ ] Configure CORS for your frontend domain
- [ ] Set secure database if using one
- [ ] Use HTTPS (always!)
- [ ] Monitor API usage at openrouter.ai
- [ ] Set up error logging
- [ ] Test all endpoints thoroughly
- [ ] Consider rate limiting
- [ ] Set proper headers for security

```env
# Production .env
DEBUG=False
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
OPENROUTER_API_KEY=your-key-here
CORS_ORIGINS=["https://yourdomain.com"]
```

---

## 📊 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENROUTER_API_KEY` | (required) | Your OpenRouter API key |
| `OPENROUTER_MODEL` | meta-llama/codellama-34b-instruct | AI model to use |
| `SERVER_HOST` | 0.0.0.0 | Server host |
| `SERVER_PORT` | 8000 | Server port |
| `DEBUG` | True | Debug mode |
| `CORS_ORIGINS` | localhost:3000 | Allowed frontend URLs |
| `RESUME_CONTEXT` | (default) | Your resume info |

See `.env.example` for all options.

---

## 🧪 Testing

### Test Health
```bash
curl http://localhost:8000/health
```

### Test Chat API
```bash
curl -X POST http://localhost:8000/api/v1/chat/message \
  -H "Content-Type: application/json" \
  -d '{"message":"Hi!","conversation_history":[]}'
```

### Run Python Tests
```bash
source venv/Scripts/activate
python test_api.py
```

### Visit Swagger UI
http://localhost:8000/docs

---

## 🐛 Troubleshooting

**Q: "Module not found error"**
- Activate virtual environment and reinstall: `pip install -r requirements.txt`

**Q: "API key not configured"**
- Edit `.env` and add your OpenRouter API key

**Q: "Port 8000 already in use"**
- Change port in `.env` or kill process using port 8000

**Q: "CORS error from frontend"**
- Add frontend URL to `CORS_ORIGINS` in `.env`

**Q: "Request timeout"**
- OpenRouter API may be slow, increase timeout in config

---

## 📦 Dependencies

All dependencies are defined in `requirements.txt`:
- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **pydantic** - Data validation
- **httpx** - Async HTTP client
- **aiohttp** - Async HTTP library
- **python-dotenv** - Environment variables

---

## 🔗 Useful Links

- **OpenRouter**: https://openrouter.ai
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Uvicorn**: https://www.uvicorn.org
- **Pydantic**: https://docs.pydantic.dev
- **Cloudflare Tunnel**: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/

---

## 💡 Next Steps

1. ✅ Backend created and running locally
2. 🎯 Connect React frontend to chat API
3. 📊 Add database for conversation history
4. 🔐 Add user authentication
5. 🚀 Deploy to production with Cloudflare or Railway

---

## 📝 Notes

- Your API key is private - don't commit .env to git
- Keep conversation history in frontend state or database
- Monitor API usage to stay within free tier limits
- Test thoroughly before production deployment

---

**Happy coding! 🚀**

For more details, see `README.md` in the backend folder.

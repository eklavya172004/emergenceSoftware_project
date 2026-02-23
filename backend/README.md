# Portfolio Backend

A FastAPI-based backend for the AI-powered portfolio with chat functionality.

## Features

- 🤖 AI Chat with OpenRouter
- 📄 Resume Q&A functionality
- 🚀 Fast and async with FastAPI
- 🔒 CORS enabled for frontend integration
- 📝 Pydantic models for data validation

## Setup

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your OpenRouter API key:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Get your free API key from [OpenRouter](https://openrouter.ai)

### 4. Run the Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Chat Endpoints

- **POST** `/api/v1/chat/message` - Send a message to the AI assistant
  - Request: `{ "message": "string", "conversation_history": [] }`
  - Response: `{ "message": "string", "role": "assistant", "timestamp": "ISO8601" }`

- **POST** `/api/v1/chat/start-conversation` - Start a new conversation
  
- **POST** `/api/v1/chat/update-resume` - Update resume context
  - Request: `{ "resume_content": "string" }`

- **GET** `/api/v1/chat/health` - Health check for chat service

### General Endpoints

- **GET** `/health` - Health check
- **GET** `/` - Root endpoint

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app factory
│   ├── config.py            # Configuration settings
│   ├── api/
│   │   ├── __init__.py
│   │   └── chat.py          # Chat routes
│   ├── models/
│   │   ├── __init__.py
│   │   └── chat.py          # Pydantic models
│   └── services/
│       ├── __init__.py
│       └── openrouter_service.py  # OpenRouter API service
├── requirements.txt
├── main.py                  # Entry point
├── .env.example             # Example environment variables
└── README.md
```

## Development

### Environment Variables

Copy `.env.example` to `.env` and configure:

- `OPENROUTER_API_KEY` - Your OpenRouter API key
- `OPENROUTER_MODEL` - The model to use (default: meta-llama/codellama-34b-instruct)
- `SERVER_HOST` - Server host (default: 0.0.0.0)
- `SERVER_PORT` - Server port (default: 8000)
- `DEBUG` - Debug mode (default: True)

### Running in Production

Set `DEBUG=False` in `.env` and run with:

```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

## Testing the API

### Using cURL

```bash
# Send a message
curl -X POST "http://localhost:8000/api/v1/chat/message" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is your experience with React?", "conversation_history": []}'

# Health check
curl http://localhost:8000/health
```

### Using Python

```python
import httpx
import asyncio

async def test_chat():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/v1/chat/message",
            json={"message": "Tell me about your experience"}
        )
        print(response.json())

asyncio.run(test_chat())
```

## Next Steps

1. Connect with frontend React app
2. Add database integration for conversation history
3. Add user authentication
4. Deploy to production with Cloudflare tunnels

## License

MIT

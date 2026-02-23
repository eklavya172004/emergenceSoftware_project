"""Example usage of the Portfolio Backend API."""
import asyncio
import httpx
import json


async def test_health():
    """Test health endpoint."""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/health")
        print("✅ Health Check:")
        print(json.dumps(response.json(), indent=2))


async def test_chat():
    """Test chat endpoint."""
    async with httpx.AsyncClient() as client:
        # Note: This will only work if you have OpenRouter API key configured
        response = await client.post(
            "http://localhost:8000/api/v1/chat/message",
            json={
                "message": "What are your main technical skills?",
                "conversation_history": []
            }
        )
        print("✅ Chat Response:")
        print(json.dumps(response.json(), indent=2))


async def test_start_conversation():
    """Test start conversation endpoint."""
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8000/api/v1/chat/start-conversation")
        print("✅ Start Conversation:")
        print(json.dumps(response.json(), indent=2))


async def test_chat_health():
    """Test chat service health."""
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/api/v1/chat/health")
        print("✅ Chat Health:")
        print(json.dumps(response.json(), indent=2))


async def main():
    """Run all tests."""
    print("🧪 Portfolio Backend API Tests\n")
    
    try:
        await test_health()
        print()
        await test_chat_health()
        print()
        await test_start_conversation()
        print()
        
        # Uncomment to test chat with OpenRouter API
        # await test_chat()
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())

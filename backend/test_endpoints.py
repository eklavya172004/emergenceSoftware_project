#!/usr/bin/env python3
"""Test the fixed API endpoints."""
import httpx
import asyncio
import json

BASE_URL = "http://localhost:8000"

async def test_endpoints():
    """Test all conversation endpoints."""
    async with httpx.AsyncClient() as client:
        print("🧪 Testing Fixed API Endpoints\n")
        
        # Test 1: Health check
        print("1️⃣  Testing /health endpoint...")
        try:
            response = await client.get(f"{BASE_URL}/health")
            print(f"   ✅ Status: {response.status_code}")
            print(f"   Response: {response.json()}\n")
        except Exception as e:
            print(f"   ❌ Error: {e}\n")
        
        # Test 2: Start conversation
        print("2️⃣  Testing POST /api/v1/conversations/start...")
        try:
            response = await client.post(
                f"{BASE_URL}/api/v1/conversations/start",
                json={"user_name": "Yusuf", "user_email": "yusuf@example.com"}
            )
            print(f"   ✅ Status: {response.status_code}")
            data = response.json()
            print(f"   Response: {data}\n")
            
            if "conversation_id" in data:
                conversation_id = data["conversation_id"]
                
                # Test 3: Get user conversations
                print(f"3️⃣  Testing GET /api/v1/conversations/Yusuf...")
                try:
                    response = await client.get(
                        f"{BASE_URL}/api/v1/conversations/Yusuf"
                    )
                    print(f"   ✅ Status: {response.status_code}")
                    print(f"   Response: {response.json()}\n")
                except Exception as e:
                    print(f"   ❌ Error: {e}\n")
                
                # Test 4: Send message with history
                print(f"4️⃣  Testing POST /api/v1/conversations/message-with-history...")
                try:
                    response = await client.post(
                        f"{BASE_URL}/api/v1/conversations/message-with-history",
                        json={
                            "message": "Tell me about your experience",
                            "conversation_id": conversation_id,
                            "conversation_history": []
                        }
                    )
                    print(f"   ✅ Status: {response.status_code}")
                    print(f"   Response: {json.dumps(response.json(), indent=2)}\n")
                except Exception as e:
                    print(f"   ❌ Error: {e}\n")
                
                # Test 5: Get conversation history
                print(f"5️⃣  Testing GET /api/v1/conversations/conversation/{conversation_id}...")
                try:
                    response = await client.get(
                        f"{BASE_URL}/api/v1/conversations/conversation/{conversation_id}"
                    )
                    print(f"   ✅ Status: {response.status_code}")
                    print(f"   Response: {json.dumps(response.json(), indent=2)}\n")
                except Exception as e:
                    print(f"   ❌ Error: {e}\n")
                
                # Test 6: Database health
                print(f"6️⃣  Testing GET /api/v1/conversations/db-health...")
                try:
                    response = await client.get(
                        f"{BASE_URL}/api/v1/conversations/db-health"
                    )
                    print(f"   ✅ Status: {response.status_code}")
                    print(f"   Response: {response.json()}\n")
                except Exception as e:
                    print(f"   ❌ Error: {e}\n")
        except Exception as e:
            print(f"   ❌ Error: {e}\n")
        
        # Test CORS preflight
        print("7️⃣  Testing CORS preflight (OPTIONS /api/v1/conversations/start)...")
        try:
            response = await client.options(f"{BASE_URL}/api/v1/conversations/start")
            print(f"   ✅ Status: {response.status_code}")
            print(f"   CORS Headers: {dict(response.headers)}\n")
        except Exception as e:
            print(f"   ❌ Error: {e}\n")

if __name__ == "__main__":
    print("⏳ Make sure the backend is running on http://localhost:8000\n")
    asyncio.run(test_endpoints())

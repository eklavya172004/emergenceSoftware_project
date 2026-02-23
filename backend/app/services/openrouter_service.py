"""Service for interacting with OpenRouter API."""
import httpx
from typing import List, Dict, Optional
import logging
from ..config import settings

logger = logging.getLogger(__name__)

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"


class OpenRouterService:
    """Service to handle OpenRouter API interactions."""
    
    def __init__(self):
        self.api_key = settings.openrouter_api_key
        self.model = settings.openrouter_model
        self.base_url = OPENROUTER_API_URL
        
        if not self.api_key:
            logger.warning("OpenRouter API key not configured")
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 512,
    ) -> Optional[str]:
        """
        Get a chat completion from OpenRouter.
        
        Args:
            messages: List of messages in the conversation
            temperature: Creativity level (0-1)
            max_tokens: Maximum tokens in response
            
        Returns:
            The assistant's response or None if error
        """
        if not self.api_key:
            logger.error("OpenRouter API key is not configured")
            return "Error: API key not configured"
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:3000",
            }
            
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }
            
            logger.info(f"Calling OpenRouter with model: {self.model}")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(self.base_url, json=payload, headers=headers)
                
                logger.info(f"OpenRouter response status: {response.status_code}")
                
                response.raise_for_status()
                
                result = response.json()
                
                if "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"]
                else:
                    logger.error(f"Unexpected response format: {result}")
                    return "Error: Unexpected response format"
                    
        except httpx.TimeoutException:
            logger.error("OpenRouter API request timed out")
            return "Error: Request timed out"
        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
            response_text = e.response.text
            logger.error(f"OpenRouter API error: {status_code} - {response_text}")
            
            if status_code == 401:
                return "Error: Invalid API key"
            elif status_code == 404:
                return f"Error: Model '{self.model}' not found or endpoint unavailable"
            else:
                return f"Error: API returned status {status_code}"
        except Exception as e:
            logger.error(f"Unexpected error in chat_completion: {str(e)}", exc_info=True)
            return f"Error: {str(e)}"
    
    def build_system_prompt(self, resume_context: str) -> str:
        """
        Build a system prompt for the chat model.
        
        Args:
            resume_context: The user's resume information
            
        Returns:
            System prompt string
        """
        return f"""You are an AI assistant acting as a professional representative for a software developer. 
You MUST use ONLY the resume information provided below to answer questions. 

RESUME INFORMATION:
================
{resume_context}
================

INSTRUCTIONS:
1. ONLY answer questions based on the resume provided above
2. If asked about something not in the resume, say: "That information isn't on my resume, but I'd be happy to discuss..."
3. Be specific and accurate - cite exact skills, projects, or experience from the resume
4. Use professional language while being warm and friendly
5. When discussing projects, provide specific details about technologies used and accomplishments
6. Highlight relevant experience when answering technical questions
7. If asked "What can you do?", describe the skills and projects from the resume
8. Keep responses concise but informative (2-4 sentences typically)
9. Ask clarifying questions if someone asks about vague topics (e.g., "Which project are you interested in?")
10. Always reference specific details from the resume when answering

CONVERSATION STYLE:
- Professional but approachable
- Confident about your experience
- Helpful and interested in the conversation
- Focus on how your skills align with the question asked"""


# Create a global instance
openrouter_service = OpenRouterService()

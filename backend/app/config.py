"""Configuration settings for the backend application."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, ConfigDict
from typing import List, Optional
import json


# Default CORS origins
DEFAULT_CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra='ignore',  # Ignore extra fields like CORS_ORIGINS
    )
    
    # API Keys
    openrouter_api_key: str = ""
    openrouter_model: str = "openai/gpt-3.5-turbo"
    
    # Server Configuration
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    debug: bool = False
    
    # Database Configuration
    database_url: str = "sqlite:///./portfolio.db"  # Default to SQLite
    DATABASE_URL: str = "sqlite:///./portfolio.db"  # Uppercase alias for compatibility
    
    # CORS - Store as optional string to avoid JSON parsing issues
    # Manually get from env, don't let pydantic-settings parse it
    cors_origins_str: Optional[str] = Field(
        default=None, 
        exclude=True,  # Don't include in model serialization
    )
    
    def __init__(self, **data):
        """Custom init to handle CORS_ORIGINS from env."""
        import os
        # Get CORS_ORIGINS directly from environment if present
        cors_env = os.getenv('CORS_ORIGINS') or os.getenv('cors_origins')
        if cors_env:
            data['cors_origins_str'] = cors_env
        elif 'cors_origins_str' not in data:
            data['cors_origins_str'] = None
        super().__init__(**data)
    
    def get_cors_origins(self) -> List[str]:
        """Get CORS origins, parsing from string if needed."""
        if not self.cors_origins_str:
            return DEFAULT_CORS_ORIGINS
        try:
            parsed = json.loads(self.cors_origins_str)
            return parsed if isinstance(parsed, list) else DEFAULT_CORS_ORIGINS
        except (json.JSONDecodeError, ValueError, TypeError):
            return DEFAULT_CORS_ORIGINS
    
    @property
    def cors_origins(self) -> List[str]:
        """Property for backward compatibility."""
        return self.get_cors_origins()
    
    # Resume Context
    resume_context: str = """
PROFESSIONAL SUMMARY
I am a passionate full-stack software developer with expertise in building modern web applications. I create engaging user interfaces and robust backend systems.

TECHNICAL SKILLS
Frontend Skills:
- React, TypeScript, Next.js, HTML/CSS, Tailwind CSS
- State management (Redux, Context API)
- Responsive design and UI/UX principles

Backend Skills:
- Python, FastAPI, Node.js, Express
- REST APIs, database design, authentication
- Asynchronous programming

Databases & Tools:
- PostgreSQL, MongoDB, SQLite
- Docker, Git, Linux/Unix

DevOps & Infrastructure:
- Docker containerization
- Basic Kubernetes deployment
- CI/CD pipelines

EXPERIENCE
Senior Full-Stack Developer (2022 - Present)
- Built scalable web applications using React and FastAPI
- Led API development and database optimization
- Mentored junior developers on best practices

Full-Stack Developer (2020 - 2022)
- Developed responsive web applications
- Created RESTful APIs serving 10k+ users
- Implemented authentication and security features

PROJECTS
1. AI Portfolio Assistant - Chat interface for resume interaction (React, FastAPI, OpenRouter AI)
2. Task Management App - Collaborative task tracker (React, Node.js, MongoDB)
3. E-commerce Platform - Full-featured online store (Next.js, PostgreSQL, Stripe API)

EDUCATION
Bachelor's Degree in Computer Science (or equivalent)
Relevant certifications and continuous learning in modern technologies

INTERESTS
Open source contributing, AI/ML applications, system design, cloud architecture
"""

settings = Settings()

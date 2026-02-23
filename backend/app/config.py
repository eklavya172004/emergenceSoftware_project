"""Configuration settings for the backend application."""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
import json


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
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
    
    # CORS - Parse from JSON string if provided, otherwise use defaults
    cors_origins: List[str] = Field(default_factory=lambda: [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ])
    
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
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

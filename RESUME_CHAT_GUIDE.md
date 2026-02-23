# Resume Chat Functionality Guide

## ✅ What You Now Have

Your chat application can now:
- ✅ Ask questions about your resume and experience
- ✅ Get accurate responses based on your professional background
- ✅ Dynamically update your resume content without restarting
- ✅ Support multi-turn conversations about your skills and projects

## 📝 Customizing Your Resume

### Method 1: Direct API Call (Recommended)

Update your resume content using a POST request:

```bash
curl -X POST "http://localhost:8000/api/v1/chat/update-resume" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_content": "YOUR FULL RESUME HERE"
  }'
```

### Method 2: Edit .env File

Edit `backend/.env` and update the `RESUME_CONTEXT` variable, then restart the server.

### Method 3: Retrieve Current Resume

See what resume content is currently loaded:

```bash
curl "http://localhost:8000/api/v1/chat/resume"
```

## 📋 Resume Template

Use this structure for best results:

```
PROFESSIONAL SUMMARY
[2-3 sentences about yourself]

TECHNICAL SKILLS
Frontend: [list your skills]
Backend: [list your skills]
Databases: [list your skills]
Tools & Platforms: [list your skills]

EXPERIENCE
[Job Title] (YYYY - YYYY)
- Key accomplishment 1
- Key accomplishment 2
- Key metric or impact

[Previous Job Title] (YYYY - YYYY)
- Key accomplishment
- Technology stack used

PROJECTS
1. [Project Name] - [Brief description] (Tech stack)
2. [Project Name] - [Brief description] (Tech stack)

EDUCATION
[Degree] in [Field]

INTERESTS
[Your interests and areas of focus]
```

## 🤖 Example Questions Users Can Ask

1. "What are your main technical skills?"
2. "What projects have you worked on?"
3. "Tell me about your experience with React"
4. "What databases are you familiar with?"
5. "What was your most recent role?"
6. "Can you work with Python?"
7. "Do you have DevOps experience?"
8. "Describe your experience with full-stack development"

## 🧪 Test Your Setup

1. **Start the backend:**
   ```bash
   cd backend
   python main.py
   ```

2. **Test the resume endpoint:**
   ```bash
   curl "http://localhost:8000/api/v1/chat/resume"
   ```

3. **Open the chat:**
   - Go to http://localhost:3000/chat
   - Enter your name
   - Ask: "What are your technical skills?"

4. **Verify the response:**
   - AI should list skills from your resume
   - Response should be specific and accurate

## 🎯 How It Works

1. **User asks a question** in the chat interface
2. **Frontend sends message** to backend API
3. **Backend retrieves resume context** from settings
4. **System prompt instructs AI** to use ONLY resume information
5. **AI generates response** based on resume
6. **Response sent back** to frontend and displayed

## 📊 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/chat/resume` | Get current resume content |
| POST | `/api/v1/chat/update-resume` | Update resume content |
| POST | `/api/v1/chat/test-openrouter` | Test AI API connection |
| POST | `/api/v1/conversations/start` | Create new conversation |
| POST | `/api/v1/conversations/message-with-history` | Send message with history |
| GET | `/api/v1/conversations/{user_name}` | Get all conversations for user |
| GET | `/api/v1/conversations/conversation/{id}` | Get conversation history |

## 🔄 Update Resume Example

Update your resume with accurate information:

```bash
curl -X POST "http://localhost:8000/api/v1/chat/update-resume" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_content": "PROFESSIONAL SUMMARY\nI am a full-stack developer with 5+ years of experience building web applications.\n\nTECHNICAL SKILLS\nFrontend: React, Next.js, TypeScript, Tailwind CSS\nBackend: Python, FastAPI, Node.js, Express\nDatabases: PostgreSQL, MongoDB, Redis\nDevOps: Docker, GitHub Actions, AWS EC2\n\nEXPERIENCE\nSenior Full-Stack Developer (2021 - Present)\n- Led development of 10+ production applications\n- Mentored 5 junior developers\n- Improved API performance by 40%\n\nPROJECTS\n1. AI Portfolio Chat - Interactive resume assistant (React, FastAPI, OpenRouter AI)\n2. Task Management Platform - Team collaboration tool (Next.js, PostgreSQL)\n3. E-commerce Store - Full-featured online platform (React, Node.js, Stripe)\n\nEDUCATION\nBachelor of Science in Computer Science"
  }'
```

## 💡 Tips

1. **Be specific** - Include actual project names, technologies, and achievements
2. **Use metrics** - Add numbers: "Improved performance by 30%", "Served 10k+ users"
3. **Update regularly** - Keep your resume current as you learn new skills
4. **Test thoroughly** - Ask various questions to ensure AI responds correctly
5. **Keep it concise** - AI responds better to well-organized, clear information

## ❓ Troubleshooting

### AI responses are generic or inaccurate
- Make sure your resume content is detailed and specific
- Try updating it with better formatted information
- Test with: `curl "http://localhost:8000/api/v1/chat/resume"`

### "That information isn't on my resume" responses
- The AI only uses your resume content
- You need to add that information to your resume
- Use `/api/v1/chat/update-resume` to add it

### Chat not responding
- Check backend is running: `http://localhost:8000/health`
- Verify API key is configured correctly
- Test with: `curl http://localhost:8000/api/v1/chat/test-openrouter`

---

**Your chat is now ready to provide accurate, resume-based responses!** 🚀

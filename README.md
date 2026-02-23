# 🚀 AI Portfolio Chat Application

A modern, full-stack AI-powered portfolio website with an interactive chat assistant that answers questions about your resume, skills, and projects using OpenRouter AI.

![Status](https://img.shields.io/badge/status-production%20ready-brightgreen)
![Next.js](https://img.shields.io/badge/Next.js-15.4-blue)
![Python](https://img.shields.io/badge/Python-3.11-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-teal)

---

## ✨ Features

- **🤖 AI Chat Assistant** - Ask questions about resume, skills, and projects
- **💬 Conversation History** - Track all previous conversations
- **📱 Responsive Design** - Works beautifully on all devices
- **🎨 Modern UI** - Gradient effects, animations, and emojis
- **📧 Contact Form** - Direct email integration
- **📥 Resume Download** - One-click PDF download
- **🔗 Social Links** - GitHub, LinkedIn, LeetCode integration
- **☁️ Production Ready** - Docker, automated deployment, security headers

---

## 🛠️ Tech Stack

### Frontend
- **Framework:** Next.js 15.4 (React 19)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Animations:** Framer Motion, React Type Animation
- **UI Components:** Heroicons, React Social Icons
- **Notifications:** Custom Toast System

### Backend
- **Framework:** FastAPI (Python 3.11)
- **Database:** SQLite (dev) / PostgreSQL (production)
- **ORM:** SQLAlchemy
- **AI:** OpenRouter API (GPT-3.5-Turbo)
- **HTTP Client:** httpx
- **Server:** Uvicorn

---

## 📋 Prerequisites

- Node.js 18+ and npm/yarn/pnpm
- Python 3.11+
- OpenRouter API key (free at https://openrouter.ai)

---

## ⚡ Quick Start

### 1. Clone & Setup Frontend
```bash
# Clone repository
git clone <your-repo>
cd portfolio

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Update .env.local with your backend URL
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Run development server
npm run dev
# Open http://localhost:3000
```

### 2. Setup Backend
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Update .env with your OpenRouter API key
OPENROUTER_API_KEY=your_key_here

# Run development server
python -m uvicorn app.main:app --reload
# API available at http://localhost:8000
```

---

## 📚 Project Structure

```
portfolio/
├── app/                         # Frontend (Next.js)
│   ├── components/              # React components
│   │   ├── Chat.tsx            # Chat interface
│   │   ├── Hero.tsx            # Hero section
│   │   ├── About.tsx           # About section
│   │   ├── Project.tsx         # Projects showcase
│   │   ├── Experience.tsx      # Work experience
│   │   ├── EmailSection.tsx    # Contact form
│   │   ├── Toast.tsx           # Notifications
│   │   └── ...
│   ├── lib/                     # Utilities
│   │   └── api.ts              # API client
│   ├── constants/               # Constants
│   │   └── index.ts            # Skills, experiences, projects
│   ├── globals.css              # Global styles
│   └── page.tsx                 # Home page
│
├── backend/                     # Backend (FastAPI)
│   ├── app/
│   │   ├── main.py             # Application entry point
│   │   ├── config.py           # Configuration & resume
│   │   ├── database.py         # Database setup
│   │   ├── api/
│   │   │   ├── chat.py         # Chat endpoints
│   │   │   └── database.py     # Conversation endpoints
│   │   ├── models/
│   │   │   └── db/
│   │   │       └── models.py   # Database schemas
│   │   └── services/
│   │       └── openrouter_service.py  # AI integration
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example             # Environment template
│   └── README.md                # Backend setup guide
│
├── public/                      # Static assets
│   ├── images/                  # Project images
│   └── assets/                  # Tech icons
│
├── package.json                 # Frontend dependencies
├── tsconfig.json                # TypeScript config
├── tailwind.config.ts           # Tailwind config
├── next.config.mjs              # Next.js config
├── Dockerfile.frontend          # Frontend Docker image
├── Dockerfile.backend           # Backend Docker image
├── docker-compose.yml           # Multi-container setup
├── .env.example                 # Frontend .env template
├── DEPLOYMENT.md                # Detailed deployment guide
├── PRODUCTION_CHECKLIST.md      # Pre-deployment checklist
└── QUICK_START_DEPLOYMENT.md    # Quick deployment guide
```

---

## 🌐 API Endpoints

### Chat Endpoints
- `POST /api/v1/chat/message` - Send a simple message
- `POST /api/v1/chat/test-openrouter` - Test OpenRouter connection
- `GET /api/v1/chat/resume` - Get current resume context
- `POST /api/v1/chat/update-resume` - Update resume context

### Conversation Endpoints
- `POST /api/v1/conversations/start` - Create new conversation
- `POST /api/v1/conversations/message-with-history` - Send message with history
- `GET /api/v1/conversations/{user_name}` - Get user conversations
- `GET /api/v1/conversations/conversation/{id}` - Get conversation details
- `DELETE /api/v1/conversations/conversation/{id}` - Delete conversation
- `GET /api/v1/conversations/db-health` - Health check

---

## 📦 Development Commands

### Frontend
```bash
npm run dev         # Development server (localhost:3000)
npm run build       # Production build
npm run start       # Start production server
npm run lint        # Run ESLint
```

### Backend
```bash
python -m uvicorn app.main:app --reload    # Dev server
python -m uvicorn app.main:app              # Production server
python update_resume.py                     # Update resume in AI
```

---

## 🐳 Docker Deployment

### Local Testing with Docker Compose
```bash
# Set your OpenRouter API key
export OPENROUTER_API_KEY=your_key_here

# Build and run all services
docker-compose up --build

# Access:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# Database: localhost:5432
```

### Build Individual Images
```bash
# Frontend
docker build -f Dockerfile.frontend -t portfolio-frontend .

# Backend
docker build -f Dockerfile.backend -t portfolio-backend .
```

---

## ☁️ Production Deployment

### Deployments Platforms Tested
- ✅ **Vercel** (Frontend) - Free tier available
- ✅ **Railway** (Backend) - $5/month starter plan
- ✅ **Heroku** (Backend) - Alternative option
- ✅ **Self-hosted** (Docker) - Any VPS or cloud provider

### Quick Deploy
**See `QUICK_START_DEPLOYMENT.md` for 3-step deployment guide!**

For detailed instructions, see:
- `DEPLOYMENT.md` - Complete deployment guide
- `PRODUCTION_CHECKLIST.md` - Pre-deployment checklist

---

## 🔐 Environment Variables

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### Backend (.env)
```env
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=openai/gpt-3.5-turbo
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=False
DATABASE_URL=sqlite:///./portfolio.db
CORS_ORIGINS=["http://localhost:3000"]
```

---

## 🚀 Production Checklist

Before deploying to production, complete the `PRODUCTION_CHECKLIST.md`:
- [ ] Code quality checks
- [ ] Environment configuration
- [ ] Security hardening
- [ ] Performance optimization
- [ ] Monitoring setup
- [ ] And more...

---

## 📸 Features Demo

### Hero Section
- Animated name with type-effect
- Gradient text and buttons
- Resume download button
- Floating chat bot

### Chat Page
- Real-time AI responses
- Conversation history with timestamps
- Question previews in sidebar
- Toast notifications
- Beautiful dark theme

### Projects Showcase
- Filter by category (All, Frontend, Fullstack)
- Project images and descriptions
- Links to live demos and source code
- Responsive grid layout

### Experience Timeline
- Work experience cards
- Technologies used
- Achievement highlights

### Contact Form
- Email integration
- Form validation
- Success toast notifications
- Direct email client opening

---

## 🐛 Troubleshooting

### Frontend Issues
- **API 500 errors** → Check backend logs and OPENROUTER_API_KEY
- **Chat not working** → Verify NEXT_PUBLIC_API_URL environment variable
- **Images not loading** → Check image paths in `/public/images`
- **Styling issues** → Run `npm install` to ensure Tailwind is properly installed

### Backend Issues
- **Database errors** → Ensure database file/connection is writable
- **API 401 errors** → Check OPENROUTER_API_KEY validity
- **CORS errors** → Update CORS_ORIGINS in .env
- **Port already in use** → Change SERVER_PORT in .env

---

## 📝 Customization

### Update Your Information
1. **Resume Content:** `/backend/app/config.py` → `resume_context`
2. **Skills & Tech:** `/app/constants/index.ts` → `services`, `technologies`
3. **Work Experience:** `/app/constants/index.ts` → `experiences`
4. **Projects:** `/app/constants/index.ts` → `projects`
5. **Social Links:** `/app/components/EmailSection.tsx` → Update URLs
6. **Hero Image:** Replace `/public/images/hero-image-01.png`
7. **Project Images:** Update `/public/images/` with your screenshots

---

## 📄 License

This project is open source and available under the MIT License.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## 📧 Contact

Have questions or suggestions? Reach out:
- **Email:** eklavyanath172004@gmail.com
- **GitHub:** https://github.com/eklavya172004
- **LinkedIn:** https://www.linkedin.com/in/eklavya-nath-506818286/
- **LeetCode:** https://leetcode.com/u/eklavya172004/

---

## 🙏 Acknowledgments

- [Next.js](https://nextjs.org) - React framework
- [Tailwind CSS](https://tailwindcss.com) - Utility CSS framework
- [FastAPI](https://fastapi.tiangolo.com) - Python API framework
- [OpenRouter](https://openrouter.ai) - AI API aggregator
- [Vercel](https://vercel.com) - Frontend hosting
- [Railway](https://railway.app) - Backend hosting

---

**Made with ❤️ by Eklavya Nath**

**Status:** ✅ Production Ready | 🚀 Ready to Deploy | 📈 Scalable

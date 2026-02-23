# 🚀 Deployment Guide

This guide will help you deploy your AI Portfolio Chat application to production.

## Table of Contents
- [Frontend Deployment](#frontend-deployment)
- [Backend Deployment](#backend-deployment)
- [Database Setup](#database-setup)
- [Environment Variables](#environment-variables)
- [Pre-Deployment Checklist](#pre-deployment-checklist)

---

## Frontend Deployment

### Option 1: Vercel (Recommended for Next.js)

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Vercel**
   - Go to https://vercel.com
   - Click "New Project"
   - Import your GitHub repository
   - Set environment variables in Vercel dashboard:
     - `NEXT_PUBLIC_API_URL` = Your backend API URL

3. **Configure Custom Domain** (optional)
   - In Vercel settings, add your custom domain

### Option 2: Docker Deployment

1. **Create Dockerfile**
   ```dockerfile
   FROM node:20-alpine AS builder
   WORKDIR /app
   COPY package*.json ./
   RUN npm ci
   COPY . .
   RUN npm run build

   FROM node:20-alpine
   WORKDIR /app
   COPY package*.json ./
   RUN npm ci --only=production
   COPY --from=builder /app/.next ./.next
   COPY --from=builder /app/public ./public

   EXPOSE 3000
   CMD ["npm", "start"]
   ```

2. **Build and Run**
   ```bash
   docker build -t portfolio-frontend .
   docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=your_api_url portfolio-frontend
   ```

---

## Backend Deployment

### Option 1: DigitalOcean / AWS / Heroku

1. **Install gunicorn** (for production ASGI server)
   ```bash
   pip install gunicorn
   ```

2. **Update requirements.txt**
   ```bash
   pip freeze > requirements.txt
   ```

3. **Create Procfile** (for Heroku):
   ```
   web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
   ```

4. **Deploy using CLI or Git push**

### Option 2: Docker Deployment

1. **Create Dockerfile** for backend:
   ```dockerfile
   FROM python:3.11-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt

   COPY app/ ./app/
   COPY .env .env

   EXPOSE 8000

   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Build and Run**
   ```bash
   docker build -t portfolio-backend .
   docker run -p 8000:8000 --env-file .env portfolio-backend
   ```

### Option 3: Railway / Render

1. Go to https://railway.app or https://render.com
2. Connect your GitHub repository
3. Select "Python" as runtime
4. Set environment variables
5. Deploy automatically on push

---

## Database Setup

### For Production (PostgreSQL Recommended)

1. **Install PostgreSQL**
   - Local: `brew install postgresql` (macOS) or `apt install postgresql` (Linux)
   - Cloud: Use managed services (AWS RDS, DigitalOcean, Heroku Postgres)

2. **Create Database**
   ```bash
   createdb portfolio_prod
   ```

3. **Update `.env` with PostgreSQL URL**
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/portfolio_prod
   ```

4. **Run Migrations**
   ```bash
   cd backend
   alembic upgrade head
   ```

---

## Environment Variables

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=https://your-backend-domain.com/api/v1
```

### Backend (.env)
```
OPENROUTER_API_KEY=your_actual_api_key
OPENROUTER_MODEL=openai/gpt-3.5-turbo
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=False
DATABASE_URL=postgresql://user:password@host:5432/portfolio_prod
CORS_ORIGINS=["https://yourdomain.com","https://www.yourdomain.com"]
```

---

## Pre-Deployment Checklist

### Frontend
- [ ] Update `NEXT_PUBLIC_API_URL` to production backend URL
- [ ] Remove all console.log() and debug statements
- [ ] Test production build locally: `npm run build && npm run start`
- [ ] Verify all images are optimized
- [ ] Check responsive design on mobile devices
- [ ] Test all navigation links
- [ ] Verify email functionality with real email address
- [ ] Test chat feature with real backend

### Backend
- [ ] Set `DEBUG=False` in production
- [ ] Update `CORS_ORIGINS` with production domain
- [ ] Update `OPENROUTER_API_KEY` with valid key
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set secure database password
- [ ] Run database migrations: `alembic upgrade head`
- [ ] Test all API endpoints
- [ ] Set up proper logging (not stdout)
- [ ] Enable SSL/HTTPS
- [ ] Set up automated backups for database

### General
- [ ] Set up domain name
- [ ] Configure SSL certificate (use Let's Encrypt)
- [ ] Set up monitoring and error tracking (Sentry)
- [ ] Configure CDN for static assets (Cloudflare)
- [ ] Set up backups and disaster recovery
- [ ] Document deployment process
- [ ] Set up CI/CD pipeline

---

## Quick Start: Deploy with Vercel + Railway

### Frontend (Vercel)
1. `git push` to GitHub
2. Go to vercel.com → Import project
3. Set `NEXT_PUBLIC_API_URL` environment variable
4. Deploy

### Backend (Railway)
1. Go to railway.app → New Project
2. Connect GitHub repository (or paste backend code)
3. Set environment variables in Railway dashboard
4. Deploy automatically

---

## Production URLs

After deployment, your URLs will be:
- Frontend: `https://yourname-portfolio.vercel.app` (or custom domain)
- Backend: `https://yourname-portfolio-api.railway.app` (or custom domain)

Update the frontend's `NEXT_PUBLIC_API_URL` to point to your backend!

---

## Support

For issues or questions:
- Check logs: `docker logs container_name`
- Monitor errors: Set up Sentry for error tracking
- Database issues: Check database connection string
- API issues: Verify OPENROUTER_API_KEY is valid

Happy deploying! 🎉

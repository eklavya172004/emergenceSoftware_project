# 🚀 Quick Start Deployment Guide

Follow these 3 simple steps to deploy your portfolio to production:

## Step 1: Frontend Deployment (Vercel)

```bash
cd portfolio
npm i -g vercel
vercel --prod
```

**Setup in Vercel:**
1. Set environment variable: `NEXT_PUBLIC_API_URL` = `https://your-backend-url.com/api/v1`
2. Your frontend is live! ✓

**Pro Tip:** Get a free domain with Vercel and connect it in settings.

---

## Step 2: Backend Deployment (Railway)

```bash
# Go to railway.app
# Click "New Project" → "Deploy from GitHub"
# Select your repository
# Add environment variables:
```

**Add these in Railway:**
```
OPENROUTER_API_KEY=your_actual_key
OPENROUTER_MODEL=openai/gpt-3.5-turbo
DATABASE_URL=postgresql://user:password@host:5432/portfolio_prod
DEBUG=False
CORS_ORIGINS=["https://yourdomain.com"]
```

**Railway will automatically:**
- Detect Python app
- Install dependencies
- Run your FastAPI server
- Provide you a public URL

---

## Step 3: Connect Frontend to Backend

1. **Get your backend URL from Railway** (looks like: `https://xxx-xxx-xxx.up.railway.app`)
2. **Update Vercel environment variable:**
   - Go to Vercel → Project Settings → Environment Variables
   - Set `NEXT_PUBLIC_API_URL` = Your Railway backend URL + `/api/v1`
   - Redeploy by pushing to GitHub

3. **Test your app:**
   - Go to your Vercel domain
   - Try the chat feature
   - Submit contact form

---

## Alternative: Docker Deployment

If you prefer Docker:

```bash
# Build
docker build -f Dockerfile.frontend -t portfolio-frontend .
docker build -f Dockerfile.backend -t portfolio-backend .

# Deploy to Docker Hub or any platform (AWS, GCP, etc.)
docker push portfolio-frontend
docker push portfolio-backend
```

---

## Cost Estimate

- **Vercel (Frontend):** Free tier available
- **Railway (Backend):** $5/month or less
- **PostgreSQL:** Free tier for small projects
- **Total:** $0-10/month for hobby projects

---

## Final Checklist Before Going Live

```bash
# 1. Test production build locally
npm run build
npm run start

# 2. Run backend in production mode
DEBUG=False python -m uvicorn app.main:app --host 0.0.0.0

# 3. Verify all environment variables are set
# 4. Update contact email if needed
# 5. Test chat feature
# 6. Test contact form
```

---

## Your Production URLs

After deployment:
- **Frontend:** `https://your-vercel-domain.vercel.app`
- **Backend:** `https://your-railway-domain.up.railway.app`
- **API:** `https://your-railway-domain.up.railway.app/api/v1`

---

## Need Help?

1. Check `DEPLOYMENT.md` for detailed instructions
2. See `PRODUCTION_CHECKLIST.md` for complete checklist
3. Check logs:
   - Vercel: Project Settings → Logs
   - Railway: Deployments → View Logs

---

**That's it! Your portfolio is live! 🎉**

Next steps:
- [ ] Monitor application
- [ ] Set up error tracking (Sentry)
- [ ] Configure domain name
- [ ] Set up SSL certificate
- [ ] Monitor performance

# Deployment Guide for Bid Bazaar

This guide will help you deploy the Bid Bazaar application to Vercel.

## Project Structure

- **Frontend**: React + Vite application in `bid-bazaar-frontend/`
- **Backend**: Flask application in `bid-bazaar-backend/`

## Prerequisites

1. Node.js 18+ installed
2. Python 3.8+ installed
3. Vercel account (free tier works)
4. Git repository

## Frontend Deployment (Vercel)

### Step 1: Prepare Frontend

1. Navigate to the frontend directory:
```bash
cd bid-bazaar-frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env` file (or set environment variables in Vercel):
```env
VITE_API_BASE_URL=https://your-backend-url.com
```

### Step 2: Deploy to Vercel

#### Option A: Using Vercel CLI

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Deploy:
```bash
cd bid-bazaar-frontend
vercel
```

4. Follow the prompts and set environment variables when asked.

#### Option B: Using Vercel Dashboard

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "New Project"
3. Import your Git repository
4. Set the root directory to `bid-bazaar-frontend`
5. Configure build settings:
   - Framework Preset: Vite
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`
6. Add environment variable:
   - Key: `VITE_API_BASE_URL`
   - Value: Your backend URL (e.g., `https://your-backend.railway.app`)
7. Click "Deploy"

### Step 3: Update CORS Settings

After deployment, update your backend CORS settings to include your Vercel frontend URL:

```python
CORS(app, origins=[
    "http://localhost:5173",
    "http://localhost:3000",
    "https://your-app.vercel.app"  # Add your Vercel URL
], supports_credentials=True)
```

## Backend Deployment

**Note**: Vercel's serverless functions have limitations with Flask-SocketIO. For the backend, consider these alternatives:

### Option 1: Railway (Recommended)

1. Go to [railway.app](https://railway.app)
2. Create a new project
3. Connect your Git repository
4. Select the `bid-bazaar-backend` directory
5. Railway will auto-detect Python
6. Set environment variables:
   - `SECRET_KEY`: Generate a secure random key
   - `DATABASE_URL`: Railway provides PostgreSQL automatically
   - `FLASK_ENV`: `production`
7. Deploy

### Option 2: Render

1. Go to [render.com](https://render.com)
2. Create a new Web Service
3. Connect your repository
4. Set:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
   - Environment: Python 3
5. Add environment variables
6. Deploy

### Option 3: Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Set environment variables:
```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DATABASE_URL=your-database-url
```
5. Deploy: `git push heroku main`

## Environment Variables

### Frontend (.env)
```env
VITE_API_BASE_URL=https://your-backend-url.com
```

### Backend
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@host:port/dbname
FLASK_ENV=production
FLASK_DEBUG=False
```

## Database Setup

### For Production (PostgreSQL)

1. Create a PostgreSQL database (Railway, Render, or Supabase provide free tiers)
2. Update `DATABASE_URL` in backend environment variables
3. The app will automatically create tables on first run

### For Development (SQLite)

SQLite is used by default. No additional setup needed.

## Post-Deployment Checklist

- [ ] Frontend deployed to Vercel
- [ ] Backend deployed to Railway/Render/Heroku
- [ ] Environment variables configured
- [ ] CORS settings updated in backend
- [ ] Database connected and tables created
- [ ] Test user registration
- [ ] Test auction creation
- [ ] Test bidding functionality

## Troubleshooting

### Frontend Issues

**Build fails:**
- Check Node.js version (should be 18+)
- Clear `node_modules` and reinstall
- Check for TypeScript/ESLint errors

**API calls fail:**
- Verify `VITE_API_BASE_URL` is set correctly
- Check CORS settings in backend
- Verify backend is running and accessible

### Backend Issues

**Database connection fails:**
- Verify `DATABASE_URL` is correct
- Check database is accessible from deployment platform
- Ensure database user has proper permissions

**SocketIO not working:**
- Vercel serverless functions don't support WebSocket
- Consider using a separate service for real-time features
- Or use polling as fallback

## Support

For issues or questions, check:
- Backend documentation: `BACKEND_DOCUMENTATION.md`
- Frontend README: `bid-bazaar-frontend/README.md`


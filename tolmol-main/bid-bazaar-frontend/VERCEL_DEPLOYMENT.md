# Vercel Deployment Guide

This guide will help you deploy the Bid Bazaar frontend to Vercel.

## Prerequisites

1. A Vercel account (sign up at [vercel.com](https://vercel.com))
2. Your code pushed to a Git repository (GitHub, GitLab, or Bitbucket)
3. Backend deployed and accessible (Railway, Render, or Heroku)

## Step-by-Step Deployment

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. **Go to Vercel Dashboard**
   - Visit [vercel.com](https://vercel.com) and sign in
   - Click "Add New..." → "Project"

2. **Import Your Repository**
   - Connect your Git provider (GitHub, GitLab, or Bitbucket)
   - Select your repository
   - Click "Import"

3. **Configure Project Settings**
   - **Root Directory**: `bid-bazaar-frontend`
   - **Framework Preset**: Vite (auto-detected)
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `dist` (auto-detected)
   - **Install Command**: `npm install` (auto-detected)

4. **Set Environment Variables**
   - Click "Environment Variables"
   - Add the following:
     ```
     VITE_API_BASE_URL=https://your-backend-url.railway.app
     ```
   - Replace with your actual backend URL
   - Make sure to add it for all environments (Production, Preview, Development)

5. **Deploy**
   - Click "Deploy"
   - Wait for the build to complete
   - Your site will be live at `https://your-project.vercel.app`

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Navigate to Frontend Directory**
   ```bash
   cd bid-bazaar-frontend
   ```

4. **Deploy**
   ```bash
   vercel
   ```
   - Follow the prompts
   - When asked for environment variables, add:
     ```
     VITE_API_BASE_URL=https://your-backend-url.railway.app
     ```

5. **Deploy to Production**
   ```bash
   vercel --prod
   ```

## Environment Variables

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Your backend API URL | `https://bid-bazaar-backend.railway.app` |

### Setting Environment Variables in Vercel

1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add each variable for the appropriate environments:
   - **Production**: Live site
   - **Preview**: Preview deployments
   - **Development**: Local development

## Post-Deployment Checklist

- [ ] Frontend deployed successfully
- [ ] Environment variables configured
- [ ] Backend CORS updated with Vercel URL
- [ ] Test user registration
- [ ] Test user login
- [ ] Test viewing auctions
- [ ] Test search and filters
- [ ] Test placing bids (requires login)
- [ ] Check browser console for errors
- [ ] Test on mobile devices

## Updating Backend CORS

After deploying to Vercel, update your backend CORS settings:

1. **Get your Vercel URL**: `https://your-project.vercel.app`

2. **Update backend environment variable**:
   ```env
   FRONTEND_URL=https://your-project.vercel.app
   ```

3. **Or update directly in `app.py`**:
   ```python
   allowed_origins = [
       "http://localhost:5173",
       "http://localhost:3000",
       "https://your-project.vercel.app"  # Add your Vercel URL
   ]
   ```

4. **Redeploy backend** if needed

## Custom Domain (Optional)

1. Go to your project settings in Vercel
2. Click "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions
5. Update `VITE_API_BASE_URL` if needed

## Troubleshooting

### Build Fails

**Issue**: Build command fails
- **Solution**: Check build logs in Vercel dashboard
- Ensure all dependencies are in `package.json`
- Check for TypeScript/ESLint errors

**Issue**: Missing environment variables
- **Solution**: Add `VITE_API_BASE_URL` in Vercel project settings

### API Calls Fail

**Issue**: CORS errors
- **Solution**: Update backend CORS to include Vercel URL

**Issue**: Network errors
- **Solution**: Verify `VITE_API_BASE_URL` is correct
- Check backend is running and accessible
- Test backend URL in browser

### Page Shows Blank

**Issue**: Routing not working
- **Solution**: Verify `vercel.json` has correct rewrites
- Check that `index.html` exists in `dist` folder

### Environment Variables Not Working

**Issue**: Variables not accessible
- **Solution**: 
  - Ensure variables start with `VITE_` prefix
  - Redeploy after adding variables
  - Check variable is set for correct environment

## Performance Optimization

### Already Configured

- ✅ Vite build optimization
- ✅ Code splitting
- ✅ Tree shaking
- ✅ Minification

### Optional Optimizations

1. **Enable Vercel Analytics**
   - Go to project settings
   - Enable Analytics

2. **Enable Edge Functions** (if needed)
   - For server-side rendering or API routes

3. **Image Optimization**
   - Use Vercel's Image Optimization API
   - Or use a CDN for static assets

## Monitoring

1. **Vercel Dashboard**
   - View deployment logs
   - Monitor performance
   - Check error rates

2. **Browser Console**
   - Check for JavaScript errors
   - Monitor network requests
   - Verify API calls

3. **Backend Logs**
   - Monitor backend for errors
   - Check API request logs

## Rollback

If something goes wrong:

1. Go to Vercel dashboard
2. Navigate to "Deployments"
3. Find the last working deployment
4. Click "..." → "Promote to Production"

## Support

- **Vercel Docs**: [vercel.com/docs](https://vercel.com/docs)
- **Vercel Support**: [vercel.com/support](https://vercel.com/support)
- **Project Issues**: Check GitHub issues

## Quick Deploy Checklist

```
□ Code pushed to Git repository
□ Vercel account created
□ Project imported to Vercel
□ Root directory set to `bid-bazaar-frontend`
□ Environment variable `VITE_API_BASE_URL` added
□ Backend deployed and accessible
□ Backend CORS updated with Vercel URL
□ Deployment successful
□ Tested all major features
□ No console errors
```

Your application is now ready for production! 🚀


# Pre-Deployment Checklist

Use this checklist to ensure everything is ready for Vercel deployment.

## ✅ Code Quality

- [x] No linter errors
- [x] All imports are correct
- [x] No console errors (except error handling)
- [x] All components properly exported
- [x] React hooks dependencies fixed

## ✅ Configuration Files

- [x] `package.json` - All dependencies listed
- [x] `vite.config.js` - Properly configured
- [x] `vercel.json` - Deployment configuration
- [x] `.env.example` - Environment variable template
- [x] `.gitignore` - Proper exclusions

## ✅ API Integration

- [x] API service layer created (`src/services/api.js`)
- [x] All endpoints connected
- [x] Error handling implemented
- [x] Environment variable for API URL configured
- [x] CORS settings ready

## ✅ Components

- [x] All components use proper React patterns
- [x] Context providers properly set up
- [x] No missing dependencies
- [x] All routes defined in App.jsx

## ✅ Build Configuration

- [x] Build command: `npm run build`
- [x] Output directory: `dist`
- [x] Framework: Vite
- [x] SPA routing configured in vercel.json

## 🔧 Before Deploying

1. **Test Build Locally**
   ```bash
   cd bid-bazaar-frontend
   npm install
   npm run build
   ```
   - Should complete without errors
   - Check `dist` folder is created

2. **Verify Environment Variables**
   - Create `.env` file with `VITE_API_BASE_URL`
   - Test that API calls work locally

3. **Check Backend**
   - Backend should be deployed and accessible
   - CORS should allow your Vercel domain

4. **Git Repository**
   - All changes committed
   - Code pushed to repository

## 🚀 Deployment Steps

1. Go to [vercel.com](https://vercel.com)
2. Import your Git repository
3. Set root directory to `bid-bazaar-frontend`
4. Add environment variable: `VITE_API_BASE_URL`
5. Deploy!

## 📝 Post-Deployment

- [ ] Test homepage loads
- [ ] Test user registration
- [ ] Test user login
- [ ] Test viewing auctions
- [ ] Test search functionality
- [ ] Test filters
- [ ] Test placing bids
- [ ] Check browser console for errors
- [ ] Test on mobile device
- [ ] Update backend CORS with Vercel URL

## 🐛 Common Issues & Solutions

### Build Fails
- Check Node.js version (should be 18+)
- Clear `node_modules` and reinstall
- Check for TypeScript errors

### API Not Working
- Verify `VITE_API_BASE_URL` is set correctly
- Check backend is running
- Verify CORS settings

### Blank Page
- Check browser console for errors
- Verify `vercel.json` rewrites are correct
- Check that `index.html` exists in build

### Environment Variables Not Working
- Ensure variables start with `VITE_`
- Redeploy after adding variables
- Check variable is set for correct environment

## ✅ Ready to Deploy!

If all items are checked, you're ready to deploy to Vercel!


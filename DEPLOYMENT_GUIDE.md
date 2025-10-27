# 🚀 Deployment Guide - Healthcare Analytics Platform

## Overview
- **Frontend**: Vercel (Free)
- **Backend**: Render (Free tier)
- **Database**: SQLite (included in backend)

---

## 📦 **Part 1: Deploy Backend to Render**

### Step 1: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub (recommended)

### Step 2: Deploy Backend
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `healthcare-analytics-api`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && python -m spacy download en_core_web_sm
     ```
   - **Start Command**: 
     ```bash
     gunicorn app:app
     ```
   - **Instance Type**: `Free`

4. Add Environment Variables:
   - `PYTHON_VERSION` = `3.11.0`

5. Click **"Create Web Service"**

6. Wait 5-10 minutes for deployment

7. **Copy your backend URL**: `https://healthcare-analytics-api-xxxx.onrender.com`

### Step 3: Initialize Database
Once deployed, run these commands in Render Shell:
```bash
python models/database.py
python models/demo_data.py
python train_model.py
```

---

## 🌐 **Part 2: Deploy Frontend to Vercel**

### Step 1: Update API URL
1. Open `frontend/.env.production`
2. Replace with your Render backend URL:
   ```
   VITE_API_URL=https://healthcare-analytics-api-xxxx.onrender.com
   ```

3. Also update `frontend/src/services/api.js` line 3:
   ```javascript
   const API_BASE_URL = import.meta.env.VITE_API_URL || (
     import.meta.env.MODE === 'production' 
       ? 'https://healthcare-analytics-api-xxxx.onrender.com'  // ← Your URL here
       : 'http://localhost:5000'
   )
   ```

### Step 2: Deploy to Vercel
1. Go to https://vercel.com
2. Sign up with GitHub
3. Click **"Add New Project"**
4. Import your GitHub repository
5. Configure:
   - **Framework Preset**: `Vite`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   
6. Add Environment Variable:
   - `VITE_API_URL` = `https://healthcare-analytics-api-xxxx.onrender.com`

7. Click **"Deploy"**

8. Wait 2-3 minutes

9. **Your app is live!** 🎉

---

## ✅ **Part 3: Test Deployment**

1. Visit your Vercel URL: `https://your-app.vercel.app`
2. Go to "Upload Data" page
3. Click "Load Demo Data"
4. Click "Train ML Model"
5. Go to Dashboard - see charts
6. Go to Patients - see list
7. Try Note Analyzer

---

## 🔧 **Troubleshooting**

### Backend Issues

**Problem**: "Application failed to respond"
- **Solution**: Check Render logs, ensure gunicorn is installed

**Problem**: "Module not found"
- **Solution**: Rebuild with `pip install -r requirements.txt`

**Problem**: "spaCy model not found"
- **Solution**: Add to build command: `python -m spacy download en_core_web_sm`

### Frontend Issues

**Problem**: "API calls failing"
- **Solution**: Check CORS settings in backend `app.py`
- **Solution**: Verify API URL in `.env.production`

**Problem**: "404 on refresh"
- **Solution**: Ensure `vercel.json` has rewrites configured

### CORS Issues

If you get CORS errors, update backend `app.py`:
```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['https://your-app.vercel.app'])
```

---

## 🎯 **Quick Deploy Commands**

### Push to GitHub
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Redeploy Frontend (Vercel)
- Automatic on git push
- Or click "Redeploy" in Vercel dashboard

### Redeploy Backend (Render)
- Automatic on git push
- Or click "Manual Deploy" in Render dashboard

---

## 💰 **Cost**

- **Vercel**: FREE (100GB bandwidth/month)
- **Render**: FREE (750 hours/month)
- **Total**: $0/month 🎉

**Note**: Free tier sleeps after 15 mins of inactivity. First request takes 30-60 seconds to wake up.

---

## 🚀 **Alternative: Deploy Backend to Railway**

If Render doesn't work, try Railway:

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub"
4. Select your repo
5. Configure:
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
   - **Start Command**: `gunicorn app:app`
6. Add PORT environment variable (Railway provides this)
7. Deploy!

---

## 📱 **Custom Domain (Optional)**

### Vercel
1. Go to Project Settings → Domains
2. Add your domain
3. Update DNS records as instructed

### Render
1. Go to Settings → Custom Domain
2. Add your domain
3. Update DNS records

---

## 🎉 **You're Live!**

Share your links:
- **Frontend**: `https://your-app.vercel.app`
- **Backend API**: `https://healthcare-analytics-api-xxxx.onrender.com`

**For Hackathon Judges:**
- Include both URLs in your submission
- Test thoroughly before submitting
- Have backup local demo ready

---

## 📊 **Monitoring**

### Vercel Analytics
- Go to your project → Analytics
- See visitor stats, performance

### Render Logs
- Go to your service → Logs
- Monitor API requests, errors

---

## 🔒 **Security Notes**

For production (post-hackathon):
1. Add authentication
2. Use PostgreSQL instead of SQLite
3. Add rate limiting
4. Enable HTTPS only
5. Add API keys
6. Implement proper error handling

---

## 💡 **Tips for Demo**

1. **Warm up the backend** before demo (visit API URL)
2. **Test on mobile** - Vercel works on phones
3. **Share link** with judges - they can try it live!
4. **Have local backup** in case internet fails

---

## 🆘 **Need Help?**

Common issues:
- Backend sleeping? → Visit API URL to wake it
- CORS errors? → Check backend CORS config
- Build failing? → Check Render/Vercel logs
- Database empty? → Run initialization scripts

---

**Good luck with your deployment! 🚀**

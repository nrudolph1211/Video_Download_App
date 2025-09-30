# Deployment Guide - Video Downloader

This guide will help you deploy your video downloader to the web so anyone can access it.

## 🚀 Quick Deployment Options

### Option 1: Railway (Recommended - Free)

1. **Create a GitHub repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YT-DOWNLOAD-APP.git
   git push -u origin main
   ```

2. **Deploy to Railway:**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway will automatically deploy your app
   - You'll get a URL like: `https://your-app-name.railway.app`

### Option 2: Render (Free)

1. **Create a GitHub repository** (same steps as above)

2. **Deploy to Render:**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Use these settings:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT app:app`
   - Click "Create Web Service"
   - You'll get a URL like: `https://your-app-name.onrender.com`

### Option 3: Heroku (Paid after free tier ended)

1. **Install Heroku CLI**
2. **Login and create app:**
   ```bash
   heroku login
   heroku create your-video-downloader-name
   git push heroku main
   ```

## 🌐 Custom Domain Setup

### Railway Custom Domain:
1. In Railway dashboard, go to your project
2. Click "Settings" → "Domains"
3. Add your custom domain
4. Update DNS records as instructed

### Render Custom Domain:
1. In Render dashboard, go to your service
2. Click "Settings" → "Custom Domains"
3. Add your domain
4. Update DNS records as instructed

## 🔧 Environment Variables (Optional)

You can set these in your deployment platform:

- `PORT` - Automatically set by the platform
- `DOWNLOAD_DIR` - Default: `/tmp/downloads` (for cloud deployments)

## 📝 Important Notes

1. **Free Tier Limitations:**
   - Railway: 500 hours/month free
   - Render: Sleeps after 15 minutes of inactivity
   - Files are temporary (deleted when app restarts)

2. **Production Considerations:**
   - Consider upgrading to paid plans for permanent file storage
   - Add error monitoring (Sentry)
   - Set up proper logging
   - Consider rate limiting for public use

3. **Legal Considerations:**
   - Add terms of service
   - Include copyright disclaimers
   - Consider adding download limits per user

## 🎯 Quick Start Commands

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit changes
git commit -m "Ready for deployment"

# Create GitHub repository and push
# (Do this manually on GitHub.com)

# Connect to Railway or Render
# (Follow platform-specific instructions above)
```

## 🚨 Troubleshooting

### Common Issues:

1. **Build fails:**
   - Check that all dependencies are in `requirements.txt`
   - Ensure Python version is compatible

2. **App crashes:**
   - Check logs in deployment platform dashboard
   - Verify PORT environment variable is set

3. **Downloads not working:**
   - yt-dlp needs to be updated regularly
   - Check if platform blocks video downloading

### Update yt-dlp:
Add this to your deployment platform's build command:
```bash
pip install --upgrade yt-dlp
```

## 🔒 Security Considerations

1. **Add rate limiting** to prevent abuse
2. **Implement download quotas** per IP/user
3. **Add CAPTCHA** for public access
4. **Monitor usage** and set up alerts

Your video downloader will be live and accessible to anyone on the web! 🌍

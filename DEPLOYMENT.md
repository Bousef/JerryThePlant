# 🌱 PlantAI API - Free Hosting Deployment Guide

## 🚀 Quick Deploy Options

### **Option 1: Railway (Recommended)**
**Best for**: Production use with persistent storage

1. **Sign up** at [railway.app](https://railway.app)
2. **Connect GitHub** and select your repository
3. **Deploy automatically** - Railway detects Python and deploys
4. **Get your URL** - Your API will be live at `https://your-app.railway.app`

**Pros**: 
- ✅ Persistent file storage
- ✅ Custom domains
- ✅ $5/month credit (usually free)
- ✅ Easy deployment

---

### **Option 2: Render**
**Best for**: Simple deployment

1. **Sign up** at [render.com](https://render.com)
2. **Create New Web Service**
3. **Connect GitHub** repository
4. **Configure**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
5. **Deploy** - Get URL like `https://your-app.onrender.com`

**Pros**: 
- ✅ Simple setup
- ✅ Automatic deployments
- ⚠️ Sleeps after 15min inactivity (cold starts)

---

### **Option 3: PythonAnywhere**
**Best for**: Learning and development

1. **Sign up** at [pythonanywhere.com](https://pythonanywhere.com)
2. **Create Web App** → Flask
3. **Upload files** via Files tab
4. **Configure WSGI** file
5. **Reload** web app

**Pros**: 
- ✅ Python-focused
- ✅ Web-based interface
- ⚠️ Limited CPU seconds on free tier

---

### **Option 4: Fly.io**
**Best for**: Global deployment

1. **Install flyctl**: `curl -L https://fly.io/install.sh | sh`
2. **Sign up**: `fly auth signup`
3. **Initialize**: `fly launch` (creates fly.toml)
4. **Deploy**: `fly deploy`

**Pros**: 
- ✅ Global edge deployment
- ✅ Docker support
- ✅ Good performance

---

## 📋 Pre-Deployment Checklist

- [x] ✅ `requirements.txt` created
- [x] ✅ `Procfile` for Heroku-style platforms
- [x] ✅ `Dockerfile` for container platforms
- [x] ✅ `runtime.txt` for Python version
- [x] ✅ App configured for production (debug=False)
- [x] ✅ Port configuration for hosting platforms

## 🔧 Environment Variables

Most platforms will automatically set `PORT` environment variable. Your app is configured to use it.

## 📁 File Storage Considerations

- **Railway**: ✅ Persistent storage
- **Render**: ⚠️ Ephemeral storage (files lost on restart)
- **PythonAnywhere**: ✅ Persistent storage
- **Fly.io**: ✅ Persistent storage

## 🧪 Testing Your Deployed API

Once deployed, test with:
```bash
curl -X POST -F "image=@test_image.jpg" https://your-app-url.com/upload
```

## 💡 Pro Tips

1. **Start with Railway** - Most reliable for file storage
2. **Use GitHub** - Connect your repo for automatic deployments
3. **Monitor usage** - Free tiers have limits
4. **Add health checks** - Your `/` endpoint serves as a health check
5. **Consider database** - For production, add a database for metadata

## 🆘 Troubleshooting

**Common Issues:**
- **Port errors**: App uses `PORT` environment variable
- **File storage**: Check platform's storage policy
- **Memory limits**: Free tiers have RAM constraints
- **Cold starts**: Some platforms sleep inactive apps

**Need help?** Check platform documentation or community forums.

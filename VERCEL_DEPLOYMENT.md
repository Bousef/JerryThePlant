# 🚀 Deploy PlantAI API to Vercel

## ⚠️ Important: File Storage Limitation

**Vercel's serverless functions don't support persistent local file storage.** Your images will be stored in **Cloudinary** (free tier available) instead of locally.

## 📋 Prerequisites

1. **GitHub Account** (for connecting to Vercel)
2. **Cloudinary Account** (free tier: 25GB storage, 25GB bandwidth/month)
3. **Vercel Account** (free tier available)

## 🔧 Step 1: Set Up Cloudinary

1. **Sign up** at [cloudinary.com](https://cloudinary.com)
2. **Get your credentials** from the Dashboard:
   - Cloud Name
   - API Key  
   - API Secret
3. **Keep these handy** - you'll need them for Vercel

## 🚀 Step 2: Deploy to Vercel

### Option A: GitHub Integration (Recommended)

1. **Push your code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "PlantAI API for Vercel"
   git branch -M main
   git remote add origin https://github.com/yourusername/plantai-api.git
   git push -u origin main
   ```

2. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your GitHub repository
   - Vercel will auto-detect Python

3. **Configure Environment Variables**:
   - In Vercel dashboard → Settings → Environment Variables
   - Add these variables:
     ```
     CLOUDINARY_CLOUD_NAME = your_cloud_name
     CLOUDINARY_API_KEY = your_api_key
     CLOUDINARY_API_SECRET = your_api_secret
     ```

4. **Deploy**:
   - Click "Deploy"
   - Your API will be live at `https://your-project.vercel.app`

### Option B: Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login and Deploy**:
   ```bash
   vercel login
   vercel
   ```

3. **Set Environment Variables**:
   ```bash
   vercel env add CLOUDINARY_CLOUD_NAME
   vercel env add CLOUDINARY_API_KEY  
   vercel env add CLOUDINARY_API_SECRET
   ```

## 📁 File Structure for Vercel

```
plantai-api/
├── app_vercel.py          # Main Flask app
├── vercel.json            # Vercel configuration
├── requirements_vercel.txt # Dependencies
└── README.md
```

## 🧪 Testing Your Deployed API

```bash
# Test home endpoint
curl https://your-project.vercel.app/

# Test upload
curl -X POST -F "image=@test_image.jpg" https://your-project.vercel.app/upload
```

## 📊 Vercel vs Local Storage Comparison

| Feature | Local Storage | Vercel + Cloudinary |
|---------|---------------|---------------------|
| **File Persistence** | ✅ Permanent | ✅ Permanent |
| **Scalability** | ❌ Limited | ✅ Unlimited |
| **Global CDN** | ❌ No | ✅ Yes |
| **Backup** | ❌ Manual | ✅ Automatic |
| **Cost** | ✅ Free | ✅ Free tier |
| **Setup** | ✅ Simple | ⚠️ More complex |

## 🎯 API Response Format

```json
{
  "success": true,
  "message": "Image uploaded successfully",
  "image_id": "123e4567-e89b-12d3-a456-426614174000",
  "image_url": "https://res.cloudinary.com/your-cloud/image/upload/v1234567890/plantai_20241201_143022_a1b2c3d4.jpg",
  "public_id": "plantai_20241201_143022_a1b2c3d4",
  "original_filename": "plant.jpg",
  "file_size": 245760,
  "upload_timestamp": "2024-12-01T14:30:22.123456",
  "storage": "cloudinary"
}
```

## 💡 Benefits of Vercel + Cloudinary

- ✅ **Global CDN**: Images served from edge locations worldwide
- ✅ **Automatic optimization**: Cloudinary optimizes images automatically
- ✅ **Transformations**: Resize, crop, filter images on-the-fly
- ✅ **Unlimited scaling**: Handle any amount of traffic
- ✅ **Free tier**: 25GB storage + 25GB bandwidth/month
- ✅ **Automatic backups**: Your images are safe

## 🆘 Troubleshooting

**Common Issues:**

1. **Environment Variables**: Make sure all Cloudinary credentials are set
2. **File Size**: Vercel has a 4.5MB request limit (your app limits to 16MB)
3. **Cold Starts**: First request might be slower (serverless nature)

**Need Help?**
- [Vercel Documentation](https://vercel.com/docs)
- [Cloudinary Documentation](https://cloudinary.com/documentation)

## 🎉 You're Done!

Your PlantAI API is now hosted globally with enterprise-grade image storage! 🌱

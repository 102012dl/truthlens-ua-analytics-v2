# TruthLens UA Analytics - Render Deployment

## 🚀 Deploy on Render (Recommended)

### Step 1: Connect GitHub
1. Go to [render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect: https://github.com/102012dl/truthlens-ua-analytics

### Step 2: Configure Service
- **Name**: truthlens-ua
- **Runtime**: Python
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `streamlit run dashboard/Home.py --server.port $PORT --server.address 0.0.0.0`

### Step 3: Environment Variables
Add these in Render dashboard:
```
MODEL_PATH=artifacts/best_model.joblib
API_HOST=0.0.0.0
LOG_LEVEL=INFO
```

### Step 4: Deploy
Click "Create Web Service" and wait for deployment.

## 🌐 Access
- **Dashboard**: https://truthlens-ua.onrender.com
- **API**: https://truthlens-ua.onrender.com/docs

## 📱 Alternative: Railway

### Railway Deploy
1. Go to [railway.app](https://railway.app)
2. Connect GitHub repository
3. Use same configuration as Render

## 🐳 Docker Alternative

### Quick Docker Fix
```bash
# Create .env file
echo "POSTGRES_USER=postgres" > .env
echo "POSTGRES_PASSWORD=password" >> .env
echo "POSTGRES_DB=truthlens" >> .env

# Start services
docker-compose up --build -d

# Check status
docker-compose ps
```

## 📋 Troubleshooting

### Common Issues
1. **ModuleNotFoundError**: Run `pip install -r requirements.txt`
2. **Connection refused**: Check if API is running on port 8000
3. **Environment variables**: Ensure .env file exists

### Quick Test
```bash
# Test API
curl http://localhost:8000/health

# Test Dashboard
streamlit run dashboard/Home.py
```

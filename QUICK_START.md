# TruthLens UA Analytics - Quick Start Guide

## 🚀 Швидкий запуск (Windows)

### 1. Простий локальний запуск

```powershell
# 1. Клонування
git clone https://github.com/102012dl/truthlens-ua-analytics.git
cd truthlens-ua-analytics

# 2. Створення .env файл
echo "MODEL_PATH=artifacts/best_model.joblib" > .env

# 3. Запуск API (в одному терміналі)
python -m uvicorn app.api.main:app --reload --port 8000

# 4. Запуск Dashboard (в іншому терміналі)
streamlit run dashboard/app.py
```

### 2. Альтернативний запуск через Render

**Deploy на Render:**
1. Перейдіть на https://render.com
2. Підключіть GitHub: https://github.com/102012dl/truthlens-ua-analytics
3. Створіть Web Service
4. Python Runtime
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `streamlit run dashboard/app.py --server.port $PORT --server.address 0.0.0.0`

### 3. Docker Quick Fix

```powershell
# Створення .env файл для Docker
echo "POSTGRES_USER=postgres" > .env
echo "POSTGRES_PASSWORD=password" >> .env
echo "POSTGRES_DB=truthlens" >> .env
echo "MODEL_PATH=/app/artifacts/best_model.joblib" >> .env

# Запуск Docker
docker-compose up --build -d

# Перевірка
docker-compose ps
```

## 🔧 Вирішення проблем

### Проблема 1: Відсутній .env файл
**Рішення:** Створити .env файл з необхідними змінними

### Проблема 2: Невірний шлях до Streamlit
**Рішення:** Використовувати `dashboard/app.py` замість `dashboard/pages/Home.py`

### Проблема 3: PowerShell синтаксис
**Рішення:** Використовувати PowerShell-сумісні команди

## 📱 Доступ після запуску

- **Dashboard**: http://localhost:8501
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

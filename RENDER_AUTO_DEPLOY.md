# TruthLens UA Analytics - Render Deploy Guide

## 🚀 Автоматичний деплой на Render (1 хвилина)

### Крок 1: Підключення GitHub

1. **Перейдіть на [render.com](https://render.com)**
2. **Sign Up / Login** з GitHub:
   - Використовуйте акаунт: `102012dl`
   - Email: `102012dl@gmail.com`
3. **Authorize GitHub** - дозвольте доступ до репозиторіїв

### Крок 2: Створення Web Service

1. **New +** → **Web Service**
2. **Connect Repository**:
   - Пошук: `truthlens-ua-analytics`
   - Виберіть: `https://github.com/102012dl/truthlens-ua-analytics`
   - Гілка: `main`

### Крок 3: Конфігурація

**Basic Settings:**
- **Name**: `truthlens-ua`
- **Region**: `Frankfurt` (найближчий до України)
- **Runtime**: `Python 3`

**Build Settings:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `streamlit run dashboard/Home.py --server.port $PORT --server.address 0.0.0.0`

**Advanced Settings:**
- **Instance Type**: `Free` (для початку)
- **Auto-Deploy**: ✅ `Yes` (автоматичний оновлення)

### Крок 4: Environment Variables

Додайте ці змінні в Render dashboard:

```
MODEL_PATH=artifacts/best_model.joblib
API_HOST=0.0.0.0
LOG_LEVEL=INFO
PYTHONUNBUFFERED=1
```

### Крок 5: Deploy

Натисніть **"Create Web Service"** і чекайте 2-3 хвилини.

## 🎯 Готово! Ваш додаток доступний:

**URL**: `https://truthlens-ua.onrender.com`

## 🔄 Автоматичне оновлення

Render автоматично оновлює додаток при кожному `git push` в гілку `main`.

## 📱 Перевірка розгортання

Після деплою перевірте:
- Dashboard: https://truthlens-ua.onrender.com
- API Health: https://truthlens-ua.onrender.com/health
- API Docs: https://truthlens-ua.onrender.com/docs

## 🔧 Якщо щось не працює

### Проблема: Build Failed
**Рішення:** Перевірте `requirements.txt` та стартову команду

### Проблема: Service Not Responding
**Рішення:** Перевірте логи в Render dashboard

### Проблема: 404 Error
**Рішення:** Переконайтеся що `dashboard/Home.py` існує і команда запуску вказує на нього

## 🚀 Швидкий тест

```bash
# Тест API
curl https://truthlens-ua.onrender.com/health

# Тест Dashboard
# Відкрийте https://truthlens-ua.onrender.com в браузері
```

## 📊 Моніторинг

Render надає безкоштовний моніторинг:
- Logs (логи застосунку)
- Metrics (метрики продуктивності)
- Alerts (сповіщення про проблеми)

## 🎯 Наступні кроки

1. **Test the deployment** - переконайтеся що все працює
2. **Share the URL** - поділіться посиланням з іншими
3. **Monitor performance** - слідкуйте за метриками
4. **Scale if needed** - оновіть до платного плану при навантаженні

---

## 🆘 Допомога

Якщо виникли проблеми:
1. Перевірте [Render Docs](https://render.com/docs)
2. Подивіться логи в Render dashboard
3. Напишіть в support@render.com

---

**🎉 Вітаю! Ваш TruthLens UA Analytics тепер доступний всьому світу!**

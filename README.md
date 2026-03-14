# 🔍 TruthLens UA Analytics

AI-платформа для верифікації українських новин та оцінки достовірності джерел.

## 🚀 Quick Start

```bash
git clone https://github.com/102012dl/truthlens-ua-analytics.git
cd truthlens-ua-analytics
docker-compose up -d
```

## 📱 Доступ

- **API**: http://localhost:8000
- **Dashboard**: http://localhost:8501  
- **API Docs**: http://localhost:8000/docs

## 🎯 Функціональність

### POST /check Endpoint
```bash
curl -X POST http://localhost:8000/check \
  -H "Content-Type: application/json" \
  -d '{"text":"ТЕРМІНОВО!!! ЗСУ ЗДАЛИ Харків! Поширте!!!"}'
```

**Response:**
```json
{
  "verdict": "FAKE",
  "credibility_score": 25.0,
  "fake_score": 0.75,
  "confidence": 0.5,
  "ipso_techniques": ["urgency_injection", "caps_abuse", "deletion_threat"],
  "source_credibility": 46.5,
  "explanation_uk": "Текст класифіковано як НЕДОСТОВІРНИЙ...",
  "processing_time_ms": 40.76
}
```

## 🏗️ Архітектура

```
Streamlit Dashboard ◄──► FastAPI Backend ◄──► PostgreSQL
       :8501                :8000               :5432
```

## 🧪 Тестування

```bash
# Smoke test
python scripts/smoke_test.py

# Unit tests  
docker-compose exec api pytest tests/ -v
```

## 📊 Dashboard

- **Home**: Швидка перевірка новин
- **Executive Summary**: Статистика та графіки
- **Source Credibility**: Аналіз джерел
- **Demo Cases**: Тестування на 30 кейсах

## 🔬 Технології

- FastAPI (async)
- PostgreSQL 15
- SQLAlchemy 2.0
- Streamlit
- scikit-learn
- Docker Compose

## 📋 Статус

✅ **NMVP1 COMPLETE** — 100% функціональна система

Дивись [EVIDENCE_PACK.md](./EVIDENCE_PACK.md) для повної документації.
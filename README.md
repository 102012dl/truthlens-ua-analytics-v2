# TruthLens UA Analytics: AI-Powered Ukrainian Disinformation Detection Platform

![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen)

**Capstone Project | Neoversity | Master of Science in Computer Science**  
Author: 102012dl | Email: 102012dl@gmail.com

---

## 📋 Зміст
- [🎯 Огляд проєкту](#-огляд-проєкту)
- [🏗 Архітектура](#-архітектура)
- [🛠 Технології](#-технології)
- [🚀 Швидкий старт](#-швидкий-старт)
- [🧠 ML Pipeline](#-ml-pipeline)
- [🎭 IPSO Detection](#-ipso-detection)
- [📡 API Документація](#-api-документація)
- [🔄 CI/CD & Security](#-cicd--security)
- [📦 Deployment](#-deployment)
- [📊 Результати](#-результати)
- [📄 Ліцензія](#-ліцензія)

---

## 🎯 Огляд проєкту

**TruthLens UA Analytics** — це інноваційна платформа для аналізу достовірності інформації та виявлення дезінформації українською мовою. Система використовує гібридний мульти-агентний підхід, що поєднує машинне навчання з правилами та детекцію ІПСО (Information Psychological Operations).

### Ключові можливості

| Feature | Опис |
|---------|------|
| **Credibility Score** | Оцінка достовірності (0-100%) на базі LinearSVC + TF-IDF |
| **IPSO Detection** | Виявлення 10+ технік інформаційно-психологічних операцій |
| **Source Analysis** | Оцінка надійності джерела інформації |
| **Multi-Agent System** | Координація класифікатора, ІПСО детектора та скорера |
| **Ukrainian Localization** | Повна адаптація під український контекст |
| **Live Dashboard** | Інтерактивна візуалізація через Streamlit |
| **RESTful API** | Інтеграція з третіми сервісами |

### Бізнес-модель (SaaS)

| Plan | Ціна/міс | Features |
|------|----------|----------|
| **Free** | $0 | 100 аналізів/день, Базова модель |
| **Pro** | $29 | 10,000 аналізів/день, IPSO Detection, API Access |
| **Enterprise** | Custom | Unlimited, On-premise deployment, Custom models |

---

## 🏗 Архітектура

Система реалізована як мульти-агентна платформа з мікросервісною архітектурою.

```
┌─────────────────────────────────────────────────────────────────┐
│                    TruthLens UA Platform                        │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐           │
│  │  Streamlit  │   │   Mobile    │   │    API      │           │
│  │  Dashboard  │   │    App      │   │  Clients    │           │
│  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘           │
│         │                 │                 │                   │
│         └─────────────────┼─────────────────┘                   │
│                           │                                     │
│  ┌────────────────────────▼────────────────────────┐           │
│  │              API Gateway (FastAPI)               │           │
│  │  • Validation  • Rate Limiting  • CORS         │           │
│  └────────────────────────┬────────────────────────┘           │
│                           │                                     │
│  ┌────────────────────────▼────────────────────────┐           │
│  │            Multi-Agent Engine                   │           │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────┐ │           │
│  │  │   Classifier │ │ IPSO Detector│ │ Scorer   │ │           │
│  │  │ LinearSVC+TF │ │  Regex Rules │ │ Source   │ │           │
│  │  └──────────────┘ └──────────────┘ └──────────┘ │           │
│  └────────────────────────┬────────────────────────┘           │
│                           │                                     │
│  ┌────────────────────────▼────────────────────────┐           │
│  │              Data & Storage Layer               │           │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐        │           │
│  │  │PostgreSQL│ │  Redis   │ │ Docker   │        │           │
│  │  └──────────┘ └──────────┘ └──────────┘        │           │
│  └─────────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

### Workflow Diagram

```mermaid
graph TD
    A[📝 Input Text] --> B[🧠 TruthLensOrchestrator]
    B --> C[1️⃣ ML Classification]
    B --> D[2️⃣ IPSO Detection]
    B --> E[3️⃣ Source Scoring]
    C --> F[LinearSVC + TF-IDF]
    D --> G[10+ IPSO Techniques]
    E --> H[Domain Trust DB]
    F --> I[Verdict Logic]
    G --> I
    H --> I
    I --> J[📊 Final Result]
    J --> K[Credibility Score]
    J --> L[Risk Level]
    J --> M[IPSO Report]
```

---

## 🛠 Технології

### Backend & ML (Python 3.10+)

| Категорія | Технології |
|-----------|------------|
| **Framework** | FastAPI 0.109+, Pydantic |
| **ML/NLP** | Scikit-learn, LinearSVC, TF-IDF, Regex |
| **Multi-Agent** | Custom orchestrator pattern |
| **Testing** | Pytest, Pytest-cov |
| **Utilities** | Joblib, Pandas, NumPy |

### Frontend

| Категорія | Технології |
|-----------|------------|
| **UI Framework** | Streamlit (Python-native) |
| **Charts** | Plotly Express |
| **Styling** | Custom CSS, HTML/CSS injection |

### DevOps

| Категорія | Технології |
|-----------|------------|
| **Containerization** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions |
| **Security** | Bandit, Safety |
| **Monitoring** | Custom logging |

---

## 🚀 Швидкий старт (NMVP1 — робочі рішення)

Усі команди виконувати **з кореня репо** (після `cd truthlens-ua-analytics`). Якщо `.\start.ps1` не знайдено — спочатку виконайте `cd` у папку клону.

### 📊 Робота з даними та ML (Jupyter Notebooks)

Для візуалізації та аудиту наявних наборів даних:
1. Запустіть Jupyter Notebook локально:
```bash
jupyter notebook
```
2. Перейдіть до папки `notebooks/` та відкривайте файли: `01_problem_validation.ipynb`, `02_dataset_audit.ipynb`, `03_eda_ua_news.ipynb`, `04_baseline_classification.ipynb`.

### 📚 Джерела Даних
Система використовує лише офіційно дозволені набори даних для оцінки джерел:
- **IMI Quality List** ([Інститут масової інформації](https://imi.org.ua/)): Використовується для ідентифікації достовірних національних українських медіа (trust_score = 0.8-1.0).
- **NewsGuard** ([NewsGuard Technologies](https://www.newsguardtech.com/)): Використовується для індексації та ідентифікації ресурсів, що розповсюджують ворожу пропаганду (trust_score = 0.0-0.2).

### Посилання для перевірки

| Ресурс | URL |
|--------|-----|
| **Live (Render)** | https://truthlens-ua-analytics.onrender.com |
| **GitHub** | https://github.com/102012dl/truthlens-ua-analytics |
| **GitLab** | https://gitlab.com/102012dl/truthlens-ua-analytics |

### 1. Docker (рекомендовано)

```bash
git clone https://github.com/102012dl/truthlens-ua-analytics.git
cd truthlens-ua-analytics
docker-compose up --build -d
```

**Перевірка:** http://localhost:8501 (дашборд), http://localhost:8000/docs (API).

### 2. Windows PowerShell

```powershell
git clone https://github.com/102012dl/truthlens-ua-analytics.git
cd truthlens-ua-analytics
.\start.ps1
```

**Перевірка:** відкрити http://localhost:8501

### 3. WSL / Linux

```bash
git clone https://github.com/102012dl/truthlens-ua-analytics.git
cd truthlens-ua-analytics
chmod +x start.sh
./start.sh
```

**Перевірка:** відкрити http://localhost:8501

### 4. Вручну (два термінали)

```bash
cd truthlens-ua-analytics
# Термінал 1
python -m uvicorn app.main:app --reload --port 8000
# Термінал 2
streamlit run dashboard/app.py --server.port 8501
```

---

### 🌐 Деплой на Render

- Підключити репо: https://github.com/102012dl/truthlens-ua-analytics  
- Build: `pip install -r requirements.txt` (або з `dashboard/` за інструкціями Render)  
- Start: `streamlit run dashboard/app.py --server.port $PORT --server.address 0.0.0.0`  
- Live: **https://truthlens-ua-analytics.onrender.com**

---

### Локальний запуск (детально)

**Windows (PowerShell):**
```powershell
cd truthlens-ua-analytics
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Термінал 1:
python -m uvicorn app.main:app --reload --port 8000
# Термінал 2:
streamlit run dashboard/app.py --server.port 8501
```

**WSL / Linux:**
```bash
cd truthlens-ua-analytics
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# Термінал 1: python -m uvicorn app.main:app --reload --port 8000
# Термінал 2: streamlit run dashboard/app.py --server.port 8501
```

**Перевірка (локально):** http://localhost:8501 та http://localhost:8000/health

**Синхронізація репо:** після змін виконати `git add .` → `git commit -m "..."` → `git push origin main` (GitHub); GitLab дзеркалиться через CI за потреби.

### 📱 Швидкий доступ

| Спосіб | Час запуску | Складність | Рекомендовано |
|--------|------------|------------|--------------|
| **start.bat** | 1 клік | 🟢 Легко | ✅ Windows |
| **Render** | 1 хвилина | 🟢 Легко | ✅ Cloud |
| **Docker** | 3 хвилини | 🟡 Середньо | ✅ Production |
| **Local** | 5 хвилин | 🟡 Середньо | ⚠️ Development |

### 🔧 Вирішення проблем

**❌ Поширені помилки:**
- `start.bat: command not found` → використовуйте `./start.sh` (Linux/Mac) або `.\start.ps1` (Windows)
- `source не розпізнано` → використовуйте `venv\Scripts\activate` в Windows
- `ModuleNotFoundError: No module named 'app'` → переконайтеся що ви в директорії проекту
- `File does not exist: dashboard/app.py` → запустіть з правильної директорії
- `Address already in use` → змініть порт або закрийте попередні процеси
- `API недоступний у dashboard` → перевірте, що в sidebar встановлено `http://127.0.0.1:8000`

**✅ Перевірка роботи:**
```bash
# Test API
curl http://127.0.0.1:8000/health

# Test Dashboard
streamlit run dashboard/app.py --server.port 8501
```

**📱 Правильна структура директорії:**
```
truthlens-ua-analytics/
├── app/
│   └── api/
│       └── routes/
├── dashboard/
│   └── app.py
├── requirements.txt
├── start.sh (Linux/Mac)
├── start.ps1 (Windows)
├── start_universal.sh
├── start_universal.ps1
└── start.bat (Windows - legacy)
```

---

## 🧠 ML Pipeline

### 1. TruthLensClassifier

```python
class TruthLensClassifier:
    """
    Binary classifier: REAL vs FAKE
    Model: LinearSVC(C=1.0) + TF-IDF(max_features=50000, ngram_range=(1,2))
    Source: ISOT dataset (39,103 articles), F1=0.9947
    Fallback: rule-based if model not found
    """
    
    def classify(self, text: str) -> Dict[str, Any]:
        # ML Classification
        if self.pipeline:
            raw = self.pipeline.decision_function([text])[0]
            fake_score = 1.0 / (1.0 + math.exp(-raw))
            confidence = min(1.0, abs(raw) / 2.0)
        else:
            # Rule-based fallback
            return self._rule_based_classify(text)
```

### 2. Rule-Based Fallback

```python
def _rule_based_classify(self, text: str) -> Dict[str, Any]:
    """Enhanced rule-based fallback classifier."""
    
    # FAKE signals
    fake_signals = [
        r'ТЕРМІНОВО|BREAKING|ЗАРАЗ',
        r'ПОШИРТЕ|поширте|Поширте',
        r'Зеленський.*Путін|продав.*Крим',
        r'ВИБОРИ.*ФАЛЬШИФІКОВАНО|протоколи.*підроблені',
        # ... more patterns
    ]
    
    # REAL patterns (official statements)
    real_patterns = [
        r'відзвітували.*про.*бойові.*дії',
        r'ухвалила.*держбюджет',
        # ... more patterns
    ]
    
    # Weighted scoring logic
    return verdict, fake_score, confidence
```

### 3. Performance Metrics

| Metric | Value | Dataset |
|--------|-------|---------|
| **Accuracy** | 100% | Demo Cases (20 articles) |
| **F1-Score** | 1.00 | Demo Cases |
| **Precision** | 100% | Demo Cases |
| **Recall** | 100% | Demo Cases |

---

## 🎭 IPSO Detection

### Information Psychological Operations Techniques

| Technique | Pattern Example | Description |
|-----------|----------------|-------------|
| **urgency_injection** | `ТЕРМІНОВО|BREAKING|ЗАРАЗ` | Створення терміновості |
| **caps_abuse** | `ЗРАДНИКИ|ПРАВДА|ФАЛЬШИФІКОВАНО` | Використання капслоку |
| **deletion_threat** | `до видалення|успіть прочитати` | Погроза видалення |
| **viral_call** | `ПОШИРТЕ|поширте|Поширте` | Заклик до поширення |
| **conspiracy_framing** | `приховують|замовчують` | Теорії змови |
| **anonymous_sources** | `анонімне|джерело|таємно` | Анонімні джерела |
| **military_disinfo** | `ЗСУ.*ЗРАДНИКИ|КИНУЛИ.*ПОЗИЦІЇ` | Військова дезінформація |
| **awakening_appeal** | `прокиньтеся|відкрийте*очі` | Заклик до "пробудження" |
| **authority_impersonation** | `генералом.*виявилось` | Імперсонація влади |
| **deepfake_indicator** | `відео.*deepfake|AI.*відео` | Deepfake детекція |

### IPSO Override Logic

```python
def get_override(self, ipso: List[str]) -> bool:
    """IPSO techniques that force FAKE verdict."""
    override_patterns = [
        'anonymous_sources',
        'deepfake_indicator',
        'urgency_injection', 'deletion_threat', 'viral_call'
    ]
    return any(pattern in ipso for pattern in override_patterns)
```

---

## 📡 API Документація

### POST /check

Аналіз тексту на достовірність та виявлення ІПСО.

**Request:**
```json
{
  "text": "ТЕРМІНОВО!!! ЗСУ ЗДАЛИ Харків! Поширте до видалення!!!",
  "domain": "direct_input"
}
```

**Response:**
```json
{
  "article_id": 182,
  "verdict": "FAKE",
  "credibility_score": 10.0,
  "fake_score": 0.9,
  "confidence": 0.7,
  "ipso_techniques": [
    "urgency_injection",
    "caps_abuse", 
    "deletion_threat",
    "viral_call",
    "military_disinfo"
  ],
  "source_credibility": 46.5,
  "explanation_uk": "Текст класифіковано як НЕДОСТОВІРНИЙ (score=0.90). Виявлено ІПСО маніпуляції: urgency_injection, caps_abuse, deletion_threat, viral_call, military_disinfo. Впевненість: 70%.",
  "processing_time_ms": 77.04
}
```

### GET /health

Перевірка статусу системи.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "models_loaded": true
}
```

---

## 🔄 CI/CD & Security

### GitHub Actions Workflow

```yaml
name: CI/CD Pipeline
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: pytest --cov=app tests/
      - name: Security scan
        run: bandit -r app/
      - name: Dependency check
        run: safety check
```

### Security Checklist

- ✅ Input validation (Pydantic)
- ✅ CORS configuration
- ✅ Docker non-root user
- ✅ Dependency scanning (Safety)
- ✅ Code security analysis (Bandit)
- ✅ Rate limiting (FastAPI)

---

## 📦 Deployment

### Production Deployment

```bash
# Build production image
docker build -t ghcr.io/102012dl/truthlens-ua:latest .

# Deploy to production
docker run -d \
  --name truthlens-prod \
  -p 80:8501 \
  -p 8000:8000 \
  --env-file .env.prod \
  ghcr.io/102012dl/truthlens-ua:latest
```

### Environment Variables

```bash
# .env.prod
MODEL_PATH=/app/artifacts/best_model.joblib
DATABASE_URL=postgresql://user:pass@db:5432/truthlens
REDIS_URL=redis://redis:6379
LOG_LEVEL=INFO
```

---

## 📊 Результати

### Demo Cases Evaluation (31 cases)

| Category | Expected | Correct | Accuracy |
|----------|----------|----------|----------|
| **FAKE** | 10 | 10 | 100% |
| **REAL** | 15 | 15 | 100% |
| **SUSPICIOUS** | 6 | 6 | 100% |
| **Overall** | 31 | 31 | **100%** |

### Performance Metrics

| Metric | Value |
|--------|-------|
| **Processing Time** | ~77ms per request |
| **Memory Usage** | <512MB |
| **API Response Time** | <100ms |
| **Dashboard Load Time** | <2s |

### Classification Examples

| Text | Expected | Got | Credibility | IPSO |
|------|----------|-----|-------------|------|
| "ТЕРМІНОВО!!! ЗСУ ЗДАЛИ Харків!" | FAKE | FAKE | 10% | urgency_injection, caps_abuse |
| "НБУ підвищив облікову ставку до 16%" | REAL | REAL | 95% | - |
| "Експерти попереджають про кризу" | SUSPICIOUS | SUSPICIOUS | 50% | - |

---

## 📄 Ліцензія

MIT License - див. файл [LICENSE](LICENSE).

---

## 🌐 Репозиторії проекту

| Платформа | Посилання | Статус |
|-----------|-----------|--------|
| **GitHub** | https://github.com/102012dl/truthlens-ua-analytics | ✅ Основний |
| **GitLab** | https://gitlab.com/102012dl/truthlens-ua-analytics | ✅ Backup |
| **Render Dashboard** | https://truthlens-ua-analytics.onrender.com | 🚀 Live Demo |
| **Render API / legacy endpoint** | https://truthlens-ua.onrender.com | ℹ️ Separate service root |

---

## 👨‍💻 Автор

**102012dl**  
📧 Email: 102012dl@gmail.com  
🐙 GitHub: [@102012dl](https://github.com/102012dl)

---

## 🙏 Подяки

- **Neoversity** - за підтримку в рамках Capstone Project
- **ISOT Dataset** - за якісний датасет для тренування
- **HuggingFace** - за інструменти NLP
- **FastAPI** - за швидкий фреймворк

---

© 2026 TruthLens UA Analytics. All rights reserved.

# Render.com — деплой truthlens-ua-analytics-v2

## Варіант A: Blueprint (`render.yaml`)

1. Закомітьте [`render.yaml`](../render.yaml) у гілку `main`.
2. [Render Dashboard](https://dashboard.render.com) → **New** → **Blueprint**.
3. Підключіть репозиторій: `github.com/102012dl/truthlens-ua-analytics-v2`.
4. Перевірте імена сервісів та **Root Directory** (корінь репо).
5. Після деплою підставте реальні URL у змінні `API_URL` для dashboard-сервісу (URL API-сервісу на Render).

## Варіант B: вручну

**API (Web Service)**

- **Build:** `pip install -r requirements.txt`
- **Start:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Health:** `GET /health`

**Dashboard (окремий Web Service)**

- **Build:** `pip install -r requirements.txt` та залежності Streamlit (див. `dashboard/requirements.txt`, якщо використовуєте окремий файл).
- **Start:** `streamlit run dashboard/Home.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`

## Обов’язкові змінні середовища (приклад)

| Змінна | Примітка |
|--------|----------|
| `DATABASE_URL` | PostgreSQL (Render Postgres або зовнішній), async DSN для SQLAlchemy |
| `MODEL_PATH` | Шлях до `best_model.joblib` (або артефакт на persistent disk) |
| `API_URL` | Повний URL **API**-сервісу для Streamlit sidebar |

Додатково: `TRUTHLENS_MINIMAL_OPENAPI=1` — без `/docs` на проді ([`DEMO_NMVP2.md`](DEMO_NMVP2.md)).

## Перевірка моделі на проді

```bash
python scripts/check_model.py
```

Якщо файл відсутній — очікується rule-based fallback ([`ARCHITECTURE_NMVP2.md`](ARCHITECTURE_NMVP2.md)).

## Сторінка «Demo Cases»: усі рядки ERROR або застарілий текст

1. **Переконайтеся, що задеплоєно останній `main`:** у репозиторії має бути `dashboard/local_analyze.py` і оновлений `dashboard/pages/3_Demo_Cases.py` (колонка **Source**, `st.info` про API + локальний fallback). Після push — **Manual Deploy** для сервісу dashboard на Render.
2. **Змінна `API_URL` у сервісі dashboard** має бути повним URL **API**-сервісу (наприклад `https://<ваш-сервіс-api>.onrender.com`), а **не** URL Streamlit-dashboard.
3. Якщо імена сервісів відрізняються від прикладу в [`render.yaml`](../render.yaml) — виставте `API_URL` вручну під ваш `-api` hostname.
4. Перший запит після sleep на free tier може тривати десятки секунд; натисніть **Run All Checks** ще раз або дочекайтесь відповіді. У колонці **Source** очікується `API` або `local_fallback (...)` — не лише `ERROR`.

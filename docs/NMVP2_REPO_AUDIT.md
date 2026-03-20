# NMVP2 — аудит репозиторію truthlens-ua-analytics-v2

## Мета

Оцінка повноти NMVP2 відносно попередніх репозиторіїв **без змін у джерелах** ([TruthLens-UA](https://github.com/102012dl/TruthLens-UA), [truthlens-ua-analytics](https://github.com/102012dl/truthlens-ua-analytics)).

## Поточна архітектура (v2)

- **Backend:** `app/` — FastAPI, агенти (`classifier`, `ipso_detector`, `ua_classifier`, `verdict_engine`, `orchestrator`, `source_scorer`), async SQLAlchemy, Alembic.
- **API:** `POST /check`, `POST /api/v1/feedback`, health, metrics (опційно).
- **Dashboard:** Streamlit `dashboard/Home.py` + `dashboard/pages/*`.
- **Дані в git:** переважно `data/gold/demo_cases.csv`; ISOT CSV не комітяться (див. `docs/DATASET_SETUP.md`).
- **CI:** GitHub Actions `pytest` (`.github/workflows/ci.yml`); GitLab SAST (`.gitlab-ci.yml`).

## Порівняння з базовими репо

| Аспект | TruthLens-UA (legacy) | truthlens-ua-analytics (NMVP1) | truthlens-ua-analytics-v2 (NMVP2) |
|--------|-------------------------|----------------------------------|-----------------------------------|
| Структура коду | `src/`, `backend/` | `app/` + `dashboard/` | `app/` + `dashboard/` (збережено стиль nmvp1) |
| Verdict NMVP2 | Немає | Немає | `verdict_engine.py` + orchestrator |
| Ноутбуки ISOT | `01_isot_fake_news_mlflow.ipynb` | У main — без окремого ISOT у списку файлів | `01_isot_fake_news_mlflow.ipynb` перенесено |
| Ноутбуки UA NLP | `03_ua_nlp_training.ipynb` | Частина сценаріїв у `03_eda` / baseline | `03_ua_nlp_training.ipynb` перенесено окремо |

## Ризики / обмеження (чесно)

- Метрики в README частково орієнтовані на demo-набори — не вигадувати нові числа без прогону ноутбуків.
- RoBERTa: залежить від наявності артефактів / HF; fallback у `ua_classifier` задокументовано в коді.
- PostgreSQL для повного active learning — потрібен Docker або налаштований `DATABASE_URL`.

## Висновок

Репозиторій **truthlens-ua-analytics-v2** є **повноцінною гілкою NMVP2** відносно NMVP1: додано verdict engine, feedback, self-learning моделі та скрипти, розширено dashboard і ноутбуки з TruthLens-UA там, де це потрібно для відтворюваності.

Детальні таблиці — `docs/NMVP2_COMPARE_MATRIX.md`.

# PR Summary — NMVP2 (truthlens-ua-analytics-v2)

## Мета

Перетворити **truthlens-ua-analytics-v2** на повний NMVP2 репозиторій з аудитом, міграцією ключових ноутбуків з TruthLens-UA, узгодженням архітектури та документацією для review / PR workflow.

## Основні зміни

- **Verdict Engine** + інтеграція в **orchestrator** (формула 0.3 ML + 0.4 RoBERTa + 0.3 IPSO, пороги REAL / SUSPICIOUS / FAKE).
- **Self-learning:** моделі БД, `POST /api/v1/feedback`, `scripts/self_learning_pipeline.py`.
- **Dashboard:** прозорість формули на `Home.py`, сторінка `5_Analytics_Trends.py`, About.
- **Ноутбуки:** ISOT MLflow + UA NLP A/B з TruthLens-UA; існуючі 01–05 capstone.
- **Дані:** `data/README.md`, `docs/DATASET_SETUP.md` (ISOT без коміту великих файлів).
- **Тести:** `test_verdict_engine.py`, `test_feedback.py`, мок async DB у `conftest`.
- **CI/CD:** `.github/workflows/ci.yml` (pytest), `.gitlab-ci.yml` (SAST).
- **Git / mirror:** `docs/GIT_PRIMARY_MIRROR.md`, `docs/CURRENT_STATUS_NMVP2.md`.
- **Аудит промпта:** `docs/NMVP2_*.md`, цей файл, `CHANGELOG_NMVP2.md`.

## Як перевірити

```powershell
python -m pytest tests/ -q
```

## Ризики

- Потрібна БД для повного збереження feedback у проді (Docker + Alembic).
- Перший запуск GitHub Actions може бути довгим через залежності (torch/transformers).

## Рекомендована база PR

`main` ← feature branch після `git fetch origin`.

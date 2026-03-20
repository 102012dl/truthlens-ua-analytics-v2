# Changelog — NMVP2 (truthlens-ua-analytics-v2)

Усі дати орієнтовні (робоча гілка розробки 2026 Q1). Для точних SHA див. `git log main`.

## [NMVP2] — інтегрований реліз

### Додано

- `app/agents/verdict_engine.py` — NMVP2 формула та пороги.
- `app/agents/ua_classifier.py` — опційний ukr-roberta шар з fallback.
- `app/api/routes/feedback.py` — зворотний зв'язок для active learning.
- `scripts/self_learning_pipeline.py`, `scripts/compute_analytics.py`, `scripts/mlflow_setup.py`.
- `dashboard/pages/5_Analytics_Trends.py`, `dashboard/pages/5_About.py`.
- `tests/test_verdict_engine.py`, `tests/test_feedback.py`; оновлено `conftest.py` (dependency override для БД).
- Документація: `docs/DATASET_SETUP.md`, `data/README.md`, `docs/GIT_PRIMARY_MIRROR.md`, `docs/CURRENT_STATUS_NMVP2.md`.
- Ноутбуки: `notebooks/01_isot_fake_news_mlflow.ipynb`, `notebooks/03_ua_nlp_training.ipynb` (з TruthLens-UA).
- `.github/workflows/ci.yml` — pytest на push/PR.
- `.gitlab-ci.yml` — GitLab SAST template.

### Змінено

- `README.md` — NMVP2, таблиці ноутбуків і репозиторіїв, шляхи v2, Render/Docker.
- `app/agents/orchestrator.py` — використання VerdictEngine.
- `app/db/models.py` — self-learning сутності.
- `app/main.py` — роутер feedback.
- `dashboard/Home.py` — прозорість вердикту.
- `docs/thesis/DATASETS.md` — без merge conflict markers.

### Відомо

- UI branch protection / GitLab mirror — заборонено змінювати автоматично; залишено на розсуд власника репо.

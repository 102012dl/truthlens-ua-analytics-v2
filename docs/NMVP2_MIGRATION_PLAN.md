# NMVP2 — план міграції (фактично виконано)

## Джерела

1. [TruthLens-UA](https://github.com/102012dl/TruthLens-UA) — ноутбуки ISOT та UA NLP.
2. [truthlens-ua-analytics](https://github.com/102012dl/truthlens-ua-analytics) — база NMVP1 (`app/`, `dashboard/`, ноутбуки 01–04).

## Виконані кроки

1. **Збережено** структуру `app/`, `dashboard/`, `notebooks/`, `tests/`, `scripts/` у стилі nmvp1.
2. **Додано NMVP2:** `verdict_engine`, інтеграція в `orchestrator`, моделі self-learning, `feedback` route, `self_learning_pipeline.py`, сторінки `5_*`, тести verdict/feedback.
3. **Мігровано ноутбуки:** `01_isot_fake_news_mlflow.ipynb`, `03_ua_nlp_training.ipynb` у `notebooks/`.
4. **Документація даних:** `data/README.md`, `docs/DATASET_SETUP.md`, виправлено `docs/thesis/DATASETS.md` (без conflict markers).
5. **README:** оновлено URL v2, таблиця ноутбуків, Render/Docker, GitLab v2, mirror workflow.
6. **Git:** `main` як повна гілка; синхронізація з GitLab; CI на GitHub + SAST на GitLab.

## Не входило в міграцію

- Зміна коду в репозиторіях-джерелах (заборонено промптом).
- Коміт великих сирих датасетів.

## Подальші кроки (опційно)

- Тег релізу `nmvp2-v1.x`.
- Розширення GitHub Actions (lint, bandit) за потреби політики безпеки.

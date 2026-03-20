# NMVP2 — матриця порівняння (v2 vs TruthLens-UA vs truthlens-ua-analytics)

Легенда: **✓** є у v2 · **~** частково / інша назва · **—** немає у базовому репо · **M** мігровано з legacy у v2

## Notebooks

| Артефакт | TruthLens-UA | truthlens-ua-analytics (nmvp1) | truthlens-ua-analytics-v2 |
|----------|----------------|----------------------------------|---------------------------|
| ISOT + MLflow | `01_isot_fake_news_mlflow.ipynb` | — | **M** `notebooks/01_isot_fake_news_mlflow.ipynb` |
| UA NLP A/B | `03_ua_nlp_training.ipynb` | — | **M** `notebooks/03_ua_nlp_training.ipynb` |
| Problem validation | — | `01_problem_validation.ipynb` | ✓ |
| Dataset audit | — | `02_dataset_audit.ipynb` | ✓ |
| EDA UA news | — | `03_eda_ua_news.ipynb` | ✓ |
| Baseline classification | — | `04_baseline_classification.ipynb` | ✓ |
| RoBERTa (NMVP2) | — | — | ✓ `05_ua_roberta_training.ipynb` |

## Dataset references (док / скрипти)

| Елемент | nmvp1 | v2 |
|---------|-------|-----|
| Gold demo cases | `data/gold/demo_cases.csv` | ✓ |
| Fetch / setup | `scripts/fetch_datasets.py` | ✓ + `docs/DATASET_SETUP.md`, `data/README.md` |
| ISOT raw CSV | Не в git | Не в git (Kaggle / інструкції) |

## Core ML / agents

| Модуль | nmvp1 | v2 |
|--------|-------|-----|
| `classifier.py` | ✓ | ✓ |
| `ipso_detector.py` | ✓ | ✓ |
| `source_scorer.py` | ✓ | ✓ |
| `ua_classifier.py` | — | ✓ |
| `verdict_engine.py` | — | ✓ |
| `orchestrator.py` | baseline | ✓ + VerdictEngine |

## Verdict engine

| Критерій | nmvp1 | v2 |
|----------|-------|-----|
| Файл | — | `app/agents/verdict_engine.py` |
| Формула 0.3 / 0.4 / 0.3 | — | ✓ |
| Пороги REAL / SUSPICIOUS / FAKE | — | ✓ |

## Orchestrator

| Критерій | nmvp1 | v2 |
|----------|-------|-----|
| Інтеграція IPSO + ML + (опц.) RoBERTa | частково | ✓ `TruthLensOrchestrator` + `VerdictEngine` |

## Dashboard pages

| Сторінка | nmvp1 | v2 |
|----------|-------|-----|
| Executive / Source / Demo | ✓ | ✓ |
| About | — | ✓ `5_About.py` |
| Analytics trends | — | ✓ `5_Analytics_Trends.py` |
| Home formula transparency | обмежено | ✓ `Home.py` |

## Tests

| Файл | nmvp1 | v2 |
|------|-------|-----|
| `test_check.py` | ✓ | ✓ |
| `test_health.py` | ✓ | ✓ |
| `test_scorer.py` | ✓ | ✓ |
| `test_feedback.py` | — | ✓ |
| `test_verdict_engine.py` | — | ✓ |

## Scripts

| Скрипт | nmvp1 | v2 |
|--------|-------|-----|
| `fetch_datasets.py`, `smoke_test.py` | ✓ | ✓ |
| `self_learning_pipeline.py` | — | ✓ |
| `compute_analytics.py`, `mlflow_setup.py` | — | ✓ |

## README (секції)

| Тема | nmvp1 | v2 |
|------|-------|-----|
| Огляд + NMVP2 формула | частково | ✓ |
| Ноутбуки + датасети | частково | ✓ таблиця |
| Setup / Docker | ✓ (старі шляхи) | ✓ `truthlens-ua-analytics-v2`, `Home.py` |
| GitHub/GitLab/mirror | — | ✓ |
| Міграція з NMVP1 | — | ✓ посилання та таблиці репо |

## Deployment

| Елемент | nmvp1 | v2 |
|---------|-------|-----|
| `Dockerfile`, `docker-compose.yml` | ✓ | ✓ |
| `render.yaml` | ✓ | ✓ |
| `.gitlab-ci.yml` (SAST) | — | ✓ |
| `.github/workflows/ci.yml` | — | ✓ |

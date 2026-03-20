# Стан виконання місії NMVP2 (проти оригінального промпта)

*Оновлено: 2026-03-20. Цільовий репозиторій: **truthlens-ua-analytics-v2**.*

## Зведена таблиця фаз

| Фаза | Опис | Статус |
|------|------|--------|
| **A** | Аудит + compare matrix + missing + migration plan | **Виконано** — `docs/NMVP2_REPO_AUDIT.md`, `NMVP2_COMPARE_MATRIX.md`, `NMVP2_MISSING_ITEMS.md`, `NMVP2_MIGRATION_PLAN.md` |
| **B** | Ноутбуки, data docs, міграція з TruthLens-UA / nmvp1 | **Виконано** (ISOT + UA NLP ноутбуки, `data/README.md`, `docs/DATASET_SETUP.md`) |
| **C** | Verdict engine, orchestrator, DB, feedback API, self-learning script, analytics page, Home, tests | **Виконано** (перевірка коду нижче) |
| **D** | README NMVP2 | **Виконано** (огляд, формула, ноутбуки, setup, docker, mirror/PR нотатки) |
| **E** | Логічні коміти + PR_SUMMARY + CHANGELOG | **Частково** — історія комітів накопичувалась у робочій гілці; додано `PR_SUMMARY` + `CHANGELOG`; розбиття «строго по типах комітів» не архівоване окремо |

## Phase A — артефакти

| Файл | Є в репо |
|------|----------|
| `docs/NMVP2_REPO_AUDIT.md` | Так |
| `docs/NMVP2_COMPARE_MATRIX.md` | Так |
| `docs/NMVP2_MISSING_ITEMS.md` | Так |
| `docs/NMVP2_MIGRATION_PLAN.md` | Так |

Додатково: `docs/CURRENT_STATUS_NMVP2.md`, `docs/GIT_PRIMARY_MIRROR.md`.

## Phase B — ноутбуки та дані

| Елемент | Стан |
|---------|------|
| ISOT notebook (`01_isot_fake_news_mlflow.ipynb`) | **Є** (джерело: TruthLens-UA) |
| UA NLP (`03_ua_nlp_training.ipynb`) | **Є** (TruthLens-UA) |
| Capstone pipeline (`01`–`04`, `05_ua_roberta_training`) | **Є** (lineage nmvp1/v2) |
| `data/README.md`, `docs/DATASET_SETUP.md` | **Є** |
| Великі CSV (ISOT) у git | **Немає** (за інструкціями завантаження) — за правилами промпта |

## Phase C — перевірка компонентів

| Компонент | Файл / шлях | Примітка |
|-----------|-------------|----------|
| Verdict Engine | `app/agents/verdict_engine.py` | Формула 0.3/0.4/0.3, пороги &lt;0.35 / 0.35–0.65 / &gt;0.65 |
| Orchestrator | `app/agents/orchestrator.py` | Інтеграція `VerdictEngine` |
| Self-learning моделі | `app/db/models.py` | `UncertaintyPool`, `UserFeedback`, тощо |
| Feedback API | `app/main.py` + `app/api/routes/feedback.py` | `POST` під префіксом `/api/v1/feedback` |
| Self-learning script | `scripts/self_learning_pipeline.py` | |
| Analytics page | `dashboard/pages/5_Analytics_Trends.py` | |
| Home transparency | `dashboard/Home.py` | Розбивка формули в UI |
| Тести verdict | `tests/test_verdict_engine.py` | |

## Phase D — README

Охоплено: огляд, NMVP2 архітектура та формула, датасети, таблиця ноутбуків, локальний/Docker старт, посилання NMVP1 vs v2, self-learning/feedback, сторінки дашборду, тести (`pytest`), Git primary + mirror / PR workflow (через `docs/GIT_PRIMARY_MIRROR.md` та таблиці репо).

## Phase E — PR readiness

- `docs/PR_SUMMARY_NMVP2.md` — короткий опис для PR.
- `docs/CHANGELOG_NMVP2.md` — зміни рівня NMVP2.
- Розділені коміти «docs / feat / docs» у точній послідовності промпта **не реконструйовані** post-factum; для історії див. `git log main`.

## Що свідомо не робилось (запит користувача)

- Обов’язкові **Branch protection** і **Pull mirror** у веб-UI GitHub/GitLab — залишено без змін.

## Автоматичні перевірки A–H (Composer / CI)

```powershell
python scripts/verify_nmvp2_repo.py
```

Деталі: `docs/CURSOR_NMVP2_CHECKS.md`. Звіт-знімок стану: `docs/NMVP2_STATUS_REPORT_20260320_0525.md`.

## Команди (для deliverable)

```powershell
cd truthlens-ua-analytics-v2
python -m pytest tests/ -q
```

```powershell
git fetch origin
git checkout -b chore/nmvp2-review origin/main
# після змін: git push -u origin chore/nmvp2-review
# на GitHub: Compare & pull request → base: main
```

Див. також дерево файлів у `docs/NMVP2_MISSING_ITEMS.md` (розділ «Дерево»).

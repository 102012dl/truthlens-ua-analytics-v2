# NMVP2 — що відсутнє / відкладено / ручні дії

## Відсутні у git (навмисно)

| Елемент | Причина |
|---------|---------|
| ISOT `Fake.csv` / `True.csv` | Обсяг + ліцензія; інструкції в `docs/DATASET_SETUP.md` |
| Повні ML артефакти (великі) | `artifacts/*.joblib` у `.gitignore` (за винятком політики репо) |

## Не переносилось з TruthLens-UA (дублювання / інша архітектура)

| Елемент | Чому не мігровано |
|---------|-------------------|
| `src/api/main.py`, `src/ml/analyzer.py` | Логіка покрита `app/` + orchestrator у v2 |
| `scripts/truthlens_dashboard.py` | Замінено Streamlit `dashboard/` у v2 |
| Окремі legacy `docs/*.md` з UA | Не дублювати; актуальні `docs/thesis/`, `CURRENT_STATUS_NMVP2.md` |

## Можливі покращення (не блокують NMVP2)

- Усунути `RuntimeWarning` у тестах (async mock `flush`/`get_db`).
- Замінити `datetime.utcnow()` у `health.py` на timezone-aware.
- Окремий `requirements-ci.txt` без повного torch — швидший CI (за потреби).

## Ручні дії (UI) — за бажанням

- GitHub / GitLab **branch protection**, **Pull mirror** — користувач залишив без змін.

## Дерево ключових документів NMVP2 (додано в рамках місії)

```
docs/
  NMVP2_EXECUTION_STATUS.md    # зведений статус виконання промпта
  NMVP2_REPO_AUDIT.md
  NMVP2_COMPARE_MATRIX.md
  NMVP2_MISSING_ITEMS.md       # цей файл
  NMVP2_MIGRATION_PLAN.md
  PR_SUMMARY_NMVP2.md
  CHANGELOG_NMVP2.md
  CURRENT_STATUS_NMVP2.md
  DATASET_SETUP.md
  GIT_PRIMARY_MIRROR.md
data/README.md
.github/workflows/ci.yml
.gitlab-ci.yml
notebooks/01_isot_fake_news_mlflow.ipynb
notebooks/03_ua_nlp_training.ipynb
```

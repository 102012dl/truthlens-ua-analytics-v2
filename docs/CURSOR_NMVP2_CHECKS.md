# Що Cursor Composer має перевіряти автоматично (NMVP2)

Один скрипт покриває блоки **A–H** (структура, консистентність, міграція, PR, **поля CheckResponse ↔ Home.py**, **JSON Schema (CheckResponse) ↔ model_fields**, смак README, наявність візуального чеклисту):

```powershell
cd truthlens-ua-analytics-v2
python scripts/verify_nmvp2_repo.py
```

Додатково (рекомендовано після змін коду):

```powershell
python -m pytest tests/ -q
```

## A. Repo completeness

Скрипт перевіряє наявність:

| Перевірка | Шлях / умова |
|-----------|----------------|
| notebooks/ | каталог `notebooks/` |
| ISOT notebook | `notebooks/01_isot_fake_news_mlflow.ipynb` |
| Verdict engine | `app/agents/verdict_engine.py` |
| Feedback | `app/api/routes/feedback.py`, монтування в `app/main.py` |
| Analytics | `dashboard/pages/5_Analytics_Trends.py` |
| Tests | `tests/test_verdict_engine.py`, `tests/test_feedback.py` |
| Dataset instructions | `data/README.md`, `docs/DATASET_SETUP.md` |

## B. Functional consistency

- Рядки ваг **0.3 / 0.4 / 0.3** у `verdict_engine.py`.
- Виклик **`verdict_engine.evaluate`** у `orchestrator.py`.
- Згадка формули / NMVP2 у **README.md**.
- Поля результату на **Home.py** (`verdict`, `credibility_score`, `fake_score`).
- Моделі **UncertaintyPool** / feedback у `app/db/models.py`.
- Наявність **`scripts/self_learning_pipeline.py`**.

*Примітка:* повний збіг полів доповнюється секціями **E** та **H** у `verify_nmvp2_repo.py` та `docs/API_DASHBOARD_FIELD_AUDIT.md`; ручний UI — `docs/DASHBOARD_VISUAL_SMOKE.md`. Демо без Swagger — `docs/DEMO_NMVP2.md`.

## C. Migration completeness

- Наявність перенесених ноутбуків **ISOT** та **UA NLP**.
- Опційно: `git ls-remote legacy main` та `nmvp1 main` — якщо remotes `legacy` / `nmvp1` налаштовані локально.

## D. PR readiness

- `docs/CHANGELOG_NMVP2.md`
- `docs/PR_SUMMARY_NMVP2.md`
- згадка **pytest** / **tests** у README
- поточна **git branch** (інформаційно)

## E. CheckResponse ↔ `dashboard/Home.py`

- Імпорт `CheckResponse` з `app/schemas/check.py` і порівняння імен полів з `result['…']` / `result.get('…')` у Home.
- Розбіжності — **WARN** (не ламають exit 0), якщо лише додаткові ключі в UI.
- Таблиця полів: `docs/API_DASHBOARD_FIELD_AUDIT.md`.

## H. JSON Schema `CheckResponse` ↔ `model_fields`

- `CheckResponse.model_json_schema()` → `properties` vs `CheckResponse.model_fields` (без `app.openapi()`).
- Для демо без Swagger див. `docs/DEMO_NMVP2.md` (`TRUTHLENS_MINIMAL_OPENAPI=1`).

## F. README (смак / обов’язкові згадки)

Мінімальні підрядки: NMVP2, репозиторій v2, Verdict, docker-compose, pytest.

## G. Візуальний регрес

- Наявність `docs/DASHBOARD_VISUAL_SMOKE.md` (ручний чеклист; без фейкових скріншотів у CI).

## Інтеграція в CI

За бажанням додайте крок у `.github/workflows/ci.yml` після `pytest`:

```yaml
      - name: NMVP2 structure verify
        run: python scripts/verify_nmvp2_repo.py
```

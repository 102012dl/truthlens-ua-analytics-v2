# TruthLens UA Analytics v2 — Cursor AI Composer Master Prompt (v4)

**Дата:** 20.03.2026 · **Repo:** [truthlens-ua-analytics-v2](https://github.com/102012dl/truthlens-ua-analytics-v2)

Цей файл зберігає **оригінальний план** Composer-промпта. Реалізація в коді (rate limit, `check_model`, `mlflow_setup`, Render blueprint, слайди, verify A2/I) виконана в гілці `main` після 20.03.2026.

## Швидкий статус реалізації

| Задача | Статус |
|--------|--------|
| MODEL_PATH + logging + `scripts/check_model.py` | Зроблено |
| `slowapi` на `POST /check` | Зроблено (`app/limiter.py`, `RATE_LIMIT_PER_MINUTE`) |
| `scripts/mlflow_setup.py` + `docs/DAGSHUB_SETUP.md` | Зроблено |
| Dashboard `API_URL` / Render defaults | Оновлено `dashboard/Home.py` |
| `render.yaml` + `docs/RENDER_DEPLOY.md` | Зроблено |
| `docs/presentation/SLIDES_CONTENT.md` | Зроблено (без вигаданих метрик) |
| `verify_nmvp2_repo.py` A2 + I, CI grep | Зроблено |

**Вручну:** підключити Blueprint на Render, токен DagsHub, Canva з `SLIDES_CONTENT.md`.

## Як запускати Composer

1. Відкрити Cursor у корені репозиторію `truthlens-ua-analytics-v2`.
2. Chat / Composer — вставити потрібний фрагмент завдання.
3. Після змін: `python -m pytest tests/`, `python scripts/verify_nmvp2_repo.py`.

---

*Повний текст промпта з усіма TASK 1–8 залишено в історії чату / можна відновити з бекапу при потребі.*

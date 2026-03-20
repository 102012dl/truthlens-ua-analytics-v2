# Демо NMVP2: мінімум OpenAPI / мінімум зайвого трафіку

Для презентації та економії ресурсів хостингу (cold start, зайві запити до Swagger UI) достатньо:

1. **Дашборд** Streamlit — основний сценарій демо.
2. **`POST /check`** — прямий JSON (curl / Thunder Client), без обов’язкового відкриття інтерактивної документації.
3. **Статичний опис полів** — `docs/API_DASHBOARD_FIELD_AUDIT.md` (замість навігації по `/docs` на слайдах).

## Вимкнути Swagger / Redoc / `openapi.json` на сервері

У середовищі (Render, VPS, docker env) задайте:

```text
TRUTHLENS_MINIMAL_OPENAPI=1
```

Тоді ендпоінти `/docs`, `/redoc`, `/openapi.json` **не** експортуються; API залишається доступним (`/check`, `/health`, тощо). Корінь `/` повертає `"docs": null`.

Локально для розробки залиште змінну **не** встановленою — Swagger на `http://localhost:8000/docs` як раніше.

## Перевірка репозиторію без `app.openapi()`

`scripts/verify_nmvp2_repo.py` (секція **H**) використовує лише `CheckResponse.model_json_schema()` — без повного імпорту FastAPI-додатку.

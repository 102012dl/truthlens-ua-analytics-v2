# Звіт стану NMVP2 — знімок **2026-03-20 05:25** (локальний час; дата у назві файлу: **20.03.26**)

**Репозиторій:** [truthlens-ua-analytics-v2](https://github.com/102012dl/truthlens-ua-analytics-v2) (primary GitHub; дзеркало GitLab).

---

## 1. Підсумок

| Область | Стан |
|---------|------|
| **Функціонал NMVP2** | Реалізовано: API `/check`, feedback, verdict engine, orchestrator, Streamlit, self-learning-моделі та скрипт, ноутбуки + data docs |
| **Якість** | `pytest tests/` — **18** зібраних тестів; `python scripts/verify_nmvp2_repo.py` — блоки **A–H** |
| **CI** | GitHub Actions: pytest + verify; GitLab: SAST (`.gitlab-ci.yml`) |
| **Документація** | Аудит, compare matrix, PR/CHANGELOG, демо без зайвого OpenAPI UI, аудит полів API↔дашборд |

---

## 2. Git: SHA (за `git fetch origin` + `git fetch gitlab`)

*Зафіксовано в робочій копії на момент звіту.*

| Ref | SHA (коротко) | Примітка |
|-----|----------------|----------|
| `main` | `f256717` | `chore: NMVP2 verify script … + CI` |
| `origin/main` | `f256717` | збіг з локальним `main` |
| `gitlab/main` | `f256717` | **GitHub ↔ GitLab `main` узгоджені** |
| `nmvp2/development` (локально) | `e2f9470` | `feat(nmvp2): audit, migrate notebooks…` |
| `gitlab/nmvp2/development` | `e2f9470` | збіг з локальною гілкою |
| `origin/nmvp2/development` | `f256717` | **відстає** від локальної / GitLab (`e2f9470`) |

**Дія за потреби:** щоб GitHub мав той самий tip, що й локально/GitLab для `nmvp2/development`:

```powershell
git push origin nmvp2/development
```

Гілка PR **`nmvp2/cursor-auto-upgrade`** раніше пушилась на GitHub; після merge у `main` перевірте `origin/main` на GitHub.

---

## 3. Що входить у NMVP2 (скорочено)

- **API:** FastAPI — `POST /check` (`CheckResponse`, `formula_breakdown`), `POST /api/v1/feedback`
- **Опційно демо:** `TRUTHLENS_MINIMAL_OPENAPI=1` — без `/docs`, `/redoc`, `/openapi.json` (`docs/DEMO_NMVP2.md`)
- **Агенти:** orchestrator, verdict engine (0.3 / 0.4 / 0.3), IPSO, UA/RoBERTa за наявності моделі
- **БД:** Alembic, active learning (`UncertaintyPool`, feedback)
- **Dashboard:** `dashboard/Home.py` + аналітика; узгодженість полів — `docs/API_DASHBOARD_FIELD_AUDIT.md`
- **Перевірки репо:** `scripts/verify_nmvp2_repo.py` (A–H: репо, консистентність, git, PR, Home↔API, JSON Schema, README, візуальний чеклист)
- **Великі дані в git:** немає (ISOT тощо — `docs/DATASET_SETUP.md`)

---

## 4. Відкриті операційні пункти (не блокують звіт)

1. **GitHub:** `git push origin nmvp2/development` — за потреби вирівняти з GitLab.
2. **GitHub / GitLab:** branch protection, pull mirror — за бажанням (`docs/GIT_PRIMARY_MIRROR.md`).
3. **Реліз:** тег `nmvp2-v1.x` після прийняття капстоуну.
4. **Техборг:** warnings у тестах (async mock), `datetime.utcnow()` у `health.py` — з `docs/NMVP2_MISSING_ITEMS.md`.

---

## 5. Ключові документи

| Файл | Призначення |
|------|-------------|
| `docs/CURRENT_STATUS_NMVP2.md` | Короткий операційний статус (оновлюється) |
| `docs/CURSOR_NMVP2_CHECKS.md` | Опис перевірок A–H |
| `docs/DEMO_NMVP2.md` | Демо без Swagger |
| `docs/API_DASHBOARD_FIELD_AUDIT.md` | Поля JSON ↔ UI |
| `docs/GIT_PRIMARY_MIRROR.md` | Primary + mirror |

---

*Підготовлено як знімок для звіту капстоуну / керівництва; при нових push оновіть розділ 2 командами з `docs/CURRENT_STATUS_NMVP2.md`.*

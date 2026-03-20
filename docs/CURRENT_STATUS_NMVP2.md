# Поточний стан — truthlens-ua-analytics-v2 (NMVP2)

*Останнє оновлення документа: **2026-03-20 05:25** (звіт-знімок: `docs/NMVP2_STATUS_REPORT_20260320_0525.md`).*

## Репозиторії та гілки

| Ресурс | URL | Примітка |
|--------|-----|----------|
| **Primary** | [GitHub: truthlens-ua-analytics-v2](https://github.com/102012dl/truthlens-ua-analytics-v2) | Канонічний код |
| **Mirror** | [GitLab: truthlens-ua-analytics-v2](https://gitlab.com/102012dl/truthlens-ua-analytics-v2) | Дзеркало + `.gitlab-ci.yml` (SAST) |

## Збіг комітів (перевірка)

```powershell
git fetch origin
git fetch gitlab
git rev-parse main origin/main gitlab/main
git rev-parse nmvp2/development origin/nmvp2/development gitlab/nmvp2/development
```

**На знімок 2026-03-20 05:25:** `main` / `origin/main` / `gitlab/main` — **однаковий SHA** (`f256717…`). Локальна **`nmvp2/development`** і **`gitlab/nmvp2/development`** — **однаковий SHA** (`e2f9470…`); **`origin/nmvp2/development`** може відставати — тоді `git push origin nmvp2/development`.

Повний табличний звіт: **`docs/NMVP2_STATUS_REPORT_20260320_0525.md`**.

## Що входить у NMVP2 (скорочено)

- **API:** FastAPI, `POST /check`, `POST /api/v1/feedback`; опційно демо без Swagger (`TRUTHLENS_MINIMAL_OPENAPI`, `docs/DEMO_NMVP2.md`)
- **Агенти:** orchestrator, verdict engine, IPSO, UA/RoBERTa шар за наявності моделі
- **БД:** Alembic, моделі active learning (`UncertaintyPool`, тощо)
- **Dashboard:** Streamlit `dashboard/Home.py`, сторінки включно з аналітикою; аудит полів — `docs/API_DASHBOARD_FIELD_AUDIT.md`
- **Ноутбуки:** capstone pipeline + ISOT + UA NLP (перенесені з TruthLens-UA), RoBERTa notebook
- **Тести:** `pytest tests/` — **18** тестів; мок БД у `conftest`
- **Verify:** `python scripts/verify_nmvp2_repo.py` — **A–H** (див. `docs/CURSOR_NMVP2_CHECKS.md`)

## CI

- **GitHub Actions:** `.github/workflows/ci.yml` — `pytest` + `verify_nmvp2_repo.py` на push/PR до `main`, push до гілок `nmvp2/**`
- **GitLab:** SAST через `.gitlab-ci.yml` (шаблон Security/SAST)

## Локальні артефакти (не в git)

У робочій копії можуть бути **невідстежувані** каталоги `docs/audit/`, `docs/compare/` — локальні знімки порівняння репо. Їх можна закомітити за потреби або видалити / додати в `.gitignore`.

## Рекомендовані наступні кроки (операційні)

1. **GitHub:** за потреби `git push origin nmvp2/development`, щоб узгодити з GitLab.
2. **GitLab — Branch protection:** захистити `main` (merge через MR або обмежені ролі), **без** постійного force push.
3. **GitLab — Pull mirror** з GitHub (див. `docs/GIT_PRIMARY_MIRROR.md`), якщо хочете автоматичне підтягування замість лише `git push gitlab main`.
4. **GitHub — Branch protection** для `main` і вимога **успішного workflow «CI»** на PR.
5. **Реліз:** тег `nmvp2-v1.x` на `main` після прийняття капстоуну.
6. **README / Render:** оновити прод-деплой v2 окремим сервісом, коли буде готовий URL.

## Документи в репо

| Файл | Призначення |
|------|-------------|
| `docs/NMVP2_STATUS_REPORT_20260320_0525.md` | Звіт-знімок з SHA та підсумком |
| `docs/ARCHITECTURE_NMVP2.md` | Шари, моделі, формула, діаграми (канонічно до коду) |
| `docs/GIT_PRIMARY_MIRROR.md` | Primary + mirror, push, перевірка SHA |
| `docs/DATASET_SETUP.md` | Завантаження ISOT тощо |
| `data/README.md` | Що в `data/`, що не комітиться |

# Поточний стан — truthlens-ua-analytics-v2 (NMVP2)

*Останнє оновлення документа: 2026-03-20 (за даними локальної перевірки `git fetch`).*

## Репозиторії та гілки

| Ресурс | URL | Примітка |
|--------|-----|----------|
| **Primary** | [GitHub: truthlens-ua-analytics-v2](https://github.com/102012dl/truthlens-ua-analytics-v2) | Канонічний код |
| **Mirror** | [GitLab: truthlens-ua-analytics-v2](https://gitlab.com/102012dl/truthlens-ua-analytics-v2) | Дзеркало + `.gitlab-ci.yml` (SAST) |

## Збіг комітів (`main` та `nmvp2/development`)

Після останнього вирівнювання очікується **однаковий SHA** для:

- `origin/main`
- `gitlab/main`
- `origin/nmvp2/development`

Перевірка:

```powershell
git fetch origin
git fetch gitlab
git rev-parse origin/main gitlab/main origin/nmvp2/development
```

*Приклад після останнього оновлення цього файлу в git:* усі три ref збігалися (див. `git log -1 --oneline`). Після нових push перевіряйте лише вивід `git rev-parse` вище.

## Що входить у NMVP2 (скорочено)

- **API:** FastAPI, `POST /check`, `POST /api/v1/feedback`
- **Агенти:** orchestrator, verdict engine, IPSO, UA/RoBERTa шар за наявності моделі
- **БД:** Alembic, моделі active learning (`UncertaintyPool`, тощо)
- **Dashboard:** Streamlit `dashboard/Home.py`, сторінки включно з аналітикою
- **Ноутбуки:** capstone pipeline + ISOT + UA NLP (перенесені з TruthLens-UA), RoBERTa notebook
- **Тести:** `pytest tests/` — 18 тестів (мок БД у `conftest`)

## CI

- **GitLab:** SAST через шаблон у корені `.gitlab-ci.yml`
- **GitHub Actions:** за наявності workflow у `.github/workflows/` (перевірте репо)

## Локальні артефакти (не в git)

У робочій копії можуть бути **невідстежувані** каталоги `docs/audit/`, `docs/compare/` — локальні знімки порівняння репо. Їх можна закомітити за потреби або видалити / додати в `.gitignore`.

## Рекомендовані наступні кроки (операційні)

1. **GitLab — Branch protection:** захистити `main` (merge через MR або обмежені ролі), **без** постійного force push.
2. **GitLab — Pull mirror** з GitHub (див. `docs/GIT_PRIMARY_MIRROR.md`), якщо хочете автоматичне підтягування замість лише `git push gitlab main`.
3. **GitHub — Branch protection** для `main` + обов’язковий CI (pytest) на PR.
4. **Реліз:** тег `nmvp2-v1.x` на `main` після прийняття капстоуну.
5. **README / Render:** оновити прод-деплой v2 окремим сервісом, коли буде готовий URL.

## Документи в репо

| Файл | Призначення |
|------|-------------|
| `docs/GIT_PRIMARY_MIRROR.md` | Primary + mirror, push, перевірка SHA |
| `docs/DATASET_SETUP.md` | Завантаження ISOT тощо |
| `data/README.md` | Що в `data/`, що не комітиться |

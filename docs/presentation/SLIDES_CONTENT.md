# TruthLens UA Analytics v2 — контент для презентації (Canva / 12 слайдів)

*Джерело: репозиторій [truthlens-ua-analytics-v2](https://github.com/102012dl/truthlens-ua-analytics-v2). Метрики на ISOT/ноутбуках — з експериментів у `notebooks/`; демо-кейси — ілюстративні, не гарантія на проді.*

---

## Slide 01 — Title

- **Title:** TruthLens UA Analytics
- **Subtitle:** AI-платформа верифікації новин та виявлення ІПСО (NMVP2)
- **Author:** 102012dl · Neoversity MSCS DS&DA 2026
- **Design:** Темний фон `#0F172A`, білий текст, акцент `#38BDF8`

---

## Slide 02 — Problem

- **Title:** Дезінформація та навантаження на фактчекінг
- **Bullets (загальні орієнтири — уточнюйте джерела для захисту):**
  - Високий обсяг потенційно маніпулятивного контенту в соцмережах і месенджерах
  - Ручна перевірка однієї новини — хвилини vs ціль системи — секунди на запит
- **Visual:** Стовпчаста діаграма вердиктів REAL / SUSPICIOUS / FAKE (скрін з дашборду)

---

## Slide 03 — Solution

- **Title:** TruthLens UA Analytics v2
- **3 колонки:**
  - **ML:** LinearSVC + TF-IDF (joblib), fallback — правила
  - **ІПСО:** regex-детектор технік, penalty у `VerdictEngine`
  - **Verdict Engine:** `0.3·ML + 0.4·RoBERTa + 0.3·IPSO` (див. `verdict_engine.py`)
- **Formula:** `Final_Score = 0.3×ML + 0.4×RoBERTa + 0.3×IPSO_penalty`

---

## Slide 04 — Architecture

- **Title:** Архітектура NMVP2
- **Flow:** Streamlit / API → FastAPI → `TruthLensOrchestrator` → класифікатор → (опц.) ukr-roberta → ІПСО → скорер джерела → Verdict Engine → PostgreSQL
- **Документ:** `docs/ARCHITECTURE_NMVP2.md`

---

## Slide 05 — Datasets

- **Title:** Дані та відтворюваність
- **Таблиця:**
  | Джерело | Примітка |
  |---------|----------|
  | ISOT (EN) | Навчання baseline — ноутбук `01_isot_fake_news_mlflow.ipynb`, файли не в git |
  | Локальні / capstone | `notebooks/01`–`05`, `data/README.md` |
  | Довіра доменів | `SourceScorer`, зовнішні списки — за політикою проєкту |

---

## Slide 06 — ML experiments

- **Title:** Експерименти (MLflow / ноутбуки)
- **Приклад:** на ISOT у ноутбуках фіксується високий F1 для LinearSVC (див. вивід MLflow у репо, не фабрикувати цифри на слайді без скріну)
- **Примітка:** семантика UA — `youscan/ukr-roberta-base` при наявності `artifacts/ua_roberta_model`

---

## Slide 07 — IPSO

- **Title:** ІПСО-техніки
- **Приклади:** `urgency_injection`, `military_disinfo`, `deletion_threat`, `viral_call` (див. `ipso_detector.py`)
- **Узгодження з Verdict Engine:** penalty нормалізується (до 4 технік як «повна» маніпуляція в orchestrator)

---

## Slide 08 — Verdict Engine

- **Title:** Гібридна формула NMVP2
- **Формула:** `P_final = 0.30×ML + 0.40×RoBERTa + 0.30×IPSO`
- **Пороги:** REAL &lt; 0.35 | SUSPICIOUS 0.35–0.65 | FAKE &gt; 0.65
- **UI/API:** `formula_breakdown` у відповіді `POST /check`

---

## Slide 09 — Self-learning

- **Title:** Active learning (NMVP2)
- **Flow:** SUSPICIOUS → `UncertaintyPool` → feedback `POST /api/v1/feedback` → подальший ре-трейн через ноутбуки / `scripts/self_learning_pipeline.py` (ручний запуск циклу)

---

## Slide 10 — Live demo

- **Title:** Демо
- **Локально:** `uvicorn` + `streamlit run dashboard/Home.py`
- **Приклад запиту:** `POST /check` з тестовим текстом (див. `tests/test_check.py`)
- **URL продакшену:** підставте фактичний Render після деплою (`docs/RENDER_DEPLOY.md`)

---

## Slide 11 — Engineering

- **Title:** Якість інженерії
- **Tests:** `pytest tests/` (автоматично в CI)
- **Verify:** `scripts/verify_nmvp2_repo.py` (структура NMVP2 + поля API)
- **Rate limit:** `slowapi` на `/check` (`RATE_LIMIT_PER_MINUTE`)

---

## Slide 12 — Roadmap

- **Title:** Розвиток і монетизація (концепт)
- **Версії:** NMVP1 (архів) → NMVP2 (поточний репо) → подальші: real-time, інтеграції
- **Pricing:** орієнтовно з README (Free / Pro / Enterprise) — для захисту уточніть як гіпотеза бізнес-моделі

---

*Кінець чернетки. Перед друком оновіть скріншоти, URL Render і будь-які статистичні твердження посиланнями на ноутбуки або публікації.*

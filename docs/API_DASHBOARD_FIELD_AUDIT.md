# Аудит полів: `CheckResponse` (JSON) ↔ Streamlit `Home.py`

Оновлено разом із схемою `app/schemas/check.py`.

## Поля API (`POST /check`)

| Поле | Тип | Відображення на Home (Головна) |
|------|-----|--------------------------------|
| `article_id` | int | Під метриками (caption) + feedback widget |
| `verdict` | enum | Заголовок картки + колір |
| `credibility_score` | float | Метрика «Рейтинг довіри» |
| `fake_score` | float | Метрика «Fake Score» |
| `confidence` | float | Метрика «Впевненість» |
| `ipso_techniques` | list | Список технік |
| `source_credibility` | float | Caption (метадані) |
| `explanation_uk` | str | `st.info` |
| `source_domain` | str | Caption |
| `language` | str | Caption |
| `processing_time_ms` | float | Метрика «Час» |
| `formula_breakdown` | object? | Блок «Розрахунок Verdict Engine» (якщо не `null`) |

## Узгодженість шляхів

- **API:** після змін у схемі `formula_breakdown` передається з orchestrator у відповіді JSON (NMVP2).
- **Вбудований аналіз:** `analyze_text_locally()` повертає ті самі ключі, що й типовий JSON від API, щоб UI не розходився.

## Автоматична перевірка

```text
python scripts/verify_nmvp2_repo.py
```

Секція **E** порівнює імена полів `CheckResponse` з використанням `result['…']` / `result.get('…')` у `dashboard/Home.py`.

Секція **H** порівнює `properties` з `CheckResponse.model_json_schema()` з ключами `CheckResponse.model_fields` (без виклику `app.openapi()` — лише Pydantic JSON Schema).

Тест **`tests/test_check.py::test_check_response_has_all_fields`** перевіряє, що фактична JSON-відповідь містить усі ключі з `CheckResponse.model_fields` (без дублювання списку полів у коді тесту).

import os
import sys
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

# Батьківський каталог dashboard/ (файл у pages/)
_DASH = Path(__file__).resolve().parent.parent
if str(_DASH) not in sys.path:
    sys.path.insert(0, str(_DASH))
from local_analyze import analyze_text_locally

st.set_page_config(page_title="Demo Cases Evaluation", page_icon="🧪", layout="wide")
st.markdown("## Оцінка на тестових кейсах (Gold Dataset)")
st.info(
    "Перевірка тест-кейсів через **REST API**; якщо API недоступний (sleep Render, невірний URL, 5xx) — "
    "використовується **локальний** NMVP2-fallback (ті самі евристики, що на Головній)."
)

IS_RENDER = "RENDER" in os.environ or bool(os.environ.get("RENDER_EXTERNAL_URL"))
# Узгоджено з render.yaml; якщо сервіс названо інакше (напр. truthlens-ua-v2-api) — задайте API_URL у env dashboard.
_DEFAULT_RENDER_API = "https://truthlens-ua-analytics-v2-api.onrender.com"
DEFAULT_API = os.environ.get(
    "API_URL",
    _DEFAULT_RENDER_API if IS_RENDER else "http://127.0.0.1:8000",
)
API_URL = DEFAULT_API.strip().rstrip("/")

with st.expander("Діагностика API", expanded=False):
    st.code(f"API_URL effective: {API_URL}\nRENDER: {IS_RENDER}", language="text")
    st.caption(
        "Якщо всі рядки ERROR / local_fallback: перевірте змінну середовища **API_URL** "
        "у сервісі **dashboard** на Render (має вказувати на ваш **API** hostname, напр. …-api.onrender.com)."
    )

FALLBACK_DEMO_DATA = [
    {"id": 1, "text": "ТЕРМІНОВО!!! ЗСУ ЗДАЛИ Харків! Поширте до видалення!!!", "expected_label": "FAKE", "language": "uk"},
    {"id": 2, "text": "НБУ підвищив облікову ставку до 16%.", "expected_label": "REAL", "language": "uk"},
    {"id": 3, "text": "Можливо, скоро запровадять нові штрафи.", "expected_label": "SUSPICIOUS", "language": "uk"},
    {"id": 4, "text": "Зеленський таємно продав Крим за мільярд доларів", "expected_label": "FAKE", "language": "uk"},
    {"id": 5, "text": "Верховна Рада ухвалила держбюджет", "expected_label": "REAL", "language": "uk"},
    {"id": 6, "text": "Деякі джерела стверджують про нові обмеження", "expected_label": "SUSPICIOUS", "language": "uk"},
    {"id": 7, "text": "ШОКУЮЧІ ВІДЕО! Влада приховує правду!", "expected_label": "FAKE", "language": "uk"},
    {"id": 8, "text": "МВФ схвалив черговий транш для України", "expected_label": "REAL", "language": "uk"},
    {"id": 9, "text": "Незалежні аналітики попереджають про кризу.", "expected_label": "SUSPICIOUS", "language": "uk"},
    {"id": 10, "text": "УВАГА!!! Мобілізацію оголошено таємно!", "expected_label": "FAKE", "language": "uk"},
]


def load_cases():
    try:
        df = pd.read_csv("data/gold/demo_cases.csv")
        return df.to_dict("records")
    except Exception:
        return FALLBACK_DEMO_DATA


cases = load_cases()

if "eval_results" not in st.session_state:
    st.session_state.eval_results = []


def _fetch_via_api(text: str, base: str, timeout: float) -> tuple[str | None, float, str, str | None]:
    """
    Returns (verdict or None, score, ipso_csv, error_hint).
    error_hint set when HTTP != 200 or network error.
    """
    if not base or base.lower() in ("", "none"):
        return None, 0.0, "", "API_URL empty"
    try:
        url = base.replace("http://localhost:", "http://127.0.0.1:")
        resp = requests.post(f"{url}/check", json={"text": text}, timeout=timeout)
        if resp.status_code != 200:
            return None, 0.0, "", f"HTTP {resp.status_code}"
        data = resp.json()
        v = data.get("verdict")
        if v not in ("REAL", "FAKE", "SUSPICIOUS"):
            return None, 0.0, "", "invalid JSON verdict"
        score = float(data.get("credibility_score", 0.0))
        ipso = ", ".join(data.get("ipso_techniques", []))
        return v, score, ipso, None
    except Exception as e:
        return None, 0.0, "", str(e)[:120]


if st.button("🚀 Run All Checks", type="primary"):
    results = []
    # Перший запит на безкоштовному Render часто «холодний» — більший timeout
    timeout = 60.0 if IS_RENDER else 20.0
    with st.spinner("Виконується масова перевірка..."):
        for i, case in enumerate(cases):
            text = case.get("text", "")
            expected = case.get("expected_label", "UNKNOWN")

            got_verdict = "ERROR"
            score = 0.0
            ipso = ""
            source = "none"

            v, sc, ip, err = _fetch_via_api(text, API_URL, timeout=timeout)
            if v is not None:
                got_verdict = v
                score = sc
                ipso = ip
                source = "API"
            else:
                try:
                    loc = analyze_text_locally(text)
                    got_verdict = loc["verdict"]
                    score = float(loc["credibility_score"])
                    ipso = ", ".join(loc.get("ipso_techniques", []))
                    source = f"local_fallback ({err or 'unknown'})"
                except Exception as ex:
                    got_verdict = "ERROR"
                    source = f"local_failed: {str(ex)[:100]}"

            match_ok = got_verdict == expected
            results.append(
                {
                    "#": i + 1,
                    "Text": text[:70] + "..." if len(text) > 70 else text,
                    "Expected": expected,
                    "Got": got_verdict,
                    "Match": "✅ OK" if match_ok else "❌ ERR",
                    "Score": f"{score:.1f}",
                    "IPSO": ipso[:80] + ("..." if len(ipso) > 80 else ""),
                    "Source": source[:60],
                }
            )
    st.session_state.eval_results = results

if st.session_state.eval_results:
    df_res = pd.DataFrame(st.session_state.eval_results)

    correct = len(df_res[df_res["Match"] == "✅ OK"])
    total = len(df_res)
    # «Помилка» лише якщо залишився чистий ERROR (не повинно статися після fallback)
    errors = len(df_res[df_res["Got"] == "ERROR"])
    accuracy = (correct / total) * 100 if total > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Accuracy", f"{accuracy:.1f}%")
    c2.metric("Total Cases", total)
    c3.metric("Correct Matches", correct)
    c4.metric("Errors (no verdict)", errors)

    st.dataframe(df_res, use_container_width=True)

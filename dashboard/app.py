"""TruthLens UA Analytics — Single-page Streamlit dashboard v3.0"""
import streamlit as st
import httpx
import os
import re
import pandas as pd
from datetime import datetime

# ── Config ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="TruthLens UA Analytics",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Environment ───────────────────────────────────────────────────
IS_RENDER = "RENDER" in os.environ or "onrender.com" in os.environ.get("RENDER_EXTERNAL_URL", "")
DEFAULT_API = os.environ.get("API_URL",
    "https://truthlens-ua-analytics.onrender.com" if IS_RENDER
    else "http://localhost:8000"
)

# ── Session state init ────────────────────────────────────────────
if "text_input" not in st.session_state:
    st.session_state.text_input = ""
if "result" not in st.session_state:
    st.session_state.result = None
if "history" not in st.session_state:
    st.session_state.history = []

# ── Sidebar ───────────────────────────────────────────────────────
st.sidebar.title("⚙️ Налаштування")
api_url = st.sidebar.text_input("API URL", value=DEFAULT_API)
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Статистика")
st.sidebar.metric("Проаналізовано", len(st.session_state.history))
fake_count = sum(1 for h in st.session_state.history if h.get("verdict") == "FAKE")
real_count = sum(1 for h in st.session_state.history if h.get("verdict") == "REAL")
st.sidebar.metric("🔴 FAKE", fake_count)
st.sidebar.metric("🟢 REAL", real_count)

# ── Styles ────────────────────────────────────────────────────────
st.markdown("""
<style>
.verdict-FAKE    { color: #EF4444; font-weight: bold; font-size: 1.5rem; }
.verdict-REAL    { color: #22C55E; font-weight: bold; font-size: 1.5rem; }
.verdict-SUSPICIOUS { color: #F59E0B; font-weight: bold; font-size: 1.5rem; }
.metric-box { background: #1E293B; border-radius: 8px; padding: 12px; margin: 4px 0; }
</style>
""", unsafe_allow_html=True)

# ── Built-in analyzer (no API needed) ─────────────────────────────
def analyze_builtin(text: str) -> dict:
    """Rule-based fallback classifier."""
    import math
    text_lower = text.lower()
    ipso_patterns = {
        "urgency_injection":       r"терміново|breaking|зараз|негайно|увага",
        "caps_abuse":              None,
        "deletion_threat":         r"до видалення|встигніть|видалять|успіть",
        "viral_call":              r"поширте|пересилайте|діліться",
        "conspiracy_framing":      r"приховують|замовчують|вони знають",
        "anonymous_sources":       r"анонімн\w+ джерел|за даними тг",
        "military_disinfo":        r"зсу здал|армія відступ|фронт прорв",
        "awakening_appeal":        r"прокиньтесь|відкрийте очі|вас обманюють",
        "authority_impersonation": r"зеленськ\w+ заявив|моз повідомив|оп підтвердив",
        "deepfake_indicator":      r"фейкове відео|синтезован|ai-відео|дипфейк",
    }
    detected = []
    for name, pattern in ipso_patterns.items():
        if name == "caps_abuse":
            upper = sum(1 for c in text if c.isupper())
            letters = sum(1 for c in text if c.isalpha())
            if letters > 10 and upper / max(letters, 1) > 0.30:
                detected.append(name)
        elif pattern and re.search(pattern, text_lower):
            detected.append(name)

    ipso_score = min(len(detected) * 0.25, 0.95)
    fake_score = round(max(0.05, ipso_score if detected else 0.1), 4)
    if len(detected) >= 2:
        verdict = "FAKE"
    elif len(detected) == 1 or fake_score >= 0.40:
        verdict = "SUSPICIOUS"
    else:
        verdict = "REAL"
    credibility = round((1.0 - fake_score) * 100, 1)
    parts = []
    if verdict == "FAKE":
        parts.append(f"Текст класифіковано як НЕДОСТОВІРНИЙ (score={fake_score:.2f}).")
        if detected:
            parts.append(f"Виявлено ІПСО: {', '.join(detected)}.")
    elif verdict == "SUSPICIOUS":
        parts.append(f"Текст потребує перевірки (score={fake_score:.2f}).")
    else:
        parts.append(f"Текст достовірний (score={fake_score:.2f}).")
    return {
        "verdict": verdict,
        "credibility_score": credibility,
        "fake_score": fake_score,
        "confidence": round(min(1.0, fake_score * 1.5), 4),
        "ipso_techniques": detected,
        "explanation_uk": " ".join(parts),
        "processing_time_ms": 8.0,
        "method": "built-in"
    }

def analyze_via_api(text: str, url: str) -> dict | None:
    """Try API first, fallback to built-in."""
    try:
        payload = {"url": text} if text.startswith("http") else {"text": text}
        r = httpx.post(f"{url.rstrip('/')}/check",
                       json=payload, timeout=15)
        if r.status_code == 200:
            data = r.json()
            data["method"] = "api"
            return data
    except Exception:
        pass
    return None

# ── Main UI ───────────────────────────────────────────────────────
st.title("🔍 TruthLens UA Analytics")
st.markdown("*AI-платформа верифікації новин та оцінки достовірності джерел*")
st.divider()

# Quick Check form
st.subheader("🔬 Перевірити новину")
col_in, col_ex = st.columns([3, 1])

with col_in:
    text_value = st.text_area(
        "Текст або URL новини:",
        value="",
        placeholder="Вставте текст або URL для перевірки...",
        height=120,
        key="main_input"
    )

with col_ex:
    st.markdown("**Приклади:**")
    if st.button("🔴 Фейк", use_container_width=True):
        st.session_state["prefill"] = "ТЕРМІНОВО!!! ЗСУ ЗДАЛИ Харків! Поширте до видалення!!!"
        st.rerun()
    if st.button("🟢 Реальна", use_container_width=True):
        st.session_state["prefill"] = "НБУ підвищив облікову ставку до 16% на засіданні."
        st.rerun()
    if st.button("🟡 Підозріла", use_container_width=True):
        st.session_state["prefill"] = "Можливо армія має проблеми — анонімне джерело."
        st.rerun()

# Handle prefill
if "prefill" in st.session_state:
    text_value = st.session_state.pop("prefill")

if st.button("⚡ Аналізувати", type="primary", use_container_width=False):
    if text_value and text_value.strip():
        with st.spinner("Аналізую..."):
            result = analyze_via_api(text_value.strip(), api_url)
            if not result:
                result = analyze_builtin(text_value.strip())
            result["text"] = text_value.strip()[:100]
            result["timestamp"] = datetime.now().strftime("%H:%M:%S")
            st.session_state.result = result
            st.session_state.history.insert(0, result)
            if len(st.session_state.history) > 50:
                st.session_state.history = st.session_state.history[:50]
    else:
        st.warning("Введіть текст або URL для аналізу")

# Display result
if st.session_state.result:
    r = st.session_state.result
    verdict = r.get("verdict", "?")
    score = r.get("credibility_score", 0)
    fake_s = r.get("fake_score", 0)
    conf = r.get("confidence", 0)
    ipso = r.get("ipso_techniques", [])
    explanation = r.get("explanation_uk", "")
    method = r.get("method", "built-in")

    st.divider()
    emoji = {"REAL": "🟢", "FAKE": "🔴", "SUSPICIOUS": "🟡"}.get(verdict, "❓")
    st.markdown(f"<div class='verdict-{verdict}'>{emoji} {verdict}</div>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Достовірність", f"{score}%")
    c2.metric("Fake Score", f"{fake_s:.3f}")
    c3.metric("Впевненість", f"{conf:.3f}")
    c4.metric("ІПСО технік", len(ipso))

    if ipso:
        st.warning(f"⚠️ ІПСО маніпуляції: **{', '.join(ipso)}**")
    else:
        st.success("✅ Маніпуляцій не виявлено")

    st.info(f"💬 {explanation}")
    st.caption(f"Метод: {method} | Час: {r.get('processing_time_ms', 0):.0f}ms | {r.get('timestamp','')}")

# History
if st.session_state.history:
    st.divider()
    st.subheader("📋 Історія аналізів")
    history_data = []
    for h in st.session_state.history[:10]:
        v = h.get("verdict", "?")
        em = {"REAL": "🟢", "FAKE": "🔴", "SUSPICIOUS": "🟡"}.get(v, "❓")
        history_data.append({
            "Час": h.get("timestamp", ""),
            "Текст": h.get("text", "")[:60] + "...",
            "Вердикт": f"{em} {v}",
            "Достовірність": f"{h.get('credibility_score', 0)}%",
            "ІПСО": len(h.get("ipso_techniques", [])),
        })
    st.dataframe(pd.DataFrame(history_data), use_container_width=True)

    if st.button("🗑️ Очистити історію"):
        st.session_state.history = []
        st.session_state.result = None
        st.rerun()

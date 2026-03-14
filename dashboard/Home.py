import streamlit as st, httpx, os, pandas as pd
from sqlalchemy import create_engine, text

st.set_page_config(
    page_title="TruthLens UA Analytics",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

DB_URL = os.getenv("DATABASE_URL","").replace("asyncpg","psycopg2").replace("+asyncpg","")
API_URL = os.getenv("API_URL", "http://api:8000")

@st.cache_data(ttl=60)
def get_stats():
    try:
        engine = create_engine(DB_URL)
        with engine.connect() as conn:
            total = conn.execute(text("SELECT count(*) FROM articles")).scalar()
            fake = conn.execute(text(
                "SELECT count(*) FROM claim_checks WHERE verdict='FAKE'")).scalar()
            real = conn.execute(text(
                "SELECT count(*) FROM claim_checks WHERE verdict='REAL'")).scalar()
            avg_cred = conn.execute(text(
                "SELECT round(avg(credibility_score)::numeric,1) FROM claim_checks")).scalar()
        return {"total":total,"fake":fake,"real":real,"avg_cred":avg_cred or 0}
    except Exception:
        return {"total":0,"fake":0,"real":0,"avg_cred":0}

st.title("🔍 TruthLens UA Analytics")
st.markdown("*AI-платформа верифікації новин та оцінки достовірності джерел*")
st.divider()

# Metric cards
stats = get_stats()
col1, col2, col3, col4 = st.columns(4)
col1.metric("📰 Проаналізовано", stats["total"])
col2.metric("🔴 FAKE виявлено", stats["fake"])
col3.metric("🟢 REAL підтверджено", stats["real"])
col4.metric("⭐ Середня достовірність", f"{stats['avg_cred']}%")
st.divider()

# Quick Check form
st.subheader("🔬 Перевірити новину")
with st.form("check_form"):
    input_text = st.text_area("Текст або URL новини:", height=100,
        placeholder="Вставте текст або URL для перевірки...")
    submitted = st.form_submit_button("⚡ Перевірити", type="primary")

if submitted and input_text:
    with st.spinner("Аналізую..."):
        try:
            payload = {"url": input_text} if input_text.startswith("http") \
                      else {"text": input_text}
            r = httpx.post(f"{API_URL}/check", json=payload, timeout=30)
            result = r.json()
            verdict = result.get("verdict", "?")
            score = result.get("credibility_score", 0)
            color = {"REAL":"🟢","FAKE":"🔴","SUSPICIOUS":"🟡"}.get(verdict,"❓")
            st.success(f"{color} **{verdict}** — достовірність: **{score}%**")
            if result.get("ipso_techniques"):
                st.warning(f"⚠️ ІПСО: {', '.join(result['ipso_techniques'])}")
            st.info(result.get("explanation_uk",""))
            st.json(result)
        except Exception as e:
            st.error(f"Помилка: {e}")
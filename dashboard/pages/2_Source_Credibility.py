import streamlit as st, pandas as pd, plotly.express as px
from sqlalchemy import create_engine, text
import os

DB_URL = os.getenv("DATABASE_URL","").replace("asyncpg","psycopg2").replace("+asyncpg","")

@st.cache_data(ttl=120)
def get_sources_data():
    try:
        engine = create_engine(DB_URL)
        with engine.connect() as conn:
            sources = conn.execute(text("""
                SELECT s.domain, s.credibility_score, s.article_count,
                       COUNT(a.id) as analyzed_articles,
                       AVG(cc.credibility_score) as avg_article_credibility,
                       COUNT(CASE WHEN cc.verdict = 'FAKE' THEN 1 END) as fake_count,
                       COUNT(CASE WHEN cc.verdict = 'REAL' THEN 1 END) as real_count,
                       MAX(a.created_at) as last_seen
                FROM sources s
                LEFT JOIN articles a ON s.id = a.source_id
                LEFT JOIN claims cl ON a.id = cl.article_id
                LEFT JOIN claim_checks cc ON cl.id = cc.claim_id
                GROUP BY s.id, s.domain, s.credibility_score, s.article_count
                ORDER BY s.credibility_score DESC
            """)).fetchall()
            
        return sources
    except Exception as e:
        st.error(f"Database error: {e}")
        return []

def get_credibility_label(score):
    if score >= 0.75: return "HIGH"
    if score >= 0.45: return "MEDIUM"
    return "LOW"

def get_credibility_color(score):
    if score >= 0.75: return "#16A34A"
    if score >= 0.45: return "#D97706"
    return "#DC2626"

st.title("🏆 Source Credibility Analysis")
st.markdown("*Аналіз достовірності медіа-джерел*")

# Filter controls
col1, col2 = st.columns([2, 1])
with col1:
    min_score = st.slider("Мінімальний рейтинг достовірності:", 0, 100, 0, 5)

with col2:
    min_articles = st.number_input("Мінімум статей:", min_value=0, value=1, step=1)

data = get_sources_data()

if data:
    # Filter data
    filtered_data = [
        (s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7])
        for s in data
        if s[1] * 100 >= min_score and s[3] >= min_articles
    ]
    
    if filtered_data:
        df = pd.DataFrame(filtered_data, columns=[
            "domain", "source_score", "total_articles", "analyzed_articles", 
            "avg_article_credibility", "fake_count", "real_count", "last_seen"
        ])
        
        # Add computed columns
        df["credibility_label"] = df["source_score"].apply(get_credibility_label)
        df["credibility_color"] = df["source_score"].apply(get_credibility_color)
        df["fake_percentage"] = (df["fake_count"] / (df["fake_count"] + df["real_count"]) * 100).round(1)
        df["real_percentage"] = (df["real_count"] / (df["fake_count"] + df["real_count"]) * 100).round(1)
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📊 Всього джерел", len(df))
        col2.metric("🟢 HIGH джерел", len(df[df["credibility_label"] == "HIGH"]))
        col3.metric("🟡 MEDIUM джерел", len(df[df["credibility_label"] == "MEDIUM"]))
        col4.metric("🔴 LOW джерел", len(df[df["credibility_label"] == "LOW"]))
        
        st.divider()
        
        # Distribution histogram
        st.subheader("📈 Розподіл рейтингів достовірності")
        fig = px.histogram(df, x="source_score", nbins=20, 
                          title="Розподіл рейтингів достовірності джерел",
                          labels={"source_score": "Рейтинг достовірності", "count": "Кількість джерел"})
        fig.update_layout(bargap=0.1)
        st.plotly_chart(fig, use_container_width=True)
        
        # Sources table
        st.subheader("📋 Таблиця джерел")
        
        # Format columns for display
        display_df = df.copy()
        display_df["source_score"] = display_df["source_score"].apply(lambda x: f"{x:.1%}")
        display_df["avg_article_credibility"] = display_df["avg_article_credibility"].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")
        display_df["credibility_badge"] = display_df.apply(
            lambda row: f"🟢 {row['credibility_label']}" if row['credibility_label'] == 'HIGH' 
                      else f"🟡 {row['credibility_label']}" if row['credibility_label'] == 'MEDIUM'
                      else f"🔴 {row['credibility_label']}", axis=1
        )
        
        # Reorder columns
        display_df = display_df[[
            "domain", "credibility_badge", "source_score", "total_articles", 
            "analyzed_articles", "avg_article_credibility", "fake_percentage", 
            "real_percentage", "last_seen"
        ]]
        
        display_df.columns = [
            "Домен", "Рівень", "Рейтинг джерела", "Всього статей", 
            "Проаналізовано", "Середня достовірність", "% FAKE", 
            "% REAL", "Останнє аналізовано"
        ]
        
        st.dataframe(display_df, use_container_width=True)
        
        # Download button
        csv = display_df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 Завантажити CSV",
            data=csv,
            file_name="source_credibility_analysis.csv",
            mime="text/csv"
        )
        
    else:
        st.warning("Немає джерел, що відповідають вибраним фільтрам.")
else:
    st.info("Немає даних про джерела в базі даних.")
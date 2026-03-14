import streamlit as st, pandas as pd, plotly.express as px, plotly.graph_objects as go
from sqlalchemy import create_engine, text
import os
from datetime import datetime, timedelta

DB_URL = os.getenv("DATABASE_URL","").replace("asyncpg","psycopg2").replace("+asyncpg","")

@st.cache_data(ttl=120)
def get_executive_data():
    try:
        engine = create_engine(DB_URL)
        with engine.connect() as conn:
            # Verdict distribution
            verdicts = conn.execute(text("""
                SELECT verdict, COUNT(*) as count 
                FROM claim_checks 
                GROUP BY verdict
            """)).fetchall()
            
            # Daily trends (last 7 days)
            daily = conn.execute(text("""
                SELECT DATE(created_at) as date, COUNT(*) as count
                FROM articles 
                WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
                GROUP BY DATE(created_at)
                ORDER BY date
            """)).fetchall()
            
            # Top sources
            sources = conn.execute(text("""
                SELECT s.domain, s.credibility_score, COUNT(a.id) as article_count,
                       AVG(cc.credibility_score) as avg_credibility
                FROM sources s
                LEFT JOIN articles a ON s.id = a.source_id
                LEFT JOIN claims cl ON a.id = cl.article_id
                LEFT JOIN claim_checks cc ON cl.id = cc.claim_id
                WHERE a.id IS NOT NULL
                GROUP BY s.id, s.domain, s.credibility_score
                ORDER BY article_count DESC
                LIMIT 5
            """)).fetchall()
            
            # Overall credibility gauge
            avg_cred = conn.execute(text("""
                SELECT ROUND(AVG(credibility_score)::numeric, 1) as avg_cred
                FROM claim_checks
            """)).scalar()
            
        return {
            "verdicts": verdicts,
            "daily": daily,
            "sources": sources,
            "avg_cred": avg_cred or 0
        }
    except Exception as e:
        st.error(f"Database error: {e}")
        return {"verdicts": [], "daily": [], "sources": [], "avg_cred": 0}

st.title("📊 Executive Summary")

st.markdown("*Аналітична панель TruthLens UA Analytics*")

data = get_executive_data()

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
total_checks = sum(v[1] for v in data["verdicts"])
fake_count = dict(data["verdicts"]).get("FAKE", 0)
real_count = dict(data["verdicts"]).get("REAL", 0)

col1.metric("📰 Загальних перевірок", total_checks)
col2.metric("🔴 FAKE", fake_count, f"{fake_count/total_checks*100:.1f}%" if total_checks > 0 else "0%")
col3.metric("🟢 REAL", real_count, f"{real_count/total_checks*100:.1f}%" if total_checks > 0 else "0%")
col4.metric("⭐ Середня достовірність", f"{data['avg_cred']}%")

st.divider()

# Charts row
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Розподіл вердиктів")
    if data["verdicts"]:
        verdict_df = pd.DataFrame(data["verdicts"], columns=["verdict", "count"])
        colors = {"FAKE": "#DC2626", "REAL": "#16A34A", "SUSPICIOUS": "#D97706"}
        fig = px.pie(verdict_df, values="count", names="verdict", 
                    color="verdict", color_discrete_map=colors,
                    title="Вердикти перевірок")
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Немає даних для відображення")

with col2:
    st.subheader("📅 Активність (останні 7 днів)")
    if data["daily"]:
        daily_df = pd.DataFrame(data["daily"], columns=["date", "count"])
        fig = px.line(daily_df, x="date", y="count", 
                     title="Кількість аналізів по днях",
                     markers=True)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Немає даних за останні 7 днів")

# Bottom row
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Топ джерела")
    if data["sources"]:
        sources_df = pd.DataFrame(data["sources"], 
                                columns=["domain", "credibility_score", "article_count", "avg_credibility"])
        fig = px.bar(sources_df, x="article_count", y="domain", 
                    title="Топ 5 джерел за кількістю статей",
                    orientation="h")
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Немає даних про джерела")

with col2:
    st.subheader("🎯 Загальна достовірність")
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = data["avg_cred"],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Середній рейтинг достовірності (%)"},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "#16A34A"},
            'steps': [
                {'range': [0, 45], 'color': "#DC2626"},
                {'range': [45, 75], 'color': "#D97706"},
                {'range': [75, 100], 'color': "#16A34A"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

# Detailed table
st.subheader("📋 Детальна статистика джерел")
if data["sources"]:
    sources_df = pd.DataFrame(data["sources"], 
                            columns=["domain", "credibility_score", "article_count", "avg_credibility"])
    sources_df.columns = ["Домен", "Рейтинг джерела", "К-сть статей", "Середня достовірність"]
    sources_df["Рейтинг джерела"] = sources_df["Рейтинг джерела"].apply(lambda x: f"{x:.1%}")
    sources_df["Середня достовірність"] = sources_df["Середня достовірність"].apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")
    st.dataframe(sources_df, use_container_width=True)
else:
    st.info("Немає даних для таблиці")
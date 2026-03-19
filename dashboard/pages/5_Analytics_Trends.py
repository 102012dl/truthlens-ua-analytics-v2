import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Analytics & Trends | TruthLens UA",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Аналітика та Тренди (NMVP2)")
st.markdown("Моніторинг інформаційного простору, ІПСО-наративів та системи самонавчання.")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Індекс ІПСО-атак (останні 7 днів)")
    st.markdown("Частота виявлення проросійських маніпуляцій та фейків.")
    
    # Mock data for 7 days
    dates = [datetime.today() - timedelta(days=i) for i in range(6, -1, -1)]
    date_strs = [d.strftime("%Y-%m-%d") for d in dates]
    
    # Simulate trend
    fake_freq = [12, 18, 15, 25, 30, 22, 28] 
    
    df_trend = pd.DataFrame({
        "Дата": date_strs,
        "Кількість Фейків": fake_freq
    })
    
    chart_trend = alt.Chart(df_trend).mark_line(point=True, color="red").encode(
        x='Дата:O',
        y='Кількість Фейків:Q',
        tooltip=['Дата', 'Кількість Фейків']
    ).properties(height=300)
    
    st.altair_chart(chart_trend, use_container_width=True)

with col2:
    st.subheader("Слабкі місця та Наративи")
    st.markdown("Топ виявлених маніпулятивних тактик.")
    
    tactics = [
        "urgency_injection", 
        "military_disinfo", 
        "viral_call", 
        "authority_impersonation", 
        "conspiracy_framing"
    ]
    counts = [45, 38, 30, 22, 15]
    
    df_tactics = pd.DataFrame({
        "Тактика": tactics,
        "Кількість": counts
    })
    
    chart_tactics = alt.Chart(df_tactics).mark_bar(color="orange").encode(
        x='Кількість:Q',
        y=alt.Y('Тактика:N', sort='-x'),
        tooltip=['Тактика', 'Кількість']
    ).properties(height=300)
    
    st.altair_chart(chart_tactics, use_container_width=True)

st.markdown("---")

st.subheader("🤖 Self-Learning Logs (Active Learning)")
st.markdown("Система автоматично збирає 'сіру зону' (Suspicious) та перенавчається на основі зворотного зв'язку.")

col_sl1, col_sl2, col_sl3 = st.columns(3)
col_sl1.metric("Uncertainty Pool (Очікують)", "24 записів", "+5 сьогодні")
col_sl2.metric("User Feedback (Підтверджено)", "18 записів", "+3 сьогодні")
col_sl3.metric("Dataset Registry (Синтетичні)", "1,250 слів", "v_20260319")

st.markdown("**Останні додані семпли до пулу перенавчання (Сьогодні):**")

# Mock SL logs
df_logs = pd.DataFrame(
    [
        {"Час": "10:15", "Текст (Snippet)": "У Києві терміново...", "Вердикт Моделі": "SUSPICIOUS", "Конфіденс": 0.52, "Валідація": "Agree (FAKE)"},
        {"Час": "11:30", "Текст (Snippet)": "За даними анонімних...", "Вердикт Моделі": "SUSPICIOUS", "Конфіденс": 0.45, "Валідація": "Pending"},
        {"Час": "14:22", "Текст (Snippet)": "Міністерство офіційно...", "Вердикт Моделі": "SUSPICIOUS", "Конфіденс": 0.58, "Валідація": "Disagree (REAL)"},
        {"Час": "16:05", "Текст (Snippet)": "ЗСУ залишили позиції...", "Вердикт Моделі": "SUSPICIOUS", "Конфіденс": 0.61, "Валідація": "Agree (FAKE)"},
    ]
)

st.dataframe(df_logs, use_container_width=True, hide_index=True)

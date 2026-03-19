import streamlit as st

st.set_page_config(page_title="About Platform - TruthLens", page_icon="ℹ️")

st.title("Про TruthLens UA Platform")
st.markdown("### AI-платформа верифікації UA новин. NMVP2.")

st.markdown("""
Ця система використовує гібридний мульти-агентний підхід, що поєднує машинне навчання (ML) 
та аналіз інформаційно-психологічних операцій (ІПСО) для оцінки достовірності текстів українською мовою.

**Версія:** NMVP2 (Full Program v4.0)
**Дата:** 2026

### Основні технології:
- **ML Моделі:** LinearSVC (базова), ukr-roberta-base (семантика)
- **Backend:** FastAPI, SQLAlchemy, PostgreSQL
- **Frontend:** Streamlit, Plotly
- **MLOps:** MLflow, DagsHub
- **Моніторинг:** Prometheus, Grafana

### Корисні посилання:
- [GitHub Repository](https://github.com/102012dl/truthlens-ua-platform)
- [GitLab Repository](https://gitlab.com/102012dl/truthlens-ua-platform)
""")

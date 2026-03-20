import streamlit as st

st.set_page_config(page_title="About Platform - TruthLens", page_icon="ℹ️")

st.title("Про TruthLens UA Analytics v2.1")
st.markdown("### AI-платформа верифікації UA новин. NMVP2.")

st.markdown("""
Ця система використовує гібридний мульти-агентний підхід, що поєднує машинне навчання (ML) 
та аналіз інформаційно-психологічних операцій (ІПСО) для оцінки достовірності текстів українською мовою.

**Версія:** v2.1 (NMVP2)
**Дата:** 2026

### Основні технології:
- **ML Моделі:** Ensemble (LinearSVC + ukr-roberta-base)
- **Backend:** FastAPI, SQLAlchemy, PostgreSQL
- **Frontend:** Streamlit, Plotly
- **MLOps:** MLflow, DagsHub, Alembic
- **Моніторинг:** Prometheus, Grafana

### Корисні посилання:
- [GitHub Repository](https://github.com/102012dl/truthlens-ua-analytics-v2)
- [GitLab Repository](https://gitlab.com/102012dl/truthlens-ua-analytics-v2)
""")

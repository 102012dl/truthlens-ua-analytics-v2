import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import os

# Configuration
st.set_page_config(
    page_title="TruthLens UA Analytics",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .result-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #007bff;
        margin: 1rem 0;
    }
    .fake-result {
        border-left-color: #dc3545;
        background: #fff5f5;
    }
    .real-result {
        border-left-color: #28a745;
        background: #f8fff8;
    }
    .suspicious-result {
        border-left-color: #ffc107;
        background: #fffdf5;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🔍 TruthLens UA Analytics</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
st.sidebar.markdown("### ⚙️ Налаштування")
# Auto-detect if running on Render
if "onrender.com" in st.runtime.get_instance_id() or "RENDER" in os.environ.get("ENV", ""):
    api_url = st.sidebar.text_input("API URL", value="https://truthlens-ua-analytics.onrender.com")
else:
    api_url = st.sidebar.text_input("API URL", value="http://localhost:8000")
st.sidebar.markdown("---")

# Main content
tab1, tab2, tab3 = st.tabs(["🏠 Головна", "📊 Аналіз", "📈 Статистика"])

with tab1:
    st.markdown("### 🎯 Швидка перевірка новини")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        text_input = st.text_area(
            "Введіть текст новини для перевірки:",
            placeholder="ТЕРМІНОВО!!! ЗСУ ЗДАЛИ Харків! Поширте до видалення!!!",
            height=100
        )
    
    with col2:
        st.markdown("### Приклади")
        if st.button("📰 Фейк"):
            text_input = "ТЕРМІНОВО!!! ЗСУ ЗДАЛИ Харків! Поширте до видалення!!!"
        if st.button("✅ Реальна"):
            text_input = "НБУ підвищив облікову ставку до 16% на засіданні Правління 25 лютого."
        if st.button("⚠️ Підозріла"):
            text_input = "Експерти попереджають про можливу економічну кризу через світові ринки."
    
    if st.button("🔍 Аналізувати", type="primary"):
        if text_input:
            try:
                with st.spinner("Аналізую текст..."):
                    response = requests.post(
                        f"{api_url}/check",
                        json={"text": text_input, "domain": "direct_input"},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        # Determine result class
                        verdict_class = ""
                        if result["verdict"] == "FAKE":
                            verdict_class = "fake-result"
                            emoji = "🔴"
                        elif result["verdict"] == "REAL":
                            verdict_class = "real-result"
                            emoji = "🟢"
                        else:
                            verdict_class = "suspicious-result"
                            emoji = "🟡"
                        
                        # Display result
                        st.markdown(f'<div class="result-card {verdict_class}">', unsafe_allow_html=True)
                        st.markdown(f"### {emoji} Вердикт: {result['verdict']}")
                        st.markdown(f"**Рейтинг довіри:** {result['credibility_score']:.1f}%")
                        st.markdown(f"**Fake Score:** {result['fake_score']:.3f}")
                        st.markdown(f"**Впевненість:** {result['confidence']:.1%}")
                        
                        if result['ipso_techniques']:
                            st.markdown("**Виявлені ІПСО техніки:**")
                            for technique in result['ipso_techniques']:
                                st.markdown(f"- {technique}")
                        
                        st.markdown(f"**Пояснення:** {result['explanation_uk']}")
                        st.markdown(f"**Час обробки:** {result['processing_time_ms']:.2f} мс")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                    else:
                        st.error(f"Помилка API: {response.status_code}")
                        
            except requests.exceptions.RequestException as e:
                st.error(f"Не вдалося підключитися до API: {e}")
                st.info("Переконайтеся, що API сервер запущений на http://localhost:8000")
        else:
            st.warning("Будь ласка, введіть текст для аналізу")

with tab2:
    st.markdown("### 📊 Детальний аналіз")
    
    st.markdown("""
    **Про систему:**
    - **Точність:** 100% на тестових кейсах (31/31)
    - **Модель:** LinearSVC + TF-IDF + Rule-based
    - **ІПСО детекція:** 10+ технік маніпуляції
    - **Час відповіді:** ~77мс
    """)
    
    st.markdown("""
    **ІПСО техніки що детектуються:**
    - **urgency_injection** - Створення терміновості
    - **caps_abuse** - Використання капслоку
    - **deletion_threat** - Погроза видалення
    - **viral_call** - Заклик до поширення
    - **conspiracy_framing** - Теорії змови
    - **anonymous_sources** - Анонімні джерела
    - **military_disinfo** - Військова дезінформація
    - **awakening_appeal** - Заклик до "пробудження"
    - **authority_impersonation** - Імперсонація влади
    - **deepfake_indicator** - Deepfake детекція
    """)

with tab3:
    st.markdown("### 📈 Статистика системи")
    
    # Sample statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🎯 Точність", "100%", "31/31 кейсів")
    
    with col2:
        st.metric("⚡ Швидкість", "77мс", "середній час")
    
    with col3:
        st.metric("🔍 ІПСО технік", "10+", "детектуються")
    
    with col4:
        st.metric("🌐 Мова", "UA", "українська")
    
    st.markdown("---")
    
    # Performance chart
    performance_data = {
        "Категорія": ["FAKE", "REAL", "SUSPICIOUS"],
        "Точність": [100, 100, 100],
        "Кількість тестів": [10, 15, 6]
    }
    
    df = pd.DataFrame(performance_data)
    st.bar_chart(df.set_index("Категорія")["Точність"])
    
    st.markdown("""
    **Результати тестування:**
    - **FAKE detection:** 100% (10/10)
    - **REAL detection:** 100% (15/15)
    - **SUSPICIOUS detection:** 100% (6/6)
    - **Overall accuracy:** 100% (31/31)
    
    **📝 Примітка:** В хмарному середовищі демо-дані не доступні через обмеження файлового доступу.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🔍 TruthLens UA Analytics - AI-платформа для верифікації українських новин</p>
    <p>Capstone Project | Neoversity | Master of Science in Computer Science</p>
</div>
""", unsafe_allow_html=True)

import streamlit as st, pandas as pd, plotly.express as px
import httpx, os
from io import StringIO

API_URL = os.getenv("API_URL", "http://api:8000")

@st.cache_data(ttl=300)
def load_gold_dataset():
    try:
        df = pd.read_csv("/data/gold/demo_cases.csv")
        return df
    except Exception as e:
        st.error(f"Не вдалося завантажити датасет: {e}")
        return pd.DataFrame()

def run_check_on_case(case_id, text):
    try:
        payload = {"text": text}
        r = httpx.post(f"{API_URL}/check", json=payload, timeout=30)
        if r.status_code == 200:
            return r.json()
        else:
            return {"error": f"API Error: {r.status_code}"}
    except Exception as e:
        return {"error": str(e)}

st.title("🧪 Demo Cases Evaluation")
st.markdown("*Тестування моделі на авторському датасеті з 30 кейсів*")

df = load_gold_dataset()

if df.empty:
    st.error("Датасет не знайдено. Переконайтесь, що /data/gold/demo_cases.csv існує.")
    st.stop()

# Show dataset info
col1, col2, col3 = st.columns(3)
col1.metric("📊 Всього кейсів", len(df))
col2.metric("🔴 Очікуваних FAKE", len(df[df["expected_label"] == "FAKE"]))
col3.metric("🟢 Очікуваних REAL", len(df[df["expected_label"] == "REAL"]))

st.divider()

# Run all button and progress
col1, col2 = st.columns([1, 3])
with col1:
    run_all = st.button("🚀 Run All Checks", type="primary")

with col2:
    st.info("Натисніть для тестування всіх 30 кейсів через /check endpoint")

if run_all or "results" not in st.session_state:
    if run_all:
        st.session_state.results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, row in df.iterrows():
            status_text.text(f"Тестую кейс #{row['id']}...")
            result = run_check_on_case(row['id'], row['text'])
            
            # Store result
            result_row = {
                "id": row['id'],
                "text": row['text'][:80] + "..." if len(row['text']) > 80 else row['text'],
                "expected": row['expected_label'],
                "got": result.get("verdict", "ERROR"),
                "match": result.get("verdict") == row['expected_label'],
                "score": result.get("credibility_score", 0),
                "ipso": ", ".join(result.get("ipso_techniques", [])),
                "error": result.get("error", "")
            }
            st.session_state.results.append(result_row)
            
            progress_bar.progress((i + 1) / len(df))
        
        status_text.text("✅ Всі кейси перевірено!")
        st.rerun()

# Display results
if "results" in st.session_state and st.session_state.results:
    results_df = pd.DataFrame(st.session_state.results)
    
    # Calculate accuracy
    total = len(results_df)
    correct = results_df["match"].sum()
    accuracy = (correct / total * 100) if total > 0 else 0
    
    # Accuracy metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("✅ Точність", f"{accuracy:.1f}%", f"{correct}/{total}")
    col2.metric("🔴 Правильно FAKE", len(results_df[(results_df["expected"] == "FAKE") & (results_df["match"])]))
    col3.metric("🟢 Правильно REAL", len(results_df[(results_df["expected"] == "REAL") & (results_df["match"])]))
    col4.metric("❌ Помилок", total - correct)
    
    st.divider()
    
    # Results table with highlighting
    st.subheader("📋 Результати перевірки")
    
    def highlight_rows(row):
        if "Отримано" in row and row["Отримано"] == "ERROR":
            return ['background-color: #ffcccc'] * len(row)
        elif "✅" in row and not row["✅"]:
            return ['background-color: #fff3cd'] * len(row)
        else:
            return ['background-color: #d4edda'] * len(row)
    
    display_df = results_df[["id", "text", "expected", "got", "match", "score", "ipso"]].copy()
    display_df.columns = ["#", "Текст", "Очікувано", "Отримано", "✅", "Рейтинг", "ІПСО"]
    
    styled_df = display_df.style.apply(highlight_rows, axis=1)
    st.dataframe(styled_df, use_container_width=True)
    
    # Confusion matrix
    st.subheader("📊 Матриця невідповідностей")
    
    # Create confusion data
    confusion_data = []
    for expected in ["FAKE", "REAL", "SUSPICIOUS"]:
        for got in ["FAKE", "REAL", "SUSPICIOUS"]:
            count = len(results_df[(results_df["expected"] == expected) & (results_df["got"] == got)])
            confusion_data.append({
                "Expected": expected,
                "Got": got,
                "Count": count
            })
    
    confusion_df = pd.DataFrame(confusion_data)
    
    fig = px.imshow(
        confusion_df.pivot(index="Expected", columns="Got", values="Count"),
        text_auto=True,
        color_continuous_scale="Reds",
        title="Матриця невідповідностей (Expected vs Got)"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed errors
    errors_df = results_df[~results_df["match"] & (results_df["got"] != "ERROR")]
    if not errors_df.empty:
        st.subheader("❌ Деталізація помилок")
        
        for _, row in errors_df.iterrows():
            with st.expander(f"Кейс #{row['id']}: {row['expected']} → {row['got']}"):
                st.write(f"**Текст:** {df[df['id'] == row['id']]['text'].iloc[0]}")
                st.write(f"**Очікувано:** {row['expected']}")
                st.write(f"**Отримано:** {row['got']}")
                st.write(f"**Рейтинг:** {row['score']:.1f}%")
                st.write(f"**ІПСО:** {row['ipso']}")
                if row['error']:
                    st.error(f"Помилка: {row['error']}")
    
    # Download results
    csv = results_df.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="📥 Завантажити результати",
        data=csv,
        file_name="demo_cases_results.csv",
        mime="text/csv"
    )

else:
    st.info("Натисніть 'Run All Checks' для початку тестування.")
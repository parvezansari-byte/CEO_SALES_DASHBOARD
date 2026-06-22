import streamlit as st
import pandas as pd

# ==================================================
# FILE UPLOAD
# ==================================================
st.sidebar.header("📂 Upload Excel File")

uploaded_file = st.sidebar.file_uploader(
    "Upload Sales Report",
    type=["xlsx", "xls"]
)

# ==================================================
# LOAD DATA
# ==================================================
@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        return pd.read_excel(uploaded_file)
    else:
        return pd.read_excel("sales_analysis_report.xlsx")

df = load_data(uploaded_file)

# Store globally
st.session_state["df"] = df

st.set_page_config(
    page_title="CEO Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 CEO Sales Dashboard")

st.markdown("""
## Welcome

Use the left sidebar to navigate:

- Executive Dashboard
- Monthly Trends
- Leaderboard
- Partner Segmentation
- Heatmap Analysis
- Target Tracker
- AI Insights
- CEO Summary
""")

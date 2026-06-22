import streamlit as st
import pandas as pd

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="CEO Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================================
# TITLE
# ==========================================================
st.title("📊 CEO Sales Dashboard")
st.markdown("### Upload Excel File For Analysis")

# ==========================================================
# FILE UPLOAD
# ==========================================================
uploaded_file = st.file_uploader(
    "📂 Upload Excel File",
    type=["xlsx", "xls"]
)

# ==========================================================
# LOAD DATA
# ==========================================================
@st.cache_data
def load_excel(file):
    return pd.read_excel(file)

# ==========================================================
# STORE DATA GLOBALLY
# ==========================================================
if uploaded_file is not None:

    df = load_excel(uploaded_file)

    st.session_state["df"] = df

    st.success("✅ File Uploaded Successfully")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rows", len(df))

    with col2:
        st.metric("Columns", len(df.columns))

    with col3:
        st.metric("Missing Values", int(df.isnull().sum().sum()))

    st.subheader("📋 Data Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True
    )

else:

    # Load default file if available
    try:
        df = pd.read_excel("sales_analysis_report.xlsx")
        st.session_state["df"] = df

        st.info("Using default file: sales_analysis_report.xlsx")

    except:
        st.warning("⬆ Please upload an Excel file.")

# ==========================================================
# DASHBOARD MODULES
# ==========================================================
st.markdown("---")

st.subheader("Available Modules")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ✅ Executive Dashboard

    ✅ CEO Summary

    ✅ Heatmap
    """)

with col2:
    st.markdown("""
    ✅ Leaderboard

    ✅ Monthly Trend

    ✅ Partner Segmentation
    """)

with col3:
    st.markdown("""
    ✅ Target Tracker

    ✅ AI Recommendation

    ✅ Opportunity Analysis
    """)

import streamlit as st
import pandas as pd

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="CEO Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==================================================
# TITLE
# ==================================================
st.title("📊 CEO Sales Dashboard")

st.markdown("### Upload Excel File For Analysis")

# ==================================================
# FILE UPLOAD
# ==================================================
uploaded_file = st.file_uploader(
    "Choose Excel File",
    type=["xlsx", "xls"]
)

# ==================================================
# LOAD DATA
# ==================================================
@st.cache_data
def load_data(file):
    return pd.read_excel(file)

# ==================================================
# PROCESS FILE
# ==================================================
if uploaded_file is not None:

    df = load_data(uploaded_file)

    # Save globally for all pages
    st.session_state["df"] = df

    st.success("✅ File Uploaded Successfully")

    col1, col2 = st.columns(2)

    col1.metric("Rows", len(df))
    col2.metric("Columns", len(df.columns))

    st.subheader("Preview")

    st.dataframe(
        df.head(),
        use_container_width=True
    )

else:

    st.info("⬆ Upload an Excel file to begin analysis.")

# ==================================================
# HOME PAGE
# ==================================================
st.markdown("---")

st.markdown("""
### Dashboard Modules

- 📈 Executive Dashboard
- 🔥 Heatmap
- 🏆 Leaderboard
- 📅 Monthly Trend
- 🎯 Partner Segmentation
- 📌 Target Tracker
- 🤖 AI Recommendation
- 👔 CEO Summary
""")

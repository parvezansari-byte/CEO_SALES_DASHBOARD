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

# ==================================================
# SIDEBAR
# ==================================================
st.sidebar.title("📂 Data Upload")

uploaded_file = st.sidebar.file_uploader(
    "Upload Excel File",
    type=["xlsx", "xls"]
)

# ==================================================
# LOAD DATA
# ==================================================
@st.cache_data
def load_data(file):
    try:
        if file is not None:
            return pd.read_excel(file)
        else:
            return pd.read_excel("sales_analysis_report.xlsx")
    except:
        return pd.DataFrame()

# Load dataframe
df = load_data(uploaded_file)

# Store globally
st.session_state["df"] = df

# ==================================================
# FILE STATUS
# ==================================================
if uploaded_file is not None:

    st.sidebar.success("✅ File Uploaded")

    st.sidebar.write("Rows :", len(df))
    st.sidebar.write("Columns :", len(df.columns))

else:

    st.sidebar.info(
        "No file uploaded.\nUsing sales_analysis_report.xlsx"
    )

# ==================================================
# HOME PAGE
# ==================================================
st.markdown("---")

st.markdown("""
# Welcome

### Use the left sidebar to navigate:

- 📈 Executive Dashboard
- 📅 Monthly Trend
- 🏆 Leaderboard
- 🎯 Partner Segmentation
- 🔥 Heatmap
- 📌 Target Tracker
- 🤖 AI Recommendation
- 👔 CEO Summary

---
""")

# ==================================================
# DATA PREVIEW
# ==================================================
if not df.empty:

    st.subheader("📋 Data Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True
    )

    st.success("Dashboard Ready ✅")

else:

    st.warning("Please upload an Excel file.")

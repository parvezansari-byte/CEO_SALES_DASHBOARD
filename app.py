import streamlit as st
import pandas as pd
st.markdown("""
<style>

/* Main Background */
.stApp{
background: linear-gradient(135deg,#020617,#0f172a,#111827);
color:white;
}

/* Sidebar */
[data-testid="stSidebar"]{
background:linear-gradient(180deg,#111827,#1e293b);
border-right:1px solid rgba(255,255,255,0.1);
}

/* Headers */
h1{
font-size:52px !important;
font-weight:800 !important;
color:white !important;
}

h2,h3{
color:white !important;
}

/* Metric Cards */
[data-testid="metric-container"]{
background:rgba(255,255,255,0.05);
border:1px solid rgba(255,255,255,0.1);
padding:20px;
border-radius:22px;
box-shadow:0 8px 25px rgba(0,0,0,0.4);
}

/* Buttons */
.stButton>button{
background:linear-gradient(135deg,#2563eb,#7c3aed);
color:white;
border:none;
border-radius:14px;
font-weight:600;
height:50px;
width:100%;
}

/* File uploader */
[data-testid="stFileUploader"]{
background:rgba(255,255,255,0.05);
padding:20px;
border-radius:20px;
border:1px solid rgba(255,255,255,0.1);
}

/* Dataframe */
[data-testid="stDataFrame"]{
border-radius:20px;
overflow:hidden;
}

/* Success box */
[data-baseweb="notification"]{
border-radius:18px;
}

</style>
""", unsafe_allow_html=True)
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
st.markdown("""
<div style="
background:linear-gradient(135deg,#2563eb,#7c3aed);
padding:30px;
border-radius:25px;
text-align:center;
box-shadow:0 15px 40px rgba(0,0,0,0.4);
">

<h1 style="color:white;">
📊 CEO SALES DASHBOARD
</h1>

<h4 style="color:#E5E7EB;">
AI Powered Wealth Analytics Platform
</h4>

</div>
""", unsafe_allow_html=True)
st.markdown("### Upload Excel File For Analysis")

# ==========================================================
# FILE UPLOAD
# ==========================================================
st.markdown("""
<div style="
background:rgba(255,255,255,0.05);
padding:30px;
border-radius:25px;
border:1px solid rgba(255,255,255,0.1);
margin-top:20px;
">

<h3>📂 Upload Excel File</h3>
<p>Upload Sales Report For Complete Analysis</p>

</div>
""", unsafe_allow_html=True)
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

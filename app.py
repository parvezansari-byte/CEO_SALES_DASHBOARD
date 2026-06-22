import streamlit as st
import pandas as pd

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
) 

# ======================================================
# PREMIUM CSS
# ======================================================
st.markdown("""
<style>

.stApp{
background:linear-gradient(135deg,#020617,#0f172a,#111827);
color:white;
}

h1,h2,h3{
color:white !important;
}

[data-testid="metric-container"]{
background:rgba(255,255,255,0.05);
border:1px solid rgba(255,255,255,0.1);
padding:20px;
border-radius:20px;
box-shadow:0 10px 30px rgba(0,0,0,0.4);
}

[data-testid="stFileUploader"]{
background:rgba(255,255,255,0.05);
padding:20px;
border-radius:20px;
border:1px solid rgba(255,255,255,0.1);
}

.stButton>button{
background:linear-gradient(135deg,#2563eb,#7c3aed);
color:white;
border:none;
border-radius:15px;
height:50px;
font-weight:600;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# HEADER
# ======================================================
st.markdown("""
<div style="
background:linear-gradient(135deg,#2563eb,#7c3aed);
padding:35px;
border-radius:25px;
text-align:center;
box-shadow:0 15px 40px rgba(0,0,0,0.4);
">

<h1 style="color:white;">
📊 CEO SALES DASHBOARD
</h1>

<h4 style="color:white;">
AI Powered Wealth Analytics Platform
</h4>

</div>
""", unsafe_allow_html=True)

st.write("")

# ======================================================
# FILE UPLOAD
# ======================================================
st.markdown("""
<div style="
background:rgba(255,255,255,0.05);
padding:25px;
border-radius:20px;
border:1px solid rgba(255,255,255,0.1);
">

<h3>📂 Upload Excel File</h3>
<p>Upload Sales Report for Complete Analysis</p>

</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "",
    type=["xlsx","xls"]
)

# ======================================================
# LOAD DATA
# ======================================================
@st.cache_data
def load_data(file):
    return pd.read_excel(file)

if uploaded_file is not None:

    df = load_data(uploaded_file)

    st.session_state["df"] = df

    st.success("✅ File Uploaded Successfully")

    c1,c2,c3 = st.columns(3)

    c1.metric("Rows", len(df))
    c2.metric("Columns", len(df.columns))
    c3.metric("Missing Values", int(df.isnull().sum().sum()))

    st.subheader("📋 Data Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True
    )

else:

    st.info("⬆ Upload an Excel file to begin analysis")

# ======================================================
# MODULES
# ======================================================
st.write("")
st.subheader("Dashboard Modules")

c1,c2,c3 = st.columns(3)

with c1:

    st.info("""
📈 Executive Dashboard

👔 CEO Summary

🔥 Heatmap
""")

with c2:

    st.info("""
🏆 Leaderboard

📅 Monthly Trend

🎯 Partner Segmentation
""")

with c3:

    st.info("""
📌 Target Tracker

🤖 AI Recommendation

📊 Opportunity Analysis
""")

# ======================================================
# FOOTER
# ======================================================
st.write("")
st.markdown("---")

st.markdown(
"""
<div style="text-align:center;color:gray;">
Developed By <b>Parvez Alam Ansari</b>
</div>
""",
unsafe_allow_html=True
)

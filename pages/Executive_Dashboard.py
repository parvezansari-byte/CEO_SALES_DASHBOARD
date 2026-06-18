import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide"
)
# ----------------------------------------
# LOAD DATA
# ----------------------------------------
@st.cache_data
def load_data():

    # Root folder of project
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Excel file path
    EXCEL_FILE = BASE_DIR / "sales_analysis_report.xlsx"

    return pd.read_excel(EXCEL_FILE)

df = load_data()

# ---------- TITLE ----------
st.title("📊 Executive Dashboard")

# ---------- KPI CALCULATIONS ----------
total_aum = df["AUM (Eq+Hybrid)"].sum()
total_sip = df["SIP Book Value"].sum()
total_clients = df["No. of Clients"].sum()
partners = len(df)

# Replace these with actual columns if available
gross_sales = df["Gross Sales"].sum() if "Gross Sales" in df.columns else 0
net_sales = df["Net Sales"].sum() if "Net Sales" in df.columns else 0

# =====================================================
# PREMIUM KPI CARDS
# =====================================================

st.markdown("""
<style>

.kpi-card{
padding:25px;
border-radius:25px;
box-shadow:0px 10px 25px rgba(0,0,0,.35);
transition:.3s;
}

.kpi-card:hover{
transform:translateY(-5px);
}

.title{
font-size:15px;
font-weight:600;
color:white;
}

.value{
font-size:42px;
font-weight:800;
color:white;
margin-top:10px;
}

</style>
""",unsafe_allow_html=True)

col1,col2,col3,col4,col5,col6 = st.columns(6)

with col1:
    st.markdown(f"""
    <div class="kpi-card"
    style="background:linear-gradient(135deg,#16a34a,#22c55e);">
    <div class="title">💰 AUM</div>
    <div class="value">₹{total_aum:.2f} Cr</div>
    </div>
    """,unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card"
    style="background:linear-gradient(135deg,#2563eb,#3b82f6);">
    <div class="title">📈 SIP Book</div>
    <div class="value">₹{sip_book:.2f} Cr</div>
    </div>
    """,unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card"
    style="background:linear-gradient(135deg,#f59e0b,#d97706);">
    <div class="title">👥 Clients</div>
    <div class="value">{clients}</div>
    </div>
    """,unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card"
    style="background:linear-gradient(135deg,#7c3aed,#9333ea);">
    <div class="title">🤝 Partners</div>
    <div class="value">{partners}</div>
    </div>
    """,unsafe_allow_html=True)

with col5:
    st.markdown("""
    <div class="kpi-card"
    style="background:linear-gradient(135deg,#dc2626,#ef4444);">
    <div class="title">💹 Gross Sales</div>
    <div class="value">₹0.00 Cr</div>
    </div>
    """,unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="kpi-card"
    style="background:linear-gradient(135deg,#0891b2,#06b6d4);">
    <div class="title">📊 Net Sales</div>
    <div class="value">₹0.00 Cr</div>
    </div>
    """,unsafe_allow_html=True)
# ---------- TOP 10 PARTNERS ----------
st.subheader("🏆 Top 10 Partners by AUM")

top10 = (
    df.sort_values("AUM (Eq+Hybrid)", ascending=False)
      .head(10)
)

fig = px.bar(
    top10,
    x="Agent Name",
    y="AUM (Eq+Hybrid)",
    text_auto=".2s",
    color="AUM (Eq+Hybrid)"
)

fig.update_layout(
    height=500,
    xaxis_title="Partner",
    yaxis_title="AUM"
)

st.plotly_chart(fig, use_container_width=True)

# ---------- PIE CHART ----------
st.subheader("Partner Concentration")

top5 = top10.head(5)

fig2 = px.pie(
    top5,
    names="Agent Name",
    values="AUM (Eq+Hybrid)",
    hole=.5
)

st.plotly_chart(fig2, use_container_width=True)

# ---------- LEADERBOARD ----------
st.subheader("📋 Top Partner Leaderboard")

show_cols = [
    "Agent Name",
    "AUM (Eq+Hybrid)",
    "SIP Book Value",
    "No. of Clients"
]

st.dataframe(
    top10[show_cols],
    use_container_width=True
)

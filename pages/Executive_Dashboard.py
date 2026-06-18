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

# ---------- KPI CARDS ----------
c1, c2, c3, c4, c5, c6 = st.columns(6)

with c1:
    st.metric("AUM", f"₹{total_aum/1e7:.2f} Cr")

with c2:
    st.metric("SIP Book", f"₹{total_sip/1e7:.2f} Cr")

with c3:
    st.metric("Clients", f"{int(total_clients)}")

with c4:
    st.metric("Partners", partners)

with c5:
    st.metric("Gross Sales", f"₹{gross_sales/1e7:.2f} Cr")

with c6:
    st.metric("Net Sales", f"₹{net_sales/1e7:.2f} Cr")

st.divider()

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

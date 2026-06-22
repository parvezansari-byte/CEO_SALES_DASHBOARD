import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="AI Recommendation", layout="wide")

st.title("🤖 AI Recommendation Engine")

# ====================================================
# LOAD DATA
# ====================================================
@st.cache_data
def load_data():

    BASE_DIR = Path(__file__).resolve().parent.parent
    EXCEL_FILE = BASE_DIR / "sales_analysis_report.xlsx"

    try:
        return pd.read_excel(EXCEL_FILE)

    except Exception as e:
        st.error(f"Error loading file : {e}")
        return pd.DataFrame()

df = st.session_state.get("df")

if df is None:
    st.warning("Please upload an Excel file.")
    st.stop()

if df.empty:
    st.warning("No data available.")
    st.stop()

# ====================================================
# KPI
# ====================================================
total_aum = df["AUM (Eq+Hybrid)"].sum()/1e7
total_sip = df["SIP Book Value"].sum()/1e7
clients = df["No. of Clients"].sum()

c1,c2,c3 = st.columns(3)

c1.metric("AUM", f"₹{total_aum:.2f} Cr")
c2.metric("SIP Book", f"₹{total_sip:.2f} Cr")
c3.metric("Clients", int(clients))

st.divider()

# ====================================================
# AI INSIGHTS
# ====================================================
st.subheader("📌 AI Recommendations")

if total_aum < 175:
    st.warning("""
### AUM Growth Opportunity
- Increase HNI acquisition
- Focus on top 20 partners
- Activate dormant partners
""")

if total_sip < 2:
    st.info("""
### SIP Growth Opportunity
- Run SIP campaigns
- Goal-based investing
- Family account mapping
""")

if clients < 3500:
    st.error("""
### Client Acquisition Opportunity
- Reactivate inactive clients
- Cross-sell existing clients
- Conduct webinars
""")

st.success("""
## Strategic Action Plan

✅ Increase monthly gross sales

✅ Focus on Growth and Emerging partners

✅ Target ₹2 Cr monthly net sales

✅ Expand active partner base

✅ Conduct partner engagement programs

✅ Increase SIP penetration

✅ Improve client retention
""")

# ====================================================
# TOP PARTNERS
# ====================================================
st.subheader("🏆 Top 10 Partners")

top10 = (
    df.sort_values("AUM (Eq+Hybrid)", ascending=False)
      [["Agent Name","AUM (Eq+Hybrid)","SIP Book Value"]]
      .head(10)
)

st.dataframe(
    top10,
    use_container_width=True,
    hide_index=True
)

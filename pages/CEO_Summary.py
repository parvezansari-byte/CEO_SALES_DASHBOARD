import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="CEO Summary Dashboard",
    page_icon="👔",
    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
@st.cache_data
def load_data():

    BASE_DIR = Path(__file__).resolve().parent.parent
    EXCEL_FILE = BASE_DIR / "sales_analysis_report.xlsx"

    if not EXCEL_FILE.exists():
        st.error(f"Excel file not found:\n{EXCEL_FILE}")
        st.stop()

    return pd.read_excel(EXCEL_FILE)

df = load_data()

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.title("👔 CEO Summary Dashboard")

# ---------------------------------------------------
# METRICS
# ---------------------------------------------------
total_aum = df["AUM (Eq+Hybrid)"].sum() / 1e7
sip_book = df["SIP Book Value"].sum() / 1e7
clients = int(df["No. of Clients"].sum())
partners = len(df)

# Targets
target_aum = 175
target_sip = 2
target_clients = 3500
target_partners = 120

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("AUM", f"₹{total_aum:.2f} Cr")
c2.metric("SIP Book", f"₹{sip_book:.2f} Cr")
c3.metric("Clients", clients)
c4.metric("Partners", partners)

st.divider()

# ---------------------------------------------------
# BUSINESS HEALTH SCORE
# ---------------------------------------------------
health_score = (
    (total_aum / target_aum) * 40
    + (sip_book / target_sip) * 20
    + (clients / target_clients) * 20
    + (partners / target_partners) * 20
)

health_score = min(100, health_score)

st.subheader("Business Health Score")

if health_score >= 85:
    st.success(f"🟢 Excellent : {health_score:.1f}/100")
elif health_score >= 70:
    st.warning(f"🟡 Moderate : {health_score:.1f}/100")
else:
    st.error(f"🔴 Attention Required : {health_score:.1f}/100")

st.progress(health_score / 100)

# ---------------------------------------------------
# TARGET STATUS
# ---------------------------------------------------
status_df = pd.DataFrame({
    "Metric": ["AUM", "SIP Book", "Clients", "Partners"],
    "Current": [round(total_aum, 2), round(sip_book, 2), clients, partners],
    "Target": [target_aum, target_sip, target_clients, target_partners]
})

plot_df = status_df.melt(
    id_vars="Metric",
    value_vars=["Current", "Target"],
    var_name="Type",
    value_name="Value"
)

fig = px.bar(
    plot_df,
    x="Metric",
    y="Value",
    color="Type",
    barmode="group",
    text_auto=True,
    title="Current vs Target"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------
# TOP PARTNERS
# ---------------------------------------------------
st.subheader("🏆 Top 10 Partners")

top10 = (
    df.sort_values(
        "AUM (Eq+Hybrid)",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top10[
        [
            "Agent Name",
            "AUM (Eq+Hybrid)",
            "SIP Book Value",
            "No. of Clients"
        ]
    ],
    use_container_width=True
)

# ---------------------------------------------------
# RISK MATRIX
# ---------------------------------------------------
st.subheader("⚠ Risk Matrix")

top5_aum = top10.head(5)["AUM (Eq+Hybrid)"].sum()

concentration = (
    top5_aum /
    df["AUM (Eq+Hybrid)"].sum()
) * 100

risk_df = pd.DataFrame({
    "Risk": [
        "Partner Concentration",
        "SIP Dependency",
        "Dormant Partners"
    ],
    "Severity": [
        concentration,
        54,
        35
    ]
})

fig2 = px.bar(
    risk_df,
    x="Risk",
    y="Severity",
    color="Severity",
    text_auto=".1f",
    title="Business Risk Matrix"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------
# CEO PRIORITIES
# ---------------------------------------------------
st.subheader("📌 CEO Priority")

st.success("""
1. Increase SIP Book to ₹2 Cr.

2. Develop next 20 Growth Partners.

3. Reactivate Dormant Partners.

4. Achieve ₹2 Cr Monthly Net Sales.

5. Expand Partner Base to 120.
""")

# ---------------------------------------------------
# TRAFFIC LIGHT
# ---------------------------------------------------
st.subheader("🚦 Traffic Signal")

if total_aum >= 150:
    st.success("🟢 AUM Growth Healthy")
else:
    st.warning("🟡 AUM Below Target")

if sip_book >= 2:
    st.success("🟢 SIP Book Healthy")
else:
    st.error("🔴 SIP Book Needs Attention")

if partners >= 100:
    st.success("🟢 Partner Base Healthy")
else:
    st.warning("🟡 Expand Partner Base")

# ---------------------------------------------------
# EXECUTIVE SUMMARY
# ---------------------------------------------------
st.subheader("📋 Executive Summary")

summary = f"""
Current AUM : ₹{total_aum:.2f} Cr

Current SIP Book : ₹{sip_book:.2f} Cr

Clients : {clients}

Partners : {partners}

Business Health Score : {health_score:.1f}/100

Focus Areas:

• Increase SIP Book
• Develop Growth Partners
• Reactivate Dormant Partners
• Expand Partner Base
• Achieve ₹2 Cr Monthly Net Sales
"""

st.code(summary)

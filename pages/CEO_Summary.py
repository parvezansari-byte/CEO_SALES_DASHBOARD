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


# =====================================================
# PREMIUM CEO KPI CARDS
# =====================================================

st.markdown("""
<style>

.card{
background:linear-gradient(135deg,#111827,#1e293b);
padding:25px;
border-radius:25px;
box-shadow:0px 10px 25px rgba(0,0,0,.45);
border:1px solid rgba(255,255,255,.08);
transition:0.3s;
}

.card:hover{
transform:translateY(-5px);
box-shadow:0px 15px 35px rgba(0,255,150,.25);
}

.card-title{
font-size:15px;
color:#94a3b8;
font-weight:600;
}

.card-value{
font-size:42px;
font-weight:800;
color:white;
}

.green{
background:linear-gradient(135deg,#00C853,#009624);
}

.blue{
background:linear-gradient(135deg,#2563eb,#1d4ed8);
}

.orange{
background:linear-gradient(135deg,#f59e0b,#d97706);
}

.purple{
background:linear-gradient(135deg,#7c3aed,#6d28d9);
}

</style>
""",unsafe_allow_html=True)

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="card green">
    <div class="card-title">💰 Total AUM</div>
    <div class="card-value">₹{total_aum:.2f} Cr</div>
    </div>
    """,unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card blue">
    <div class="card-title">📈 SIP Book</div>
    <div class="card-value">₹{sip_book:.2f} Cr</div>
    </div>
    """,unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card orange">
    <div class="card-title">👥 Clients</div>
    <div class="card-value">{clients}</div>
    </div>
    """,unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="card purple">
    <div class="card-title">🤝 Partners</div>
    <div class="card-value">{partners}</div>
    </div>
    """,unsafe_allow_html=True)


# ---------------------------------------------------
# BUSINESS HEALTH SCORE
# ---------------------------------------------------
st.markdown(f"""
<div style="
background:linear-gradient(90deg,#065f46,#22c55e);
padding:25px;
border-radius:25px;
box-shadow:0px 10px 25px rgba(0,255,120,.25);
margin-top:15px;
">
<h3 style='color:white'>🏆 Business Health Score</h3>
<h1 style='color:white'>{health_score:.1f}/100</h1>
<h4 style='color:#dcfce7'>Moderate Growth</h4>
</div>
""",unsafe_allow_html=True)


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

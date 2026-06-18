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


# =====================================================
# BUSINESS HEALTH SCORE
# =====================================================

health_score = (
    (total_aum / target_aum) * 40
    + (sip_book / target_sip) * 20
    + (clients / target_clients) * 20
    + (partners / target_partners) * 20
)

health_score = min(100, health_score)

status = "Moderate Growth"

if health_score >= 85:
    status = "Excellent Growth"
elif health_score < 70:
    status = "Needs Attention"

st.markdown(
f"""
<div style="
background:linear-gradient(135deg,#065f46,#16a34a);
padding:30px;
border-radius:25px;
box-shadow:0px 10px 30px rgba(0,255,120,.25);
margin-top:20px;
">

<h3 style='color:white;'>🏆 Business Health Score</h3>

<h1 style='color:white;'>{health_score:.1f}/100</h1>

<h4 style='color:#dcfce7'>{status}</h4>

</div>
""",
unsafe_allow_html=True
)
# ============================================
# CURRENT VS TARGET CARDS
# ============================================

st.subheader("🎯 Current vs Target")

aum_pct = min((total_aum/target_aum)*100,100)
sip_pct = min((sip_book/target_sip)*100,100)
client_pct = min((clients/target_clients)*100,100)
partner_pct = min((partners/target_partners)*100,100)

col1,col2 = st.columns(2)
col3,col4 = st.columns(2)

with col1:

    st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#0f766e,#14b8a6);
    padding:25px;
    border-radius:25px;
    box-shadow:0px 8px 25px rgba(20,184,166,.3);
    ">
    <h3 style='color:white'>💰 AUM</h3>
    <h1 style='color:white'>₹{total_aum:.2f} Cr</h1>
    <h4 style='color:white'>Target : ₹{target_aum} Cr</h4>
    </div>
    """,unsafe_allow_html=True)

    st.progress(aum_pct/100)
    st.write(f"{aum_pct:.1f}% Achieved")

with col2:

    st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#1d4ed8,#3b82f6);
    padding:25px;
    border-radius:25px;
    box-shadow:0px 8px 25px rgba(59,130,246,.3);
    ">
    <h3 style='color:white'>📈 SIP Book</h3>
    <h1 style='color:white'>₹{sip_book:.2f} Cr</h1>
    <h4 style='color:white'>Target : ₹{target_sip} Cr</h4>
    </div>
    """,unsafe_allow_html=True)

    st.progress(sip_pct/100)
    st.write(f"{sip_pct:.1f}% Achieved")


with col3:

    st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#d97706,#f59e0b);
    padding:25px;
    border-radius:25px;
    box-shadow:0px 8px 25px rgba(245,158,11,.3);
    ">
    <h3 style='color:white'>👥 Clients</h3>
    <h1 style='color:white'>{clients}</h1>
    <h4 style='color:white'>Target : {target_clients}</h4>
    </div>
    """,unsafe_allow_html=True)

    st.progress(client_pct/100)
    st.write(f"{client_pct:.1f}% Achieved")


with col4:

    st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#7c3aed,#9333ea);
    padding:25px;
    border-radius:25px;
    box-shadow:0px 8px 25px rgba(147,51,234,.3);
    ">
    <h3 style='color:white'>🤝 Partners</h3>
    <h1 style='color:white'>{partners}</h1>
    <h4 style='color:white'>Target : {target_partners}</h4>
    </div>
    """,unsafe_allow_html=True)

    st.progress(partner_pct/100)
    st.write(f"{partner_pct:.1f}% Achieved")

# ==========================================================
# TOP 10 PARTNERS SECTION
# ==========================================================

import plotly.express as px

st.markdown("## 🏆 Top 10 Partners")

top10 = (
    df.sort_values(
        "AUM (Eq+Hybrid)",
        ascending=False
    )
    .head(10)
)

top10["AUM Cr"] = top10["AUM (Eq+Hybrid)"]/1e7

# ==========================================================
# TOP 10 HORIZONTAL BAR
# ==========================================================

fig = px.bar(
    top10.sort_values("AUM Cr"),
    x="AUM Cr",
    y="Agent Name",
    orientation="h",
    color="AUM Cr",
    text="AUM Cr",

    color_continuous_scale=[
        "#16a34a",
        "#22c55e",
        "#38bdf8",
        "#2563eb",
        "#7c3aed"
    ]
)

fig.update_traces(
    texttemplate="₹%{text:.2f} Cr",
    textposition="outside"
)

fig.update_layout(

    height=650,

    paper_bgcolor="#020817",
    plot_bgcolor="#020817",

    font=dict(
        color="white",
        size=14
    ),

    xaxis_title="AUM (Cr)",

    yaxis_title="",

    coloraxis_showscale=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# TOP 3 PARTNER CARDS
# ==========================================================

col1,col2,col3 = st.columns(3)

# GOLD
with col1:

    st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#fbbf24,#f59e0b);
    padding:25px;
    border-radius:25px;
    box-shadow:0px 8px 25px rgba(251,191,36,.3);
    ">
    <h3 style='color:white'>🥇 Gold Partner</h3>

    <h2 style='color:white'>{top10.iloc[0]["Agent Name"]}</h2>

    <h1 style='color:white'>₹{top10.iloc[0]["AUM Cr"]:.2f} Cr</h1>

    <h4 style='color:white'>
    Clients : {top10.iloc[0]["No. of Clients"]}
    </h4>

    </div>
    """,
    unsafe_allow_html=True)

# SILVER
with col2:

    st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#94a3b8,#64748b);
    padding:25px;
    border-radius:25px;
    box-shadow:0px 8px 25px rgba(148,163,184,.3);
    ">
    <h3 style='color:white'>🥈 Silver Partner</h3>

    <h2 style='color:white'>{top10.iloc[1]["Agent Name"]}</h2>

    <h1 style='color:white'>₹{top10.iloc[1]["AUM Cr"]:.2f} Cr</h1>

    <h4 style='color:white'>
    Clients : {top10.iloc[1]["No. of Clients"]}
    </h4>

    </div>
    """,
    unsafe_allow_html=True)

# BRONZE
with col3:

    st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#b45309,#92400e);
    padding:25px;
    border-radius:25px;
    box-shadow:0px 8px 25px rgba(180,83,9,.3);
    ">
    <h3 style='color:white'>🥉 Bronze Partner</h3>

    <h2 style='color:white'>{top10.iloc[2]["Agent Name"]}</h2>

    <h1 style='color:white'>₹{top10.iloc[2]["AUM Cr"]:.2f} Cr</h1>

    <h4 style='color:white'>
    Clients : {top10.iloc[2]["No. of Clients"]}
    </h4>

    </div>
    """,
    unsafe_allow_html=True)

st.divider()

# ==========================================================
# TOP 10 CONTRIBUTION PIE CHART
# ==========================================================

st.subheader("📊 Top 10 AUM Contribution")

fig2 = px.pie(
    top10,
    names="Agent Name",
    values="AUM Cr",
    hole=.6,

    color_discrete_sequence=px.colors.sequential.Agsunset
)

fig2.update_layout(

    height=600,

    paper_bgcolor="#020817",
    plot_bgcolor="#020817",

    font=dict(
        color="white"
    )
)

st.plotly_chart(
    fig2,
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

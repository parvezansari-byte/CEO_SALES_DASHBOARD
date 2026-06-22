import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Target Tracker",
    page_icon="📌",
    layout="wide"
)

st.title("📌 Annual Target Tracker")

# =====================================================
# LOAD DATA
# =====================================================
@st.cache_data
def load_data():
    BASE_DIR = Path(__file__).resolve().parent.parent
    EXCEL_FILE = BASE_DIR / "sales_analysis_report.xlsx"

    try:
        return pd.read_excel(EXCEL_FILE)
    except Exception as e:
        st.error(f"Error loading Excel file : {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# =====================================================
# REQUIRED COLUMNS
# =====================================================
required_cols = [
    "AUM (Eq+Hybrid)",
    "SIP Book Value",
    "No. of Clients"
]

missing = [col for col in required_cols if col not in df.columns]

if missing:
    st.error(f"Missing columns : {missing}")
    st.write(df.columns.tolist())
    st.stop()

# =====================================================
# CURRENT VALUES
# =====================================================
current_aum = df["AUM (Eq+Hybrid)"].sum()/1e7
current_sip = df["SIP Book Value"].sum()/1e7
current_clients = int(df["No. of Clients"].sum())
current_partners = len(df)

# =====================================================
# TARGETS
# =====================================================
target_aum = 175
target_sip = 2
target_clients = 3500
target_partners = 120

# =====================================================
# ACHIEVEMENT %
# =====================================================
aum_progress = min(current_aum/target_aum*100,100)
sip_progress = min(current_sip/target_sip*100,100)
client_progress = min(current_clients/target_clients*100,100)
partner_progress = min(current_partners/target_partners*100,100)

# =====================================================
# KPI CARDS
# =====================================================
c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "AUM",
    f"₹{current_aum:.2f} Cr",
    f"{aum_progress:.1f}%"
)

c2.metric(
    "SIP Book",
    f"₹{current_sip:.2f} Cr",
    f"{sip_progress:.1f}%"
)

c3.metric(
    "Clients",
    current_clients,
    f"{client_progress:.1f}%"
)

c4.metric(
    "Partners",
    current_partners,
    f"{partner_progress:.1f}%"
)

st.divider()

# =====================================================
# PROGRESS BARS
# =====================================================
st.subheader("Progress Toward Annual Target")

st.write("AUM")
st.progress(aum_progress/100)

st.write("SIP Book")
st.progress(sip_progress/100)

st.write("Clients")
st.progress(client_progress/100)

st.write("Partners")
st.progress(partner_progress/100)

# =====================================================
# TARGET TABLE
# =====================================================
tracker_df = pd.DataFrame({

    "Metric":[
        "AUM",
        "SIP Book",
        "Clients",
        "Partners"
    ],

    "Current":[
        round(current_aum,2),
        round(current_sip,2),
        current_clients,
        current_partners
    ],

    "Target":[
        target_aum,
        target_sip,
        target_clients,
        target_partners
    ],

    "Achievement %":[
        round(aum_progress,1),
        round(sip_progress,1),
        round(client_progress,1),
        round(partner_progress,1)
    ]

})

st.subheader("Target Achievement")

st.dataframe(
    tracker_df,
    use_container_width=True
)

# =====================================================
# BAR CHART
# =====================================================
try:

    fig = px.bar(
        tracker_df,
        x="Metric",
        y="Achievement %",
        color="Achievement %",
        text="Achievement %",
        color_continuous_scale="RdYlGn"
    )

    fig.update_layout(
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

except Exception as e:
    st.error(f"Chart Error : {e}")

# =====================================================
# GAP ANALYSIS
# =====================================================
gap_df = pd.DataFrame({

    "Metric":[
        "AUM",
        "SIP Book",
        "Clients",
        "Partners"
    ],

    "Gap":[
        round(target_aum-current_aum,2),
        round(target_sip-current_sip,2),
        target_clients-current_clients,
        target_partners-current_partners
    ]
})

st.subheader("Gap Analysis")

st.dataframe(
    gap_df,
    use_container_width=True
)

# =====================================================
# GAP CHART
# =====================================================
fig2 = px.bar(
    gap_df,
    x="Metric",
    y="Gap",
    color="Gap",
    text="Gap"
)

fig2.update_layout(
    height=450,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =====================================================
# AI SUGGESTIONS
# =====================================================
st.subheader("🤖 AI Suggestions")

if aum_progress < 80:
    st.warning(
        "Increase AUM by activating Growth partners and HNI campaigns."
    )

if sip_progress < 80:
    st.info(
        "Strengthen monthly SIP campaigns and family account mapping."
    )

if partner_progress < 80:
    st.error(
        "Reactivate dormant partners and expand active partner base."
    )

st.success("""
✅ Focus on Top 20 partners

✅ Increase SIP campaigns

✅ Target ₹2 Cr monthly net sales

✅ Develop emerging partners

✅ Conduct quarterly partner engagement programs
""")

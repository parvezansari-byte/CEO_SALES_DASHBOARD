import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# --------------------------------
# LOAD DATA
# --------------------------------
@st.cache_data
def load_data():
    return pd.read_excel("sales_analysis_report.xlsx")

df = load_data()

st.title("📌 Target Tracker")

# -------------------------------
# CURRENT VALUES
# -------------------------------
current_aum = df["AUM (Eq+Hybrid)"].sum()/1e7
current_sip = df["SIP Book Value"].sum()/1e7
current_clients = df["No. of Clients"].sum()
current_partners = len(df)

# -------------------------------
# TARGETS
# -------------------------------
target_aum = 175
target_sip = 2
target_clients = 3500
target_partners = 120

# -------------------------------
# PROGRESS %
# -------------------------------
aum_progress = min(current_aum/target_aum*100,100)
sip_progress = min(current_sip/target_sip*100,100)
client_progress = min(current_clients/target_clients*100,100)
partner_progress = min(current_partners/target_partners*100,100)

# -------------------------------
# KPI CARDS
# -------------------------------
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
    int(current_clients),
    f"{client_progress:.1f}%"
)

c4.metric(
    "Partners",
    current_partners,
    f"{partner_progress:.1f}%"
)

st.divider()

# -------------------------------
# PROGRESS BARS
# -------------------------------
st.subheader("Progress Toward Annual Target")

st.write("AUM")
st.progress(aum_progress/100)

st.write("SIP Book")
st.progress(sip_progress/100)

st.write("Clients")
st.progress(client_progress/100)

st.write("Partners")
st.progress(partner_progress/100)

# -------------------------------
# TARGET TABLE
# -------------------------------
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
        int(current_clients),
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

st.subheader("Target vs Achievement")

st.dataframe(
    tracker_df,
    use_container_width=True
)

# -------------------------------
# BAR CHART
# -------------------------------
fig = px.bar(
    tracker_df,
    x="Metric",
    y="Achievement %",
    color="Achievement %",
    text="Achievement %"
)

fig.update_layout(height=500)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------
# SHORTFALL
# -------------------------------
st.subheader("Gap Analysis")

gap_aum = target_aum-current_aum
gap_sip = target_sip-current_sip
gap_clients = target_clients-current_clients
gap_partners = target_partners-current_partners

gap_df = pd.DataFrame({

    "Metric":[
        "AUM",
        "SIP Book",
        "Clients",
        "Partners"
    ],

    "Gap":[
        round(gap_aum,2),
        round(gap_sip,2),
        int(gap_clients),
        gap_partners
    ]

})

st.dataframe(
    gap_df,
    use_container_width=True
)

# -------------------------------
# AI RECOMMENDATIONS
# -------------------------------
st.subheader("🤖 AI Suggestions")

if aum_progress < 80:
    st.warning(
        "Increase AUM by activating Growth partners and HNI campaigns."
    )

if sip_progress < 80:
    st.info(
        "SIP Book target requires monthly SIP campaigns and family account mapping."
    )

if partner_progress < 80:
    st.error(
        "Expand active partner base through reactivation programs."
    )

st.success(
"""
✓ Focus on Top 20 partners.

✓ Increase SIP campaigns.

✓ Target ₹2 Cr monthly net sales.

✓ Develop emerging partners.
"""
)
import streamlit as st
import pandas as pd
from pathlib import Path

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

st.title("🔥 Heatmap Analysis")

# ------------------------------------
# SCORE CALCULATION
# ------------------------------------
df["AUM Score"] = pd.qcut(
    df["AUM (Eq+Hybrid)"],
    q=5,
    labels=[1,2,3,4,5]
)

df["Client Score"] = pd.qcut(
    df["No. of Clients"],
    q=5,
    labels=[1,2,3,4,5]
)

df["SIP Score"] = pd.qcut(
    df["SIP Book Value"],
    q=5,
    labels=[1,2,3,4,5]
)

df["Overall Score"] = (
    df["AUM Score"].astype(int)
    + df["Client Score"].astype(int)
    + df["SIP Score"].astype(int)
)

# ------------------------------------
# ZONES
# ------------------------------------
def zone(score):

    if score >= 13:
        return "Green Zone"

    elif score >= 8:
        return "Yellow Zone"

    else:
        return "Red Zone"

df["Zone"] = df["Overall Score"].apply(zone)

# ------------------------------------
# KPI CARDS
# ------------------------------------
c1,c2,c3 = st.columns(3)

green_count = (df["Zone"]=="Green Zone").sum()
yellow_count = (df["Zone"]=="Yellow Zone").sum()
red_count = (df["Zone"]=="Red Zone").sum()

c1.metric("🟢 Green Zone", green_count)
c2.metric("🟡 Yellow Zone", yellow_count)
c3.metric("🔴 Red Zone", red_count)

st.divider()

# ------------------------------------
# HEATMAP TABLE
# ------------------------------------
st.subheader("Partner Heatmap")

heat_cols = [
    "Agent Name",
    "AUM (Eq+Hybrid)",
    "SIP Book Value",
    "No. of Clients",
    "Overall Score",
    "Zone"
]

styled_df = (
    df[heat_cols]
    .sort_values("Overall Score", ascending=False)
    .style.background_gradient(
        subset=["Overall Score"],
        cmap="RdYlGn"
    )
)

st.dataframe(styled_df, use_container_width=True)

# ------------------------------------
# ZONE DISTRIBUTION
# ------------------------------------
st.subheader("Zone Distribution")

zone_summary = (
    df.groupby("Zone")
    .size()
    .reset_index(name="Partners")
)

fig1 = px.pie(
    zone_summary,
    names="Zone",
    values="Partners",
    hole=0.5
)

st.plotly_chart(fig1, use_container_width=True)

# ------------------------------------
# TOP 10 PARTNERS
# ------------------------------------
st.subheader("Top Opportunity Partners")

top10 = (
    df.sort_values(
        "Overall Score",
        ascending=False
    )
    .head(10)
)

fig2 = px.bar(
    top10,
    x="Agent Name",
    y="Overall Score",
    color="Overall Score",
    text_auto=True
)

st.plotly_chart(fig2, use_container_width=True)

# ------------------------------------
# BOTTOM PARTNERS
# ------------------------------------
st.subheader("Attention Required")

bottom10 = (
    df.sort_values(
        "Overall Score"
    )
    .head(10)
)

st.dataframe(
    bottom10[
        [
            "Agent Name",
            "AUM (Eq+Hybrid)",
            "SIP Book Value",
            "No. of Clients",
            "Zone"
        ]
    ],
    use_container_width=True
)

# ------------------------------------
# AI INSIGHTS
# ------------------------------------
st.subheader("🤖 AI Recommendations")

st.success("""
🟢 Green Zone

Focus on HNI clients and PMS opportunities.
""")

st.warning("""
🟡 Yellow Zone

Convert to Elite category through SIP campaigns.
""")

st.error("""
🔴 Red Zone

Reactivation campaigns required.

Monthly engagement needed.
""")

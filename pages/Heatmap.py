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

# =========================================================
# ZONE DISTRIBUTION
# =========================================================
import pandas as pd
import plotly.express as px
import streamlit as st

st.subheader("Zone Distribution")

try:

    # Create zone dataframe
    zone_df = (
        df.groupby("Zone")["AUM"]
        .sum()
        .reset_index()
    )

    # Remove null values
    zone_df = zone_df.dropna()

    # Check if dataframe is empty
    if zone_df.empty:
        st.warning("No Zone data available.")

    else:

        fig1 = px.pie(
            zone_df,
            names="Zone",
            values="AUM",
            hole=0.55,
            color_discrete_sequence=px.colors.qualitative.Set3
        )

        fig1.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        fig1.update_layout(
            height=500,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white", size=14),
            showlegend=True,
            legend_title="Zone"
        )

        st.plotly_chart(fig1, use_container_width=True)

except KeyError as e:
    st.error(f"Column not found: {e}")
    st.write("Available columns:")
    st.write(df.columns)

except Exception as e:
    st.error(f"Error creating Zone Distribution chart")
    st.exception(e)

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

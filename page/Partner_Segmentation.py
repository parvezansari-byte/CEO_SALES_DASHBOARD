import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# ----------------------------------
# LOAD DATA
# ----------------------------------
@st.cache_data
def load_data():
    return pd.read_excel("sales_analysis_report.xlsx")

df = load_data()

st.title("🎯 Partner Segmentation")

# ----------------------------------
# SEGMENT FUNCTION
# ----------------------------------
def segment(aum):

    if aum >= 5e7:
        return "Elite"

    elif aum >= 1e7:
        return "Growth"

    elif aum >= 2.5e6:
        return "Emerging"

    else:
        return "Dormant"


df["Segment"] = df["AUM (Eq+Hybrid)"].apply(segment)

# ----------------------------------
# SUMMARY
# ----------------------------------
summary = (
    df.groupby("Segment")
    .agg(
        Partners=("Agent Name", "count"),
        Total_AUM=("AUM (Eq+Hybrid)", "sum"),
        Clients=("No. of Clients", "sum"),
        SIP_Book=("SIP Book Value", "sum")
    )
    .reset_index()
)

# ----------------------------------
# KPI CARDS
# ----------------------------------
c1, c2, c3, c4 = st.columns(4)

elite_count = (df["Segment"]=="Elite").sum()
growth_count = (df["Segment"]=="Growth").sum()
emerging_count = (df["Segment"]=="Emerging").sum()
dormant_count = (df["Segment"]=="Dormant").sum()

c1.metric("Elite", elite_count)
c2.metric("Growth", growth_count)
c3.metric("Emerging", emerging_count)
c4.metric("Dormant", dormant_count)

st.divider()

# ----------------------------------
# PIE CHART
# ----------------------------------
st.subheader("Partner Distribution")

fig1 = px.pie(
    summary,
    names="Segment",
    values="Partners",
    hole=0.5
)

st.plotly_chart(fig1, use_container_width=True)

# ----------------------------------
# AUM DISTRIBUTION
# ----------------------------------
st.subheader("Segment Wise AUM")

fig2 = px.bar(
    summary,
    x="Segment",
    y="Total_AUM",
    color="Segment",
    text_auto=".2s"
)

st.plotly_chart(fig2, use_container_width=True)

# ----------------------------------
# TABLE
# ----------------------------------
st.subheader("Segment Summary")

st.dataframe(
    summary,
    use_container_width=True
)

# ----------------------------------
# FILTER
# ----------------------------------
selected_segment = st.selectbox(
    "Select Segment",
    ["Elite", "Growth", "Emerging", "Dormant"]
)

filtered_df = df[df["Segment"] == selected_segment]

st.subheader(f"{selected_segment} Partners")

cols = [
    "Agent Name",
    "AUM (Eq+Hybrid)",
    "SIP Book Value",
    "No. of Clients"
]

st.dataframe(
    filtered_df[cols],
    use_container_width=True
)

# ----------------------------------
# OPPORTUNITY ANALYSIS
# ----------------------------------
st.subheader("AI Opportunity Analysis")

if selected_segment == "Elite":

    st.success("""
    ✓ Focus on HNI clients

    ✓ PMS opportunities

    ✓ Target ₹15 Cr incremental AUM

    ✓ Family account mapping
    """)

elif selected_segment == "Growth":

    st.info("""
    ✓ Double AUM in 12 months

    ✓ Monthly SIP campaigns

    ✓ Child education planning

    ✓ Goal-based investments
    """)

elif selected_segment == "Emerging":

    st.warning("""
    ✓ Activate 5 SIPs/month

    ✓ Lead generation support

    ✓ Monthly training sessions
    """)

else:

    st.error("""
    ✓ Dormant partner activation

    ✓ Reactivation campaign

    ✓ Webinar support

    ✓ Monthly engagement calls
    """)
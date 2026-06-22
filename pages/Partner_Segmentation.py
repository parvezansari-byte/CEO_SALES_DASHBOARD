import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(page_title="Partner Segmentation", layout="wide")

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
        st.error(f"Unable to load Excel file: {e}")
        return pd.DataFrame()

df = st.session_state.get("df")

if df is None:
    st.warning("Please upload an Excel file.")
    st.stop()

st.title("🎯 Partner Segmentation")

if df.empty:
    st.stop()

# =====================================================
# CHECK REQUIRED COLUMNS
# =====================================================
required_cols = [
    "Agent Name",
    "AUM (Eq+Hybrid)",
    "SIP Book Value",
    "No. of Clients"
]

missing_cols = [col for col in required_cols if col not in df.columns]

if missing_cols:
    st.error(f"Missing columns: {missing_cols}")
    st.write(df.columns.tolist())
    st.stop()

# =====================================================
# SEGMENT FUNCTION
# =====================================================
def segment(aum):

    if aum >= 5e7:
        return "Elite"

    elif aum >= 1e7:
        return "Growth"

    elif aum >= 2.5e6:
        return "Emerging"

    else:
        return "Dormant"

df["Segment"] = df["AUM (Eq+Hybrid)"].fillna(0).apply(segment)

# =====================================================
# SUMMARY
# =====================================================
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

# =====================================================
# KPI CARDS
# =====================================================
st.subheader("Partner Categories")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Elite", (df["Segment"]=="Elite").sum())
c2.metric("Growth", (df["Segment"]=="Growth").sum())
c3.metric("Emerging", (df["Segment"]=="Emerging").sum())
c4.metric("Dormant", (df["Segment"]=="Dormant").sum())

st.divider()

# =====================================================
# PIE CHART
# =====================================================
st.subheader("Partner Distribution")

try:
    fig1 = px.pie(
        summary,
        names="Segment",
        values="Partners",
        hole=0.55,
        color="Segment"
    )

    fig1.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    fig1.update_layout(
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig1, use_container_width=True)

except Exception as e:
    st.error(e)

# =====================================================
# AUM CHART
# =====================================================
st.subheader("Segment Wise AUM")

try:

    fig2 = px.bar(
        summary,
        x="Segment",
        y="Total_AUM",
        color="Segment",
        text_auto=".2s"
    )

    fig2.update_layout(
        height=500,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig2, use_container_width=True)

except Exception as e:
    st.error(e)

# =====================================================
# SUMMARY TABLE
# =====================================================
st.subheader("Segment Summary")

st.dataframe(summary, use_container_width=True)

# =====================================================
# FILTER
# =====================================================
selected_segment = st.selectbox(
    "Select Segment",
    ["Elite", "Growth", "Emerging", "Dormant"]
)

filtered_df = df[df["Segment"] == selected_segment]

# =====================================================
# PARTNER TABLE
# =====================================================
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

# =====================================================
# AI OPPORTUNITY ANALYSIS
# =====================================================
st.subheader("AI Opportunity Analysis")

if selected_segment == "Elite":

    st.success("""
✅ Focus on HNI clients

✅ PMS opportunities

✅ Target ₹15 Cr incremental AUM

✅ Family account mapping
""")

elif selected_segment == "Growth":

    st.info("""
✅ Double AUM in 12 months

✅ Monthly SIP campaigns

✅ Goal-based investments

✅ Child education planning
""")

elif selected_segment == "Emerging":

    st.warning("""
✅ Activate 5 SIPs/month

✅ Lead generation support

✅ Monthly training sessions
""")

else:

    st.error("""
✅ Dormant partner activation

✅ Reactivation campaign

✅ Webinar support

✅ Monthly engagement calls
""")

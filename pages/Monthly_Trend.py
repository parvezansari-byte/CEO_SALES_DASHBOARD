import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Monthly Trend", layout="wide")

st.title("📈 Monthly Trend Analysis")

# ==========================================================
# LOAD DATA
# ==========================================================
@st.cache_data(ttl=0)
def load_data():
    BASE_DIR = Path(__file__).resolve().parent.parent
    EXCEL_FILE = BASE_DIR / "sales_analysis_report.xlsx"

    try:
        return pd.read_excel(EXCEL_FILE)
    except Exception as e:
        st.error(f"Error loading Excel file : {e}")
        return pd.DataFrame()

col1, col2 = st.columns([1,5])

with col1:
    if st.button("🔄 Refresh"):
        st.cache_data.clear()
        st.rerun()

df = load_data()

if df.empty:
    st.stop()

# ==========================================================
# REQUIRED COLUMNS
# ==========================================================
required_cols = [
    "Month",
    "Gross Sales",
    "Net Sales",
    "SIP Sales",
    "Redemption"
]

missing = [col for col in required_cols if col not in df.columns]

if missing:
    st.error(f"Missing columns : {missing}")
    st.write(df.columns.tolist())
    st.stop()

# ==========================================================
# NUMERIC CONVERSION
# ==========================================================
numeric_cols = [
    "Gross Sales",
    "Net Sales",
    "SIP Sales",
    "Redemption"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# ==========================================================
# MONTHLY SUMMARY
# ==========================================================
monthly_df = (
    df.groupby("Month", as_index=False)
    .agg({
        "Gross Sales":"sum",
        "Net Sales":"sum",
        "SIP Sales":"sum",
        "Redemption":"sum"
    })
)

# Sort Month
try:
    monthly_df["Sort"] = pd.to_datetime(
        monthly_df["Month"],
        format="%b-%y"
    )

    monthly_df = (
        monthly_df
        .sort_values("Sort")
        .drop(columns="Sort")
    )

except:
    pass

# ==========================================================
# KPI CARDS
# ==========================================================
c1,c2,c3,c4 = st.columns(4)

c1.metric("Gross Sales", round(monthly_df["Gross Sales"].sum(),2))
c2.metric("Net Sales", round(monthly_df["Net Sales"].sum(),2))
c3.metric("SIP Sales", round(monthly_df["SIP Sales"].sum(),2))
c4.metric("Redemption", round(monthly_df["Redemption"].sum(),2))

st.divider()

# ==========================================================
# TABLE
# ==========================================================
st.subheader("📅 Monthly Summary")

st.dataframe(
    monthly_df,
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# LINE CHART
# ==========================================================
st.subheader("Monthly Trend")

fig = px.line(
    monthly_df,
    x="Month",
    y=["Gross Sales","Net Sales","SIP Sales","Redemption"],
    markers=True
)

fig.update_layout(
    height=600,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# BAR CHART
# ==========================================================
st.subheader("Net Sales Trend")

fig2 = px.bar(
    monthly_df,
    x="Month",
    y="Net Sales",
    color="Net Sales",
    text_auto=".2f"
)

fig2.update_layout(height=500)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ==========================================================
# DOWNLOAD
# ==========================================================
csv = monthly_df.to_csv(index=False)

st.download_button(
    "⬇ Download Monthly Summary",
    csv,
    "monthly_summary.csv",
    "text/csv"
)

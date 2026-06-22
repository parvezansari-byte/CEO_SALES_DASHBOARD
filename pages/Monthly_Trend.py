import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Monthly Trend Analysis", layout="wide")

st.title("📈 Monthly Trend Analysis")

# =====================================================
# LOAD DATA
# =====================================================
@st.cache_data(ttl=0)
def load_data():
    BASE_DIR = Path(__file__).resolve().parent.parent
    EXCEL_FILE = BASE_DIR / "sales_analysis_report.xlsx"

    try:
        return pd.read_excel(EXCEL_FILE)
    except Exception as e:
        st.error(f"Error loading file : {e}")
        return pd.DataFrame()

if st.button("🔄 Refresh"):
    st.cache_data.clear()
    st.rerun()

df = st.session_state.get("df")

if df is None:
    st.warning("Please upload an Excel file.")
    st.stop()

if df.empty:
    st.stop()

# =====================================================
# FIND MONTHLY COLUMNS
# =====================================================
gross_cols = [c for c in df.columns if "Gross Sales excl SIP" in c]

if len(gross_cols) == 0:
    st.error("No monthly sales columns found.")
    st.write(df.columns.tolist())
    st.stop()

# =====================================================
# CREATE MONTHLY SUMMARY
# =====================================================
records = []

for col in gross_cols:

    month = col.replace("Gross Sales excl SIP ", "")

    gross = df[col].fillna(0).sum()

    records.append({
        "Month": month,
        "Gross Sales": round(gross,2)
    })

monthly_df = pd.DataFrame(records)

# Sort months
monthly_df["Month_dt"] = pd.to_datetime(monthly_df["Month"])
monthly_df = (
    monthly_df
    .sort_values("Month_dt")
    .drop(columns="Month_dt")
)

# =====================================================
# KPI
# =====================================================
c1, c2 = st.columns(2)

c1.metric(
    "Months Available",
    len(monthly_df)
)

c2.metric(
    "Total Gross Sales",
    round(monthly_df["Gross Sales"].sum(),2)
)

st.divider()

# =====================================================
# TABLE
# =====================================================
st.subheader("📅 Monthly Summary")

st.dataframe(
    monthly_df,
    use_container_width=True,
    hide_index=True
)

# =====================================================
# LINE CHART
# =====================================================
st.subheader("📈 Monthly Trend")

fig = px.line(
    monthly_df,
    x="Month",
    y="Gross Sales",
    markers=True
)

fig.update_layout(
    height=550,
    xaxis_title="Month",
    yaxis_title="Gross Sales",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# BAR CHART
# =====================================================
st.subheader("📊 Monthly Gross Sales")

fig2 = px.bar(
    monthly_df,
    x="Month",
    y="Gross Sales",
    color="Gross Sales",
    text_auto=".2f"
)

fig2.update_layout(
    height=500,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =====================================================
# DOWNLOAD
# =====================================================
csv = monthly_df.to_csv(index=False)

st.download_button(
    "⬇ Download Monthly Summary",
    csv,
    "monthly_summary.csv",
    "text/csv"
)

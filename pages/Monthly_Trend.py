# ==========================================================
# MONTHLY SUMMARY - DYNAMIC VERSION
# ==========================================================
import streamlit as st
import pandas as pd
from pathlib import Path

# ----------------------------------------------------------
# LOAD DATA
# ----------------------------------------------------------
@st.cache_data(ttl=0)
def load_data():

    BASE_DIR = Path(__file__).resolve().parent.parent
    EXCEL_FILE = BASE_DIR / "sales_analysis_report.xlsx"

    try:
        df = pd.read_excel(EXCEL_FILE)
        return df

    except Exception as e:
        st.error(f"Error loading file : {e}")
        return pd.DataFrame()

# Refresh button
col1, col2 = st.columns([1,5])

with col1:
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

# Load latest data
df = load_data()

# ----------------------------------------------------------
# REQUIRED COLUMNS CHECK
# ----------------------------------------------------------
required_cols = [
    "Month",
    "Gross Sales",
    "Net Sales",
    "SIP Sales",
    "Redemption"
]

missing_cols = [col for col in required_cols if col not in df.columns]

if missing_cols:
    st.error(f"Missing columns: {missing_cols}")
    st.write("Available columns:")
    st.write(df.columns.tolist())
    st.stop()

# ----------------------------------------------------------
# CONVERT NUMERIC COLUMNS
# ----------------------------------------------------------
for col in [
    "Gross Sales",
    "Net Sales",
    "SIP Sales",
    "Redemption"
]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# ----------------------------------------------------------
# MONTHLY SUMMARY
# ----------------------------------------------------------
monthly_summary = (
    df.groupby("Month", as_index=False)
      .agg({
          "Gross Sales":"sum",
          "Net Sales":"sum",
          "SIP Sales":"sum",
          "Redemption":"sum"
      })
)

# ----------------------------------------------------------
# SORT MONTHS
# ----------------------------------------------------------
try:
    monthly_summary["SortMonth"] = pd.to_datetime(
        monthly_summary["Month"],
        format="%b-%y"
    )

    monthly_summary = (
        monthly_summary
        .sort_values("SortMonth")
        .drop(columns="SortMonth")
    )

except:
    pass

# ----------------------------------------------------------
# ROUND VALUES
# ----------------------------------------------------------
monthly_summary[
    ["Gross Sales","Net Sales","SIP Sales","Redemption"]
] = monthly_summary[
    ["Gross Sales","Net Sales","SIP Sales","Redemption"]
].round(2)

# ----------------------------------------------------------
# TITLE
# ----------------------------------------------------------
st.subheader("📅 Monthly Summary")

# ----------------------------------------------------------
# TABLE
# ----------------------------------------------------------
st.dataframe(
    monthly_summary,
    use_container_width=True,
    hide_index=True
)

# ----------------------------------------------------------
# DOWNLOAD
# ----------------------------------------------------------
csv = monthly_summary.to_csv(index=False)

st.download_button(
    "⬇ Download Monthly Summary",
    csv,
    "monthly_summary.csv",
    "text/csv"
)

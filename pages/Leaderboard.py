import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ========================================
# LOAD DATA
# ========================================
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

st.title("🏆 Partner Leaderboard")

if df.empty:
    st.stop()

# ========================================
# REQUIRED COLUMNS CHECK
# ========================================
required_cols = [
    "Agent Name",
    "AUM (Eq+Hybrid)",
    "SIP Book Value",
    "No. of Clients"
]

missing_cols = [col for col in required_cols if col not in df.columns]

if missing_cols:
    st.error(f"Missing columns: {missing_cols}")
    st.write("Available columns:")
    st.write(df.columns.tolist())
    st.stop()

# ========================================
# FILTERS
# ========================================
metric = st.selectbox(
    "Rank Partners By",
    [
        "AUM (Eq+Hybrid)",
        "SIP Book Value",
        "No. of Clients"
    ]
)

top_n = st.slider(
    "Top Partners",
    min_value=5,
    max_value=25,
    value=10
)

search_partner = st.text_input("🔍 Search Partner")

# ========================================
# SEARCH
# ========================================
if search_partner:
    df = df[
        df["Agent Name"]
        .astype(str)
        .str.contains(search_partner, case=False, na=False)
    ]

# ========================================
# TOP N DATA
# ========================================
leaderboard = (
    df.sort_values(metric, ascending=False)
      .head(top_n)
      .copy()
)

# ========================================
# BAR CHART
# ========================================
st.subheader(f"Top {top_n} Partners by {metric}")

try:
    fig = px.bar(
        leaderboard,
        x="Agent Name",
        y=metric,
        color=metric,
        text_auto=".2s"
    )

    fig.update_layout(
        height=550,
        xaxis_title="Partner",
        yaxis_title=metric,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Chart Error: {e}")

# ========================================
# STAR RANK
# ========================================
leaderboard["Rank"] = range(1, len(leaderboard) + 1)

leaderboard["Star"] = [
    "⭐⭐⭐⭐⭐" if x <= 3 else
    "⭐⭐⭐⭐" if x <= 7 else
    "⭐⭐⭐"
    for x in leaderboard["Rank"]
]

# ========================================
# TABLE
# ========================================
st.subheader("📋 Leaderboard")

show_cols = [
    "Rank",
    "Star",
    "Agent Name",
    "AUM (Eq+Hybrid)",
    "SIP Book Value",
    "No. of Clients"
]

st.dataframe(
    leaderboard[show_cols],
    use_container_width=True
)

# ========================================
# DOWNLOAD
# ========================================
csv = leaderboard.to_csv(index=False)

st.download_button(
    "⬇ Download Leaderboard",
    data=csv,
    file_name="leaderboard.csv",
    mime="text/csv"
)

# ========================================
# PIE CHART
# ========================================
st.subheader("Top 5 Contribution")

top5 = leaderboard.head(5)

try:
    fig2 = px.pie(
        top5,
        names="Agent Name",
        values=metric,
        hole=0.55
    )

    fig2.update_layout(height=500)

    st.plotly_chart(fig2, use_container_width=True)

except Exception as e:
    st.error(f"Pie Chart Error: {e}")

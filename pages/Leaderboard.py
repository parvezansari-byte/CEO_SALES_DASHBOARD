import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# -------------------------
# LOAD DATA
# -------------------------
@st.cache_data
def load_data():
    return pd.read_excel("sales_analysis_report.xlsx")

df = load_data()

st.title("🏆 Partner Leaderboard")

# -------------------------
# FILTER
# -------------------------
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
    5,
    25,
    10
)

search_partner = st.text_input("🔍 Search Partner")

# -------------------------
# SEARCH
# -------------------------
if search_partner:
    df = df[
        df["Agent Name"]
        .str.contains(search_partner, case=False)
    ]

# -------------------------
# TOP N
# -------------------------
leaderboard = (
    df.sort_values(metric, ascending=False)
      .head(top_n)
)

# -------------------------
# CHART
# -------------------------
st.subheader(f"Top {top_n} Partners by {metric}")

fig = px.bar(
    leaderboard,
    x="Agent Name",
    y=metric,
    color=metric,
    text_auto=".2s"
)

fig.update_layout(height=550)

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# STAR PARTNER SCORE
# -------------------------
leaderboard["Rank"] = range(1, len(leaderboard)+1)

leaderboard["Star"] = [
    "⭐⭐⭐⭐⭐" if x <= 3
    else "⭐⭐⭐⭐"
    if x <= 7
    else "⭐⭐⭐"
    for x in leaderboard["Rank"]
]

# -------------------------
# TABLE
# -------------------------
show_cols = [
    "Rank",
    "Star",
    "Agent Name",
    "AUM (Eq+Hybrid)",
    "SIP Book Value",
    "No. of Clients"
]

st.subheader("📋 Leaderboard")

st.dataframe(
    leaderboard[show_cols],
    use_container_width=True
)

# -------------------------
# DOWNLOAD
# -------------------------
csv = leaderboard.to_csv(index=False)

st.download_button(
    "⬇ Download Leaderboard",
    csv,
    "leaderboard.csv",
    "text/csv"
)

# -------------------------
# TOP 5 PIE
# -------------------------
st.subheader("Top 5 Contribution")

top5 = leaderboard.head(5)

fig2 = px.pie(
    top5,
    names="Agent Name",
    values=metric,
    hole=0.5
)

st.plotly_chart(fig2, use_container_width=True)
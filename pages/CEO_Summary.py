import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==================================================
# LOAD DATA
# ==================================================
@st.cache_data
def load_data():

    BASE_DIR = Path(__file__).resolve().parent.parent
    FILE = BASE_DIR / "sales_analysis_report.xlsx"

    return pd.read_excel(FILE)

df = st.session_state.get("df")

if df is None:
    st.warning("Please upload an Excel file.")
    st.stop()

# ==================================================
# METRICS
# ==================================================
total_aum = df["AUM (Eq+Hybrid)"].sum()/1e7
sip_book = df["SIP Book Value"].sum()/1e7
clients = int(df["No. of Clients"].sum())
partners = len(df)

# ==================================================
# TITLE
# ==================================================
st.markdown("# 📊 Executive Dashboard")

# ==================================================
# KPI CARDS
# ==================================================
col1,col2,col3,col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#16a34a,#22c55e);
    padding:25px;
    border-radius:25px;">
    <h4 style='color:white'>💰 AUM</h4>
    <h1 style='color:white'>₹{total_aum:.2f} Cr</h1>
    </div>
    """,unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#2563eb,#3b82f6);
    padding:25px;
    border-radius:25px;">
    <h4 style='color:white'>📈 SIP Book</h4>
    <h1 style='color:white'>₹{sip_book:.2f} Cr</h1>
    </div>
    """,unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#f59e0b,#d97706);
    padding:25px;
    border-radius:25px;">
    <h4 style='color:white'>👥 Clients</h4>
    <h1 style='color:white'>{clients}</h1>
    </div>
    """,unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="
    background:linear-gradient(135deg,#7c3aed,#9333ea);
    padding:25px;
    border-radius:25px;">
    <h4 style='color:white'>🤝 Partners</h4>
    <h1 style='color:white'>{partners}</h1>
    </div>
    """,unsafe_allow_html=True)

st.divider()

# ==================================================
# TOP 10 PARTNERS
# ==================================================
st.subheader("🏆 Top 10 Partners by AUM")

top10 = (
    df.sort_values(
        "AUM (Eq+Hybrid)",
        ascending=False
    )
    .head(10)
)

top10["AUM Cr"] = top10["AUM (Eq+Hybrid)"]/1e7

fig = px.bar(
    top10.sort_values("AUM Cr"),
    x="AUM Cr",
    y="Agent Name",
    orientation="h",
    color="AUM Cr",
    text="AUM Cr",
    color_continuous_scale="Turbo"
)

fig.update_traces(
    texttemplate="₹%{text:.2f} Cr",
    textposition="outside"
)

fig.update_layout(
    height=650,
    paper_bgcolor="#020817",
    plot_bgcolor="#020817",
    font=dict(color="white"),
    coloraxis_showscale=False
)

st.plotly_chart(fig, use_container_width=True)

# ==================================================
# TOP 3 PARTNERS
# ==================================================
col1,col2,col3 = st.columns(3)

with col1:
    st.success(f"""
### 🥇 Gold Partner

{top10.iloc[0]['Agent Name']}

₹{top10.iloc[0]['AUM Cr']:.2f} Cr
""")

with col2:
    st.info(f"""
### 🥈 Silver Partner

{top10.iloc[1]['Agent Name']}

₹{top10.iloc[1]['AUM Cr']:.2f} Cr
""")

with col3:
    st.warning(f"""
### 🥉 Bronze Partner

{top10.iloc[2]['Agent Name']}

₹{top10.iloc[2]['AUM Cr']:.2f} Cr
""")

st.divider()

# ==================================================
# DONUT CHART
# ==================================================
st.subheader("📊 AUM Contribution")

fig2 = px.pie(
    top10,
    names="Agent Name",
    values="AUM Cr",
    hole=0.65,
    color_discrete_sequence=px.colors.sequential.Agsunset
)

fig2.update_layout(
    height=650,
    paper_bgcolor="#020817",
    font=dict(color="white")
)

st.plotly_chart(fig2,use_container_width=True)

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# LOAD DATA
# ==========================================
@st.cache_data
def load_data():
    BASE_DIR = Path(__file__).resolve().parent.parent
    FILE = BASE_DIR / "sales_analysis_report.xlsx"
    return pd.read_excel(FILE)

df = load_data()

# ==========================================
# METRICS
# ==========================================
total_aum = df["AUM (Eq+Hybrid)"].sum()/1e7
sip_book = df["SIP Book Value"].sum()/1e7
clients = int(df["No. of Clients"].sum())
partners = len(df)

# ==========================================
# CSS
# ==========================================
st.markdown("""
<style>

.card{
padding:25px;
border-radius:25px;
box-shadow:0px 8px 25px rgba(0,0,0,.35);
text-align:center;
margin-bottom:20px;
}

.title{
color:white;
font-size:16px;
font-weight:600;
}

.value{
color:white;
font-size:42px;
font-weight:700;
margin-top:15px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# TITLE
# ==========================================
st.title("📊 Executive Dashboard")

# ==========================================
# KPI CARDS
# ==========================================
c1,c2,c3,c4 = st.columns(4)

with c1:
    st.markdown(
        f"""
        <div class="card" style="background:linear-gradient(135deg,#16a34a,#22c55e)">
        <div class="title">💰 AUM</div>
        <div class="value">₹{total_aum:.2f} Cr</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div class="card" style="background:linear-gradient(135deg,#2563eb,#3b82f6)">
        <div class="title">📈 SIP Book</div>
        <div class="value">₹{sip_book:.2f} Cr</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div class="card" style="background:linear-gradient(135deg,#f59e0b,#d97706)">
        <div class="title">👥 Clients</div>
        <div class="value">{clients}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        f"""
        <div class="card" style="background:linear-gradient(135deg,#7c3aed,#9333ea)">
        <div class="title">🤝 Partners</div>
        <div class="value">{partners}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# ==========================================
# TOP 10 PARTNERS
# ==========================================
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
    paper_bgcolor="#0B1120",
    plot_bgcolor="#0B1120",
    font_color="white",
    coloraxis_showscale=False,
    height=650
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# TOP 3 CARDS
# ==========================================
st.subheader("🥇 Top Performers")

a,b,c = st.columns(3)

with a:
    st.success(
        f"""
🥇 GOLD

{top10.iloc[0]['Agent Name']}

₹{top10.iloc[0]['AUM Cr']:.2f} Cr
"""
    )

with b:
    st.info(
        f"""
🥈 SILVER

{top10.iloc[1]['Agent Name']}

₹{top10.iloc[1]['AUM Cr']:.2f} Cr
"""
    )

with c:
    st.warning(
        f"""
🥉 BRONZE

{top10.iloc[2]['Agent Name']}

₹{top10.iloc[2]['AUM Cr']:.2f} Cr
"""
    )

# ==========================================
# DONUT CHART
# ==========================================
st.subheader("📊 Contribution Analysis")

fig2 = px.pie(
    top10,
    values="AUM Cr",
    names="Agent Name",
    hole=.65,
    color_discrete_sequence=px.colors.sequential.Agsunset
)

fig2.update_layout(
    paper_bgcolor="#0B1120",
    font_color="white",
    height=600
)

st.plotly_chart(fig2, use_container_width=True)

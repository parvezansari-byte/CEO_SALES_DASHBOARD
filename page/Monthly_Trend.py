import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("📈 Monthly Trends Dashboard")

# --------------------
# Monthly Data
# --------------------
trend_df = pd.DataFrame({
    "Month": ["Jan-26","Feb-26","Mar-26","Apr-26","May-26","Jun-26"],
    "Gross Sales":[1.20,1.45,1.80,0.85,1.55,1.35],
    "Net Sales":[0.75,1.05,1.35,-3.93,2.57,0.89],
    "SIP Sales":[3.2,3.5,4.1,3.8,4.0,4.52],
    "Redemption":[0.45,0.40,0.45,4.78,-1.02,0.46]
})

# --------------------
# KPI Cards
# --------------------
c1,c2,c3,c4=st.columns(4)

with c1:
    st.metric("Latest Gross Sales","₹1.35 Cr")

with c2:
    st.metric("Latest Net Sales","₹89 L")

with c3:
    st.metric("Latest SIP Sales","₹4.52 L")

with c4:
    st.metric("Monthly Growth","+12.4 %")

st.divider()

# --------------------
# Gross Sales Trend
# --------------------
st.subheader("Gross Sales Trend")

fig1=px.area(
    trend_df,
    x="Month",
    y="Gross Sales",
    markers=True
)

st.plotly_chart(fig1,use_container_width=True)

# --------------------
# Net Sales Trend
# --------------------
st.subheader("Net Sales Trend")

fig2=px.line(
    trend_df,
    x="Month",
    y="Net Sales",
    markers=True
)

st.plotly_chart(fig2,use_container_width=True)

# --------------------
# SIP Sales Trend
# --------------------
st.subheader("SIP Sales Trend")

fig3=px.bar(
    trend_df,
    x="Month",
    y="SIP Sales",
    color="SIP Sales",
    text_auto=True
)

st.plotly_chart(fig3,use_container_width=True)

# --------------------
# Redemption Trend
# --------------------
st.subheader("Redemption Trend")

fig4=px.line(
    trend_df,
    x="Month",
    y="Redemption",
    markers=True
)

st.plotly_chart(fig4,use_container_width=True)

# --------------------
# Monthly Table
# --------------------
st.subheader("Monthly Summary")

st.dataframe(
    trend_df,
    use_container_width=True
)

import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CEO Sales Dashboard", layout="wide")

st.title("📊 CEO Sales Dashboard")

uploaded_file = st.file_uploader("Upload Sales Analysis Excel", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    st.subheader("Data Preview")
    st.dataframe(df.head())

    st.subheader("Top 10 Partners")

    if "Agent Name" in df.columns and "AUM (Eq+Hybrid)" in df.columns:

        top10 = (
            df.sort_values("AUM (Eq+Hybrid)", ascending=False)
            .head(10)
        )

        fig = px.bar(
            top10,
            x="Agent Name",
            y="AUM (Eq+Hybrid)",
            title="Top 10 Partners by AUM"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(top10)

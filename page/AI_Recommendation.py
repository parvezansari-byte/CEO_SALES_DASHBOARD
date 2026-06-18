import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# --------------------------------
# LOAD DATA
# --------------------------------
@st.cache_data
def load_data():
    return pd.read_excel("sales_analysis_report.xlsx")

df = load_data()

st.title("🤖 AI Insights Engine")

# --------------------------------
# BASIC METRICS
# --------------------------------
total_aum = df["AUM (Eq+Hybrid)"].sum()

top5 = (
    df.sort_values(
        "AUM (Eq+Hybrid)",
        ascending=False
    )
    .head(5)
)

top5_aum = top5["AUM (Eq+Hybrid)"].sum()

concentration = top5_aum / total_aum * 100

# --------------------------------
# KPI CARDS
# --------------------------------
c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "Total AUM",
    f"₹{total_aum/1e7:.2f} Cr"
)

c2.metric(
    "Top 5 Contribution",
    f"{concentration:.1f}%"
)

c3.metric(
    "Partners",
    len(df)
)

c4.metric(
    "Clients",
    int(df["No. of Clients"].sum())
)

st.divider()

# --------------------------------
# CONCENTRATION RISK
# --------------------------------
st.subheader("⚠ Concentration Risk")

if concentration > 50:

    st.error(
        f"Top 5 partners contribute {concentration:.1f}% of AUM."
    )

    st.warning(
        "Develop next 20 mid-sized partners."
    )

else:

    st.success(
        "Partner concentration is healthy."
    )

# --------------------------------
# DORMANT PARTNERS
# --------------------------------
dormant = df[
    df["AUM (Eq+Hybrid)"] < 2500000
]

st.subheader("🔴 Dormant Partner Opportunity")

st.metric(
    "Dormant Partners",
    len(dormant)
)

st.info(
"""
Reactivation Campaign:

✓ Monthly calls

✓ Webinar support

✓ SIP activation drive

✓ Family account mapping
"""
)

# --------------------------------
# TOP PARTNERS
# --------------------------------
st.subheader("🏆 Top 10 AUM Contributors")

top10 = (
    df.sort_values(
        "AUM (Eq+Hybrid)",
        ascending=False
    )
    .head(10)
)

fig = px.bar(
    top10,
    x="Agent Name",
    y="AUM (Eq+Hybrid)",
    color="AUM (Eq+Hybrid)",
    text_auto=".2s"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------
# OPPORTUNITY MATRIX
# --------------------------------
st.subheader("📈 AI Growth Opportunities")

st.success(
"""
Elite Partners

✓ PMS

✓ HNI acquisition

✓ Alternate funds

✓ Family office opportunities
"""
)

st.info(
"""
Growth Partners

✓ Child plans

✓ Retirement plans

✓ Goal based SIP
"""
)

st.warning(
"""
Emerging Partners

✓ Monthly SIP campaign

✓ Lead generation support

✓ Cross sell opportunities
"""
)

st.error(
"""
Dormant Partners

✓ Reactivation drive

✓ Monthly engagement

✓ Webinar programs
"""
)

# --------------------------------
# CEO ACTION ITEMS
# --------------------------------
st.subheader("👔 CEO Action Plan")

action_df = pd.DataFrame({

"Priority":[
1,2,3,4,5
],

"Action":[
"Increase SIP Book to ₹2 Cr",
"Develop Top 20 Growth Partners",
"Reactivate Dormant Partners",
"Target ₹2 Cr Monthly Net Sales",
"Expand Partner Base to 120"
]

})

st.dataframe(
    action_df,
    use_container_width=True
)

# --------------------------------
# PRIORITY CHART
# --------------------------------
fig2 = px.funnel(
    action_df,
    x="Priority",
    y="Action"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# --------------------------------
# AI SUMMARY
# --------------------------------
st.subheader("🧠 AI Summary")

summary = f"""

Current AUM = ₹{total_aum/1e7:.2f} Cr

Top 5 partners contribute {concentration:.1f}% of total AUM.

Priority:

1. Increase SIP Book.

2. Develop Growth Partners.

3. Reactivate Dormant Partners.

4. Achieve ₹2 Cr monthly net sales.

5. Expand partner base.

"""

st.code(summary)

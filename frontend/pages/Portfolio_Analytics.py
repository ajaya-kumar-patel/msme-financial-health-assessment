import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Portfolio Analytics",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Portfolio Analytics")

# -------------------------------------------------------
# Check Prediction
# -------------------------------------------------------

if "prediction" not in st.session_state:
    st.warning("Please generate a prediction from the Home page.")
    st.stop()

result = st.session_state["prediction"]

# -------------------------------------------------------
# Current Business Summary
# -------------------------------------------------------

st.header("Current Business")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Financial Health",
    f'{result["financial_health_score"]:.2f}'
)

col2.metric(
    "Credit Risk Score",
    f'{result["credit_risk_score"]:.2f}'
)

col3.metric(
    "Probability of Default",
    f'{result["probability_of_default"]:.2f}%'
)

col4.metric(
    "Grade",
    result["grade"]
)

st.divider()

# -------------------------------------------------------
# Dimension Scores
# -------------------------------------------------------

st.header("Dimension Performance")

scores = result["dimension_scores"]

df = pd.DataFrame({
    "Dimension": [
        x.replace("_", " ").title()
        for x in scores.keys()
    ],
    "Score": list(scores.values())
})

fig = px.bar(
    df,
    x="Dimension",
    y="Score",
    text="Score",
    range_y=[0, 100],
    title="Business Dimension Scores"
)

fig.update_traces(texttemplate="%{text:.1f}")

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -------------------------------------------------------
# Radar Chart
# -------------------------------------------------------

st.header("Financial Health Radar")

radar = px.line_polar(
    df,
    r="Score",
    theta="Dimension",
    line_close=True,
)

radar.update_traces(fill="toself")

radar.update_layout(
    polar=dict(radialaxis=dict(range=[0, 100])),
    showlegend=False
)

st.plotly_chart(
    radar,
    use_container_width=True
)

st.divider()

# -------------------------------------------------------
# Score Table
# -------------------------------------------------------

st.header("Dimension Details")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# -------------------------------------------------------
# Overall Assessment
# -------------------------------------------------------

st.header("Portfolio Summary")

if result["financial_health_score"] >= 90:
    st.success(
        "Excellent financial profile with very low credit risk."
    )

elif result["financial_health_score"] >= 80:
    st.success(
        "Strong financial profile with low credit risk."
    )

elif result["financial_health_score"] >= 70:
    st.warning(
        "Moderate financial profile. Some improvements are recommended."
    )

else:
    st.error(
        "High credit risk. Business performance should be improved before loan approval."
    )
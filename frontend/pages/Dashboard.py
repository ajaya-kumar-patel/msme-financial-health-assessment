import streamlit as st

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Financial Health Dashboard")

# -------------------------------------------------
# Check prediction exists
# -------------------------------------------------

if "prediction" not in st.session_state:
    st.warning("Please generate a prediction from the Home page.")
    st.stop()

result = st.session_state["prediction"]

# -------------------------------------------------
# Top Metrics
# -------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Financial Health Score",
        f'{result["financial_health_score"]:.2f}'
    )

with col2:
    st.metric(
        "Credit Risk Score",
        f'{result["credit_risk_score"]:.2f}'
    )

with col3:
    st.metric(
        "Probability of Default",
        f'{result["probability_of_default"]:.2f}%'
    )

st.divider()

col4, col5 = st.columns(2)

with col4:
    st.metric(
        "Credit Grade",
        result["grade"]
    )

with col5:
    st.metric(
        "Loan Readiness",
        result["loan_readiness"]
    )

# -------------------------------------------------
# Dimension Scores
# -------------------------------------------------

st.header("Business Dimension Scores")

scores = result["dimension_scores"]

for dimension, score in scores.items():

    st.write(f"**{dimension.replace('_',' ').title()}**")

    st.progress(score / 100)

    st.caption(f"{score:.2f}/100")

st.divider()

# -------------------------------------------------
# Explanation
# -------------------------------------------------

if "explanation" in result:

    st.header("Explanation")

    explanation = result["explanation"]

    if "summary" in explanation:

        for item in explanation["summary"]:

            st.success(item)

st.divider()

# -------------------------------------------------
# Recommendations
# -------------------------------------------------

if "recommendations" in result:

    st.header("Recommendations")

    recommendations = result["recommendations"]

    if isinstance(recommendations, list):

        for rec in recommendations:
            st.info(rec)

    elif isinstance(recommendations, dict):

        for category, recs in recommendations.items():

            st.subheader(category.replace("_", " ").title())

            for rec in recs:
                st.write("•", rec)
import streamlit as st

st.set_page_config(
    page_title="Explainability",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Model Explainability")

# -------------------------------------------------------
# Check prediction exists
# -------------------------------------------------------

if "prediction" not in st.session_state:
    st.warning("Please generate a prediction from the Home page.")
    st.stop()

result = st.session_state["prediction"]

if "explanation" not in result:
    st.warning("No explanation available.")
    st.stop()

explanation = result["explanation"]

# -------------------------------------------------------
# Overall Summary
# -------------------------------------------------------

st.header("Overall Assessment")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Financial Health",
        f'{explanation["financial_health_score"]:.2f}'
    )

with col2:
    st.metric(
        "Business Health",
        f'{explanation["business_health_score"]:.2f}'
    )

with col3:
    st.metric(
        "Grade",
        explanation["grade"]
    )

st.divider()

# -------------------------------------------------------
# Model Explanation
# -------------------------------------------------------

st.header("Why did the model assign this score?")

for item in explanation["summary"]:
    st.success(item)

st.divider()

# -------------------------------------------------------
# Dimension-wise Analysis
# -------------------------------------------------------

st.header("Business Dimension Analysis")

scores = result["dimension_scores"]

for dimension, score in scores.items():

    st.subheader(dimension.replace("_", " ").title())

    st.progress(score / 100)

    if score >= 80:
        st.success("Excellent performance.")

    elif score >= 60:
        st.warning("Average performance. There is room for improvement.")

    else:
        st.error("Weak performance. This dimension is reducing the overall financial health score.")

st.divider()

# -------------------------------------------------------
# Probability of Default
# -------------------------------------------------------

st.header("Credit Risk")

st.metric(
    "Probability of Default",
    f'{result["probability_of_default"]:.2f}%'
)

st.write(
    """
The Probability of Default (PD) represents the estimated likelihood
that the business will default on its financial obligations.

Lower PD indicates lower credit risk and contributes positively
to the overall Financial Health Score.
"""
)
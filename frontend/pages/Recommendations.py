import streamlit as st

st.set_page_config(
    page_title="Recommendations",
    page_icon="💡",
    layout="wide"
)

st.title("💡 Business Improvement Recommendations")

# -------------------------------------------------------
# Check Prediction
# -------------------------------------------------------

if "prediction" not in st.session_state:
    st.warning("Please generate a prediction from the Home page.")
    st.stop()

result = st.session_state["prediction"]

if "recommendations" not in result:
    st.warning("No recommendations available.")
    st.stop()

recommendations = result["recommendations"]

# -------------------------------------------------------
# Overall Summary
# -------------------------------------------------------

st.info(
    "The following recommendations are generated automatically "
    "based on the financial health assessment."
)

st.divider()

# -------------------------------------------------------
# If recommendations are grouped by category
# -------------------------------------------------------

if isinstance(recommendations, dict):

    for category, recs in recommendations.items():

        st.subheader(category.replace("_", " ").title())

        if isinstance(recs, list):

            for rec in recs:
                st.success(rec)

        else:
            st.write(recs)

# -------------------------------------------------------
# If recommendations are simple list
# -------------------------------------------------------

elif isinstance(recommendations, list):

    for rec in recommendations:
        st.success(rec)

# -------------------------------------------------------
# Unexpected Format
# -------------------------------------------------------

else:
    st.write(recommendations)

st.divider()

# -------------------------------------------------------
# General Best Practices
# -------------------------------------------------------

st.header("General Best Practices")

best_practices = [
    "Maintain GST compliance above 95%.",
    "Reduce vendor payment delays.",
    "Keep sufficient average bank balance.",
    "Increase digital transaction adoption.",
    "Reduce cashflow volatility.",
    "Avoid EMI payment defaults.",
    "Maintain consistent payroll payments.",
    "Improve working capital management.",
]

for item in best_practices:
    st.write(f"✅ {item}")
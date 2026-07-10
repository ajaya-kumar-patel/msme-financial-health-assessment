import streamlit as st

st.set_page_config(
    page_title="CredPulse",
    page_icon="🏦",
    layout="wide"
)

## ======================
##        Header
## ======================
st.title("🏦 CredPulse")
st.subheader("AI-powered MSME Credit Risk Assessment")
st.markdown("---")


left, right = st.columns([2, 1])
with left:
    st.markdown(
        """
        CredPulse is an AI-powered credit assessment platform designed for banks,
        NBFCs, and financial institutions to evaluate MSMEs using machine learning
        and financial health analytics.

        The platform provides both **single business assessment** and
        **portfolio-level credit risk analysis**.
        """
    )

with right:
    with st.container(border=True):
        st.markdown("## Quick Overview")
        items = [
            "🏦 <b>MSME Credit Assessment</b>",
            "📊 <b>Portfolio Risk Analytics</b>",
            "📈 </b>PD & Health Score</b>",
            "🟢 </b>Loan Readiness Classification</b>",
            "🔍 <b>Explainable AI</b>",
            "💡 <b>Smart Recommendations</b>",
        ]
        for item in items:
            st.markdown(
                f"""
                <div style="padding:6px 0;">
                    {item}
                </div>
                <hr style="margin:4px 0;">
                """,
                unsafe_allow_html=True,
            )

st.markdown("---")
## ======================
##      MAIN MODULES
## ======================

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("## 📋 Business Assessment")
        st.write("""
                Assess a single MSME by entering its financial,
                transactional and operational information.

                ### Features

                - Probability of Default (PD)
                - Financial Health Score
                - Credit Risk Score
                - Business Health Dimensions
                - Explainability
                - Smart Recommendations
                - Download Assessment Report
                        """
            )

        if st.button("📋 Open Customer Assessment", use_container_width=True):
            st.switch_page("pages/Customer_Assessment.py")

with col2:
    with st.container(border=True):
        st.markdown("## 🏢 Portfolio Analytics")
        st.write("""
                Upload an MSME portfolio and evaluate the overall
                credit quality of all businesses.

                ### Features

                - Portfolio KPIs
                - Risk Distribution
                - Grade Distribution
                - Loan Readiness Analysis
                - Industry-wise Insights
                - High Risk Businesses
                - Drill-down to Individual Business
                        """
            )
        
        if st.button("🏢 Open Portfolio Analytics", use_container_width=True):
            st.switch_page("pages/Portfolio_Analytics.py")

st.markdown("---")
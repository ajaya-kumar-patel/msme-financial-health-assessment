import streamlit as st
import pandas as pd
import plotly.express as px


def display_result(result):
    row1 = st.columns(4)
    with row1[0]:
        with st.container(border=True):
            st.metric("Loan Readiness", result["loan_readiness"])
    with row1[1]: 
        with st.container(border=True):
            st.metric("Financial Health", result["financial_health_score"])
    with row1[2]:
        with st.container(border=True):
            st.metric("Probability of Default", f"{result['probability_of_default']:.1%}")
    with row1[3]:
        with st.container(border=True):
            st.metric("Grade", result["grade"])

    ## Explanation
    st.markdown("""
        <style>

        /* Space between tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 12px;
        }

        /* Each tab */
        .stTabs [data-baseweb="tab"] {
            background: #F3F4F6;
            border: 1px solid #D1D5DB;
            border-radius: 12px;
            padding: 10px 24px;
            height: 52px;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.2s ease;
        }

        /* Hover */
        .stTabs [data-baseweb="tab"]:hover {
            background: #E5E7EB;
        }

        /* Selected tab */
        .stTabs [aria-selected="true"] {
            background: #2563EB;
            color: white;
            border-color: #2563EB;
        }

        </style>
        """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(
    [
        "📝 Explanation",
        "📊 Dimension Analysis",
        "💡 Recommendations",
    ])

    with tab1:
        st.write("### 📝 Explanation")

        explanation = result["explanation"]

        st.markdown("#### Summary")
        st.info(explanation["summary"])

        st.markdown("#### Credit Risk")
        st.write(explanation["credit_risk"])

        st.markdown("#### Key Strength")
        st.success(explanation["strength"])

        st.markdown("#### Area for Improvement")
        st.warning(explanation["weakness"])

    with tab2:
        st.markdown("#### Dimension Analysis")
        row1 = st.columns(3)
        row2 = st.columns(3)
        count = 0

        for dimension, details in explanation["dimension_analysis"].items():
            if(count<3):
                with row1[count]:
                    with st.container(border=True):
                        st.markdown(f"""
                                    **{dimension.replace("_", " ").title()}**

                                    - **Score:** {details['score']}
                                    - **Status:** {details['status'].title()}
                                    - {details['message']}
                                    """
                                    )
            else:
                with row2[count-3]:
                    with st.container(border=True):
                        st.markdown(f"""
                                    **{dimension.replace("_", " ").title()}**

                                    - **Score:** {details['score']}
                                    - **Status:** {details['status'].title()}
                                    - {details['message']}
                                    """
                                    )
            
            count+=1

    with tab3:
        st.write("### 💡 Recommendations")

        for rec in result["recommendations"]:
            st.markdown(f"- {rec}")
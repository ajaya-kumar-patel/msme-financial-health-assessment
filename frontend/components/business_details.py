import streamlit as st
import pandas as pd


def show_business_details(df):
    st.subheader("🏢 Business Details")
    df = df.set_index("Business_ID").copy()

    business_ids = sorted(
                    df.index,
                    key=lambda x: int(x.replace("BID", ""))
                )
    
    business = st.selectbox(
        "Select Business ID",
        business_ids
    )

    row = df.loc[business]

    row1 = st.columns(4)
    with row1[0]:
        with st.container(border=True):
            st.metric("Loan Readiness", row["loan_readiness"])
    with row1[1]: 
        with st.container(border=True):
            st.metric("Financial Health", row["financial_health_score"])
    with row1[2]:
        with st.container(border=True):
            st.metric("Probability of Default", f"{row['probability_of_default']:.1%}")
    with row1[3]:
        with st.container(border=True):
            st.metric("Grade", row["grade"])
            # st.metric("Credit Risk Score",row["credit_risk_score"])

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
                
        button[data-baseweb="tab"] {
            flex: 15;
            justify-content: center;
        }

        div[data-baseweb="tab-list"] {
            display: flex;
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

        explanation = row["explanation"]

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

        for rec in row["recommendations"]:
            st.markdown(f"- {rec}")
        

    
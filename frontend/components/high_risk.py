import streamlit as st

def show_high_risk(df):
    st.subheader("🔴 Highest Risk Businesses")
    high = (
        df.sort_values(
            "probability_of_default",
            ascending=False
        )
        .head(5)
    )

    columns = []
    if "Business_ID" in df.columns:
        columns.append("Business_ID")
    columns.extend([
                "financial_health_score",
                "probability_of_default",
                "grade",
                "loan_readiness"
            ])
    
    filtered_df = high[columns].copy()
    filtered_df.rename(columns = {
        "Business_ID":"BID",
        "financial_health_score":"Health Score",
        "probability_of_default": "PD",
        "grade": "Grade",
        "loan_readiness": "Loan Readiness"
    }, inplace = True)

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )
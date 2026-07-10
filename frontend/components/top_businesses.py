import streamlit as st


def show_top_businesses(df, n=5):

    st.subheader("🏆 Top Businesses")

    top = (
        df.sort_values(
            "financial_health_score",
            ascending=False
        )
        .head(n)
    )

    columns = []

    ## Include Business_Name if available
    if "Business_ID" in df.columns:
        columns.append("Business_ID")

    columns.extend([
        "financial_health_score",
        "grade",
        "probability_of_default",
        "loan_readiness"
    ])

    filtered_df = top[columns].copy()
    
    filtered_df.rename(columns = {
        "Business_ID":"BID",
        "financial_health_score":"Health Score",
        "probability_of_default": "PD",
        "grade": "Grade",
        "loan_readiness": "Loan Readiness"
    }, inplace = True)

    st.dataframe(
        filtered_df,
        hide_index=True,
        use_container_width=True
    )
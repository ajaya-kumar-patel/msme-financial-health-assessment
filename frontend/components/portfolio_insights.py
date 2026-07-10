import streamlit as st
import pandas as pd


def show_portfolio_insights(df):

    # st.subheader("🧠 Portfolio Insights")
    total_businesses = len(df)
    insights = []
    insights.append(f"Total Businesses: **{total_businesses}**")

    ## Average Financial Health Score
    avg_health = df["financial_health_score"].mean()
    avg_pd = df["probability_of_default"].mean()
    insights.append(f"Average Financial Health Score: **{avg_health:.1f}/100**")
    insights.append(f"Average Probability of Default: **{(avg_pd*100):.1f}%**")

    ## Highest risk industry
    highest_risk_industry = (
        df.groupby("Industry_Type")["probability_of_default"]
        .mean()
        .idxmax()
    )
    insights.append(f"Highest Risk Industry: {highest_risk_industry}")
    
    ## Low risk industry
    lowest_risk_industry = (
        df.groupby("Industry_Type")["probability_of_default"]
        .mean()
        .idxmin()
    )
    insights.append(f"Lowest Risk Industry: {lowest_risk_industry}")

    ## Weakest Dimension
    dimension_df = pd.DataFrame(df["dimension_scores"].tolist())

    weakest_dimension = (
        dimension_df.mean()
        .sort_values()
        .index[0]
    )
    insights.append(f"Weakest Portfolio Dimension: {weakest_dimension}")

    ## High PD
    high_pd = (
        df["probability_of_default"] > 0.30
    ).sum()

    insights.append(
        f"**{high_pd}** businesses have PD above **30%**."
    )

    ## Display
    for insight in insights:
        st.markdown(f"✅ {insight}")
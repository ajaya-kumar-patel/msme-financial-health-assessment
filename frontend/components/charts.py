import plotly.express as px
import streamlit as st
import pandas as pd

def show_score_distribution(df):

    ##   Portfolio average
    avg_score = df["financial_health_score"].mean()

    fig = px.histogram(
        df,
        x="financial_health_score",
        nbins=20,
        color_discrete_sequence=["#4F81BD"],
        opacity=0.85
    )

    ## Average reference line
    fig.add_vline(
        x=avg_score,
        line_dash="dash",
        line_color="red",
        line_width=2,
        annotation_text=f"Avg: {avg_score:.1f}",
        annotation_position="top right"
    )

    fig.update_layout(
        title="📊 Financial Health Score Distribution",
        height=320,
        bargap=0.05,
        legend_title="Grade",
        xaxis_title="Financial Health Score",
        yaxis_title="Number of Businesses",
        margin=dict(l=20, r=20, t=60, b=20)
    )

    fig.update_xaxes(range=[0, 100])

    st.plotly_chart(
        fig,
        use_container_width=True
    )

def show_industry_risk(df):

    industry = (
        df.groupby("Industry_Type", as_index=False)
        .agg(
            Avg_PD=("probability_of_default", "mean"),
            Businesses=("Industry_Type", "count")
        )
        .sort_values("Avg_PD", ascending=False)
    )

    fig = px.bar(
        industry,
        x="Avg_PD",
        y="Industry_Type",
        orientation="h",
        color="Avg_PD",
        color_continuous_scale="Reds",
        text=industry["Avg_PD"].map(lambda x: f"{x:.1%}"),
        hover_data={
            "Avg_PD": ":.2%",
            "Businesses": True
        }
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        title="🏭 Industry Risk",
        height=320,
        xaxis_title="Average Probability of Default",
        yaxis_title="Industry",
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    fig.update_xaxes(tickformat=".0%")

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    
def show_pd_distribution(df):

    fig = px.histogram(
        df,
        x="probability_of_default",
        nbins=10,
        color="grade"
    )

    fig.update_layout(
        height=320,
        xaxis_title="Probability of Default",
        yaxis_title="Number of Businesses",
        bargap=0.05
    )

    st.plotly_chart(fig, use_container_width=True)


def show_dimension_scores(df):

    # Convert list of dictionaries into DataFrame
    dimensions = pd.DataFrame(df["dimension_scores"].tolist())

    # Calculate average score for each dimension
    avg = (
        dimensions.mean()
        .reset_index()
    )

    avg.columns = [
        "Dimension",
        "Average Score"
    ]

    # Sort from weakest to strongest
    avg = avg.sort_values(
        "Average Score",
        ascending=True
    )

    fig = px.bar(
        avg,
        x="Average Score",
        y="Dimension",
        orientation="h",
        color="Average Score",
        text="Average Score",
        color_continuous_scale="RdYlGn",
        range_color=[0, 100]
    )

    fig.update_traces(
        texttemplate="%{text:.1f}",
        textposition="outside"
    )

    fig.update_layout(
        title="📊 Average Dimension Scores",
        height=320,
        xaxis_title="Average Score",
        yaxis_title="Dimension",
        coloraxis_showscale=False,
        margin=dict(l=20, r=20, t=50, b=20)
    )

    fig.update_xaxes(
        range=[0, 100]
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def show_risk_matrix(df):

    # Portfolio averages
    avg_health = df["financial_health_score"].mean()
    avg_pd = df["probability_of_default"].mean()

    fig = px.scatter(
        df,
        x="financial_health_score",
        y="probability_of_default",
        color="grade",
        size="Monthly_GST_Sales",
        hover_name="Industry_Type",
        hover_data={
            "financial_health_score":":.1f",
            "probability_of_default":":.2%",
            "Monthly_GST_Sales":":,.0f",
            "Business_Size":True,
            "loan_readiness":True,
            "grade":True
        },
        labels={
            "financial_health_score":"Financial Health Score",
            "probability_of_default":"Probability of Default"
        },
        size_max=25,
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    # Average Health Score
    fig.add_vline(
        x=avg_health,
        line_dash="dash",
        line_color="gray",
        annotation_text=f"Avg Health: {avg_health:.1f}",
        annotation_position="top"
    )

    # Average PD
    fig.add_hline(
        y=avg_pd,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Avg PD: {avg_pd:.1%}",
        annotation_position="right"
    )

    fig.update_layout(
        title="🎯 Portfolio Risk Matrix",
        height=350,
        legend_title="Grade",
        margin=dict(l=20, r=20, t=50, b=20)
    )

    fig.update_xaxes(
        title="Financial Health Score",
        range=[0, 100]
    )

    fig.update_yaxes(
        title="Probability of Default",
        tickformat=".0%"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
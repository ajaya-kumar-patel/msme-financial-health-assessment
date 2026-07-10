import streamlit as st
import plotly.express as px
import pandas as pd

def show_portfolio_summary(df):

    st.markdown("""
                <div style="
                background:#1E3A8A;
                padding:10px 15px;
                border-radius:8px;
                color:white;
                font-size:22px;
                font-weight:600;
                margin-top:10px;
                margin-bottom:15px;
                ">
                📂 Portfolio Composition
                </div>
                """, unsafe_allow_html=True)

    # ==========================
    # Counts
    # ==========================

    total = len(df)

    size_counts = df["Business_Size"].value_counts()

    micro = size_counts.get("Micro", 0)
    small = size_counts.get("Small", 0)
    medium = size_counts.get("Medium", 0)

    # ==========================
    # KPI Cards
    # ==========================

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.metric(
            "Businesses",
            total
        )

    with k2:
        st.metric(
            "Micro",
            micro
        )

    with k3:
        st.metric(
            "Small",
            small
        )

    with k4:
        st.metric(
            "Medium",
            medium
        )

    st.markdown("---")

    # ==========================
    # Charts
    # ==========================

    left, right = st.columns(2)

    with left:

        st.markdown("#### Industry Distribution")

        industry = (
            df["Industry_Type"]
            .value_counts()
            .reset_index()
        )

        industry.columns = [
            "Industry",
            "Businesses"
        ]

        fig = px.bar(
            industry,
            x="Industry",
            y="Businesses",
            color="Industry",
            text="Businesses"
        )

        fig.update_layout(
            showlegend=False,
            height=300,
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.markdown("#### Entity Type Distribution")

        entity = (
            df["Entity_Type"]
            .value_counts()
            .reset_index()
        )

        entity.columns = [
            "Entity Type",
            "Businesses"
        ]

        fig = px.pie(
            entity,
            names="Entity Type",
            values="Businesses",
            hole=0.55
        )

        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=20, b=20)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )
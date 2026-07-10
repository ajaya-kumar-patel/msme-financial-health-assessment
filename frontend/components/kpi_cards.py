import streamlit as st

def show_kpis(df):
    row1 = st.columns(4)
    with row1[0]:
        with st.container(border=True):
            st.metric(
                "Businesses",
                len(df)
            )
    with row1[1]:
        with st.container(border=True):
            st.metric(
                "Avg Health Score",
                round(df["financial_health_score"].mean(), 2)
            )
    with row1[2]:
        with st.container(border=True):
            st.metric(
                "Avg PD",
                f"{df['probability_of_default'].mean():.1%}"
            )
    with row1[3]:
        with st.container(border=True):
            st.metric(
                "High Risk",
                df["grade"].isin(["BB", "B", "CCC"]).sum()
            )

    with st.container(border=True):
        st.markdown("#### 🏦 Loan Readiness")
        row2 = st.columns(4)
        with row2[0]:
            st.metric(
                "🟢 Loan Ready",
                (df["loan_readiness"] == "LOAN READY").sum()
            )
        with row2[1]:
            st.metric(
                "🟡 Fast Review",
                (df["loan_readiness"] == "FAST REVIEW").sum()
            )
        with row2[2]:
            st.metric(
                "🟠 Review",
                (df["loan_readiness"] == "REVIEW").sum()
            )
        with row2[3]:
            st.metric(
                "🔴 Not Ready",
                (df["loan_readiness"] == "NOT READY").sum()
            )
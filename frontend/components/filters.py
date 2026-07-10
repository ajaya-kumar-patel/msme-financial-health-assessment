import streamlit as st

def portfolio_filters(df):
    c1, c2 = st.columns(2)
    with c1:
        grade = st.selectbox(
            "Grade",
            ["All"] + sorted(df["grade"].unique())
        )
    with c2:
        readiness = st.selectbox(
            "Loan Readiness",
            ["All", "LOAN READY", "FAST REVIEW", "REVIEW", "NOT READY"]
        )
    
    filtered = df.copy()
    if grade != "All":
        filtered = filtered[
            filtered["grade"] == grade
        ]
    if readiness != "All":
        filtered = filtered[
            filtered["loan_readiness"] == readiness
        ]

    return filtered
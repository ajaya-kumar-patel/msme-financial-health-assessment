import streamlit as st

def format_recommendations(recs):
    if not recs:
        return ""

    return "\n".join(
        f"• {r['recommendation']}"
        for r in recs
    )

def show_tables(df):
    df = df.drop(columns = ["raw_pd", "dimension_scores","explanation", "recommendations"])

    # df["recommendations"] = df["recommendations"].apply(
    #     format_recommendations
    # )

    st.dataframe(
        df,
        use_container_width=True
    )
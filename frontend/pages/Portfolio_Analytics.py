import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import StringIO

from components.filters import portfolio_filters
from components.kpi_cards import show_kpis
from components.charts import (show_score_distribution, show_industry_risk, 
                               show_dimension_scores, show_risk_matrix)
from components.tables import show_tables
from components.portfolio_summary import show_portfolio_summary

from components.high_risk import show_high_risk
from components.business_details import show_business_details
from components.portfolio_insights import show_portfolio_insights
from components.top_businesses import show_top_businesses


@st.cache_data
def analyze_portfolio(file_bytes):
    input_df = pd.read_csv(StringIO(file_bytes.decode()))

    model_df = input_df.drop(columns=["Business_ID"], errors="ignore")

    csv_buffer = StringIO()
    model_df.to_csv(csv_buffer, index=False)

    files = {
        "file": (
            "portfolio.csv",
            csv_buffer.getvalue(),
            "text/csv"
        )
    }

    response = requests.post(
        "http://127.0.0.1:8000/portfolio",
        files=files,
        timeout=300
    )

    response.raise_for_status()
    
    data = response.json()

    return input_df, data


st.set_page_config(
    page_title="Portfolio_Analytics",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Portfolio Analytics")

st.write(
    """ Upload a portfolio CSV containing multiple MSMEs.
    Each business will be evaluated using the CredPulse model.
    """)

upload_file = st.file_uploader(
    "Upload Portfolio CSV 📤",
    type = ["csv"]
)

if upload_file is not None:
    file_bytes = upload_file.getvalue()
    if ("file_bytes" not in st.session_state or st.session_state.file_bytes != file_bytes):
        with st.spinner("Analyzing portfolio..."):
            try:
                input_df, data = analyze_portfolio(file_bytes)
                st.toast("✅ Portfolio analyzed successfully!", icon="🎉")
            except Exception as e:
                st.error(f"Portfolio analysis failed:\n{e}")
                st.stop()

            predictions = pd.DataFrame(data["predictions"])

            dashboard_df = pd.concat(
                [input_df.reset_index(drop=True),
                 predictions.reset_index(drop=True)],
                axis=1
            )

            st.session_state.file_bytes = file_bytes
            st.session_state.dashboard_df = dashboard_df
            st.session_state.input_df = input_df
        
    dashboard_df = st.session_state.dashboard_df
    input_df = st.session_state.input_df

    with st.expander(
            "📂 Portfolio Composition (Click to view uploaded portfolio summary)",
            expanded=False
            ):
        with st.container(border=True):
            show_portfolio_summary(input_df)
    
    ## Load Readiness classification
    with st.expander("📖 Loan Readiness Guide"):
        st.table({
            "Health Score": ["90–100", "80–89", "70–79", "<70"],
            "Decision": [
                "🟢 Loan Ready",
                "🟡 Fast Review",
                "🟠 Review",
                "🔴 Not Ready"
            ]
        })

    with st.container(border=True):
        st.markdown("""
            <div style="
            background:#166534;
            padding:10px 15px;
            border-radius:8px;
            color:white;
            font-size:22px;
            font-weight:600;
            margin-top:30px;
            margin-bottom:15px;
            ">
            📈 Risk Analytics
            </div>
            """, unsafe_allow_html=True)
        filtered_df = portfolio_filters(dashboard_df)

        if filtered_df.empty:
            st.warning(
                "No businesses match the selected filters. "
                "Try broadening your filter criteria or reset the filters."
            )
            st.stop()

        # KPIs
        show_kpis(filtered_df)

        # st.divider()
        st.info(
            "💡 Want a quick portfolio summary? Expand **'View Portfolio Insights'** below."
        )
        with st.expander("🧠 View Portfolio Insights", expanded=False):
            show_portfolio_insights(filtered_df)
        st.divider()

        # Main charts
        left, right = st.columns(2)
        with left:
            show_score_distribution(filtered_df)
        with right:
            show_industry_risk(filtered_df)

        st.divider()

        # Advanced analytics
        left, right = st.columns(2)
        with left:
            show_dimension_scores(filtered_df)
        with right:
            show_risk_matrix(filtered_df)

        st.divider()

        # Risk matrix
        left, right = st.columns(2)
        with left:
            show_top_businesses(filtered_df)
        with right:
            show_high_risk(filtered_df)

        st.divider()

        # Business drill-down
        show_business_details(filtered_df)

        st.divider()

        # Download
        csv = dashboard_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇ Download Results",
            csv,
            "portfolio_predictions.csv",
            "text/csv"
        )

        # Portfolio table (only once)
        with st.expander("📋 Portfolio Details", expanded=False):
            show_tables(filtered_df)

else:
    st.info("📤 Upload a portfolio CSV to begin analysis.")
    
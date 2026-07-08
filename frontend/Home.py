# Collects all MSME input features.
# Sends them to the FastAPI /predict endpoint.
# Saves the prediction in st.session_state, allowing the remaining pages (Dashboard.py, Explainability.py, Recommendations.py, etc.) to access the same prediction without calling the API again.

import streamlit as st
from api_client import predict

st.set_page_config(
    page_title="CredPulse",
    page_icon="💳",
    layout="wide"
)

st.title("💳 CredPulse")
st.subheader("AI-powered MSME Credit Risk Assessment & Financial Health Scoring")

st.markdown("---")

with st.form("prediction_form"):

    st.header("Business Information")

    col1, col2 = st.columns(2)

    with col1:
        business_size = st.selectbox(
            "Business Size",
            ["Micro", "Small", "Medium"]
        )

        business_age = st.number_input(
            "Business Age (Years)",
            min_value=0.0,
            value=5.0
        )

        industry = st.selectbox(
            "Industry Type",
            [
                "Manufacturing",
                "Retail",
                "Services",
                "Agriculture"
            ]
        )

        entity = st.selectbox(
            "Entity Type",
            [
                "Proprietorship",
                "Partnership",
                "Private Limited",
                "LLP"
            ]
        )

        monthly_gst_sales = st.number_input(
            "Monthly GST Sales",
            min_value=0.0,
            value=100000.0
        )

        gst_growth = st.number_input(
            "GST Growth Rate",
            value=0.10,
            format="%.4f"
        )

        gst_delay = st.number_input(
            "GST Filing Delay (Days)",
            min_value=0.0,
            value=5.0
        )

        gst_compliance = st.slider(
            "GST Compliance Rate",
            0.0,
            1.0,
            0.95
        )

        upi_count = st.number_input(
            "Monthly UPI Count",
            min_value=0,
            value=20
        )

        upi_value = st.number_input(
            "Monthly UPI Value",
            min_value=0.0,
            value=20000.0
        )

    with col2:

        digital_ratio = st.slider(
            "Digital Sales Ratio",
            0.0,
            1.0,
            0.50
        )

        bank_balance = st.number_input(
            "Average Bank Balance",
            min_value=0.0,
            value=50000.0
        )

        monthly_credit = st.number_input(
            "Monthly Credit",
            min_value=0.0,
            value=100000.0
        )

        monthly_debit = st.number_input(
            "Monthly Debit",
            min_value=0.0,
            value=80000.0
        )

        cashflow_volatility = st.slider(
            "Cashflow Volatility",
            0.0,
            1.0,
            0.20
        )

        employee_count = st.number_input(
            "Employee Count",
            min_value=0,
            value=5
        )

        payroll = st.slider(
            "Payroll Consistency",
            0.0,
            1.0,
            0.90
        )

        vendor_delay = st.number_input(
            "Vendor Payment Delay (Days)",
            min_value=0.0,
            value=10.0
        )

        working_cycle = st.number_input(
            "Working Capital Cycle (Days)",
            min_value=0.0,
            value=60.0
        )

        emi_bounce = st.number_input(
            "EMI Bounce Count",
            min_value=0,
            value=0
        )

    submit = st.form_submit_button(
        "Predict Financial Health",
        use_container_width=True
    )


if submit:

    customer = {
        "Business_Size": business_size,
        "Business_Age": business_age,
        "Industry_Type": industry,
        "Entity_Type": entity,
        "Monthly_GST_Sales": monthly_gst_sales,
        "GST_Growth_Rate": gst_growth,
        "GST_Filing_Delay": gst_delay,
        "GST_Compliance_Rate": gst_compliance,
        "Monthly_UPI_Count": upi_count,
        "Monthly_UPI_Value": upi_value,
        "Digital_Sales_Ratio": digital_ratio,
        "Average_Bank_Balance": bank_balance,
        "Monthly_Credit": monthly_credit,
        "Monthly_Debit": monthly_debit,
        "Cashflow_Volatility": cashflow_volatility,
        "Employee_Count": employee_count,
        "Payroll_Consistency": payroll,
        "Vendor_Payment_Delay": vendor_delay,
        "Working_Capital_Cycle": working_cycle,
        "EMI_Bounce_Count": emi_bounce
    }

    with st.spinner("Running AI model..."):

        result = predict(customer)

    if result.get("success") is False:
        st.error(result["message"])

    else:
        st.success("Prediction completed successfully.")

        st.session_state["customer"] = customer
        st.session_state["prediction"] = result

        st.info(
            "Go to the Dashboard page from the left sidebar to view the complete analysis."
        )
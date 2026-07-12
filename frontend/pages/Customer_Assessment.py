import streamlit as st
from api_client import predict
from components.display_assessment_result import display_result
st.set_page_config(
    page_title="Customer Assessment",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Customer Assessment")
st.caption(
    "Enter the MSME details below to assess financial health, "
    "credit risk, and loan readiness."
)

st.markdown("---")

with st.form("prediction_form"):

    # ======================
    #     Business Profile
    # ======================
    with st.container(border=True):
        st.subheader("🏢 Business Profile")
        c1, c2 = st.columns(2)

        with c1:
            business_size = st.selectbox(
                "Business Size",
                ["Micro", "Small", "Medium"],
                help="Select the business category.",
                index = 0
            )

            business_age = st.number_input(
                "Business Age (Years)",
                min_value=0.0,
                value=8.0,
                step=0.5
            )

        with c2:
            industry = st.selectbox(
                "Industry Type",
                ["Manufacturing", "Retail", "Services", "Agriculture", "Wholesale", "Hospitality"],
                index = 1
            )
            entity = st.selectbox(
                "Entity Type",
                ["Proprietorship", "Partnership", "Private Limited", "LLP"],
                index = 3
            )

    st.write("")

    # ======================
    # Financial Performance
    # ======================
    with st.container(border=True):
        st.subheader("💰 Financial Performance")
        c1, c2 = st.columns(2)
        with c1:
            monthly_gst_sales = st.number_input(
                "Monthly GST Sales (₹)",
                min_value=0.0,
                value= 670910.0,
                step = 10000.0
            )
            monthly_credit = st.number_input(
                "Monthly Credit (₹)",
                min_value=0.0,
                value = 681154.0,
                step = 10000.0
            )

            average_bank_balance = st.number_input(
                "Average Bank Balance (₹)",
                min_value=0.0,
                value=94554.0,
                step = 5000.0
            )

        with c2:
            monthly_debit = st.number_input(
                "Monthly Debit (₹)",
                min_value=0.0,
                value = 508850.0,
                step = 5000.0
            )
            gst_growth = st.slider(
                "GST Growth Rate (%)",
                -50, 100, 2,
                help="Annual GST sales growth."
            ) / 100

            cashflow_volatility = st.slider(
                "Cashflow Volatility",
                0.0, 1.0, 0.395,
                help="Lower is better."
            )

    st.write("")

    # ======================
    #       Compliance
    # ======================
    with st.container(border=True):
        st.subheader("📑 Compliance")
        c1, c2 = st.columns(2)
        with c1:
            gst_compliance = st.slider(
                "GST Compliance Rate",
                0.0, 1.0,
                1.0
            )

        with c2:
            gst_delay = st.number_input(
                "GST Filing Delay (Days)",
                min_value=0.0, value=1.0, step = 1.0
            )
    st.write("")

    # ======================
    #      Digital Adoption
    # ======================
    with st.container(border=True):
        st.subheader("📱 Digital Adoption")
        c1, c2 = st.columns(2)
        with c1: 
            upi_count = st.number_input(
                "Monthly UPI Count",
                min_value=0,
                value=45
            )

            digital_ratio = st.slider(
                "Digital Sales Ratio",
                0.0, 1.0,
                0.8
            )

        with c2:
            upi_value = st.number_input(
                "Monthly UPI Value (₹)",
                min_value=0.0, value = 57322.0, step = 1000.0
            )

    st.write("")

    # ======================
    # Operations & Stability
    # ======================
    with st.container(border=True):
        st.subheader("⚙️ Operations & Stability")
        c1, c2 = st.columns(2)
        with c1:
            employee_count = st.number_input(
                "Employee Count",
                min_value=0, value=6
            )

            payroll = st.slider(
                "Payroll Consistency",
                0.0, 1.0,
                0.80
            )

            vendor_delay = st.number_input(
                "Vendor Payment Delay (Days)",
                min_value=0.0,
                value=17.0,
                step = 1.0
            )

        with c2:
            working_cycle = st.number_input(
                "Working Capital Cycle (Days)",
                min_value=0.0,
                value= 46.0,
                step = 1.0
            )

            emi_bounce = st.number_input(
                "EMI Bounce Count",
                min_value=0, value = 1
            )

    st.markdown("---")

    submit = st.form_submit_button(
        "🚀 Assess Business",
        use_container_width=True,
        type="primary"
    )

# ======================
# Prediction
# ======================
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
        "Average_Bank_Balance": average_bank_balance,
        "Monthly_Credit": monthly_credit,
        "Monthly_Debit": monthly_debit,
        "Cashflow_Volatility": cashflow_volatility,
        "Employee_Count": employee_count,
        "Payroll_Consistency": payroll,
        "Vendor_Payment_Delay": vendor_delay,
        "Working_Capital_Cycle": working_cycle,
        "EMI_Bounce_Count": emi_bounce,
    }

    with st.spinner("🤖 Running AI assessment..."):
        result = predict(customer)

    if result.get("success") is False:
        st.error(result["message"])

    else:
        st.toast(
            "Assessment completed successfully.",
            icon="🎉"
        )

        st.session_state["customer"] = customer
        st.session_state["prediction"] = result


if "prediction" in st.session_state:
    result = st.session_state["prediction"]
    st.markdown("---")
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

    st.header("📊 Assessment Result")
    
    display_result(result)
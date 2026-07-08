import numpy as np
import pandas as pd
import logging
from config import RANDOM_SEED

industry_profile = {
    "Retail": {
        "sales_mean": 14.8,
        "sales_sigma": 0.70,
        "digital_beta": (8,2),
        "employees": 6,
        "working_capital": 35,
        "gst_delay": (2,4)
    },

    "Manufacturing": {
        "sales_mean": 15.5,
        "sales_sigma": 0.80,
        "digital_beta": (4,4),
        "employees": 25,
        "working_capital": 95,
        "gst_delay": (2.5,6)
    },

    "Services": {
        "sales_mean": 14.9,
        "sales_sigma": 0.65,
        "digital_beta": (7,2),
        "employees": 10,
        "working_capital": 40,
        "gst_delay": (2,3)
    },

    "Wholesale": {
        "sales_mean": 15.3,
        "sales_sigma": 0.75,
        "digital_beta": (5,3),
        "employees": 12,
        "working_capital": 60,
        "gst_delay": (2.2,5)
    },

    "Hospitality": {
        "sales_mean": 14.7,
        "sales_sigma": 0.90,
        "digital_beta": (7,3),
        "employees": 15,
        "working_capital": 30,
        "gst_delay": (2.5,5)
    },

    "Agriculture": {
        "sales_mean": 14.4,
        "sales_sigma": 1.00,
        "digital_beta": (3,5),
        "employees": 8,
        "working_capital": 75,
        "gst_delay": (3,8)
    }
}

upi_lambda = {
    "Retail": 120,
    "Manufacturing": 35,
    "Services": 80,
    "Wholesale": 55,
    "Hospitality": 100,
    "Agriculture": 25
}


def generate_msmes(n, random_state = RANDOM_SEED):
    np.random.seed(random_state)

    logging.info("Generating MSME features...")
    # ==================================
    #               Industry Type
    # ===================================
    industries = [
        "Retail", "Manufacturing", "Services",
        "Wholesale", "Hospitality", "Agriculture"
    ]

    probabilities = [
        0.30, 0.20, 0.25,
        0.10, 0.10, 0.05
    ]

    industry_type = np.random.choice(
        industries,
        size=n,
        p=probabilities
    )

    # ==================================
    # Business Size
    # ==================================
    business_sizes = ["Micro", "Small", "Medium"]
    business_size = np.random.choice(business_sizes, size=n, p=[0.88, 0.10, 0.02])

    # ==================================
    #               Entity Type
    # ===================================
    entity_types = [
        "Proprietorship", "Partnership",
        "LLP", "Private Limited"
    ]

    probabilities = [
        0.60, 0.20,
        0.10, 0.10
    ]

    entity_type = np.random.choice(
        entity_types,
        size=n,
        p=probabilities
    )

    # ==================================
    #                Business Age
    # ===================================
    business_age = np.random.exponential(scale=6, size=n)
    business_age = np.clip(business_age, 1, 30)

    # ==================================
    #                
    # ===================================
    gst_sales = np.zeros(n)
    digital_sales_ratio = np.zeros(n)
    employee_count = np.zeros(n, dtype = int)
    working_capital_cycle = np.zeros(n)
    gst_filing_delay = np.zeros(n)
    gst_growth = np.zeros(n)
    upi_count = np.zeros(n, dtype = int)

    for i in range(n):
        profile = industry_profile[industry_type[i]]

        # GST Sales
        if business_size[i] == "Micro":
            mean = profile["sales_mean"] - 2.2
            sigma = 0.85
        elif business_size[i] == "Small":
            mean = profile["sales_mean"] - 1.0
            sigma = 0.75
        else: # Medium
            mean = profile["sales_mean"]
            sigma = profile["sales_sigma"]

        gst_sales[i] = np.random.lognormal(mean, sigma)

        gst_sales[i] = np.clip(
            gst_sales[i],
            5e4,
            2e7
        )

        # Digital Sales Ratio
        a,b = profile["digital_beta"]

        digital_sales_ratio[i] = np.random.beta(a,b)

        # Employee Count
        if business_size[i] == "Micro":
            employee_count[i] = np.random.randint(1, 8)
        elif business_size[i] == "Small":
            employee_count[i] = np.random.randint(8, 40)
        else:
            employee_count[i] = np.random.randint(40, 120)

        # Working Capital Cycle
        working_capital_cycle[i] = np.random.normal(profile["working_capital"],10)

        working_capital_cycle[i] = np.clip(working_capital_cycle[i], 20, 180)

        # GST Delay
        shape,scale = profile["gst_delay"]

        gst_filing_delay[i] = np.random.gamma(shape, scale)

        gst_filing_delay[i] = np.clip(
            gst_filing_delay[i],
            0,
            180
        )

        # GST Growth
        # Younger businesses tend to grow faster but with more variability.
        if business_age[i] < 3:
            mean_growth = 0.18
        elif business_age[i] < 10:
            mean_growth = 0.10
        else:
            mean_growth = 0.05

        gst_growth[i] = np.clip(
            np.random.normal(mean_growth, 0.12),
            -0.40,
            0.60
        )

        # Monthly UPI Count
        base = upi_lambda[industry_type[i]]
        if business_size[i] == "Micro":
            lam = base * 0.40
        elif business_size[i] == "Small":
            lam = base * 0.75
        else:
            lam = base

        upi_count[i] = np.random.poisson(lam)
    

    # ==================================
    #           Banking Features (AA)
    # ===================================
    #Monthly credit
    # Bank credits may slightly exceed GST sales due to non-sales inflows.
    credit_ratio = np.random.uniform(0.85, 1.05, size=n)
    monthly_credit = gst_sales * credit_ratio


    #Monthly debit
    expense_ratio = np.random.uniform(0.55, 0.90, size = n)
    # Around 10% of businesses have expenses exceeding monthly credits - temporary losses
    loss_mask = np.random.rand(n) < 0.10
    expense_ratio[loss_mask] = np.random.uniform(1.02, 1.20, size=loss_mask.sum())
    monthly_debit = monthly_credit * expense_ratio

    # Average Balance
    factor = np.zeros(n)
    for i in range(n):
        if business_size[i] == "Micro":
            factor[i] = np.random.uniform(0.05,0.18)
        elif business_size[i] == "Small":
            factor[i] = np.random.uniform(0.10,0.30)
        else:
            factor[i] = np.random.uniform(0.20,0.45)

    average_bank_balance = (monthly_credit * factor)
    average_bank_balance *= (0.8 + business_age/40)

    # ==================================
    #                Cashflow Volatility
    # ===================================
    # Young firms generally have less stable cash flow.
    cashflow_volatility = (
        np.random.beta(2,5,n)
        + 0.12*(business_age<3)
    )

    cashflow_volatility = np.clip(cashflow_volatility, 0, 1)


    # ==================================
    #                Payroll Consistency
    # ===================================
    # Businesses with more employees tend to have more structured payroll.
    payroll_consistency = (
        0.7
        + 0.25*np.tanh(employee_count/20)
        + np.random.normal(0,0.05,n)
    )

    payroll_consistency = np.clip(payroll_consistency, 0, 1)


    # ==================================
    #                Vendor Delay
    # ===================================
    # Longer working capital cycles often lead to slower vendor payments.
    vendor_delay = (
        working_capital_cycle*0.15
        + np.random.gamma(2,3,n)
    )

    vendor_delay = np.clip(vendor_delay, 0, 120)


    # ==================================
    #                GST Compliance Rate
    # ===================================
    #  High delay -> Low compliance
    gst_compliance = (1- gst_filing_delay/180 + np.random.normal(0,0.05,n))
    gst_compliance = np.clip(gst_compliance, 0, 1)


    # ==================================
    #                Monthly UPI Value
    # ===================================
    # Higher GST Sales -> Higher UPI Value
    avg_ticket = np.random.uniform(400, 2500, n)
    upi_value = upi_count * avg_ticket
    upi_value = np.minimum(upi_value, gst_sales * digital_sales_ratio * 1.1)

    # ==================================
    #                Missing EMI Bounce
    # ===================================
    emi_lambda = 0.2 + 2 * cashflow_volatility
    emi_bounce = np.random.poisson(emi_lambda)
    emi_bounce = np.clip(emi_bounce, 0, 5)

    return pd.DataFrame({
        "Business_Size": business_size,
        "Business_Age": business_age,
        "Industry_Type": industry_type,
        "Entity_Type": entity_type,
        "Monthly_GST_Sales": gst_sales,
        "GST_Growth_Rate": gst_growth,
        "GST_Filing_Delay": gst_filing_delay,
        "GST_Compliance_Rate": gst_compliance,
        "Monthly_UPI_Count": upi_count.astype(int),
        "Monthly_UPI_Value": upi_value,
        "Digital_Sales_Ratio": digital_sales_ratio,
        "Average_Bank_Balance": average_bank_balance,
        "Monthly_Credit": monthly_credit,
        "Monthly_Debit": monthly_debit,
        "Cashflow_Volatility": cashflow_volatility,
        "Employee_Count": employee_count.astype(int),
        "Payroll_Consistency": payroll_consistency,
        "Vendor_Payment_Delay": vendor_delay,
        "Working_Capital_Cycle": working_capital_cycle,
        "EMI_Bounce_Count": emi_bounce.astype(int)
    })


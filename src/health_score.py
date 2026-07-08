import numpy as np
import json

# ==============================
# FEATURE TYPE
# ==============================

POSITIVE_FEATURES = {
    "Business_Age",
    "Monthly_GST_Sales",
    "GST_Growth_Rate",
    "GST_Compliance_Rate",
    "Monthly_UPI_Count",
    "Monthly_UPI_Value",
    "Digital_Sales_Ratio",
    "Average_Bank_Balance",
    "Monthly_Credit",
    "Monthly_Debit",
    "Employee_Count",
    "Payroll_Consistency",
}

NEGATIVE_FEATURES = {
    "GST_Filing_Delay",
    "Cashflow_Volatility",
    "Vendor_Payment_Delay",
    "Working_Capital_Cycle",
    "EMI_Bounce_Count",
}

# ==============================
# FEATURE WEIGHTS
# ==============================

CASHFLOW_WEIGHTS = {
    "Monthly_GST_Sales": 0.25,
    "Average_Bank_Balance": 0.20,
    "Monthly_Credit": 0.15,
    "Monthly_Debit": 0.15,
    "GST_Growth_Rate": 0.15,
    "Cashflow_Volatility": 0.10,
}

COMPLIANCE_WEIGHTS = {
    "GST_Compliance_Rate": 0.70,
    "GST_Filing_Delay": 0.30,
}

OPERATIONAL_WEIGHTS = {
    "Payroll_Consistency": 0.40,
    "Vendor_Payment_Delay": 0.30,
    "Working_Capital_Cycle": 0.30,
}

DIGITAL_WEIGHTS = {
    "Monthly_UPI_Count": 0.40,
    "Monthly_UPI_Value": 0.30,
    "Digital_Sales_Ratio": 0.30,
}

STABILITY_WEIGHTS = {
    "Business_Age": 0.40,
    "Employee_Count": 0.30,
    "Payroll_Consistency": 0.30,
}

#  cash flow > compliance > operational, etc.
# BUSINESS_HEALTH_WEIGHTS 
with open("../models/shap_dimension_weights.json") as file:
    BUSINESS_HEALTH_WEIGHTS = json.load(file)

FINAL_HEALTH_WEIGHTS = {
    "business_health": 0.50,
    "credit_risk": 0.50,
}

# ==============================
# LOAD NORMALIZATION STATS
# ==============================

with open("../models/normalization_stats.json") as f:
    NORMALIZATION_STATS = json.load(f)

LOG_FEATURES = {
    "Monthly_GST_Sales",
    "Monthly_UPI_Value",
    "Average_Bank_Balance",
    "Monthly_Credit",
    "Monthly_Debit",
}

# ==============================
# NORMALIZATION
# ==============================
def _normalize(customer_data, feature_name):

    value = customer_data[feature_name]

    # -----------------------------
    # Rule-based scoring
    # -----------------------------

    if feature_name == "EMI_Bounce_Count":
        if value == 0:
            return 100
        elif value == 1:
            return 70
        elif value == 2:
            return 40
        else:
            return 0

    if feature_name == "GST_Filing_Delay":
        if value <= 3:
            return 100
        elif value <= 7:
            return 90
        elif value <= 15:
            return 70
        elif value <= 30:
            return 40
        else:
            return 0

    if feature_name == "Vendor_Payment_Delay":
        if value <= 5:
            return 100
        elif value <= 10:
            return 85
        elif value <= 20:
            return 60
        elif value <= 30:
            return 30
        else:
            return 0

    # -----------------------------
    # Select normalization stats
    # -----------------------------

    business_size = customer_data["Business_Size"]
    if business_size not in NORMALIZATION_STATS:
        raise ValueError(f"Unknown Business_Size: {business_size}")
    
    stats = NORMALIZATION_STATS[business_size][feature_name]

    p5 = stats["p5"]
    p95 = stats["p95"]

    # -----------------------------
    # Log normalization
    # -----------------------------

    if feature_name in LOG_FEATURES:
        value = np.log1p(value)
        p5 = np.log1p(p5)
        p95 = np.log1p(p95)

    if p95 == p5:
        return 100

    score = (value - p5) / (p95 - p5)
    score = np.clip(score, 0, 1)

    if feature_name in NEGATIVE_FEATURES:
        score = 1 - score

    return round(score * 100, 2)

# ==============================
# GENERIC DIMENSION SCORER
# ==============================

def _compute_dimension_score(customer_data, weights):

    score = 0

    for feature, weight in weights.items():
        score += weight * _normalize(customer_data, feature)

    return round(score, 2)

# ==============================
# DIMENSION SCORES
# ==============================

def compute_cashflow_score(customer_data):
    return _compute_dimension_score(customer_data, CASHFLOW_WEIGHTS)


def compute_compliance_score(customer_data):
    return _compute_dimension_score(customer_data, COMPLIANCE_WEIGHTS)


def compute_operational_score(customer_data):
    return _compute_dimension_score(customer_data, OPERATIONAL_WEIGHTS)


def compute_digital_score(customer_data):
    return _compute_dimension_score(customer_data, DIGITAL_WEIGHTS)


def compute_stability_score(customer_data):
    return _compute_dimension_score(customer_data, STABILITY_WEIGHTS)

# ==============================
# CREDIT RISK
# ==============================

def compute_credit_risk_score(customer_data):
    return round((1 - customer_data["calibrated_pd"]) * 100, 2)

# ==============================
# GRADE
# ==============================

def assign_grade(score):

    if score >= 90:
        return "AAA"
    elif score >= 80:
        return "AA"
    elif score >= 70:
        return "A"
    elif score >= 60:
        return "BBB"
    else:
        return "High Risk"

# ==============================
# LOAN READINESS
# ==============================
def loan_readiness(score):
    if score >= 90:
        return "READY"
    elif score >= 80:
        return "FAST REVIEW"
    elif score >= 70:
        return "REVIEW"
    else:
        return "NOT READY"

# ==============================
# FINANCIAL HEALTH SCORE
# ==============================

def compute_financial_health_score(customer_data):

    scores = {
        "cash_flow": compute_cashflow_score(customer_data),
        "compliance": compute_compliance_score(customer_data),
        "operational": compute_operational_score(customer_data),
        "digital": compute_digital_score(customer_data),
        "stability": compute_stability_score(customer_data)
    }

    
    business_health = 0
    for dimension, weight in BUSINESS_HEALTH_WEIGHTS.items():
        business_health += weight * scores[dimension]

    credit_risk_score = compute_credit_risk_score(customer_data)

    overall = (
        FINAL_HEALTH_WEIGHTS["business_health"] * business_health
        + FINAL_HEALTH_WEIGHTS["credit_risk"] * credit_risk_score
    )

    overall = round(overall, 2)

    return {
        "scores": scores,
        "business_health": round(business_health, 2),
        "credit_risk": round(credit_risk_score, 2),
        "overall": overall,
        "grade": assign_grade(overall),
        "loan_readiness": loan_readiness(overall),
    }
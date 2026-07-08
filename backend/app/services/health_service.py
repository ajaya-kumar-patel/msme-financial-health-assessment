import numpy as np
import json
from pathlib import Path


# ==============================
# LOAD PATH
# ==============================

BASE_DIR = Path(__file__).resolve().parents[3]

MODEL_DIR = BASE_DIR / "models"


# ==============================
# FEATURE TYPES
# ==============================

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



# ==============================
# BUSINESS HEALTH WEIGHTS
# ==============================

with open(MODEL_DIR / "shap_dimension_weights.json") as f:
    BUSINESS_HEALTH_WEIGHTS = json.load(f)



FINAL_HEALTH_WEIGHTS = {
    "business_health": 0.50,
    "credit_risk": 0.50,
}



# ==============================
# NORMALIZATION STATS
# ==============================

with open(MODEL_DIR / "normalization_stats.json") as f:
    NORMALIZATION_STATS = json.load(f)



LOG_FEATURES = {
    "Monthly_GST_Sales",
    "Monthly_UPI_Value",
    "Average_Bank_Balance",
    "Monthly_Credit",
    "Monthly_Debit",
}



# ==============================
# NORMALIZATION FUNCTION
# ==============================

def _normalize(customer_data, feature_name):

    value = customer_data[feature_name]


    # EMI rule

    if feature_name == "EMI_Bounce_Count":

        if value == 0:
            return 100
        elif value == 1:
            return 70
        elif value == 2:
            return 40
        else:
            return 0


    # GST delay

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


    # Vendor delay

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



    # size based normalization

    business_size = customer_data["Business_Size"]

    stats = NORMALIZATION_STATS[business_size][feature_name]


    p5 = stats["p5"]
    p95 = stats["p95"]


    if feature_name in LOG_FEATURES:

        value = np.log1p(value)
        p5 = np.log1p(p5)
        p95 = np.log1p(p95)



    if p95 == p5:
        return 100


    score = (value - p5)/(p95-p5)

    score = np.clip(score,0,1)



    if feature_name in NEGATIVE_FEATURES:
        score = 1-score


    return round(score*100,2)




# ==============================
# DIMENSION SCORE
# ==============================

def _compute_dimension_score(customer_data, weights):

    score = 0

    for feature, weight in weights.items():

        score += weight * _normalize(
            customer_data,
            feature
        )


    return round(score,2)



# ==============================
# DIMENSION FUNCTIONS
# ==============================

def compute_cashflow_score(data):
    return _compute_dimension_score(
        data,
        CASHFLOW_WEIGHTS
    )


def compute_compliance_score(data):
    return _compute_dimension_score(
        data,
        COMPLIANCE_WEIGHTS
    )


def compute_operational_score(data):
    return _compute_dimension_score(
        data,
        OPERATIONAL_WEIGHTS
    )


def compute_digital_score(data):
    return _compute_dimension_score(
        data,
        DIGITAL_WEIGHTS
    )


def compute_stability_score(data):
    return _compute_dimension_score(
        data,
        STABILITY_WEIGHTS
    )



# ==============================
# CREDIT RISK SCORE
# ==============================

def compute_credit_risk_score(data):

    return round(
        (1-data["calibrated_pd"])*100,
        2
    )



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
        return "INSTANT APPROVAL"

    elif score >= 80:
        return "FAST REVIEW"

    elif score >= 70:
        return "MANUAL REVIEW"

    else:
        return "NOT READY"



# ==============================
# MAIN FUNCTION
# ==============================

def compute_financial_health_score(customer_data):


    scores = {

        "cash_flow":
            compute_cashflow_score(customer_data),

        "compliance":
            compute_compliance_score(customer_data),

        "operational":
            compute_operational_score(customer_data),

        "digital":
            compute_digital_score(customer_data),

        "stability":
            compute_stability_score(customer_data)
    }



    business_health = 0


    for dimension, weight in BUSINESS_HEALTH_WEIGHTS.items():

        business_health += (
            weight * scores[dimension]
        )



    credit_risk = compute_credit_risk_score(
        customer_data
    )



    overall = (
        FINAL_HEALTH_WEIGHTS["business_health"]
        * business_health
        +
        FINAL_HEALTH_WEIGHTS["credit_risk"]
        * credit_risk
    )


    overall = round(overall,2)



    return {

        "dimension_scores": scores,

        "business_health":
            round(business_health,2),

        "credit_risk":
            credit_risk,

        "overall":
            overall,

        "grade":
            assign_grade(overall),

        "loan_readiness":
            loan_readiness(overall)

    }
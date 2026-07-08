import numpy as np
import logging
from sklearn.preprocessing import StandardScaler
from config import RANDOM_SEED


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def generate_default(df, random_state = RANDOM_SEED):
    logging.info("Generating PD and Default...")
    np.random.seed(random_state)

    # Standardize continous features
    continuous_cols = [
        "Business_Age",
        "Monthly_GST_Sales",
        "GST_Growth_Rate",
        "GST_Filing_Delay",
        "GST_Compliance_Rate",
        "Monthly_UPI_Count",
        "Monthly_UPI_Value",
        "Digital_Sales_Ratio",
        "Average_Bank_Balance",
        "Monthly_Credit",
        "Monthly_Debit",
        "Cashflow_Volatility",
        "Employee_Count",
        "Payroll_Consistency",
        "Vendor_Payment_Delay",
        "Working_Capital_Cycle",
        "EMI_Bounce_Count",
    ]

    scaler = StandardScaler()
    X = scaler.fit_transform(df[continuous_cols])
    X = dict(zip(continuous_cols, X.T))

    ## Hiddent Variables
    local_economy = np.random.normal(0, 1, len(df))
    management_quality = np.random.beta(5, 2, len(df))
    unexpected_event = np.random.binomial(1, 0.04, len(df))

    # Risk Function
    risk = (
        0.40 * X["GST_Filing_Delay"]
        + 0.35 * X["Vendor_Payment_Delay"]
        + 0.60 * X["Cashflow_Volatility"]
        + 0.50 * X["EMI_Bounce_Count"]
        - 0.50 * X["GST_Compliance_Rate"]
        - 0.30 * X["Business_Age"]
        - 0.35 * X["Average_Bank_Balance"]
        - 0.20 * X["GST_Growth_Rate"]
        - 0.20 * X["Digital_Sales_Ratio"]
        - 0.15 * X["Payroll_Consistency"]
        + 0.10 * local_economy
        - 0.15 * management_quality
        + 0.25 * unexpected_event
    )

    # -------------------------------
    #        Interaction Effects
    # -------------------------------
    interaction = np.zeros(len(df))
    
    ##  low compliance + unstable cashflow = serious financial stress (strong risk signal)
    interaction += np.where(
        (df["GST_Compliance_Rate"]<0.60) & 
        (df["Cashflow_Volatility"] > 0.60),
        0.80,
        0
    )

    # High vendor delay + high GST delay
    interaction += np.where(
        (df["Vendor_Payment_Delay"] > 45) &
        (df["GST_Filing_Delay"] > 45),
        0.60,
        0
    )

    # Older businesses get slight benefit
    interaction -= np.where(
        df["Business_Age"] > 15,
        0.30,
        0
    )

    risk += interaction

    # -------------------------------
    #            Random Noise
    # -------------------------------
    noise = np.random.normal(0, 0.15, len(df))
    risk += noise


    # -----------------------------
    #         Base Default Rate
    # -----------------------------
    risk -= 2.0

    # ------------------------------
    #         Probability of Default
    # ------------------------------
    k = 2.5 # Increase k to reduce randomness in binomial
    pd_true = sigmoid(k*risk)


    # -------------------------------
    # Generate Defaults
    # -------------------------------
    # This randomness reflects that even businesses with the same risk don't all default.
    # Why not just use a threshold?
    # A business with 49% risk is almost as risky as one with 51%, yet this rule treats them completely differently. Using the binomial distribution preserves the probabilistic nature of default.
    
    default = np.random.binomial(1, pd_true)

    # default = (pd_true >= 0.5).astype(int) -> deterministic function of risk

    # -----------------------------
    #          Add to dataframe
    # -----------------------------

    df = df.copy()
    df["PD_True"] = pd_true
    df["Default"] = default

    return df





















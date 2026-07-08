import pandas as pd
from sklearn.model_selection import train_test_split
import logging
import sys

logging.basicConfig(level=logging.INFO,
                    stream=sys.stdout,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",)

logger = logging.getLogger(__name__)

def save_data(df, file_path):
    df.to_csv(file_path, index=False)
    logger.info(f"Dataset saved to {file_path}")

def load_data(file_path):
    """
    Input: filepath
    output: dataframe
    """
    logger.info(f"Loading dataset from {file_path}")
    df = pd.read_csv(file_path)
    return df

def inspect_data(df, target="Default"):
    """
    Generate a basic data quality report.
    """

    report = {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": df.dtypes.to_dict(),
        "duplicates": int(df.duplicated().sum()),
        "missing_values": df.isna().sum().to_dict(),
        "memory_usage_mb": round(
            df.memory_usage(deep=True).sum() / 1024**2, 2
        ),
        "target_distribution": df[target].value_counts().to_dict(),
        "target_percentage": (
            df[target].value_counts(normalize=True) * 100
        ).round(2).to_dict()
    }

    return report

def remove_target_leakage(df):
    """
    Remove columns that introduce target leakage.
    """

    return df.drop(columns=["PD_True"], errors="ignore")

def handle_missing_values(df):
    """Handle missing values if present."""

    if df.isna().sum().sum() == 0:
        logger.info("No missing values detected.")
        return df

    # Future implementation - skping now as we have synthetic data
    logger.warning("Missing values detected. Future implementation required.")
    return df

def detect_outliers(df):
    """Generate an outlier report."""

    logger.info("Synthetic dataset: outlier treatment skipped.")
    return df

def engineer_features(df):
    """Feature engineering."""

    logger.info("Using provided engineered features. -> skip for synthetic data")
    return df

def create_train_test_split(df, target="Default", test_size=0.20, random_state=2026,):
    """Perform train-test split."""
    X = df.drop(columns=[target])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    df_train = X_train.copy()
    df_train[target] = y_train
    df_train = df_train.reset_index(drop = True)

    df_test = X_test.copy()
    df_test[target] = y_test
    df_test = df_test.reset_index(drop = True)

    return df_train, df_test
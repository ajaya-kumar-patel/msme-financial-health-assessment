import joblib
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from xgboost import XGBClassifier
import logging
import sys

logging.basicConfig(level=logging.INFO,
                    stream=sys.stdout,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

logger = logging.getLogger(__name__)

SEED = 2026

def build_preprocessor(X):
    """
    Build Preprocessor pipeline
    """
    categorical_features = ["Business_Size", "Industry_Type", "Entity_Type"]

    numeric_features = [
        col for col in X.columns
        if col not in categorical_features
    ]

    numeric_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="median"))
    ])

    categorical_transformer = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features)
        ]
    )

    return preprocessor

def build_model(scale_pos_weight):
    """
    Create XGBoost Classifier
    """

    model = XGBClassifier(
        n_estimators=600,
        learning_rate=0.03,
        max_depth=4,
        min_child_weight=3,
        gamma=0.2,
        subsample=0.9,
        colsample_bytree=0.9,
        random_state=SEED,
        eval_metric="logloss",
        scale_pos_weight = scale_pos_weight
    )

    return model


def train_model(train_df, target = "Default"):
    """
    Train model
    """

    X = train_df.drop(columns = [target])
    y = train_df[target]
    
    neg = (y == 0).sum()
    pos = (y == 1).sum()
    logger.info(f"Negative samples: {neg}")
    logger.info(f"Positive samples: {pos}")

    if pos == 0:
        raise ValueError("Training data contains no positive samples.")
    scale_pos_weight = neg / pos
    logger.info(f"scale_pos_weight: {scale_pos_weight:.2f}")

    pipeline = Pipeline([
        ("preprocessor", build_preprocessor(X)),
        ("model", build_model(scale_pos_weight)),
    ])

    logger.info("Training XGBoost model...")

    pipeline.fit(X, y)

    logger.info("Model training completed successfully.")
    
    return pipeline

def save_model(model, file_path):
    """
    Save trained model.
    """
    joblib.dump(model, file_path)
    logger.info(f"Model saved to {file_path}")

def load_model(file_path):
    """
    Load trained model.
    """
    logger.info(f"Loading model from {file_path}")
    model = joblib.load(file_path)
    return model

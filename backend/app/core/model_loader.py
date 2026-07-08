import json
import joblib

from app.core.config import (
    PIPELINE_PATH,
    CALIBRATION_MODEL_PATH,
    NORMALIZATION_STATS_PATH,
    SHAP_WEIGHTS_PATH,
)


class ModelLoader:
    """
    Loads all required models and configuration files once
    when the FastAPI application starts.
    """

    def __init__(self):
        self.pipeline = None
        self.calibrator = None
        self.normalization_stats = None
        self.shap_weights = None

    def load(self):
        """Load all artifacts into memory."""

        self.pipeline = joblib.load(PIPELINE_PATH)

        self.calibrator = joblib.load(CALIBRATION_MODEL_PATH)

        with open(NORMALIZATION_STATS_PATH, "r") as f:
            self.normalization_stats = json.load(f)

        with open(SHAP_WEIGHTS_PATH, "r") as f:
            self.shap_weights = json.load(f)

        print("Models loaded successfully.")


model_loader = ModelLoader()
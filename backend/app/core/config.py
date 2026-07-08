from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parents[3]

# Models directory
MODELS_DIR = BASE_DIR / "models"

# Model files
PIPELINE_PATH = MODELS_DIR / "financial_health_xgboost_pipeline.pkl"
CALIBRATION_MODEL_PATH = MODELS_DIR / "calibrated_model.pkl"
NORMALIZATION_STATS_PATH = MODELS_DIR / "normalization_stats.json"
SHAP_WEIGHTS_PATH = MODELS_DIR / "shap_dimension_weights.json"
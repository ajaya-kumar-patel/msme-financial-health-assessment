import joblib
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.metrics import brier_score_loss, log_loss
import logging
import sys

logging.basicConfig(level = logging.INFO,
                    stream = sys.stdout,
                    format = "%(asctime)s - %(levelname)s - %(message)s",
                    datefmt = "%Y-%m-%d %H:%M:%S"
                    )

logger = logging.getLogger(__name__)

def fit_probability_calibration(pipeline, X_train, y_train,
                                method: str = "isotonic",
                                cv: int = 5
                                ):
    """
    Fit probability calibration on a trained pipeline.
    Parameters
    ----------
    pipeline : sklearn Pipeline
    X_train : DataFrame
    y_train : Series

    Returns
    -------
    calibrated_model
    """

    calibrator = CalibratedClassifierCV(
        estimator=pipeline,
        method = method,
        cv = cv
    )

    calibrator.fit(X_train, y_train)

    return calibrator

def evaluate_calibration(raw_model, calibrated_model, X_test, y_test):
    """
    Compare raw vs calibration probability
    """

    raw_prob = raw_model.predict_proba(X_test)[:,1]
    calibrated_prob = calibrated_model.predict_proba(X_test)[:, 1]

    metric = {
        "raw_brier_score": brier_score_loss(y_test, raw_prob),
        "calibrated_brier_score": brier_score_loss(y_test, calibrated_prob),
        "raw_log_loss": log_loss(y_test, raw_prob),
        "calibrated_log_loss": log_loss(y_test, calibrated_prob)
    }

    return metric


import logging
import sys
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, ConfusionMatrixDisplay,
    classification_report, precision_recall_curve, auc, roc_curve, brier_score_loss, log_loss
)

logging.basicConfig(level=logging.INFO,
                    stream=sys.stdout,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",)
logger = logging.getLogger(__name__)

def evaluate_model(model, test_df, target="Default"):
    """
    Evaluate classification model.
    """

    X_test = test_df.drop(columns=[target])
    y_test = test_df[target]

    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    metrics = {
        "Accuracy": accuracy_score(y_test, y_pred),
        "Precision": precision_score(y_test, y_pred),
        "Recall": recall_score(y_test, y_pred),
        "F1 Score": f1_score(y_test, y_pred),
        "ROC-AUC": roc_auc_score(y_test, y_prob),
        "brier score": brier_score_loss(y_test, y_prob),
        "Log Loss": log_loss(y_test, y_prob)
    }

    logger.info("Model evaluation completed.")

    return metrics


def get_classification_report(model, test_df, target="Default"):
    X_test = test_df.drop(columns=[target])
    y_test = test_df[target]
    y_pred = model.predict(X_test)
    return classification_report(y_test, y_pred)


def plot_confusion_matrix(model, test_df, target="Default"):
    X_test = test_df.drop(columns=[target])
    y_test = test_df[target]
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(cm)
    disp.plot()
    plt.title("Confusion Matrix")
    plt.show()

def plot_roc_pr_curves(model, test_df, target="Default"):
    """
    Plot ROC Curve and Precision-Recall Curve.
    """

    X_test = test_df.drop(columns=[target])
    y_test = test_df[target]

    # Predicted probabilities
    y_prob = model.predict_proba(X_test)[:, 1]

    # -----------------------
    #          ROC Curve
    # -----------------------
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = roc_auc_score(y_test, y_prob)

    plt.figure(figsize=(5, 4))
    plt.plot(fpr, tpr, label=f"ROC AUC = {roc_auc:.3f}")
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend(loc="lower right")
    plt.grid(True)
    plt.show()

    # -------------------------
    #   Precision-Recall Curve
    # -------------------------
    precision, recall, _ = precision_recall_curve(y_test, y_prob)
    pr_auc = auc(recall, precision)

    plt.figure(figsize=(5, 4))
    plt.plot(recall, precision, label=f"PR AUC = {pr_auc:.3f}")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title("Precision-Recall Curve")
    plt.legend(loc="lower left")
    plt.grid(True)
    plt.show()

    return {
        "ROC-AUC": roc_auc,
        "PR-AUC": pr_auc,
    }


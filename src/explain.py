import numpy as np
import pandas as pd
import shap
import logging
import sys

logging.basicConfig(level=logging.INFO,
                    stream=sys.stdout,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

logger = logging.getLogger(__name__)

def compute_shap(pipeline, X):
    preprocessor = pipeline.named_steps["preprocessor"]
    model = pipeline.named_steps["model"]

    X_processed = preprocessor.transform(X)

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_processed)

    feature_names = preprocessor.get_feature_names_out()

    return explainer, shap_values, X_processed, feature_names


def explain_customer(shap_values, feature_names, index=0):
    """Return feature contributions for one customer."""

    customer_shap = shap_values[index]

    feature_map = [
        f.split("__", 1)[1] if "__" in f else f
        for f in feature_names
    ]

    explanation_df = (
        pd.DataFrame({
            "feature": feature_map,
            "shap_value": customer_shap,
        })
        .groupby("feature", as_index=False)["shap_value"]
        .sum()
    )

    explanation_df = explanation_df.iloc[
        explanation_df["shap_value"].abs().argsort()[::-1]
    ].reset_index(drop=True)

    return explanation_df


def plot_shap(explainer, X_processed, shap_values,
              feature_names, plot_type="summary",
              index=0, show=True
              ):
    import shap

    if plot_type == "summary":
        shap.summary_plot(
            shap_values,
            X_processed,
            feature_names=feature_names,
            show=show
        )

    elif plot_type == "bar":
        shap.summary_plot(
            shap_values,
            X_processed,
            feature_names=feature_names,
            plot_type="bar",
            show=show
        )

    elif plot_type == "waterfall":
        explanation = explainer(X_processed)
        shap.plots.waterfall(explanation[index])

    else:
        raise ValueError("plot_type must be: summary | bar | waterfall")
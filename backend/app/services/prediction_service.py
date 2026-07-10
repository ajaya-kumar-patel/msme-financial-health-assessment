import pandas as pd

from app.core.model_loader import model_loader
from app.services.health_service import compute_financial_health_score
from app.services.explanation_service import explanation_service
from app.services.recommendation_service import recommendation_service

from app.core.logging import get_logger

logger = get_logger(__name__)

class PredictionService:

    @staticmethod
    def predict(customer_data):
        logger.info("Prediction request received.")

        input_df = pd.DataFrame([customer_data])
        raw_pd = model_loader.pipeline.predict_proba(input_df)[0][1]
        calibrated_pd = model_loader.calibrator.predict_proba(input_df)[0][1]

        # Add calibrated PD
        customer_data["calibrated_pd"] = calibrated_pd


        # ------------------------
        # Financial Health
        # ------------------------
        health_result = compute_financial_health_score(customer_data)

        explanation = explanation_service.generate(customer_data, health_result)

        recommendations = recommendation_service.generate(customer_data, health_result)
        
        logger.info(
            "Prediction completed. Health Score = %.2f",
            health_result["overall"],
        )
        
        return {
            "raw_pd": round(float(raw_pd), 4),
            "probability_of_default":  round(float(calibrated_pd), 4),
            "credit_risk_score": health_result["credit_risk"],
            "financial_health_score": health_result["overall"],
            "grade": health_result["grade"],
            "loan_readiness": health_result["loan_readiness"],
            "dimension_scores": health_result["dimension_scores"],
            "explanation": explanation,
            "recommendations": recommendations
        }

prediction_service = PredictionService()
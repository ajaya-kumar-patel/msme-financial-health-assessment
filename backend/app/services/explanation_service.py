# from typing import Dict


# class ExplanationService:
#     """
#     Generates human-readable explanations for
#     financial health and credit risk results.
#     """

#     @staticmethod
#     def generate(
#         customer_data: Dict,
#         health_result: Dict,
#     ) -> Dict:

#         explanations = []

#         scores = health_result["dimension_scores"]

#         # -------------------------
#         # Cash Flow
#         # -------------------------

#         if scores["cash_flow"] >= 80:
#             explanations.append(
#                 "Excellent cash flow with strong revenue and healthy bank transactions."
#             )
#         elif scores["cash_flow"] >= 60:
#             explanations.append(
#                 "Cash flow is stable but there is room for improvement."
#             )
#         else:
#             explanations.append(
#                 "Weak cash flow is increasing overall credit risk."
#             )

#         # -------------------------
#         # Compliance
#         # -------------------------

#         if scores["compliance"] >= 80:
#             explanations.append(
#                 "GST compliance history is strong."
#             )
#         else:
#             explanations.append(
#                 "Poor GST compliance or filing delays are reducing the financial health score."
#             )

#         # -------------------------
#         # Operational
#         # -------------------------

#         if scores["operational"] < 60:
#             explanations.append(
#                 "Operational efficiency is affected by payment delays or working capital cycle."
#             )

#         # -------------------------
#         # Digital Adoption
#         # -------------------------

#         if scores["digital"] >= 80:
#             explanations.append(
#                 "High digital transaction activity improves business transparency."
#             )

#         # -------------------------
#         # Stability
#         # -------------------------

#         if scores["stability"] >= 80:
#             explanations.append(
#                 "Business demonstrates good long-term stability."
#             )

#         return {
#             "summary": explanations,
#             "business_health_score": health_result["business_health"],
#             "financial_health_score": health_result["overall"],
#             "grade": health_result["grade"],
#         }


# explanation_service = ExplanationService()


from app.core.logging import get_logger

logger = get_logger(__name__)


class ExplanationService:

    DIMENSION_NAMES = {
        "cash_flow": "Cash Flow",
        "compliance": "Compliance",
        "operational": "Operational Efficiency",
        "digital": "Digital Adoption",
        "stability": "Business Stability",
    }

    @staticmethod
    def _dimension_comment(score):

        if score >= 85:
            return "excellent"

        elif score >= 70:
            return "good"

        elif score >= 55:
            return "average"

        elif score >= 40:
            return "weak"

        else:
            return "poor"

    def generate(self, customer_data, health_result):

        scores = health_result["dimension_scores"]

        best_dimension = max(scores, key=scores.get)
        worst_dimension = min(scores, key=scores.get)

        explanation = {
            "summary": (
                f"The business has an overall Financial Health Score of "
                f"{health_result['overall']:.2f} with grade "
                f"{health_result['grade']}."
            ),

            "credit_risk": (
                f"The estimated probability of default is "
                f"{customer_data['calibrated_pd']*100:.2f}%, resulting in a "
                f"Credit Risk Score of {health_result['credit_risk']:.2f}."
            ),

            "strength": (
                f"The strongest area is "
                f"{self.DIMENSION_NAMES[best_dimension]} "
                f"with a score of {scores[best_dimension]:.2f}."
            ),

            "weakness": (
                f"The weakest area is "
                f"{self.DIMENSION_NAMES[worst_dimension]} "
                f"with a score of {scores[worst_dimension]:.2f}."
            ),

            "dimension_analysis": {}
        }

        for dimension, score in scores.items():

            explanation["dimension_analysis"][dimension] = {

                "score": score,

                "status": self._dimension_comment(score),

                "message":
                    f"{self.DIMENSION_NAMES[dimension]} performance is "
                    f"{self._dimension_comment(score)}."
            }

        logger.info("Explanation generated.")

        return explanation


explanation_service = ExplanationService()
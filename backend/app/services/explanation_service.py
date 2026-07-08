from typing import Dict


class ExplanationService:
    """
    Generates human-readable explanations for
    financial health and credit risk results.
    """

    @staticmethod
    def generate(
        customer_data: Dict,
        health_result: Dict,
    ) -> Dict:

        explanations = []

        scores = health_result["dimension_scores"]

        # -------------------------
        # Cash Flow
        # -------------------------

        if scores["cash_flow"] >= 80:
            explanations.append(
                "Excellent cash flow with strong revenue and healthy bank transactions."
            )
        elif scores["cash_flow"] >= 60:
            explanations.append(
                "Cash flow is stable but there is room for improvement."
            )
        else:
            explanations.append(
                "Weak cash flow is increasing overall credit risk."
            )

        # -------------------------
        # Compliance
        # -------------------------

        if scores["compliance"] >= 80:
            explanations.append(
                "GST compliance history is strong."
            )
        else:
            explanations.append(
                "Poor GST compliance or filing delays are reducing the financial health score."
            )

        # -------------------------
        # Operational
        # -------------------------

        if scores["operational"] < 60:
            explanations.append(
                "Operational efficiency is affected by payment delays or working capital cycle."
            )

        # -------------------------
        # Digital Adoption
        # -------------------------

        if scores["digital"] >= 80:
            explanations.append(
                "High digital transaction activity improves business transparency."
            )

        # -------------------------
        # Stability
        # -------------------------

        if scores["stability"] >= 80:
            explanations.append(
                "Business demonstrates good long-term stability."
            )

        return {
            "summary": explanations,
            "business_health_score": health_result["business_health"],
            "financial_health_score": health_result["overall"],
            "grade": health_result["grade"],
        }


explanation_service = ExplanationService()
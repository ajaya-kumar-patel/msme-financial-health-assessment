from app.core.logging import get_logger

logger = get_logger(__name__)


class RecommendationService:

    RECOMMENDATIONS = {

        "cash_flow": [

            "Increase average bank balance to improve liquidity.",

            "Maintain consistent monthly sales growth.",

            "Reduce cash-flow volatility by forecasting monthly expenses.",

            "Improve working capital management."

        ],

        "compliance": [

            "File GST returns on time.",

            "Maintain a GST compliance rate above 95%.",

            "Avoid repeated filing delays."

        ],

        "operational": [

            "Pay vendors on time.",

            "Reduce the working capital cycle.",

            "Maintain consistent employee payroll."

        ],

        "digital": [

            "Increase digital payment adoption.",

            "Encourage UPI transactions.",

            "Increase digital sales ratio."

        ],

        "stability": [

            "Maintain employee retention.",

            "Expand business sustainably.",

            "Continue stable business operations."

        ]
    }

    def generate(self, customer_data, health_result):

        recommendations = []

        scores = health_result["dimension_scores"]

        for dimension, score in scores.items():

            if score >= 80:
                continue

            recommendations.extend(
                self.RECOMMENDATIONS[dimension]
            )

        if health_result["credit_risk"] < 70:

            recommendations.append(
                "Reduce debt obligations to improve creditworthiness."
            )

            recommendations.append(
                "Avoid EMI payment defaults."
            )

        if len(recommendations) == 0:

            recommendations.append(
                "Maintain current financial discipline and continue monitoring business performance."
            )

        logger.info("Recommendations generated.")

        return recommendations


recommendation_service = RecommendationService()
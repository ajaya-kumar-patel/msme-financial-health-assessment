from typing import Dict, List
from app.core.logging import get_logger

logger = get_logger(__name__)

class RecommendationService:
    """
    Generate actionable business recommendations
    based on financial health scores and probability
    of default.
    """
    logger.info("Generating recommendations...")
    
    PRIORITY_ORDER = {
        "Critical": 0,
        "High": 1,
        "Medium": 2,
        "Low": 3,
        "Info": 4,
    }

    @staticmethod
    def generate(
        customer_data: Dict,
        health_result: Dict,
    ) -> List[Dict]:

        recommendations = []

        scores = health_result["dimension_scores"]

        pd = customer_data["calibrated_pd"] * 100

        # ============================================
        # CASH FLOW
        # ============================================

        if scores["cash_flow"] < 60:

            recommendations.append({
                "priority": "High",
                "category": "Cash Flow",
                "issue": "Weak Cash Flow",
                "recommendation":
                    "Increase monthly revenue, maintain a healthier bank balance, and reduce cash-flow volatility.",
                "expected_impact": "High"
            })

        elif scores["cash_flow"] < 80:

            recommendations.append({
                "priority": "Medium",
                "category": "Cash Flow",
                "issue": "Moderate Cash Flow",
                "recommendation":
                    "Improve cash reserves and maintain steady monthly transactions.",
                "expected_impact": "Medium"
            })

        # ============================================
        # COMPLIANCE
        # ============================================

        if scores["compliance"] < 80:

            recommendations.append({
                "priority": "High",
                "category": "Compliance",
                "issue": "GST Compliance",
                "recommendation":
                    "File GST returns on time and maintain a higher compliance rate.",
                "expected_impact": "High"
            })

        # ============================================
        # OPERATIONAL
        # ============================================

        if scores["operational"] < 60:

            recommendations.append({
                "priority": "Medium",
                "category": "Operations",
                "issue": "Operational Efficiency",
                "recommendation":
                    "Reduce vendor payment delays and shorten the working capital cycle.",
                "expected_impact": "Medium"
            })

        # ============================================
        # DIGITAL
        # ============================================

        if scores["digital"] < 60:

            recommendations.append({
                "priority": "Medium",
                "category": "Digital",
                "issue": "Low Digital Adoption",
                "recommendation":
                    "Increase UPI transactions and improve the digital sales ratio.",
                "expected_impact": "Medium"
            })

        # ============================================
        # STABILITY
        # ============================================

        if scores["stability"] < 60:

            recommendations.append({
                "priority": "Low",
                "category": "Business Stability",
                "issue": "Business Stability",
                "recommendation":
                    "Improve payroll consistency and strengthen workforce stability.",
                "expected_impact": "Medium"
            })

        # ============================================
        # CREDIT RISK
        # ============================================

        if pd >= 20:

            recommendations.append({
                "priority": "Critical",
                "category": "Credit Risk",
                "issue": "High Probability of Default",
                "recommendation":
                    "Strengthen liquidity, improve repayment behavior, and reduce financial risk before applying for additional credit.",
                "expected_impact": "Very High"
            })

        elif pd >= 10:

            recommendations.append({
                "priority": "High",
                "category": "Credit Risk",
                "issue": "Moderate Credit Risk",
                "recommendation":
                    "Improve financial discipline and reduce outstanding liabilities.",
                "expected_impact": "High"
            })

        # ============================================
        # LOAN READINESS
        # ============================================

        readiness = health_result["loan_readiness"]

        if readiness == "NOT READY":

            recommendations.append({
                "priority": "Critical",
                "category": "Loan Readiness",
                "issue": "Business Not Ready",
                "recommendation":
                    "Improve the weakest financial dimensions before applying for a business loan.",
                "expected_impact": "Very High"
            })

        elif readiness == "MANUAL REVIEW":

            recommendations.append({
                "priority": "Medium",
                "category": "Loan Readiness",
                "issue": "Manual Review Required",
                "recommendation":
                    "Provide additional financial documents and improve weaker business metrics.",
                "expected_impact": "Medium"
            })

        elif readiness == "FAST REVIEW":

            recommendations.append({
                "priority": "Info",
                "category": "Loan Readiness",
                "issue": "Fast Review Eligible",
                "recommendation":
                    "Business appears healthy. Standard verification is likely sufficient.",
                "expected_impact": "Low"
            })

        elif readiness == "INSTANT APPROVAL":

            recommendations.append({
                "priority": "Info",
                "category": "Loan Readiness",
                "issue": "Excellent Financial Health",
                "recommendation":
                    "Maintain current financial discipline to preserve your strong credit profile.",
                "expected_impact": "Low"
            })

        # ============================================
        # SORT BY PRIORITY
        # ============================================

        recommendations.sort(
            key=lambda x: RecommendationService.PRIORITY_ORDER[x["priority"]]
        )

        return recommendations


recommendation_service = RecommendationService()
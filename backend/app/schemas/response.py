from pydantic import BaseModel
from typing import Dict, List

# ======================================
# Recommendation
# ======================================
class ExplanationResponse(BaseModel):
    summary: List[str]
    business_health_score: float
    financial_health_score: float
    grade: str


# ======================================
# Recommendation
# ======================================
class RecommendationResponse(BaseModel):
    priority: str
    category: str
    issue: str
    recommendation: str
    expected_impact: str

# ======================================
# Prediction Response
# ======================================
class PredictionResponse(BaseModel):
    raw_pd: float
    probability_of_default: float
    credit_risk_score: float
    financial_health_score: float
    grade: str
    loan_readiness: str
    dimension_scores: Dict[str,float]
    explanation: ExplanationResponse
    recommendations: List[RecommendationResponse]


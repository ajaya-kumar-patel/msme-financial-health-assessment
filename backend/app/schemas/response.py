from pydantic import BaseModel
from typing import Dict, List

# ======================================
# Dimension Analysis
# ======================================
class DimensionAnalysisResponse(BaseModel):
    score: float
    status: str
    message: str

# ======================================
# Explanation
# ======================================
class ExplanationResponse(BaseModel):
    summary: str
    credit_risk: str
    strength: str
    weakness: str
    dimension_analysis: Dict[str, DimensionAnalysisResponse]



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
    dimension_scores: Dict[str, float]
    explanation: ExplanationResponse
    recommendations: List[str]


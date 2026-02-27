from fastapi import APIRouter

from app.models.schema import AnalyzeRequest, AnalyzeResponse
from app.nlp.semantic_detector import analyze_semantics
from app.scoring.risk_engine import score_risk

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze_text(payload: AnalyzeRequest) -> AnalyzeResponse:
    raw_scores = analyze_semantics(payload.text)
    return score_risk(raw_scores)
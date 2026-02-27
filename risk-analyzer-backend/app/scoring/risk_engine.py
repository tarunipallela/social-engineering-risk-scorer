from typing import Dict

from app.models.schema import AnalyzeResponse, Breakdown
from app.utils.recommendations import get_recommendations


# 🔥 Rebalanced weights
WEIGHTS: Dict[str, float] = {
    "contact": 40.0,
    "corporate": 20.0,
    "location": 15.0,
    "family": 15.0,
    "routine": 10.0,
}


def _risk_level(score: float) -> str:
    if score < 30:
        return "Low"
    elif score < 60:
        return "Medium"
    return "High"


def _risk_summary(level: str, score: float) -> str:
    return f"Risk assessed as {level} ({score:.1f}/100)."


# 🧠 NEW: Context Boost Layer
def _context_boost(raw_scores: dict[str, float]) -> float:
    boost = 0.0

    routine = raw_scores.get("routine", 0.0)
    family = raw_scores.get("family", 0.0)
    location = raw_scores.get("location", 0.0)
    contact = raw_scores.get("contact", 0.0)

    # 🚨 Physical vulnerability scenario
    if routine > 0.5 and family > 0.5:
        boost += 20.0  # leaving home + family alone

    # 🚨 Travel + location disclosure
    if routine > 0.5 and location > 0.5:
        boost += 15.0

    # 🚨 Contact + corporate = targeted phishing risk
    if contact > 0.5 and raw_scores.get("corporate", 0.0) > 0.5:
        boost += 15.0

    # 🚨 Extreme oversharing scenario
    total_active = sum(1 for v in raw_scores.values() if v > 0.5)
    if total_active >= 3:
        boost += 10.0

    return boost


def score_risk(raw_scores: dict[str, float]) -> AnalyzeResponse:
    """
    Convert raw detection signals into weighted + context-aware risk score.
    """

    weighted = {
        key: raw_scores.get(key, 0.0) * WEIGHTS[key]
        for key in WEIGHTS
    }

    base_score = sum(weighted.values())

    # 🔥 Apply context boost
    boost = _context_boost(raw_scores)

    final_score = min(base_score + boost, 100.0)
    final_score = round(final_score, 1)

    level = _risk_level(final_score)

    breakdown_obj = Breakdown(
        contact=round(weighted["contact"], 1),
        corporate=round(weighted["corporate"], 1),
        location=round(weighted["location"], 1),
        family=round(weighted["family"], 1),
        routine=round(weighted["routine"], 1),
    )

    return AnalyzeResponse(
        score=final_score,
        risk_level=level,
        breakdown=breakdown_obj,
        recommendations=get_recommendations(raw_scores),
        risk_summary=_risk_summary(level, final_score),
    )
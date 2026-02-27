from typing import List, Literal

from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    text: str


class Breakdown(BaseModel):
    contact: float
    corporate: float
    location: float
    family: float
    routine: float


class AnalyzeResponse(BaseModel):
    score: float
    # front-end expects `risk_level` so we rename the field accordingly
    risk_level: Literal["Low", "Medium", "High"]
    breakdown: Breakdown
    recommendations: List[str]
    risk_summary: str

    class Config:
        # allow using field names when instantiating even if aliases are defined
        allow_population_by_field_name = True

from pydantic import BaseModel

from app.schemas.planner import PlannerOutput
from app.schemas.market import MarketOutput

class DueDiligenceState(BaseModel):
    startup_description: str

    planner_output: PlannerOutput | None = None

    market_analysis: MarketOutput | None = None

    product_analysis: str | None = None

    competition_analysis: str | None = None

    finance_analysis: str | None = None

    risk_analysis: str | None = None

    critic_review: str | None = None

    final_recommendation: str | None = None
from pydantic import BaseModel

from app.schemas.planner import PlannerOutput
from app.schemas.market import MarketOutput
from app.schemas.finance import FinanceOutput
from app.schemas.competition import CompetitionOutput
from app.schemas.risk import RiskOutput
from app.schemas.product import ProductOutput

class DueDiligenceState(BaseModel):
    startup_description: str

    planner_output: PlannerOutput | None = None

    market_analysis: MarketOutput | None = None

    product_analysis: ProductOutput | None = None

    competition_analysis: CompetitionOutput | None = None

    finance_analysis: FinanceOutput | None = None

    risk_analysis: RiskOutput | None = None

    critic_review: str | None = None

    final_recommendation: str | None = None
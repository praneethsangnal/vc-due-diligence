from app.agents.market import run_market
from app.agents.planner import run_planner
from app.schemas.due_diligence import DueDiligenceState


class DueDiligenceService:
    def run(self, startup_description: str) -> DueDiligenceState:
        state = DueDiligenceState(
            startup_description=startup_description
        )

        # Step 1: Planning
        planner_output = run_planner(startup_description)
        state.planner_output = planner_output

        # Step 2: Specialist Analyses
        #
        # For now we only have the Market Agent.
        # Later this section will dynamically execute the required
        # specialist agents in parallel.
        market_output = run_market(state)
        state.market_analysis = market_output

        return state
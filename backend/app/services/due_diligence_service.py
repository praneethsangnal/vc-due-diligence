import asyncio

from app.agents.competition import run_competition
from app.agents.finance import run_finance
from app.agents.market import run_market
from app.agents.planner import run_planner
from app.schemas.due_diligence import DueDiligenceState

AGENT_REGISTRY = {
    "market": run_market,
    "finance": run_finance,
    "competition": run_competition,
}

STATE_MAPPING = {
    "market": "market_analysis",
    "finance": "finance_analysis",
    "competition": "competition_analysis",
}


class DueDiligenceService:

    async def run(self, startup_description: str) -> DueDiligenceState:

        # Shared state
        state = DueDiligenceState(
            startup_description=startup_description
        )

        # -----------------------------
        # Step 1: Planner (Added missing await)
        # -----------------------------
        planner_output = await run_planner(startup_description)
        state.planner_output = planner_output

        # -----------------------------
        # Step 2: Extract & Filter Valid Agents
        # -----------------------------
        # This keeps lists completely synchronized across Steps 3 & 4
        active_agents = [
            agent for agent in dict.fromkeys(planner_output.required_agents)
            if agent in AGENT_REGISTRY
        ]

        # -----------------------------
        # Step 3: Execute specialists in parallel
        # -----------------------------
        tasks = [AGENT_REGISTRY[agent](state) for agent in active_agents]
        
        # If no valid agents are selected, skip network overhead entirely
        if tasks:
            results = await asyncio.gather(*tasks)
        else:
            results = []

        # -----------------------------
        # Step 4: Store outputs safely
        # -----------------------------
        for agent_name, result in zip(active_agents, results):
            setattr(
                state,
                STATE_MAPPING[agent_name],
                result,
            )

        return state
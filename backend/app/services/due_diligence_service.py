import asyncio

from app.agents.competition import run_competition
from app.agents.finance import run_finance
from app.agents.market import run_market
from app.agents.risk import run_risk
from app.agents.product import run_product
from app.agents.planner import run_planner
from app.agents.critic import run_critic

from app.schemas.due_diligence import DueDiligenceState

AGENT_REGISTRY = {
    "market": run_market,
    "finance": run_finance,
    "competition": run_competition,
    "product": run_product,
    "risk": run_risk,
}

STATE_MAPPING = {
    "market": "market_analysis",
    "finance": "finance_analysis",
    "competition": "competition_analysis",
    "product": "product_analysis",
    "risk": "risk_analysis",
}


class DueDiligenceService:

    async def run(self, startup_description: str) -> DueDiligenceState:

        # Shared state
        state = DueDiligenceState(
            startup_description=startup_description
        )

        # -----------------------------
        # Step 1: Planner
        # -----------------------------
        planner_output = await run_planner(startup_description)
        state.planner_output = planner_output

        # -----------------------------
        # Step 2: Extract & Filter Valid Agents
        # -----------------------------
        active_agents = [
            agent for agent in dict.fromkeys(planner_output.required_agents)
            if agent in AGENT_REGISTRY
        ]

        # -----------------------------
        # Step 3: Execute specialists in parallel
        # -----------------------------
        tasks = [AGENT_REGISTRY[agent](state) for agent in active_agents]
        
        if tasks:
            results = await asyncio.gather(*tasks)
        else:
            results = []

        # -----------------------------
        # Step 4: Store specialist outputs
        # -----------------------------
        for agent_name, result in zip(active_agents, results):
            setattr(
                state,
                STATE_MAPPING[agent_name],
                result,
            )

        # -----------------------------
        # Step 5: Critic review
        # -----------------------------
        critic_output = await run_critic(state)
        state.critic_review = critic_output

        return state
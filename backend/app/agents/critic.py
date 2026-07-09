import asyncio

from app.agents.competition import run_competition
from app.agents.critic import run_critic
from app.agents.finance import run_finance
from app.agents.market import run_market
from app.agents.planner import run_planner
from app.agents.product import run_product
from app.agents.risk import run_risk
from app.schemas.due_diligence import DueDiligenceState


AGENT_REGISTRY = {
    "market": run_market,
    "finance": run_finance,
    "competition": run_competition,
    "risk": run_risk,
    "product": run_product,
}


STATE_MAPPING = {
    "market": "market_analysis",
    "finance": "finance_analysis",
    "competition": "competition_analysis",
    "risk": "risk_analysis",
    "product": "product_analysis",
}


class DueDiligenceService:

    async def run(
        self,
        startup_description: str,
    ) -> DueDiligenceState:

        # -----------------------------
        # Step 1: Create shared state
        # -----------------------------
        state = DueDiligenceState(
            startup_description=startup_description
        )

        # -----------------------------
        # Step 2: Run planner
        # -----------------------------
        planner_output = await run_planner(startup_description)
        state.planner_output = planner_output

        # -----------------------------
        # Step 3: Extract valid agents
        # and remove duplicates while
        # preserving planner order
        # -----------------------------
        active_agents = [
            agent
            for agent in dict.fromkeys(planner_output.required_agents)
            if agent in AGENT_REGISTRY
        ]

        # -----------------------------
        # Step 4: Run selected
        # specialists in parallel
        # -----------------------------
        tasks = [
            AGENT_REGISTRY[agent](state)
            for agent in active_agents
        ]

        if tasks:
            results = await asyncio.gather(*tasks)
        else:
            results = []

        # -----------------------------
        # Step 5: Store specialist
        # outputs in shared state
        # -----------------------------
        for agent_name, result in zip(active_agents, results):
            setattr(
                state,
                STATE_MAPPING[agent_name],
                result,
            )

        # -----------------------------
        # Step 6: First critic review
        # -----------------------------
        critic_output = await run_critic(state)
        state.critic_review = critic_output

        # -----------------------------
        # Step 7: Group revision
        # requests by agent
        # -----------------------------
        revision_instructions = {}

        for request in critic_output.revision_requests:
            agent_name = request.agent_name

            if agent_name not in AGENT_REGISTRY:
                continue

            instruction = (
                f"Reason: {request.reason}\n"
                f"Instructions: {request.instructions}"
            )

            if agent_name in revision_instructions:
                revision_instructions[agent_name] += (
                    f"\n\n{instruction}"
                )
            else:
                revision_instructions[agent_name] = instruction

        # -----------------------------
        # Step 8: Rerun only affected
        # specialists in parallel
        # -----------------------------
        if revision_instructions:

            revision_agents = list(
                revision_instructions.keys()
            )

            revision_tasks = [
                AGENT_REGISTRY[agent](
                    state,
                    revision_instructions[agent],
                )
                for agent in revision_agents
            ]

            revised_results = await asyncio.gather(
                *revision_tasks
            )

            # -------------------------
            # Step 9: Replace old
            # outputs with revisions
            # -------------------------
            for agent_name, result in zip(
                revision_agents,
                revised_results,
            ):
                setattr(
                    state,
                    STATE_MAPPING[agent_name],
                    result,
                )

            # -------------------------
            # Step 10: Final critic
            # review of updated state
            # -------------------------
            final_critic_output = await run_critic(state)
            state.critic_review = final_critic_output

        return state
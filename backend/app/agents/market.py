from crewai import Agent, Crew, Task

from app.core.config import settings
from app.schemas.due_diligence import DueDiligenceState
from app.schemas.market import MarketOutput


def get_market_agent() -> Agent:
    return Agent(
        role="Venture Capital Market Analyst",
        goal=(
            "Evaluate the startup's market opportunity, industry growth, "
            "market size, opportunities, and risks."
        ),
        backstory=(
            "You are a senior venture capital market analyst with expertise "
            "in evaluating startup markets. Your responsibility is limited "
            "to market analysis. You do not evaluate financials, competition, "
            "or investment decisions."
        ),
        llm=settings.MODEL_SPECIALIST,
        verbose=True,
    )


async def run_market(
    state: DueDiligenceState,
    revision_instructions: str | None = None,
) -> MarketOutput:
    market_agent = get_market_agent()

    revision_context = ""

    if revision_instructions:
        revision_context = f"""
This analysis is being revised after a quality review by the Critic Agent.

Revision Instructions:
{revision_instructions}

Address the specific issues identified above while remaining within your role
as the Market Analyst. Re-evaluate any unsupported or inconsistent conclusions
using only the available evidence. Do not invent facts.
"""

    task = Task(
        description=f"""
Analyze ONLY the market aspects of the following startup.

Startup Description:
{state.startup_description}

Evaluate:

1. Market size and overall addressable opportunity.
2. Market growth potential.
3. Key market opportunities.
4. Major market risks.
5. Overall market outlook.

Use only information explicitly provided or reasonably inferred from the
available startup description.

Do not invent facts. If important information is unavailable, clearly state
that it cannot be assessed from the available evidence.

{revision_context}
""",
        expected_output="Return a MarketOutput object.",
        output_pydantic=MarketOutput,
        agent=market_agent,
    )

    crew = Crew(
        agents=[market_agent],
        tasks=[task],
        verbose=True,
    )

    result = await crew.akickoff()

    return result.pydantic
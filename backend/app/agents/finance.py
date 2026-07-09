from crewai import Agent, Crew, Task

from app.core.config import settings
from app.schemas.due_diligence import DueDiligenceState
from app.schemas.finance import FinanceOutput


def get_finance_agent() -> Agent:
    return Agent(
        role="Venture Capital Financial Analyst",
        goal=(
            "Evaluate the financial viability of the startup from an "
            "investment perspective."
        ),
        backstory=(
            "You are a senior venture capital financial analyst. "
            "Your responsibility is limited to financial evaluation. "
            "Do not analyze the market, competition, product, or risks."
        ),
        llm=settings.MODEL_SPECIALIST,
        verbose=True,
    )


async def run_finance(
    state: DueDiligenceState,
    revision_instructions: str | None = None,
) -> FinanceOutput:
    finance_agent = get_finance_agent()

    revision_context = ""

    if revision_instructions:
        revision_context = f"""
This analysis is being revised after a quality review by the Critic Agent.

Revision Instructions:
{revision_instructions}

Address the specific issues identified above while remaining within your role
as the Financial Analyst. Re-evaluate any unsupported or inconsistent conclusions
using only the available evidence. Do not invent facts.
"""

    task = Task(
        description=f"""
Analyze ONLY the financial aspects of the following startup.

Startup Description:

{state.startup_description}

Evaluate:

1. Revenue model.
2. Financial strengths.
3. Financial risks.
4. Funding stage assessment.
5. Overall financial summary.

If information is unavailable, explicitly mention that instead of making assumptions.

{revision_context}
""",
        expected_output="Return a FinanceOutput object.",
        output_pydantic=FinanceOutput,
        agent=finance_agent,
    )

    crew = Crew(
        agents=[finance_agent],
        tasks=[task],
        verbose=True,
    )

    result = await crew.akickoff()

    return result.pydantic
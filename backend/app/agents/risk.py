from crewai import Agent, Crew, Task

from app.core.config import settings
from app.schemas.due_diligence import DueDiligenceState
from app.schemas.risk import RiskOutput


def get_risk_agent() -> Agent:
    return Agent(
        role="Venture Capital Risk Analyst",
        goal=(
            "Identify and evaluate the major risks associated with investing "
            "in the startup."
        ),
        backstory=(
            "You are a senior venture capital risk analyst specializing in "
            "identifying business, operational, regulatory, and technology "
            "risks. Your responsibility is limited to risk assessment. "
            "Do not evaluate the market, competition, financials, or product."
        ),
        llm=settings.MODEL_SPECIALIST,
        verbose=True,
    )


async def run_risk(
    state: DueDiligenceState,
    revision_instructions: str | None = None,
) -> RiskOutput:
    risk_agent = get_risk_agent()

    revision_context = ""

    if revision_instructions:
        revision_context = f"""
This analysis is being revised after a quality review by the Critic Agent.

Revision Instructions:
{revision_instructions}

Address the specific issues identified above while remaining within your role
as the Risk Analyst. Re-evaluate any unsupported or inconsistent conclusions
using only the available evidence. Do not invent facts.
"""

    task = Task(
        description=f"""
Analyze ONLY the risks associated with the following startup.

Startup Description:

{state.startup_description}

Evaluate:

1. Business risks.
2. Operational risks.
3. Regulatory risks.
4. Technology risks.
5. Possible mitigation strategies.
6. Overall risk assessment.

Use only information that is explicitly provided or can be reasonably inferred.

Do not invent facts.

If information is unavailable, explicitly state that it cannot be assessed.

{revision_context}
""",
        expected_output="Return a RiskOutput object.",
        output_pydantic=RiskOutput,
        agent=risk_agent,
    )

    crew = Crew(
        agents=[risk_agent],
        tasks=[task],
        verbose=True,
    )

    result = await crew.akickoff()

    return result.pydantic
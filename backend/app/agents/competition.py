from crewai import Agent, Crew, Task

from app.core.config import settings
from app.schemas.competition import CompetitionOutput
from app.schemas.due_diligence import DueDiligenceState


def get_competition_agent() -> Agent:
    return Agent(
        role="Venture Capital Competitive Intelligence Analyst",
        goal=(
            "Evaluate the competitive landscape and determine how well "
            "the startup can differentiate itself."
        ),
        backstory=(
            "You are an experienced venture capital analyst specializing "
            "in competitive intelligence. Your responsibility is limited "
            "to identifying competitors, competitive advantages, barriers "
            "to entry, and competitive risks. You do not evaluate market "
            "size, financials, product quality, or investment decisions."
        ),
        llm=settings.MODEL_SPECIALIST,
        verbose=True,
    )


async def run_competition(
    state: DueDiligenceState,
    revision_instructions: str | None = None,
) -> CompetitionOutput:
    competition_agent = get_competition_agent()

    revision_context = ""

    if revision_instructions:
        revision_context = f"""
This analysis is being revised after a quality review by the Critic Agent.

Revision Instructions:
{revision_instructions}

Address the specific issues identified above while remaining within your role
as the Competitive Intelligence Analyst. Re-evaluate any unsupported or inconsistent conclusions
using only the available evidence. Do not invent facts.
"""

    task = Task(
        description=f"""
Analyze ONLY the competitive aspects of the following startup.

Startup Description:

{state.startup_description}

Evaluate:

1. Competitive advantages.
2. Major competitors.
3. Barriers to entry.
4. Competitive risks.
5. Overall competitive assessment.

Use only information that can reasonably be inferred from the startup description.
If information is unavailable, explicitly state that instead of making assumptions.

{revision_context}
""",
        expected_output="Return a CompetitionOutput object.",
        output_pydantic=CompetitionOutput,
        agent=competition_agent,
    )

    crew = Crew(
        agents=[competition_agent],
        tasks=[task],
        verbose=True,
    )

    result = await crew.akickoff()

    return result.pydantic
from crewai import Agent, Crew, Task

from app.core.config import settings
from app.schemas.due_diligence import DueDiligenceState


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


def run_market(state: DueDiligenceState):
    market_agent = get_market_agent()

    task = Task(
        description=f"""
Analyze ONLY the market aspects of the following startup.

Startup Description:
{state.startup_description}

Your responsibilities:

1. Estimate the market size.
2. Evaluate market growth potential.
3. Identify key opportunities.
4. Identify major market risks.
5. Summarize the overall market outlook.

Return ONLY valid JSON in the following format:

{{
    "market_size": "...",
    "growth_potential": "...",
    "key_opportunities": [
        "...",
        "..."
    ],
    "key_risks": [
        "...",
        "..."
    ],
    "summary": "..."
}}
""",
        expected_output="A JSON object containing the market analysis.",
        agent=market_agent,
    )

    crew = Crew(
        agents=[market_agent],
        tasks=[task],
        verbose=True,
    )

    return crew.kickoff()
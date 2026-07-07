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


def run_market(state: DueDiligenceState):
    market_agent = get_market_agent()

    task = Task(
        description=f"""
Analyze ONLY the market aspects of the following startup.

Startup Description:
{state.startup_description}
""",
        expected_output="A MarketOutput object.",
        output_pydantic=MarketOutput,
        agent=market_agent,
    )

    crew = Crew(
        agents=[market_agent],
        tasks=[task],
        verbose=True,
    )
    result=crew.kickoff()
    return result.pydantic
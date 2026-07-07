from crewai import Agent, Crew, Task

from app.core.config import settings
from app.schemas.due_diligence import DueDiligenceState
from app.schemas.product import ProductOutput


def get_product_agent() -> Agent:
    return Agent(
        role="Venture Capital Product Analyst",
        goal=(
            "Evaluate the startup's product, its value proposition, "
            "innovation, scalability, and overall product quality."
        ),
        backstory=(
            "You are a senior venture capital product analyst. "
            "Your responsibility is limited to evaluating the startup's "
            "product. Do not analyze the market, competition, financials, "
            "or investment risks."
        ),
        llm=settings.MODEL_SPECIALIST,
        verbose=True,
    )


async def run_product(state: DueDiligenceState) -> ProductOutput:
    product_agent = get_product_agent()

    task = Task(
        description=f"""
Analyze ONLY the product aspects of the following startup.

Startup Description:

{state.startup_description}

Evaluate:

1. The startup's value proposition.
2. Product strengths.
3. Product weaknesses.
4. Innovation and differentiation.
5. Product scalability.
6. Overall product assessment.

Use only information that is explicitly provided or can be reasonably inferred.

Do not invent facts.

If information is unavailable, explicitly state that it cannot be assessed.
""",
        expected_output="Return a ProductOutput object.",
        output_pydantic=ProductOutput,
        agent=product_agent,
    )

    crew = Crew(
        agents=[product_agent],
        tasks=[task],
        verbose=True,
    )

    result = await crew.akickoff()

    return result.pydantic
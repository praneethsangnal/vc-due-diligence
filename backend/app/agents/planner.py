from crewai import Agent, Crew, Task

from app.core.config import settings
from app.schemas.planner import PlannerOutput


def get_planner_agent() -> Agent:
    return Agent(
        role="Venture Capital Planning Specialist",
        goal=(
            "Determine the startup type and identify the specialist agents "
            "required to perform a complete venture capital due diligence."
        ),
        backstory=(
            "You are an experienced venture capitalist responsible for planning "
            "the due diligence process. You never perform the analysis yourself. "
            "Your responsibility is to identify the startup category and decide "
            "which specialist analysts should participate in the evaluation."
        ),
        llm=settings.MODEL_PLANNER,
        verbose=True,
    )


def run_planner(startup_description: str) -> PlannerOutput:
    planner = get_planner_agent()

    task = Task(
        description=f"""
Analyze the following startup.

Startup Description:
{startup_description}

Your responsibilities are:

1. Identify the startup type.
2. Determine which specialist agents are required.
3. Explain why each specialist is needed.

Focus only on planning the due diligence workflow.
Do not perform the actual analysis.
""",
        expected_output=(
            "A PlannerOutput object containing the startup type, "
            "required specialist agents, and reasoning."
        ),
        output_pydantic=PlannerOutput,
        agent=planner,
    )

    crew = Crew(
        agents=[planner],
        tasks=[task],
        verbose=True,
    )

    result = crew.kickoff()

    return result.pydantic
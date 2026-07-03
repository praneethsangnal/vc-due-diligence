from crewai import Agent, Crew, Task

from app.core.config import settings


def get_planner_agent() -> Agent:
    return Agent(
        role="Venture Capital Planning Specialist",
        goal=(
            "Determine the startup type and identify which specialist "
            "agents are required for a complete venture capital due diligence."
        ),
        backstory=(
            "You are an experienced venture capitalist responsible only for "
            "planning the due diligence workflow. You never perform the "
            "analysis yourself. You only decide which expert agents should "
            "participate."
        ),
        llm=settings.MODEL_PLANNER,
        verbose=True,
    )


def run_planner(startup_description: str):
    planner = get_planner_agent()

    task = Task(
        description=f"""
Analyze the following startup description.

Startup Description:
{startup_description}

Identify:

1. Startup type
2. Specialist agents required
3. Explain why those agents are needed

Return the result as valid JSON.

Example:

{{
    "startup_type": "AI SaaS",
    "required_agents": [
        "market",
        "finance",
        "competition",
        "risk"
    ],
    "reasoning": "..."
}}
""",
        expected_output="A JSON object describing the execution plan.",
        agent=planner,
    )

    crew = Crew(
        agents=[planner],
        tasks=[task],
        verbose=True,
    )

    return crew.kickoff()
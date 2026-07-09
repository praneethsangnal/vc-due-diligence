from crewai import Agent, Crew, Task

from app.core.config import settings
from app.schemas.critic import CriticOutput
from app.schemas.due_diligence import DueDiligenceState


def get_critic_agent() -> Agent:
    return Agent(
        role="Senior Venture Capital Due Diligence Reviewer",
        goal=(
            "Critically review all available specialist analyses, identify "
            "material evidence gaps, unsupported conclusions, cross-agent "
            "inconsistencies, and high-priority unanswered due diligence questions."
        ),
        backstory=(
            "You are a senior venture capital partner responsible for quality "
            "control before a startup reaches the investment committee. You do "
            "not perform new market, financial, competitive, product, or risk "
            "analysis. You critically evaluate the work already produced by "
            "specialist analysts and request targeted revisions only when "
            "material problems could affect the investment decision."
        ),
        llm=settings.MODEL_CRITIC,
        verbose=True,
    )


async def run_critic(state: DueDiligenceState) -> CriticOutput:
    critic_agent = get_critic_agent()

    specialist_analyses = {
        "market": state.market_analysis,
        "finance": state.finance_analysis,
        "competition": state.competition_analysis,
        "risk": state.risk_analysis,
        "product": state.product_analysis,
    }

    available_analyses = {
        name: analysis.model_dump()
        for name, analysis in specialist_analyses.items()
        if analysis is not None
    }

    task = Task(
        description=f"""
Review the complete venture capital due diligence evidence below.

Original Startup Description:
{state.startup_description}

Specialist Analyses:
{available_analyses}

Your responsibilities:

1. MISSING EVIDENCE
Identify critical information that is absent and materially limits the quality
of the due diligence. Do not request a specialist revision merely because the
original startup description does not contain information that no specialist
could reasonably know.

2. UNSUPPORTED CONCLUSIONS
Identify conclusions made by specialists that are not adequately supported by
the original startup description or the available evidence.

3. CROSS-AGENT INCONSISTENCIES
Identify meaningful contradictions between specialist analyses. Only flag
disagreements that could materially affect an investment decision.

4. HIGH-PRIORITY DUE DILIGENCE QUESTIONS
Generate the most important questions that should be answered by the founders
or through further investigation before making an investment decision.

5. REVISION REQUESTS
Request a specialist revision only when:
- the specialist made a materially unsupported conclusion,
- its analysis contradicts another specialist in a meaningful way,
- or its reasoning can realistically be improved using the evidence already available.

Do NOT request a revision simply because information is missing from the
original startup description. Missing founder-provided information should
instead become a due diligence question.

For every revision request:
- identify the exact specialist agent,
- explain why revision is necessary,
- provide specific instructions for what should be corrected.

Do not make an investment decision.
Do not perform new specialist analysis.
Focus only on evidence quality, consistency, completeness, and reasoning quality.
""",
        expected_output="Return a CriticOutput object.",
        output_pydantic=CriticOutput,
        agent=critic_agent,
    )

    crew = Crew(
        agents=[critic_agent],
        tasks=[task],
        verbose=True,
    )

    result = await crew.akickoff()

    return result.pydantic
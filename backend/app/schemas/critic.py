from typing import Literal

from pydantic import BaseModel, Field


AgentName = Literal[
    "market",
    "finance",
    "competition",
    "risk",
    "product",
]


class CriticIssue(BaseModel):
    issue_type: Literal[
        "missing_evidence",
        "unsupported_conclusion",
        "cross_agent_inconsistency",
    ] = Field(
        description="The category of the identified issue."
    )

    description: str = Field(
        description="Clear explanation of the issue."
    )

    affected_agents: list[AgentName] = Field(
        description="Specialist agents associated with this issue."
    )

    severity: Literal["low", "medium", "high"] = Field(
        description="Material importance of the issue to the investment decision."
    )


class RevisionRequest(BaseModel):
    agent_name: AgentName = Field(
        description="The specialist agent that should revise its analysis."
    )

    reason: str = Field(
        description="Why this agent needs to revise its analysis."
    )

    instructions: str = Field(
        description="Specific instructions for improving the analysis."
    )


class CriticOutput(BaseModel):
    issues: list[CriticIssue] = Field(
        description="Material issues identified across the specialist analyses."
    )

    due_diligence_questions: list[str] = Field(
        description="High-priority questions that should be answered before investing."
    )

    revision_requests: list[RevisionRequest] = Field(
        description="Targeted revision requests for specialist agents with material issues."
    )

    overall_assessment: str = Field(
        description="Overall assessment of the quality, consistency, and completeness of the available analyses."
    )
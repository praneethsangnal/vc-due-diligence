from typing import Literal

from pydantic import BaseModel, Field


class PlannerOutput(BaseModel):
    startup_type: str = Field(
        description="The category of the startup."
    )

    required_agents: list[
        Literal[
            "market",
            "finance",
            "competition",
            "product",
            "risk",
        ]
    ] = Field(
        description="List of specialist agents required for this startup."
    )

    reasoning: str = Field(
        description="Explanation of why these specialist agents were selected."
    )
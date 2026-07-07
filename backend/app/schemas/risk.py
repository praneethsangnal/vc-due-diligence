from pydantic import BaseModel, Field


class RiskOutput(BaseModel):
    business_risks: list[str] = Field(
        description="Business risks that could negatively impact the startup."
    )

    operational_risks: list[str] = Field(
        description="Operational risks related to scaling and execution."
    )

    regulatory_risks: list[str] = Field(
        description="Legal or regulatory risks affecting the startup."
    )

    technology_risks: list[str] = Field(
        description="Technical risks associated with the product or technology."
    )

    mitigation_strategies: list[str] = Field(
        description="Possible ways to reduce or manage the identified risks."
    )

    summary: str = Field(
        description="Overall risk assessment."
    )
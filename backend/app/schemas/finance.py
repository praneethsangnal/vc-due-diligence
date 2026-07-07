from pydantic import BaseModel, Field


class FinanceOutput(BaseModel):
    revenue_model: str = Field(
        description="Description of how the startup generates revenue."
    )

    financial_strengths: list[str] = Field(
        description="Key financial strengths of the startup."
    )

    financial_risks: list[str] = Field(
        description="Major financial risks or concerns."
    )

    funding_assessment: str = Field(
        description="Assessment of the startup's funding stage and capital position."
    )

    summary: str = Field(
        description="Overall financial assessment."
    )
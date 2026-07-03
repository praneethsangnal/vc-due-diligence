from pydantic import BaseModel, Field


class MarketOutput(BaseModel):
    market_size: str = Field(
        description="Estimated market size for the startup."
    )

    growth_potential: str = Field(
        description="Expected market growth and future outlook."
    )

    key_opportunities: list[str] = Field(
        description="Major market opportunities."
    )

    key_risks: list[str] = Field(
        description="Major market risks."
    )

    summary: str = Field(
        description="Overall market assessment."
    )
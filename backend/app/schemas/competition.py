from pydantic import BaseModel, Field


class CompetitionOutput(BaseModel):
    competitive_advantages: list[str] = Field(
        description="Key competitive advantages of the startup."
    )

    major_competitors: list[str] = Field(
        description="Likely competitors based on the startup description."
    )

    barriers_to_entry: list[str] = Field(
        description="Factors that make it difficult for competitors to enter the market."
    )

    competitive_risks: list[str] = Field(
        description="Major competitive threats faced by the startup."
    )

    summary: str = Field(
        description="Overall competitive assessment."
    )
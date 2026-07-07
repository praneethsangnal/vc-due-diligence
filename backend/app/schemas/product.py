from pydantic import BaseModel, Field


class ProductOutput(BaseModel):
    value_proposition: str = Field(
        description="The core value proposition offered by the startup."
    )

    product_strengths: list[str] = Field(
        description="Key strengths of the product."
    )

    product_weaknesses: list[str] = Field(
        description="Limitations or weaknesses of the product."
    )

    innovation_assessment: str = Field(
        description="Assessment of the product's uniqueness and innovation."
    )

    scalability_assessment: str = Field(
        description="Assessment of how well the product can scale."
    )

    summary: str = Field(
        description="Overall product assessment."
    )
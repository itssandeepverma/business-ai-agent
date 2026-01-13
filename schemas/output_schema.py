from pydantic import BaseModel, Field


class BusinessOverview(BaseModel):
    summary: str = Field(description="Clear one paragraph business summary")
    primary_target_audience: str = Field(description="Specific audience description (One primary target)")
    core_pain_point: str = Field(description="Main problem this audience has (One core pain point)")
    unique_value_proposition: str = Field(description="Why this business wins (One clear advantage)")
    not_a_priority: str = Field(description="What should be avoided or deprioritized")
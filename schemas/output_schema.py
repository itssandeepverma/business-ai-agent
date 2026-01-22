from typing import List

from pydantic import BaseModel, Field


class BusinessOverview(BaseModel):
    summary: str = Field(description="Clear one paragraph business summary")
    primary_target_audience: str = Field(description="Specific audience description (One primary target)")
    core_pain_point: str = Field(description="Main problem this audience has (One core pain point)")
    unique_value_proposition: str = Field(description="Why this business wins (One clear advantage)")
    not_a_priority: str = Field(description="What should be avoided or deprioritized")
    

class MarketingChannel(BaseModel):
    channel: str = Field(description="Name of the marketing channel")
    priority: int = Field(description="Priority level of the channel (1 being highest)")
    why_this_channel: str = Field(description="Specific reason for choosing this channel")

class IgnoredChannel(BaseModel):
    channel: str = Field(description="Name of the ignored marketing channel")
    reason: str = Field(description="Reason for ignoring this channel")

class MarketingStrategy(BaseModel):
    primary_goal: str = Field(description="Main marketing goal")
    core_message: str = Field(description="Key message to communicate")
    channels: List[MarketingChannel] = Field(description="List of 3 marketing channels")
    ignored_channel: IgnoredChannel = Field(description="One marketing channel to avoid and why")

class FinalOutput(BaseModel):
    business_overview: BusinessOverview 
    marketing_strategy: MarketingStrategy
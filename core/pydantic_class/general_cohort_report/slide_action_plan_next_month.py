from typing import Annotated
from pydantic import BaseModel, Field


class ActionPlanRow(BaseModel):
    focus_area: Annotated[str, Field(max_length=24)] = Field(
        ...,
        description="Platform or metric area needing improvement (e.g., 'Facebook Posts', 'Instagram Posts', 'Facebook Ads', 'Engagement & Brand Trust')",
    )
    action: Annotated[str, Field(max_length=78)] = Field(
        ...,
        description="What content or information customer needs to provide (e.g., 'Share visuals of new cake designs along with flavors available')",
    )
    goal: Annotated[str, Field(max_length=71)] = Field(
        ...,
        description="Realistic target based on current performance data (e.g., 'Maintain 10 posts per month', 'Keep CTR above 6%')",
    )
    execution: Annotated[str, Field(max_length=78)] = Field(
        ...,
        description="Type of request needed: On-Demand (promotions, events, new products) or Ongoing (extra images)",
    )


class ActionPlanReport(BaseModel):
    report_title: Annotated[str, Field(max_length=80)] = Field(
        default="Action Plan for the Next Month",
        description="Title for the action plan report",
    )
    rows: list[ActionPlanRow] = Field(
        ...,
        description="List of action items, typically 3-5 rows covering different focus areas",
    )
    what_does_it_mean: Annotated[str, Field(max_length=235)] | None = Field(
        default=None,
        description="1-2 sentence summary explaining the overall strategy and expected outcomes",
    )

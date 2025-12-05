from pydantic import BaseModel, Field
from typing import Annotated


class TimelineEvent(BaseModel):
    """A single segment in the delivery timeline"""

    date: Annotated[str, Field(max_length=30)] = Field(
        ...,
        description="The date range for this segment (e.g., 'Sept 23 - Oct 6'). Max 30 chars.",
    )
    category: Annotated[str, Field(max_length=30)] = Field(
        ...,
        description="The type of posts delivered (e.g., 'Ongoing Social Posts', 'On-Demand Social Posts', or 'Ongoing & On-Demand Posts') or Ads. Max 30 chars.",
    )
    description: Annotated[str, Field(max_length=148)] = Field(
        ...,
        description="A one-line specific summary of the content topics covered in this duration. Max 148 chars.",
    )


class DeliveryTimelineSlide(BaseModel):
    """The complete structure for the 'What We Delivered' slide"""

    title: str = Field(
        default="Here's What We Delivered for You",
        description="The fixed title of the slide",
    )
    timeline_events: list[TimelineEvent] = Field(
        ...,
        description="List of exactly 4 timeline events representing the delivery segments",
        min_length=4,
        max_length=4,
    )

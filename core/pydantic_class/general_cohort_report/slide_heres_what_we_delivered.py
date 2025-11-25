from typing import Annotated
from pydantic import BaseModel, Field

SegmentLabel = Annotated[str, Field(strip_whitespace=True, max_length=30)]
TitleStr = Annotated[str, Field(strip_whitespace=True, max_length=30)]
SummaryStr = Annotated[str, Field(strip_whitespace=True, max_length=148)]
PostTypeStr = Annotated[str, Field(strip_whitespace=True, max_length=30)]


class DeliverySegment(BaseModel):
    segment_label: SegmentLabel | None = Field(
        ..., description="Short date or date-range label (<=30 chars)"
    )
    title: TitleStr | None = Field(
        ..., description="Short header/title for the segment (<=30 chars)"
    )
    summary: SummaryStr | None = Field(
        ..., description="One-line content summary for that duration (<=148 chars)"
    )
    post_types: PostTypeStr | None = Field(
        ..., description="Either 'Ongoing' or 'On-Demand' (<=30 chars)"
    )


class DeliverySegmentsReport(BaseModel):
    report_title: Annotated[str, Field(max_length=60)] | None = Field(
        "Delivery Segments", description="Optional report title"
    )
    segments: list[DeliverySegment] = Field(
        ..., description="List of 4-5 chronological segments"
    )

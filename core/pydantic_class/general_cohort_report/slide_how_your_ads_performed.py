from typing import Annotated
from pydantic import BaseModel, Field


class AdPerformanceRow(BaseModel):
    ad_label: Annotated[str, Field(max_length=68)] = Field(
        ..., description="Example: 'Facebook Ads September'"
    )
    performance_summary: Annotated[str, Field(max_length=71)] = Field(
        ..., description="Simple one-line summary"
    )
    metrics_line: Annotated[str, Field(max_length=90)] = Field(
        ..., description="Metrics sentence (<=90 chars)"
    )


class AdsPerformanceReport(BaseModel):
    report_title: Annotated[str, Field(max_length=80)] | None = Field(
        "How Your Ads Performed"
    )
    rows: list[AdPerformanceRow]
    what_does_it_mean: Annotated[str, Field(max_length=235)] | None = None

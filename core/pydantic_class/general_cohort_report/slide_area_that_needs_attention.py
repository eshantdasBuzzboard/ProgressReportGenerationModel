from typing import Annotated
from pydantic import BaseModel, Field


class MetricPeriod(BaseModel):
    period_label: str = Field(
        ...,
        description="Period label - either short month format (e.g., 'Sep', 'Oct', 'Aug') for 2-3 months data, or weekly format (e.g., 'Week 1', 'Week 2', 'Week 3', 'Week 4') for single month data",
    )
    value: float | int = Field(..., description="Metric value for this period")


class AttentionMetricRow(BaseModel):
    metric_name: Annotated[str, Field(max_length=32)] = Field(
        ...,
        description="Name of the metric needing attention (e.g., 'Facebook Posts', 'Facebook Impressions', 'Instagram Impressions')",
    )
    periods: list[MetricPeriod] = Field(
        ...,
        description="List of period data points showing the metric over time. Format depends on data: monthly (Aug, Sep, Oct) if 2-3 months present, or weekly (Week 1, Week 2, Week 3, Week 4) if only 1 month present",
    )
    how_to_fix: Annotated[str, Field(max_length=94)] = Field(
        ...,
        description="One-line actionable suggestion on how to improve this metric, including post themes and request type",
    )


class AreasNeedingAttentionReport(BaseModel):
    report_title: Annotated[str, Field(max_length=80)] = Field(
        default="Areas That Need Attention",
        description="Title for the attention areas report",
    )
    rows: list[AttentionMetricRow] = Field(
        ...,
        min_length=6,
        max_length=6,
        description="Exactly 6 metric rows dynamically selected based on QuickSight data. Prioritize core social metrics (Facebook Posts, Facebook Impressions, Instagram Impressions) first, then other declining or underperforming metrics",
    )
    what_does_it_mean: Annotated[str, Field(max_length=235)] | None = Field(
        default=None,
        description="One-line summary explaining the overall situation and what needs to be done",
    )

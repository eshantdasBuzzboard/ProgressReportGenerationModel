from pydantic import BaseModel, Field
from typing import Annotated


class MetricRow(BaseModel):
    """A single metric row with start value, end value, and change percentage"""

    metric_name: str = Field(
        ...,
        description="Name of the metric (e.g., 'Facebook Posts', 'Instagram Impressions')",
    )
    start_value: str = Field(
        ...,
        description="Value at the start period (can be number or text like 'Started posting')",
    )
    end_value: str = Field(..., description="Value at the end period")
    change_percentage: str = Field(
        ..., description="Percentage change with +/- sign (e.g., '+266.7%', '-76.9%')"
    )
    start_period: str = Field(
        ..., description="Starting period label (e.g., 'Sep', 'Week 1')"
    )
    end_period: str = Field(
        ..., description="Ending period label (e.g., 'Oct', 'Week 4')"
    )


class GrowthAtGlanceReport(BaseModel):
    """Complete performance table report with 8 rows of metrics"""

    facebook_posts: MetricRow = Field(..., description="Facebook Posts metric row")
    facebook_impressions: MetricRow = Field(
        ..., description="Facebook Impressions metric row"
    )
    instagram_posts: MetricRow = Field(..., description="Instagram Posts metric row")
    instagram_impressions: MetricRow = Field(
        ..., description="Instagram Impressions metric row"
    )
    facebook_ads_ctr: MetricRow = Field(
        ..., description="Facebook Ads Click Through Rate metric row"
    )
    facebook_ads_cpc: MetricRow = Field(
        ..., description="Facebook Ads Cost Per Click metric row"
    )
    google_metric_1: MetricRow = Field(
        ..., description="Best performing Google metric (1st choice)"
    )
    google_metric_2: MetricRow | None = Field(
        None,
        description="Second best performing Google metric (optional, if space allows)",
    )

    what_does_it_mean: Annotated[str, Field(max_length=235)] = Field(
        ...,
        description="2-line footer note summarizing the overall big wins in simple English (max 235 characters)",
    )

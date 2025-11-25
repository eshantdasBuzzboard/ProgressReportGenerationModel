from typing import Annotated
from pydantic import BaseModel, Field


class PostStats(BaseModel):
    """Statistics for posts showing start and end values"""

    start_value: int = Field(..., description="Number of posts in the starting month")
    end_value: int = Field(..., description="Number of posts in the ending month")
    start_period: str = Field(
        ..., description="Starting period label (e.g., 'Aug', 'Week 1')"
    )
    end_period: str = Field(
        ..., description="Ending period label (e.g., 'Oct', 'Week 4')"
    )


class ImpressionStats(BaseModel):
    """Statistics for impressions with summary"""

    start_value: int = Field(
        ..., description="Number of impressions in the starting month"
    )
    end_value: int = Field(..., description="Number of impressions in the ending month")
    start_period: str = Field(
        ..., description="Starting period label (e.g., 'Aug', 'Week 1')"
    )
    end_period: str = Field(
        ..., description="Ending period label (e.g., 'Oct', 'Week 4')"
    )
    one_line_summary: Annotated[str, Field(max_length=68)] = Field(
        ...,
        description="Summary of post frequency and engagement performance (max 68 characters)",
    )


class FacebookSection(BaseModel):
    """Facebook posts and impressions data"""

    posts: PostStats | None = Field(
        None, description="Facebook posts statistics from start to end period"
    )
    impressions: ImpressionStats | None = Field(
        None,
        description="Facebook impressions with one-line summary about post frequency and engagement",
    )


class InstagramSection(BaseModel):
    """Instagram posts and impressions data"""

    posts: PostStats | None = Field(
        None, description="Instagram posts statistics from start to end period"
    )
    impressions: ImpressionStats | None = Field(
        None,
        description="Instagram impressions with one-line summary about post frequency and engagement",
    )


class FacebookAdsSection(BaseModel):
    """Facebook Ads (Post Creatives) performance metrics"""

    click_through_rate_start: float | None = Field(
        None, description="Click Through Rate percentage at start period (e.g., 5.23)"
    )
    click_through_rate_end: float | None = Field(
        None, description="Click Through Rate percentage at end period (e.g., 6.46)"
    )
    cost_per_click_start: float | None = Field(
        None, description="Cost Per Click in dollars at start period (e.g., 0.92)"
    )
    cost_per_click_end: float | None = Field(
        None, description="Cost Per Click in dollars at end period (e.g., 1.10)"
    )
    start_period: str | None = Field(
        None, description="Starting period label (e.g., 'Aug', 'Week 1')"
    )
    end_period: str | None = Field(
        None, description="Ending period label (e.g., 'Oct', 'Week 4')"
    )
    one_line_summary: Annotated[str, Field(max_length=68)] | None = Field(
        None,
        description="Summary of Facebook Ads performance and creative relevance (max 68 characters)",
    )


class GoogleAdsSection(BaseModel):
    """Google Ads performance metrics"""

    click_through_rate_start: float | None = Field(
        None, description="Click Through Rate percentage at start period"
    )
    click_through_rate_end: float | None = Field(
        None, description="Click Through Rate percentage at end period"
    )
    cost_per_click_start: float | None = Field(
        None, description="Cost Per Click in dollars at start period"
    )
    cost_per_click_end: float | None = Field(
        None, description="Cost Per Click in dollars at end period"
    )
    start_period: str | None = Field(
        None, description="Starting period label (e.g., 'Aug', 'Week 1')"
    )
    end_period: str | None = Field(
        None, description="Ending period label (e.g., 'Oct', 'Week 4')"
    )
    one_line_summary: Annotated[str, Field(max_length=68)] | None = Field(
        None, description="Summary of Google Ads performance (max 68 characters)"
    )


class GoogleVisibilitySection(BaseModel):
    """Google Visibility metrics (shown when Google Ads data is not available)"""

    metric_1_name: str | None = Field(
        None,
        description="Name of first Google metric (e.g., 'Search Impressions', 'Map Impressions')",
    )
    metric_1_start: int | None = Field(
        None, description="First metric value at start period"
    )
    metric_1_end: int | None = Field(
        None, description="First metric value at end period"
    )
    metric_2_name: str | None = Field(
        None,
        description="Name of second Google metric (e.g., 'Site Clicks', 'Call Clicks')",
    )
    metric_2_start: int | None = Field(
        None, description="Second metric value at start period"
    )
    metric_2_end: int | None = Field(
        None, description="Second metric value at end period"
    )
    start_period: str | None = Field(
        None, description="Starting period label (e.g., 'Aug', 'Week 1')"
    )
    end_period: str | None = Field(
        None, description="Ending period label (e.g., 'Oct', 'Week 4')"
    )
    one_line_summary: Annotated[str, Field(max_length=68)] | None = Field(
        None, description="Summary of Google Visibility performance (max 68 characters)"
    )


class PerformanceOverviewReport(BaseModel):
    """Complete performance overview report with all platform sections"""

    facebook: FacebookSection = Field(
        ..., description="Facebook posts and impressions statistics"
    )
    instagram: InstagramSection = Field(
        ..., description="Instagram posts and impressions statistics"
    )
    facebook_ads: FacebookAdsSection | None = Field(
        None, description="Facebook Ads (Post Creatives) performance metrics"
    )
    google_ads: GoogleAdsSection | None = Field(
        None,
        description="Google Ads performance metrics. Use this if Google Ads data is available.",
    )
    google_visibility: GoogleVisibilitySection | None = Field(
        None,
        description="Google Visibility metrics. Use this if Google Ads data is NOT available.",
    )
    what_does_it_mean: Annotated[str, Field(max_length=235)] = Field(
        ...,
        description="Summary of overall slide content in one or two lines (max 235 characters)",
    )

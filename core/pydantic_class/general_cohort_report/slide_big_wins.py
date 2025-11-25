from typing import Annotated
from pydantic import BaseModel, Field


class PostStats(BaseModel):
    """Statistics for posts showing start and end values"""

    start_value: int = Field(..., description="Number of posts in the starting period")
    end_value: int = Field(..., description="Number of posts in the ending period")
    start_period: str = Field(
        ..., description="Starting period label (e.g., 'Sep', 'Week 1')"
    )
    end_period: str = Field(
        ..., description="Ending period label (e.g., 'Oct', 'Week 4')"
    )


class ImpressionStats(BaseModel):
    """Statistics for impressions showing start and end values"""

    start_value: int = Field(
        ..., description="Number of impressions in the starting period"
    )
    end_value: int = Field(
        ..., description="Number of impressions in the ending period"
    )
    start_period: str = Field(
        ..., description="Starting period label (e.g., 'Sep', 'Week 1')"
    )
    end_period: str = Field(
        ..., description="Ending period label (e.g., 'Oct', 'Week 4')"
    )


class FacebookBigWins(BaseModel):
    """Facebook big wins - posts, impressions, and summary"""

    posts: PostStats | None = Field(
        None, description="Facebook posts statistics from start to end period"
    )
    impressions: ImpressionStats | None = Field(
        None, description="Facebook impressions statistics from start to end period"
    )
    one_line_summary: Annotated[str, Field(max_length=94)] | None = Field(
        None,
        description="One-line summary of Facebook posts and impressions trend showing growth or positive performance (max 94 characters)",
    )


class InstagramBigWins(BaseModel):
    """Instagram big wins - posts, impressions, and summary"""

    posts: PostStats | None = Field(
        None, description="Instagram posts statistics from start to end period"
    )
    impressions: ImpressionStats | None = Field(
        None, description="Instagram impressions statistics from start to end period"
    )
    one_line_summary: Annotated[str, Field(max_length=94)] | None = Field(
        None,
        description="One-line summary of Instagram posts and impressions trend showing growth or positive performance (max 94 characters)",
    )


class FacebookAdsPerformance(BaseModel):
    """Facebook Ads performance metrics highlighting wins"""

    click_through_rate_start: float | None = Field(
        None, description="Click Through Rate percentage at start period (e.g., 15.35)"
    )
    click_through_rate_end: float | None = Field(
        None, description="Click Through Rate percentage at end period (e.g., 20.03)"
    )
    cost_per_click_start: float | None = Field(
        None, description="Cost Per Click in dollars at start period (e.g., 0.13)"
    )
    cost_per_click_end: float | None = Field(
        None, description="Cost Per Click in dollars at end period (e.g., 0.03)"
    )
    start_period: str | None = Field(
        None, description="Starting period label (e.g., 'Sep', 'Week 1')"
    )
    end_period: str | None = Field(
        None, description="Ending period label (e.g., 'Oct', 'Week 4')"
    )
    one_line_summary: Annotated[str, Field(max_length=94)] | None = Field(
        None,
        description="One-line summary describing Facebook Ads growth and efficiency (max 94 characters)",
    )


class GoogleAdsPerformance(BaseModel):
    """Google Ads performance metrics highlighting wins"""

    click_through_rate_start: float | None = Field(
        None, description="Click Through Rate percentage at start period"
    )
    click_through_rate_end: float | None = Field(
        None, description="Click Through Rate percentage at end period"
    )
    cost_per_mille_start: float | None = Field(
        None, description="Cost Per Mille (CPM) in dollars at start period"
    )
    cost_per_mille_end: float | None = Field(
        None, description="Cost Per Mille (CPM) in dollars at end period"
    )
    start_period: str | None = Field(
        None, description="Starting period label (e.g., 'Sep', 'Week 1')"
    )
    end_period: str | None = Field(
        None, description="Ending period label (e.g., 'Oct', 'Week 4')"
    )
    one_line_summary: Annotated[str, Field(max_length=94)] | None = Field(
        None,
        description="One-line summary describing Google Ads growth and performance (max 94 characters)",
    )


class GoogleSiteClicksPerformance(BaseModel):
    """Google site clicks and search/map impressions performance (used when Google Ads not present)"""

    site_clicks_start: int | None = Field(
        None, description="Google site clicks at start period"
    )
    site_clicks_end: int | None = Field(
        None, description="Google site clicks at end period"
    )
    search_impressions_start: int | None = Field(
        None, description="Google search impressions at start period (optional)"
    )
    search_impressions_end: int | None = Field(
        None, description="Google search impressions at end period (optional)"
    )
    map_impressions_start: int | None = Field(
        None, description="Google map impressions at start period (optional)"
    )
    map_impressions_end: int | None = Field(
        None, description="Google map impressions at end period (optional)"
    )
    start_period: str | None = Field(
        None, description="Starting period label (e.g., 'Sep', 'Week 1')"
    )
    end_period: str | None = Field(
        None, description="Ending period label (e.g., 'Oct', 'Week 4')"
    )
    one_line_summary: Annotated[str, Field(max_length=94)] | None = Field(
        None,
        description="One-line summary describing Google site clicks and impressions growth (max 94 characters)",
    )


class BigWinsReport(BaseModel):
    """Complete big wins report highlighting positive performance across platforms"""

    facebook: FacebookBigWins | None = Field(
        None,
        description="Facebook big wins showing posts, impressions growth, and summary",
    )
    instagram: InstagramBigWins | None = Field(
        None,
        description="Instagram big wins showing posts, impressions growth, and summary",
    )
    facebook_ads: FacebookAdsPerformance | None = Field(
        None,
        description="Facebook Ads performance highlighting CTR, CPC improvements and growth",
    )
    google_ads: GoogleAdsPerformance | None = Field(
        None,
        description="Google Ads performance with CTR, CPM. Use this if Google Ads data is available.",
    )
    google_site_clicks: GoogleSiteClicksPerformance | None = Field(
        None,
        description="Google site clicks and impressions. Use this ONLY if Google Ads data is NOT available.",
    )
    what_does_it_mean: Annotated[str, Field(max_length=235)] = Field(
        ...,
        description="2-line footer note summarizing the overall big wins in simple English (max 235 characters)",
    )

from pydantic import BaseModel, Field
from typing import Literal


class TimeSeriesValue(BaseModel):
    period_type: Literal["week", "month", "year"] = Field(
        ..., description="Type of time period (week, month, or year)."
    )
    period_label: str = Field(
        ..., description="Label for the period (e.g., 'Aug 2025', 'Week 1', 'Q1 2025')."
    )
    value: str | None = Field(None, description="The metric value for this period.")


class TimeSeriesStats(BaseModel):
    periods: list[TimeSeriesValue] = Field(
        ..., description="List of time periods with their values."
    )


class BusinessInfo(BaseModel):
    business_name: str | None = Field(None, description="Official business name.")
    business_url: str | None = Field(None, description="Website URL of the business.")
    facebook: str | None = Field(None, description="Facebook page URL.")
    instagram: str | None = Field(None, description="Instagram profile URL.")


class SocialStats(BaseModel):
    facebook_posts: TimeSeriesStats = Field(
        ..., description="Facebook posts per period."
    )
    facebook_impressions: TimeSeriesStats = Field(
        ..., description="Facebook impressions."
    )
    facebook_likes: TimeSeriesStats = Field(..., description="Facebook likes.")
    instagram_posts: TimeSeriesStats = Field(
        ..., description="Instagram posts per period."
    )
    instagram_impressions: TimeSeriesStats = Field(
        ..., description="Instagram impressions."
    )
    instagram_followers: TimeSeriesStats = Field(
        ..., description="Instagram followers."
    )
    facebook_ads: TimeSeriesStats = Field(
        ..., description="Facebook ads run per period."
    )
    facebook_ads_clicks: TimeSeriesStats = Field(
        ..., description="Clicks from Facebook ads."
    )
    facebook_ads_ctr: TimeSeriesStats = Field(..., description="CTR for Facebook ads.")
    facebook_ads_cpc: TimeSeriesStats = Field(..., description="CPC for Facebook ads.")
    google_search_impressions: TimeSeriesStats = Field(
        ..., description="Google search impressions."
    )
    google_map_impressions: TimeSeriesStats = Field(
        ..., description="Google Maps impressions."
    )
    google_site_clicks: TimeSeriesStats = Field(
        ..., description="Clicks to site from Google."
    )
    google_call_clicks: TimeSeriesStats = Field(
        ..., description="Clicks to call from Google."
    )
    google_ads: TimeSeriesStats = Field(..., description="Google Ads run per period.")
    google_ads_clicks: TimeSeriesStats = Field(
        ..., description="Clicks from Google Ads."
    )
    google_ads_cpm: TimeSeriesStats = Field(..., description="CPM for Google Ads.")
    google_ads_cpc: TimeSeriesStats = Field(..., description="CPC for Google Ads.")
    on_demand_post_requests: TimeSeriesStats = Field(
        ..., description="On-demand post requests."
    )
    ongoing_post_requests: TimeSeriesStats = Field(
        ..., description="Ongoing content requests."
    )


class DeliveryItem(BaseModel):
    social_post_type: str = Field(..., description="Type of social post delivered.")
    resolved: str | None = Field(
        None, description="ISO timestamp of delivery/resolution."
    )


class BusinessSnapshot(BaseModel):
    business_info: BusinessInfo = Field(..., description="Basic business information.")
    about_this_business: str | None = Field(
        None, description="High-level description of the business."
    )
    social_stats: SocialStats = Field(..., description="Performance metrics over time.")
    delivery_dates: list[DeliveryItem] = Field(
        ..., description="All delivery/resolution entries."
    )
    recent_post_content: list[str] | None = Field(
        None,
        description="List of recent social media post content strings with dates removed. Returns null if no post content is available.",
    )


class CategoryIdentification(BaseModel):
    category: str
    reason_selected: str


class AdsScore(BaseModel):
    score: int
    reason: str
    flag: int

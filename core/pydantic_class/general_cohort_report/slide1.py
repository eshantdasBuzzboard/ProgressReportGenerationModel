from pydantic import BaseModel, Field


class BusinessInfo(BaseModel):
    """Basic business information and social profiles."""

    business_name: str = Field(..., description="Official name of the business")
    website: str = Field(..., description="Business website URL")
    category: str = Field(..., description="Business category or industry type")
    address: str = Field(..., description="Physical address of the business")
    facebook: str = Field(..., description="Facebook page URL")
    instagram: str = Field(..., description="Instagram profile URL")


class MarketingReport(BaseModel):
    """Model for extracting high-level marketing report details."""

    report_title: str = Field(..., description="Title of the report")
    report_period: str = Field(..., description="Period covered by the report")
    business_info: BusinessInfo = Field(
        ..., description="Nested business information details"
    )

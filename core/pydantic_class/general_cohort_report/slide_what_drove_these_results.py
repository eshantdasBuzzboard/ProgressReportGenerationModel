from typing import Annotated
from pydantic import BaseModel, Field


class WhatDroveSection(BaseModel):
    section_title: Annotated[str, Field(max_length=22)] = Field(
        ...,
        description=(
            "Short heading for the driver explaining what influenced results "
            "(e.g., 'Consistent Posting', 'Stronger Reviews')"
        ),
    )
    bullet_1: Annotated[str, Field(max_length=78)] = Field(
        ...,
        description=(
            "First concise point explaining how this factor drove performance "
            "(max 78 characters)"
        ),
    )
    bullet_2: Annotated[str, Field(max_length=78)] = Field(
        ...,
        description=(
            "Second concise point adding detail on this driver (max 78 characters)"
        ),
    )


class WhatDroveTheseResultsReport(BaseModel):
    report_title: Annotated[str, Field(max_length=80)] = Field(
        default="What Drove These Results",
        description="Title for this section of the report",
    )
    sections: list[WhatDroveSection] = Field(
        ...,
        description="Exactly 3 sections, each describing a key driver of performance",
    )

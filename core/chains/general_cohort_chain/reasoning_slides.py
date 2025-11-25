from typing import Annotated, List
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import json

from core.prompts.general_cohort_prompts.reasoning_slides import (
    quick_action_prompt,
    closing_statement_prompt,
)

load_dotenv()


class QuickActionBullet(BaseModel):
    text: Annotated[str, Field(max_length=157)] = Field(
        ...,
        description=(
            "Single action-oriented bullet for the 'Quick Actions for You' slide. "
            "Must be <= 157 characters."
        ),
    )


class QuickActionsForYouSlide(BaseModel):
    title: str = Field(
        default="Quick Actions for You",
        description="Title of the slide/section.",
    )
    bullets: List[QuickActionBullet] = Field(
        ...,
        min_items=4,
        max_items=4,
        description=(
            "Exactly 4 action bullets telling the business what to share or "
            "what type of requests (Ad, On-Demand, Ongoing Post) to submit."
        ),
    )


class ClosingStatement(BaseModel):
    headline: Annotated[
        str,
        Field(
            ...,
            max_length=220,
            description=(
                "Main closing headline line. Must start with the brand name and "
                "summarize what the brand achieved this period."
            ),
        ),
    ]
    supporting_text: Annotated[
        str,
        Field(
            ...,
            max_length=500,
            description=(
                "Short supporting paragraph (1–2 sentences) that highlights a key "
                "achievement and emphasizes future growth potential."
            ),
        ),
    ]


llm = ChatOpenAI(
    temperature=0, model="gpt-5.1", reasoning_effort="medium", use_responses_api=True
)


async def quick_action_reasoning_chain(preprocessed_input, other_analysis):
    llmr = llm.with_structured_output(QuickActionsForYouSlide)
    achain = quick_action_prompt | llmr
    input_data = {
        "preprocessed_input": preprocessed_input,
        "other_analysis": other_analysis,
    }
    response = await achain.ainvoke(input_data)
    return json.loads(response.model_dump_json())


async def closing_statement_chain(preprocessed_input, other_analysis):
    llmr = llm.with_structured_output(ClosingStatement)
    achain = closing_statement_prompt | llmr
    input_data = {
        "preprocessed_input": preprocessed_input,
        "other_analysis": other_analysis,
    }
    response = await achain.ainvoke(input_data)
    return json.loads(response.model_dump_json())

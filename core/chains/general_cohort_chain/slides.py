from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import json

from core.prompts.general_cohort_prompts.slides import (
    business_info_extraction_prompt,
    heres_what_we_delivered_prompt,
    how_your_ads_performed_prompt,
    action_plan_prompt,
    areas_needing_attention_prompt,
    performance_summary_prompt,
    big_wins_prompt,
    growth_at_glance_prompt,
    what_drove_results_prompt,
)
from core.pydantic_class.general_cohort_report.slide1 import MarketingReport
from core.pydantic_class.general_cohort_report.slide_heres_what_we_delivered import (
    DeliverySegmentsReport,
)
from core.pydantic_class.general_cohort_report.slide_how_your_ads_performed import (
    AdsPerformanceReport,
)
from core.pydantic_class.general_cohort_report.slide_action_plan_next_month import (
    ActionPlanReport,
)
from core.pydantic_class.general_cohort_report.slide_area_that_needs_attention import (
    AreasNeedingAttentionReport,
)
from core.pydantic_class.general_cohort_report.slide_performence_summary import (
    PerformanceOverviewReport,
)
from core.pydantic_class.general_cohort_report.slide_big_wins import BigWinsReport
from core.pydantic_class.general_cohort_report.slide_growth_at_glance import (
    GrowthAtGlanceReport,
)
from core.pydantic_class.general_cohort_report.slide_what_drove_these_results import (
    WhatDroveTheseResultsReport,
)

load_dotenv()

llm = ChatOpenAI(model="gpt-4.1", temperature=0, use_responses_api=True, max_retries=3)


async def slide1_introduction_chain(ignite_payload, quicksight_data):
    llmr = llm.with_structured_output(MarketingReport)
    achain = business_info_extraction_prompt | llmr
    input_data = {
        "quicksight_data": quicksight_data,
        "ignite_payload": ignite_payload,
    }
    response = await achain.ainvoke(input_data)
    return json.loads(response.model_dump_json())


async def here_is_what_we_delivered_chain(zylo_v6_data):
    llmr = llm.with_structured_output(DeliverySegmentsReport)
    achain = heres_what_we_delivered_prompt | llmr
    input_data = {
        "zylo_v6_data": zylo_v6_data,
    }
    response = await achain.ainvoke(input_data)
    return json.loads(response.model_dump_json())


async def how_your_ads_performed_chain(quicksight_data):
    llmr = llm.with_structured_output(AdsPerformanceReport)
    achain = how_your_ads_performed_prompt | llmr
    input_data = {
        "quicksight_data": quicksight_data,
    }
    response = await achain.ainvoke(input_data)
    return json.loads(response.model_dump_json())


async def action_plan_next_month_chain(quicksight_data):
    llmr = llm.with_structured_output(ActionPlanReport)
    achain = action_plan_prompt | llmr
    input_data = {
        "quicksight_data": quicksight_data,
    }
    response = await achain.ainvoke(input_data)
    return json.loads(response.model_dump_json())


async def areas_needing_attention_chain(quicksight_data):
    llmr = llm.with_structured_output(AreasNeedingAttentionReport)
    achain = areas_needing_attention_prompt | llmr
    input_data = {
        "quicksight_data": quicksight_data,
    }
    response = await achain.ainvoke(input_data)
    return json.loads(response.model_dump_json())


async def performence_summary_chain(quicksight_data):
    llmr = llm.with_structured_output(PerformanceOverviewReport)
    achain = performance_summary_prompt | llmr
    input_data = {
        "quicksight_data": quicksight_data,
    }
    response = await achain.ainvoke(input_data)
    return json.loads(response.model_dump_json())


async def big_wins_chain(quicksight_data):
    llmr = llm.with_structured_output(BigWinsReport)
    achain = big_wins_prompt | llmr
    input_data = {
        "quicksight_data": quicksight_data,
    }
    response = await achain.ainvoke(input_data)
    return json.loads(response.model_dump_json())


async def growth_at_glance_chain(quicksight_data):
    llmr = llm.with_structured_output(GrowthAtGlanceReport)
    achain = growth_at_glance_prompt | llmr
    input_data = {
        "quicksight_data": quicksight_data,
    }
    response = await achain.ainvoke(input_data)
    return json.loads(response.model_dump_json())


async def what_drove_results_chain(quicksight_data, ignite_payload):
    llmr = llm.with_structured_output(WhatDroveTheseResultsReport)
    achain = what_drove_results_prompt | llmr
    input_data = {
        "quicksight_data": quicksight_data,
        "ignite_data": ignite_payload,
    }
    response = await achain.ainvoke(input_data)
    return json.loads(response.model_dump_json())

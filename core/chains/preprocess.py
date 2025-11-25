from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import json


from core.prompts.preprocess import (
    data_structuring_prompt,
    trend_analysis_prompt,
    ads_presence_prompt,
)
from core.pydantic_class.preprocess_structure import (
    BusinessSnapshot,
    CategoryIdentification,
    AdsScore,
)

load_dotenv()


llm = ChatOpenAI(model="gpt-4.1", temperature=0, use_responses_api=True, max_retries=3)


async def preprocess_chain(ignite_api_data, quick_sight_data, zylo_v6_data, msp_data):
    llmr = llm.with_structured_output(BusinessSnapshot)
    achain = data_structuring_prompt | llmr
    input_data = {
        "quicksight_data": quick_sight_data,
        "ignite_api_data": ignite_api_data,
        "zylo_v6_data": zylo_v6_data,
        "msp_data": msp_data,
    }
    response = await achain.ainvoke(input_data)
    return json.loads(response.model_dump_json())


async def category_chain(social_stats):
    llmr = llm.with_structured_output(CategoryIdentification)
    achain = trend_analysis_prompt | llmr
    input_data = {"social_stats": social_stats}
    response = await achain.ainvoke(input_data)
    return json.loads(response.model_dump_json())


async def ads_score_chain(quicksight_data):
    llmr = llm.with_structured_output(AdsScore)
    achain = ads_presence_prompt | llmr
    input_data = {"quicksight_data": quicksight_data}
    response = await achain.ainvoke(input_data)
    return json.loads(response.model_dump_json())

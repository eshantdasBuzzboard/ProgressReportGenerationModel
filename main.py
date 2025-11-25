import streamlit as st
import asyncio
from src.preprocess_data_for_report import return_preprocess_data, identify_cohort
from src.slide_mapping import run_slide_generation
from core.chains.preprocess import category_chain
from core.chains.general_cohort_chain.reasoning_slides import (
    quick_action_reasoning_chain,
    closing_statement_chain,
)


async def main():
    st.title("Data Input Interface")

    # Create three columns for side-by-side layout
    col1, col2, col3 = st.columns(3)

    with col1:
        quicksight_data = st.text_area(
            "QuickSight Data", height=400, placeholder="Enter QuickSight data here..."
        )

    with col2:
        zylov6_data = st.text_area(
            "Zylov6 Data", height=400, placeholder="Enter Zylov6 data here..."
        )

    with col3:
        ignite_payload_data = st.text_area(
            "Ignite Payload Data",
            height=400,
            placeholder="Enter Ignite Payload data here...",
        )
    msp_data = ""

    # Analyze Button
    if st.button("Analyse"):
        with st.spinner("Preprocessing your input"):
            new_response, social_stats = await return_preprocess_data(
                ignite_api_data=ignite_payload_data,
                quicksight_data_declining=quicksight_data,
                zylo_v6_data=zylov6_data,
            )
            if new_response:
                st.header("Preprocessed Input")
                st.json(new_response)
        with st.spinner("Analysing Uptrending or Downtrending Data"):
            category_task = category_chain(social_stats)
            cohort_task = identify_cohort(
                quicksight_data=quicksight_data,
                ignite_api_data=ignite_payload_data,
                zylo_v6_data=zylov6_data,
                social_stats=social_stats,
                msp_data=msp_data,
            )

            category, cohort = await asyncio.gather(category_task, cohort_task)
            if category:
                st.header("Category (Uptrend or Downtrend)")
                st.json(category)
                st.header("Cohort Number")
                st.text(cohort)
        with st.spinner("Report Generation Started"):
            response = await run_slide_generation(
                str(cohort),
                category["category"],
                ignite_payload_data,
                quicksight_data,
                zylov6_data,
                social_stats,
            )
            data = response
            st.header("Final report")
            for key, value in data.items():
                st.subheader(key.replace("_", " ").title())
                st.json(value)
        with st.spinner("Generating the final two slides with reasoning"):
            quick_action_response, closing_statement_response = await asyncio.gather(
                quick_action_reasoning_chain(
                    other_analysis=data, preprocessed_input=new_response
                ),
                closing_statement_chain(
                    other_analysis=data, preprocessed_input=new_response
                ),
            )
            st.subheader("QuickActionForYou")
            st.json(quick_action_response)
            st.subheader("Closing Statement")
            st.json(closing_statement_response)


if __name__ == "__main__":
    asyncio.run(main())

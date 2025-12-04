import streamlit as st
import asyncio
import logging
import json
from datetime import datetime
from pathlib import Path
from constants import guidelines
from src.preprocess_data_for_report import return_preprocess_data, identify_cohort
from src.slide_mapping import run_slide_generation
from core.chains.preprocess import category_chain
from core.chains.general_cohort_chain.reasoning_slides import (
    quick_action_reasoning_chain,
    closing_statement_chain,
)
from core.chains.guidelines_chain import return_updated_report_checking_guidelines

# Configure logging
LOG_DIR = Path("logs")
OUTPUT_DIR = Path("outputs")
LOG_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Setup logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / f"app_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def save_json_response(data, filename_prefix):
    """Save JSON response to a file with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = OUTPUT_DIR / f"{filename_prefix}_{timestamp}.json"

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Successfully saved {filename_prefix} to {filename}")
        return filename
    except Exception as e:
        logger.error(f"Error saving {filename_prefix}: {str(e)}")
        return None


def merge_final_report(final_report, quick_action_response, closing_statement_response):
    """Merge final report with quick action and closing statement"""
    merged_report = final_report.copy()

    # Add quick_action_for_you section
    merged_report["quick_action_for_you"] = quick_action_response.get(
        "quick_action", quick_action_response
    )

    # Add closing_statement section
    merged_report["closing_statement"] = closing_statement_response.get(
        "closing_statement", closing_statement_response
    )

    return merged_report


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
        logger.info("Analysis started")

        # Variables to store intermediate results
        new_response = None
        social_stats = None
        category = None
        cohort = None
        data = None
        quick_action_response = None
        closing_statement_response = None
        complete_report = None

        with st.spinner("Preprocessing Input"):
            # Preprocessing
            new_response, social_stats = await return_preprocess_data(
                ignite_api_data=ignite_payload_data,
                quicksight_data_declining=quicksight_data,
                zylo_v6_data=zylov6_data,
            )
            logger.info("Preprocessing completed successfully")

        with st.spinner("Identifying Cohort and Uptrend or Downtrend"):
            # Category and Cohort Analysis
            category_task = category_chain(social_stats)
            cohort_task = identify_cohort(
                quicksight_data=quicksight_data,
                ignite_api_data=ignite_payload_data,
                zylo_v6_data=zylov6_data,
                social_stats=social_stats,
                msp_data=msp_data,
            )

            category, cohort = await asyncio.gather(category_task, cohort_task)
            logger.info(f"Category: {category['category']}, Cohort: {cohort}")
        with st.expander("📊 Preprocessed Input", expanded=False):
            if new_response:
                st.json(new_response)
                # Collapsible section for Category and Cohort
        with st.expander("📈 Category & Cohort Analysis", expanded=False):
            if category:
                st.subheader("Category (Uptrend or Downtrend)")
                st.json(category)
            if cohort:
                st.subheader("Cohort Number")
                st.text(cohort)

        with st.spinner("Generating the Generic slides"):
            # Report Generation
            response = await run_slide_generation(
                str(cohort),
                category["category"],
                ignite_payload_data,
                quicksight_data,
                zylov6_data,
                social_stats,
            )
            data = response
            logger.info("Report generation completed successfully")

        with st.spinner("Generating the final slides with reasoning"):
            # Final slides generation
            (
                quick_action_response,
                closing_statement_response,
            ) = await asyncio.gather(
                quick_action_reasoning_chain(
                    other_analysis=data, preprocessed_input=new_response
                ),
                closing_statement_chain(
                    other_analysis=data, preprocessed_input=new_response
                ),
            )

            # Merge final report
            complete_report_without_checking_guidelines = merge_final_report(
                data, quick_action_response, closing_statement_response
            )

            logger.info("Analysis completed successfully")
        with st.expander("📈 Report before checking guidelines", expanded=False):
            if complete_report_without_checking_guidelines:
                st.json(complete_report_without_checking_guidelines)
        with st.spinner(
            "Checking Guidlines and returning the final report with reasoning"
        ):
            complete_report = await return_updated_report_checking_guidelines(
                complete_report_without_checking_guidelines, guidelines=guidelines
            )

        # Display results with collapsible sections
        st.success("✅ Analysis completed successfully!")

        # Display Complete Merged Report (expanded by default)
        st.header("📋 Complete Report")
        if complete_report:
            st.json(complete_report)


if __name__ == "__main__":
    asyncio.run(main())

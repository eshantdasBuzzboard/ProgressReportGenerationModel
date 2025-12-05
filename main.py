import streamlit as st
import asyncio
import logging
import json
import pandas as pd  # Added pandas for the table display
from datetime import datetime
from pathlib import Path
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


guidelines = {
    "fulfillment_workflow": {
        "description": "Customer actions and corresponding fulfillment responses",
        "categories": {
            "on_demand_content": {
                "boosted_post": {
                    "customer_action": "Submit Boosted On-Demand Post request (FB/IG only, $5 one-time boost)",
                    "action_type": "On-Demand Post Request",
                    "fulfillment_action": "Publishes post and applies boost",
                },
                "non_boosted_post": {
                    "customer_action": "Submit On-Demand Post Request (non-boosted) for promotions, seasonal content, or new visuals",
                    "action_type": "On-Demand Post Request",
                    "fulfillment_action": "Creates posts immediately with provided inputs",
                },
                "testimonials_reviews": {
                    "customer_action": "Submit testimonials/reviews via On-Demand Post Request",
                    "action_type": "On-Demand Post Request",
                    "fulfillment_action": "Creates new testimonial/review posts immediately",
                },
                "visual_assets": {
                    "customer_action": "Submit visual assets (before/after, event photos) via On-Demand Post Request",
                    "action_type": "On-Demand Post Request",
                    "fulfillment_action": "Creates new posts using submitted assets",
                },
            },
            "ads_monthly_campaigns": {
                "facebook_ads_edit": {
                    "customer_action": "Submit edit on paused Facebook Ads (Meta Ads)",
                    "action_type": "Edit",
                    "fulfillment_action": "Updates details if needed and resumes $50/month campaign",
                },
                "google_ads_edit": {
                    "customer_action": "Submit edit on paused Google Ads",
                    "action_type": "Edit",
                    "fulfillment_action": "Updates details if needed and resumes $50/month campaign",
                },
                "budget_reallocation": {
                    "customer_action": "Submit separate edits for budget reallocation (Google / Meta Ads)",
                    "action_type": "Edit",
                    "fulfillment_action": "Adjusts budgets and resumes $50/month campaigns",
                },
            },
            "scheduled_posts": {
                "approve_with_approvals": {
                    "customer_action": "Approve/request edits on scheduled posts (if on approvals)",
                    "action_type": "Edit",
                    "fulfillment_action": "Updates and publishes approved content",
                },
                "review_without_approvals": {
                    "customer_action": "Review scheduled posts & request edits (if not on approvals)",
                    "action_type": "Edit",
                    "fulfillment_action": "Updates content before publishing",
                },
            },
            "other_inputs": {
                "media_library_upload": {
                    "customer_action": "Upload visual assets to Media Library",
                    "action_type": "Upload",
                    "fulfillment_action": "Stores assets for use in future Ongoing Content",
                },
                "testimonials_to_specialist": {
                    "customer_action": "Send testimonials/reviews to Marketing Specialist",
                    "action_type": "Specialist",
                    "fulfillment_action": "Logged as Content Feedback (Brand Guide edit) → used in future Ongoing Content",
                },
                "brand_inputs_to_specialist": {
                    "customer_action": "Send brand inputs/testimonials to Marketing Specialist",
                    "action_type": "Specialist",
                    "fulfillment_action": "Added as Content Feedback → guides future content creation",
                },
            },
        },
        "legend": {
            "on_demand_post_request": "Immediate new posts (promotions, testimonials, visuals)",
            "boosted_on_demand_post": "FB/IG only, $5 one-time boost",
            "meta_ads": "$50/month campaigns, only updated if edits submitted",
            "google_ads": "$50/month campaigns, only updated if edits submitted",
            "edit": "Changes to scheduled posts or Ads (resume, update, budget reallocation)",
            "upload": "Add assets to Media Library for future content",
            "specialist": "Inputs to Marketing Specialist (logged as Content Feedback / Brand Guide edits)",
        },
    },
    "content_guidelines": {
        "terminology": {
            "do": "Separate Ads (Google/Meta) vs. Posts (Ongoing/On-Demand). Use clear phrasing: 'Request edits for ad creatives → Fulfillment will update visuals.'",
            "dont": "Use vague terms like 'Approve September Ad Creatives' or 'Boost this post.'",
        },
        "ad_status_clarity": {
            "do": "If paused → 'No active ads this month; only On-Demand boosted posts were run.' If reactivating → 'To relaunch Google Ads, confirm budget → Fulfillment will restart.'",
            "dont": "Do not leave ad status unclear.",
        },
        "boosting_workflow": {
            "do": "Always: 'Submit an On-Demand request to recreate and boost this post.'",
            "dont": "Suggest DIY boosts with dollar amounts (e.g., $50–100).",
        },
        "scope_alignment": {
            "do": "Video → 'Fulfillment cannot create video. You may record clips.' A/B → 'Request two ad variations via OD → Fulfillment will test.'",
            "dont": "Do not recommend reels, videos, or clips directly.",
        },
        "action_item_phrasing": {
            "do": "Make every action Customer instruction → Fulfillment task. Example: 'Request edits → Fulfillment updates ad visuals and copy.'",
            "dont": "Avoid unclear or one-sided phrasing (e.g., 'Update ads').",
        },
        "content_and_language": {
            "do": "Use full forms (CTR = Click Through Rate, CPC = Cost Per Click). Keep text plain English with direct instructions. Links: Instagram, Facebook, Business site only.",
            "dont": "Do not include contact info, reels/video suggestions, or create reports for declining stats businesses.",
        },
        "data_and_metrics": {
            "do": "Use Zylo + Quicksight from the same timeframe (weekly if possible). Show 0 (not '–'). Round to 1 decimal point. Use ↑ ↓ arrows. Show Ads posts separately. Prefer Zylo posts if available.",
            "dont": "Do not mismatch Zylo/Quicksight dates. Do not leave blanks or inconsistent metric formatting.",
        },
        "footer_notes": {
            "do": "Add insightful, performance-related notes at footer. Tie to context (e.g., 'Content consistency built strong engagement').",
            "dont": "Avoid generic/filler notes.",
        },
    },
    "validation_checklist": {
        "terminology_consistency": [
            "Did I clearly distinguish Ads (paid) vs Posts (Ongoing/On-Demand)?",
            "Did I avoid ambiguous terms like 'Approve September Ad Creatives'?",
            "Did I phrase boosting correctly ('Submit an On-Demand request to recreate and boost')?",
            "Did I use consistent terms: On-Demand Post, Ongoing Social Media Post, Facebook Ad, Google Ad?",
        ],
        "ad_status_clarity": [
            "If Google/Meta Ads are paused, did I explicitly state 'No active ads this month; only On-Demand boosted posts were run'?",
            "If reactivation is suggested, did I phrase it as: 'Confirm budget → Fulfillment will restart campaigns'?",
        ],
        "boosting_workflow": [
            "Did I avoid DIY-style boost suggestions (e.g., 'Spend $50–100 boosting this')?",
            "Did I always link boosting to an OD request?",
        ],
        "scope_alignment": [
            "Did I avoid recommending reels/videos outright?",
            "If video was mentioned, did I include the disclaimer ('Fulfillment cannot create video; you may record clips')?",
            "Did I phrase A/B testing correctly as OD variations?",
        ],
        "action_item_phrasing": [
            "Are all Quick Actions phrased as clear customer instruction + fulfillment action?",
            "Do all action items map directly to something Fulfillment can deliver?",
        ],
        "positive_structure": [
            "Did I keep Ongoing vs On-Demand separation?",
            "Did I highlight fulfillment-created content (not only customer-sent)?",
            "Did I follow the structure: Big Wins → How Ads Performed → What's Coming → Quick Actions?",
        ],
        "content_and_language": [
            "Did I expand acronyms (CTR = Click Through Rate, CPC = Cost Per Click)?",
            "Did I keep text in plain, simple English with direct instructions?",
            "Did I use 'scheduled posts' (not 're-scheduled')?",
            "Did I exclude contact info (only Instagram, Facebook, Business links allowed)?",
            "Did I exclude reports for businesses with declining stats?",
        ],
        "data_and_metrics": [
            "Are Zylo data dates aligned with Quicksight stats (same timeframe, weekly preferred)?",
            "Did I show 0 where metrics are empty (not '–')?",
            "Did I round decimals to 1 decimal point?",
            "Did I apply ↑/↓ arrows correctly with performance changes?",
            "Did I display Ads posts separately if ads were run?",
            "Did I prefer Zylo posts if present?",
        ],
        "footer_notes": [
            "Is the footer summary related and insightful (not filler)?",
            "Did I add Google Review data if MSP report is present?",
        ],
    },
    "validation_example": {
        "incorrect_draft": [
            "Approve September Ad Creatives",
            "Confirm willingness to boost with $50–100",
        ],
        "validation_result": [
            "❌ Fails terminology consistency",
            "❌ Fails boosting workflow",
        ],
        "corrected_output": [
            "Request edits for ad creatives → Fulfillment will update visuals, messaging, and ad copy.",
            "Submit an On-Demand request to recreate and boost this post.",
        ],
    },
}


DEFAULT_QUICKSIGHT_DATA = """
| Metric                       | Oct 2025 | Nov 2025 |
|-----------------------------|----------|----------|
| Facebook Posts              | 4        | 4        |
| Facebook Impressions        | 11       | 24       |
| Facebook Likes              | 0        | 1        |
| Facebook Site Clicks        | 0        | 0        |
| Facebook Direction Clicks   | 0        | 0        |
| Facebook Phone Clicks       | 0        | 0        |
| Instagram Posts             | 2        | 4        |
| Instagram Impressions       | 48       | 160      |
| Instagram Site Clicks       | 0        | 0        |
| Instagram Direction Clicks  | 0        | 0        |
| Instagram Phone Clicks      | 0        | 0        |
| Instagram Followers         | 0        | 0        |
| Facebook Ads                | –        | 1        |
| Facebook Ads Clicks         | –        | 59       |
| Facebook Ads CTR           | –        | 1.25     |
| Facebook Ads CPC           | –        | 0.33     |
| Google Search Impressions   | 151      | 404      |
| Google Map Impressions      | 11       | 25       |
| Google Site Clicks          | 10       | 24       |
| Google Call Clicks          | 5        | 4        |
| Google Ads                  | 1        | –        |
| Google Ads Clicks           | 165      | –        |
| Google Ads CPM              | 4.62     | –        |
| Google Ads CPC              | 0.2      | –        |

"""

DEFAULT_ZYLOV6_DATA = """
Delivery Details 

| Post Type                  | Date       |
|---------------------------|------------|
| Ongoing                  | 2025-11-28 |
| On-Demand Social Posts   | 2025-11-27 |
| On-Demand Social Posts   | 2025-11-26 |
| On-Demand Social Posts   | 2025-11-24 |
| On-Demand Social Posts   | 2025-11-21 |
| On-Demand Social Posts   | 2025-11-20 |
| On-Demand Social Posts   | 2025-11-12 |
| Ongoing Posts            | 2025-11-12 |
| On-Demand Social Posts   | 2025-11-11 |
| Ongoing Posts            | 2025-11-10 |
| Ongoing Posts            | 2025-11-10 |
| Ongoing Posts            | 2025-11-10 |
| Ongoing Posts            | 2025-11-10 |
| On-Demand Social Posts   | 2025-11-10 |
| Ongoing Posts            | 2025-11-10 |
| Ongoing Posts            | 2025-11-09 |
| Ongoing Posts            | 2025-11-09 |
| Ongoing Posts            | 2025-11-09 |
| On-Demand Social Posts   | 2025-11-06 |
| On-Demand Social Posts   | 2025-11-05 |
| On-Demand Social Posts   | 2025-11-05 |
| On-Demand Social Posts   | 2025-11-05 |
| On-Demand Social Posts   | 2025-11-05 |
| On-Demand Social Posts   | 2025-11-05 |
| On-Demand Social Posts   | 2025-11-05 |
| On-Demand Social Posts   | 2025-11-05 |
| On-Demand Social Posts   | 2025-11-05 |
| On-Demand Social Posts   | 2025-11-05 |
| Ongoing                  | 2025-11-05 |
| Ongoing                  | 2025-11-05 |
| On-Demand Social Posts   | 2025-11-04 |
| On-Demand Social Posts   | 2025-11-04 |
| On-Demand Social Posts   | 2025-11-03 |
| On-Demand Social Posts   | 2025-11-03 |
| Ongoing Posts            | 2025-10-28 |
| On-Demand Social Posts   | 2025-10-23 |
| On-Demand Social Posts   | 2025-10-23 |
| Ongoing Social Posts     | 2025-10-23 |
| Ongoing Social Posts     | 2025-10-23 |
| Ongoing Social Posts     | 2025-10-23 |
| Ongoing Social Posts     | 2025-10-23 |
| Ongoing Social Posts     | 2025-10-09 |
| On-Demand Social Posts   | 2025-10-09 |
| On-Demand Social Posts   | 2025-10-09 |
| On-Demand Social Posts   | 2025-10-09 |
| On-Demand Social Posts   | 2025-10-09 |
| Ongoing Social Posts     | 2025-10-08 |
| Ongoing Social Posts     | 2025-10-08 |
| Ongoing Social Posts     | 2025-10-06 |
| On-Demand Social Posts   | 2025-09-29 |
| On-Demand Social Posts   | 2025-09-29 |
| On-Demand Social Posts   | 2025-09-29 |
| On-Demand Social Posts   | 2025-09-29 |
| Ongoing Posts            | 2025-09-19 |
| Ongoing Posts            | 2025-09-19 |
| Ongoing Posts            | 2025-09-19 |
| On-Demand Social Posts   | 2025-09-19 |
| Ongoing Posts            | 2025-09-19 |
| Ongoing Posts            | 2025-09-19 |
| Ongoing Posts            | 2025-09-19 |
| Ongoing Posts            | 2025-09-19 |
| Ongoing Posts            | 2025-09-19 |
| On-Demand Social Posts   | 2025-09-16 |
| Ongoing Posts            | 2025-09-15 |
| On-Demand Social Posts   | 2025-09-05 |
| On-Demand Social Posts   | 2025-09-05 |
| On-Demand Social Posts   | 2025-09-05 |
| Facebook Ads            | 2025-11-20 |
| Facebook Ads            | 2025-08-29 |
| Facebook Ads            | 2025-08-28 |


"""

DEFAULT_ZYLOV6_CONTENT = """
November 20 at 6:30 PM - "Comfort and dignity return to daily life when care is shaped around personal needs. Our in-home nursing and caregiver support brings trust and gentle guidance to your f..." (with image of text)


November 17 at 2:30 PM - "Flexible home care is possible with our transparent pricing starting at $27 per hour. We help families plan confidently, regardless of insurance. Let's talk about how w..." (with hospital image)


November 10 at 3:30 PM - "Baltimore families receive care shaped by local knowledge and deep community roots. Our team understands your needs and traditions, offering support that feels truly fa..." (with image of healthcare team)


November 4 at 5:30 PM - "Personal care journals keep routines and preferences clear for everyone involved. We use these tools to support independence and comfort. Ask us how care journals can h..." (with diary/studying image)


November 2 - "West Pointe Healthcare, LLC is at Baltimore City." - "Druid Heights Community Health Fair. 10.25.2025" (with multiple photos from the health fair event)


November 1 - "West Pointe Healthcare, LLC updated their cover photo" (profile update post)


November 1 - "West Pointe Healthcare, LLC updated their profile picture." (profile update post with "WEST POINTE HEALTHCARE" text graphic)


October 28 - "Call today for a bed or a private room! At Pointe to Wellness, Inc., we believe everyone deserves a safe and supportive place to rebuild. Whether you're experiencing ha..." (transitional housing post)


October 24 - "Join Us Tomorrow" - Druid Heights Community Health Fair announcement with event details (Saturday, October 25th, Unity Hall 1505 Eutaw Place, 1pm-3pm, with information about free health screenings)


September 14 - "Now Hiring Part Time Psych NP: Telemedicine" (recruitment post)
"""

DEFAULT_IGNITE_PAYLOAD = """

Business Name -
 West Pointe Healthcare, LLC
Business URL -
 https://www.westpointehealthcarestaffing.com

Instagram -
 https://instagram.com/westpointehealthcarewestpointehealthcarestaffing​
Facebook -
 https://m.facebook.com/West-Pointe-Healthcare-LLC-113112768279549/westpointehealthcarestaffing​
About business
West Pointe Healthcare is an independent healthcare company that provides staffing and home care services to both public and private sector clients, including clinics, care homes, hospitals, assisted living facilities, and individuals needing in‑home care. The company focuses on simplifying healthcare staffing and delivering premier home care through its Healthcare Staffing and Residential Services Agency offerings from its office in Owings Mills, Maryland.

"""


def calculate_char_counts(data, path=""):
    """
    Recursive function to traverse a nested dictionary/list.
    Returns a list of dicts containing the path, counts, and preview.
    """
    report = []

    # Handle Dictionary
    if isinstance(data, dict):
        for key, value in data.items():
            # Create a breadcrumb path (e.g., intro_slide.business_info.name)
            new_path = f"{path}.{key}" if path else key
            report.extend(calculate_char_counts(value, new_path))

    # Handle List
    elif isinstance(data, list):
        for index, item in enumerate(data):
            # Create path with index (e.g., timeline_events[0])
            new_path = f"{path}[{index}]"
            report.extend(calculate_char_counts(item, new_path))

    # Handle String (The actual content we want to count)
    elif isinstance(data, str):
        # We generally don't count empty strings or purely whitespace strings as 'content'
        if data.strip():
            count_with_spaces = len(data)
            count_no_spaces = len(data.replace(" ", ""))

            # Create a preview (truncate if too long)
            preview = (data[:75] + "...") if len(data) > 75 else data

            report.append({
                "Section": path,
                "With Spaces": count_with_spaces,
                "No Spaces": count_no_spaces,
                "Content": preview,
            })

    return report


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
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        quicksight_data = st.text_area(
            "QuickSight Data",
            value=DEFAULT_QUICKSIGHT_DATA,
            height=400,
            placeholder="Enter QuickSight data here...",
        )

    with col2:
        zylov6_data = st.text_area(
            "Zylov6 Data",
            value=DEFAULT_ZYLOV6_DATA,
            height=400,
            placeholder="Enter Zylov6 data here...",
        )
    with col3:
        zylov6_post_content = st.text_area(
            "Zylov6 Content Data",
            value=DEFAULT_ZYLOV6_CONTENT,
            height=400,
            placeholder="Enter Zylov6_post_content data here...",
        )

    with col4:
        ignite_payload_data = st.text_area(
            "Ignite Payload Data",
            value=DEFAULT_IGNITE_PAYLOAD,
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
                zylo_v6_post_content=zylov6_post_content,
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
                new_response.get("delivery_dates"),
                new_response.get("recent_post_content"),
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
            "Checking Guidelines and returning the final report with reasoning"
        ):
            complete_report = await return_updated_report_checking_guidelines(
                complete_report_without_checking_guidelines, guidelines=guidelines
            )

        # Display results with collapsible sections
        st.success("✅ Analysis completed successfully!")

        # Display Complete Merged Report
        st.header("📋 Complete Report")
        if complete_report:
            st.json(complete_report)

        # ------------------------------------------------------------------
        # NEW SECTION: Character Count Analysis
        # ------------------------------------------------------------------
        with st.expander("📏 Character Count Analysis", expanded=False):
            if complete_report:
                # 1. Calculate the counts
                char_data = calculate_char_counts(complete_report)

                # 2. Create DataFrame
                df_chars = pd.DataFrame(char_data)

                # 3. Display interactive table
                if not df_chars.empty:
                    st.dataframe(
                        df_chars,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Section": st.column_config.TextColumn(
                                "Section Key", width="medium"
                            ),
                            "With Spaces": st.column_config.NumberColumn(
                                "Chars (with spaces)", format="%d"
                            ),
                            "No Spaces": st.column_config.NumberColumn(
                                "Chars (no spaces)", format="%d"
                            ),
                            "Content": st.column_config.TextColumn(
                                "Content Preview", width="large"
                            ),
                        },
                    )
                else:
                    st.info("No text content found to analyze.")
            else:
                st.warning("Report generation failed, no data to count.")


if __name__ == "__main__":
    asyncio.run(main())

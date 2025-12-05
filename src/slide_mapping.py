import asyncio
from typing import List, Dict, Any
from core.chains.general_cohort_chain.slides import (
    slide1_introduction_chain,
    here_is_what_we_delivered_chain,
    how_your_ads_performed_chain,
    action_plan_next_month_chain,
    performence_summary_chain,
    areas_needing_attention_chain,
    big_wins_chain,
    growth_at_glance_chain,
    what_drove_results_chain,
)


def get_slide_functions(cohort: str, exact_category: str) -> List[Dict[str, Any]]:
    """
    Returns a list of slide function configurations based on cohort and category.
    """

    # Define the config for the delivery slide
    # The 'requires' keys MUST match the arguments in 'here_is_what_we_delivered_chain'
    delivery_slide_config = {
        "name": "here_is_what_we_delivered",
        "func": here_is_what_we_delivered_chain,
        "requires": ["zylo_v6_data_json", "zylo_v6_post_content"],
    }

    # ---------------------------------------------------------
    # COHORT 8
    # ---------------------------------------------------------
    if cohort == "8":
        return [
            {
                "name": "intro_slide",
                "func": slide1_introduction_chain,
                "requires": ["ignite_payload", "quicksight_data"],
            },
            delivery_slide_config,
            {
                "name": "action_plan_next_month",
                "func": action_plan_next_month_chain,
                "requires": ["quicksight_data"],
            },
        ]

    # ---------------------------------------------------------
    # STANDARD LOGIC (Cohorts 1, 2, 5, 6, 7)
    # ---------------------------------------------------------

    slides = [
        {
            "name": "intro_slide",
            "func": slide1_introduction_chain,
            "requires": ["ignite_payload", "quicksight_data"],
        }
    ]

    # -------------------- UPTREND --------------------
    if exact_category == "uptrend":
        # Insert Delivery Slide for Cohort 1 & 2
        if cohort in ["1", "2"]:
            slides.append(delivery_slide_config)

        slides.extend([
            {
                "name": "big_wins_this_month",
                "func": big_wins_chain,
                "requires": ["quicksight_data"],
            },
            {
                "name": "growth_at_glance",
                "func": growth_at_glance_chain,
                "requires": ["quicksight_data"],
            },
        ])

        if cohort in ["1", "5", "6a", "7a"]:
            slides.append({
                "name": "how_your_ads_performed",
                "func": how_your_ads_performed_chain,
                "requires": ["quicksight_data"],
            })

        if cohort in ["1", "2", "5", "6a", "6b", "7a", "7b"]:
            slides.append({
                "name": "what_drove_results",
                "func": what_drove_results_chain,
                "requires": ["quicksight_data", "ignite_payload"],
            })

        slides.append({
            "name": "action_plan_next_month",
            "func": action_plan_next_month_chain,
            "requires": ["quicksight_data"],
        })

    # -------------------- DOWNTREND --------------------
    elif exact_category == "downtrend":
        # Insert Delivery Slide for Cohort 1 & 2
        if cohort in ["1", "2"]:
            slides.append(delivery_slide_config)

        slides.extend([
            {
                "name": "performance_summary",
                "func": performence_summary_chain,
                "requires": ["quicksight_data"],
            },
            {
                "name": "areas_that_need_attention",
                "func": areas_needing_attention_chain,
                "requires": ["quicksight_data"],
            },
            {
                "name": "how_your_ads_performed",
                "func": how_your_ads_performed_chain,
                "requires": ["quicksight_data"],
            },
            {
                "name": "action_plan_next_month",
                "func": action_plan_next_month_chain,
                "requires": ["quicksight_data"],
            },
        ])

    return slides


async def run_slide_generation(
    cohort: str,
    exact_category: str,
    ignite_payload: str,
    quicksight_data: str,
    zylo_v6_data: str,
    social_stats="",
    zylo_v6_data_json=None,  # This comes from the main input
    zylo_v6_post_content=None,  # This comes from the main input
    msp_data="",
) -> Dict[str, Any]:
    """
    Run all slide generation functions based on cohort and category.
    """

    slide_configs = get_slide_functions(cohort, exact_category)

    # MAP DATA: Ensure keys here match the 'requires' list in config
    data_map = {
        "ignite_payload": ignite_payload,
        "quicksight_data": social_stats,
        "zylo_v6_data": zylo_v6_data,
        # Explicit mapping for the delivery slide
        "zylo_v6_data_json": zylo_v6_data_json,
        "zylo_v6_post_content": zylo_v6_post_content,
    }

    tasks = []
    slide_names = []

    for config in slide_configs:
        kwargs = {}
        for param in config["requires"]:
            if param in data_map:
                kwargs[param] = data_map[param]
            else:
                kwargs[param] = None

        task = config["func"](**kwargs)
        tasks.append(task)
        slide_names.append(config["name"])

    results = await asyncio.gather(*tasks, return_exceptions=True)

    output = {}
    for name, result in zip(slide_names, results):
        if isinstance(result, Exception):
            # Print error for debugging
            print(f"Error generating slide {name}: {str(result)}")
            output[name] = {"error": str(result)}
        else:
            output[name] = result

    return output

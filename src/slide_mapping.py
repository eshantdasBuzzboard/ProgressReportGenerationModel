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

    Each function config is a dict with:
    - 'name': function name
    - 'func': the async function to call
    - 'requires': list of required data parameters

    Args:
        cohort: Cohort identifier ('1', '2', '5', '6a', '6b', '7a', '7b', '8')
        exact_category: Category ('uptrend' or 'downtrend')

    Returns:
        List of function configurations to run
    """

    # Cohort 8 has special logic - no category check needed
    if cohort == "8":
        return [
            {
                "name": "intro_slide",
                "func": slide1_introduction_chain,
                "requires": ["ignite_payload", "quicksight_data"],
            },
            {
                "name": "your_brand_in_action",
                "func": here_is_what_we_delivered_chain,
                "requires": ["zylo_v6_data"],
            },
            {
                "name": "action_plan_next_month",
                "func": action_plan_next_month_chain,
                "requires": ["quicksight_data"],
            },
        ]

    # Initialize with intro slide (common to all)
    slides = [
        {
            "name": "intro_slide",
            "func": slide1_introduction_chain,
            "requires": ["ignite_payload", "quicksight_data"],
        }
    ]

    # Uptrend logic
    if exact_category == "uptrend":
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

        # Add "how your ads performed" for cohorts 1, 5, 6a, 7a
        if cohort in ["1", "5", "6a", "7a"]:
            slides.append({
                "name": "how_your_ads_performed",
                "func": how_your_ads_performed_chain,
                "requires": ["quicksight_data"],
            })

        # Add "what drove results" for cohorts 1, 2, 5, 6a, 6b, 7a, 7b (uptrend only)
        if cohort in ["1", "2", "5", "6a", "6b", "7a", "7b"]:
            slides.append({
                "name": "what_drove_results",
                "func": what_drove_results_chain,
                "requires": ["quicksight_data", "ignite_payload"],
            })

        # Action plan is common to all uptrend
        slides.append({
            "name": "action_plan_next_month",
            "func": action_plan_next_month_chain,
            "requires": ["quicksight_data"],
        })

    # Downtrend logic
    elif exact_category == "downtrend":
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
    msp_data="",
) -> Dict[str, Any]:
    """
    Run all slide generation functions based on cohort and category.

    Args:
        cohort: Cohort identifier
        exact_category: Category ('uptrend' or 'downtrend')
        ignite_payload: Ignite payload data
        quicksight_data: QuickSight data
        zylo_v6_data: Zylov6 data

    Returns:
        Dictionary with slide names as keys and their generated data as values
    """

    # Get the functions to run
    slide_configs = get_slide_functions(cohort, exact_category)

    # Prepare data mapping
    data_map = {
        "ignite_payload": ignite_payload,
        "quicksight_data": social_stats,
        "zylo_v6_data": zylo_v6_data,
    }

    # Create tasks for async execution
    tasks = []
    slide_names = []

    for config in slide_configs:
        # Build kwargs based on what the function requires
        kwargs = {param: data_map[param] for param in config["requires"]}

        # Create task
        task = config["func"](**kwargs)
        tasks.append(task)
        slide_names.append(config["name"])

    # Run all tasks concurrently
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Map results to slide names
    output = {}
    for name, result in zip(slide_names, results):
        if isinstance(result, Exception):
            output[name] = {"error": str(result)}
        else:
            output[name] = result

    return output

import logging
from core.chains.preprocess import preprocess_chain, ads_score_chain


def process_data(data):
    """
    Processes social stats data:
    1. Keeps None as None (does not convert to 0)
    2. Calculates changes between consecutive periods (first to last) only for valid data
    3. Rounds to 1 decimal place
    4. Cleans terminology
    5. Removes metrics where all periods are 0 or None
    6. Returns processed data with change strings
    """

    # Helper functions
    def parse_value(value):
        """Parse value, handle comma-separated numbers, keep None as None"""
        if value in (None, "", "-"):
            return None
        try:
            # Remove commas if present (e.g., "3,536" -> "3536")
            if isinstance(value, str):
                value = value.replace(",", "")
            return float(value)
        except Exception as e:
            logging.error(f"{e}")
            return None

    def one_dec(value):
        """Round to 1 decimal place"""
        if value is None:
            return None
        try:
            val = float(value)
            return 0.0 if val == 0 else round(val, 1)
        except Exception as e:
            logging.error(f"{e}")
            return value

    def pct_change(old, new):
        """Calculate percentage change with arrow"""
        # If either value is None, can't calculate change
        if old is None or new is None:
            return "Insufficient data"

        if old == 0:
            if new > 0:
                return f"+{new:.1f} (from 0)"
            return "No change"

        change = ((new - old) / abs(old)) * 100
        arrow = "▲" if change > 0 else ("▼" if change < 0 else "▶")
        return f"{arrow} {change:+.1f}%"

    def pts_change(old, new):
        """Calculate points change (for CTR, etc.)"""
        # If either value is None, can't calculate change
        if old is None or new is None:
            return "Insufficient data"

        diff = new - old
        arrow = "▲" if diff > 0 else ("▼" if diff < 0 else "▶")
        return f"{arrow} {diff:+.1f} pts"

    def has_valid_data(periods):
        """Check if periods have at least one non-zero, non-None value"""
        for period in periods:
            value = parse_value(period.get("value"))
            if value is not None and value != 0:
                return True
        return False

    def clean_term(text):
        """Standardize terminology"""
        if text is None:
            return None
        replacements = {
            "OnGoing": "Ongoing Social Media Post",
            "On Demand": "On-Demand Post",
            "On-Demand Post": "On-Demand Post",
            "Ongoing Social Post": "Ongoing Social Media Post",
            "Ongoing Social Posts": "Ongoing Social Media Post",
            "On-Demand Posts": "On-Demand Post",
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text

    # Process social_stats
    processed_stats = {}
    social_stats = data.get("social_stats", {})

    for metric_name, time_series_data in social_stats.items():
        periods = time_series_data.get("periods", [])

        # Skip if no periods available
        if not periods or len(periods) == 0:
            continue  # Remove this metric entirely

        # Check if all values are 0 or None - if so, skip this metric
        if not has_valid_data(periods):
            continue  # Remove this metric entirely

        # Get first and last period values
        first_period = periods[0]
        last_period = periods[-1]

        first_value = parse_value(first_period.get("value"))
        last_value = parse_value(last_period.get("value"))

        # Determine if it's a percentage/rate metric (CTR) or count metric
        # is_rate_metric = any(
        #     x in metric_name.lower() for x in ["ctr", "rate", "cpm", "cpc"]
        # )

        # Calculate change between first and last period
        if "ctr" in metric_name.lower() or "rate" in metric_name.lower():
            change_str = pts_change(first_value, last_value)
        else:
            change_str = pct_change(first_value, last_value)

        # Process all periods with rounded values
        processed_periods = []
        for period in periods:
            parsed_value = parse_value(period.get("value"))
            processed_periods.append({
                "period_type": period.get("period_type"),
                "period_label": period.get("period_label"),
                "value": one_dec(parsed_value) if parsed_value is not None else None,
                "raw_value": parsed_value,
            })

        # Calculate raw change (only if both values exist)
        raw_change = None
        if first_value is not None and last_value is not None:
            raw_change = one_dec(last_value - first_value)

        processed_stats[metric_name] = {
            "periods": processed_periods,
            "first_period": {
                "label": first_period.get("period_label"),
                "value": one_dec(first_value) if first_value is not None else None,
            },
            "last_period": {
                "label": last_period.get("period_label"),
                "value": one_dec(last_value) if last_value is not None else None,
            },
            "change": change_str,
            "raw_change": raw_change,
            "period_count": len(periods),
        }

    # Process delivery dates with cleaned terminology
    processed_delivery = []
    for delivery in data.get("delivery_dates", []):
        processed_delivery.append({
            "social_post_type": clean_term(delivery.get("social_post_type")),
            "resolved": delivery.get("resolved"),
        })

    # Return complete processed data
    return {
        "business_info": data.get("business_info", {}),
        "about_this_business": data.get("about_this_business", ""),
        "social_stats": processed_stats,
        "delivery_dates": processed_delivery,
    }


async def return_preprocess_data(
    ignite_api_data, quicksight_data_declining, zylo_v6_data, msp_data=""
):
    response = await preprocess_chain(
        ignite_api_data=ignite_api_data,
        quick_sight_data=quicksight_data_declining,
        zylo_v6_data=zylo_v6_data,
        msp_data=msp_data,
    )
    new_response = process_data(response)
    social_stats = new_response["social_stats"]
    return new_response, social_stats


async def identify_cohort(
    quicksight_data, ignite_api_data, zylo_v6_data, msp_data, social_stats
):
    cohort = None
    if (not quicksight_data) and ignite_api_data and zylo_v6_data and msp_data:
        cohort = "4"
    elif (not quicksight_data) and (not msp_data) and ignite_api_data and zylo_v6_data:
        cohort = "8"
    else:
        if quicksight_data:
            ads_response = await ads_score_chain(quicksight_data=social_stats)
            flag = ads_response.get("flag", None)
            if (not zylo_v6_data) and ignite_api_data and quicksight_data and msp_data:
                if flag == 0:
                    cohort = "6b"
                elif flag == 1:
                    cohort = "6a"
                else:
                    cohort = "6"
            elif (
                (not zylo_v6_data)
                and (not msp_data)
                and quicksight_data
                and ignite_api_data
            ):
                if flag == 0:
                    cohort = "7b"
                elif flag == 1:
                    cohort = "7a"
                else:
                    cohort = "7"
            elif quicksight_data and ignite_api_data and zylo_v6_data and msp_data:
                cohort = str(ads_response.get("score", 0))
            elif (
                quicksight_data and ignite_api_data and zylo_v6_data and (not msp_data)
            ):
                cohort = str(ads_response.get("score", 0))
        else:
            cohort = "0"

    return cohort

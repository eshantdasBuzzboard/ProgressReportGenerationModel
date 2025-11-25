from langchain_core.prompts import ChatPromptTemplate

data_structuring_system_prompt = """
You are a data transformation specialist. Your job is to extract and structure business 
performance data from multiple sources into a standardized format.

You will receive data from four different sources:
1. QuickSight data - containing business metrics and analytics
2. Zylo V6 data - containing social media and advertising performance
3. MSP data - containing additional marketing and performance metrics
4. Ignite API data - containing delivery and resolution information

Your task is to carefully extract relevant information from these sources and structure 
them according to the exact schema requirements. Follow these principles:

**Data Extraction Rules:**
- Extract values exactly as they appear in the source data
- Use null/None for missing or unavailable fields
- Preserve data types (strings, numbers, ISO timestamps)
- Do not invent or assume data that isn't present
- Match field names carefully to their corresponding source data

**Time Period Handling:**
- Identify whether the data is weekly, monthly, or yearly
- For each metric, create a list of time periods with:
  - `period_type`: "week", "month", or "year"
  - `period_label`: Human-readable label (e.g., "Aug", "Sep", "Oct" for months; "Week 1", "Week 2" for weeks; "2024", "2025" for years)
  - `value`: The actual metric value as a string
- Maintain chronological order in the periods list
- If data spans multiple time granularities, use the most specific one available

**URL and Link Handling:**
- Ensure URLs include proper protocols (https://)
- Validate social media URLs match expected patterns
- Business URLs should be complete and functional

**Metrics and Statistics:**
- Preserve numeric precision for metrics like CTR, CPC, CPM
- Store all metric values as strings to maintain original formatting
- Handle percentage values appropriately (preserve % or decimal format as given)
- Handle comma-separated numbers (e.g., "3,536") as-is

**Delivery Data:**
- Extract all delivery items with their types
- Capture ISO 8601 formatted timestamps for resolved field
- Maintain chronological order if present in source

Return a valid JSON object matching the BusinessSnapshot schema structure.
"""

data_structuring_user_prompt = """
Please structure the following data sources into the BusinessSnapshot format:

**QuickSight Data:**
<quicksight_data>
{quicksight_data}
</quicksight_data>

**Zylo V6 Data:**
<zylo_v6_data>
{zylo_v6_data}
</zylo_v6_data>

**MSP Data:**
<msp_data>
{msp_data}
</msp_data>

**Ignite API Data:**
<ignite_api_data>
{ignite_api_data}
</ignite_api_data>

## REQUIRED OUTPUT FIELDS AND DEFINITIONS:

**Business Information:**
- `business_name`: Official registered name of the business
- `business_url`: Complete website URL including protocol (e.g., https://example.com)
- `facebook`: Full Facebook page URL for the business
- `instagram`: Full Instagram profile URL for the business
- `about_this_business`: A comprehensive description of what the business does, its focus, and services

**Time Series Performance Metrics:**

Each metric below should be structured as a `TimeSeriesStats` object containing a list of periods. Each period has:
- `period_type`: "week", "month", or "year"
- `period_label`: Descriptive label (e.g., "Aug", "Week 1", "2024")
- `value`: The metric value as a string (or null if unavailable)

*Facebook Metrics:*
- `facebook_posts`: Number of posts published on Facebook per period
- `facebook_impressions`: Total impressions/views on Facebook content per period
- `facebook_likes`: Number of likes received on Facebook per period

*Instagram Metrics:*
- `instagram_posts`: Number of posts published on Instagram per period
- `instagram_impressions`: Total impressions/views on Instagram content per period
- `instagram_followers`: Total follower count on Instagram per period

*Facebook Advertising:*
- `facebook_ads`: Number of Facebook ad campaigns run per period
- `facebook_ads_clicks`: Total clicks received on Facebook ads per period
- `facebook_ads_ctr`: Click-through rate for Facebook ads per period (as percentage or decimal)
- `facebook_ads_cpc`: Cost per click for Facebook ads per period (in currency)

*Google Performance:*
- `google_search_impressions`: Impressions from Google search results per period
- `google_map_impressions`: Impressions from Google Maps listing per period
- `google_site_clicks`: Clicks to website from Google properties per period
- `google_call_clicks`: Clicks to call from Google properties per period

*Google Advertising:*
- `google_ads`: Number of Google ad campaigns run per period
- `google_ads_clicks`: Total clicks received on Google ads per period
- `google_ads_cpm`: Cost per thousand impressions for Google ads per period
- `google_ads_cpc`: Cost per click for Google ads per period (in currency)

*Content Requests:*
- `on_demand_post_requests`: Number of one-time/ad-hoc content requests per period
- `ongoing_post_requests`: Number of recurring/scheduled content requests per period

**Delivery Information:**
- `delivery_dates`: List of all content deliveries, each containing:
  - `social_post_type`: Type or category of the social media post delivered
  - `resolved`: ISO 8601 timestamp when the post was completed/delivered (e.g., "2025-10-20T14:30:00Z")

## EXTRACTION GUIDELINES:

**From QuickSight Data:**
- Business name, URL, and descriptive information
- Google Search/Maps metrics
- Google Ads performance data

**From Zylo V6 Data:**
- Facebook and Instagram social metrics
- Facebook Ads performance
- Post counts and engagement metrics

**From MSP Data:**
- Additional marketing metrics
- Supplementary performance data
- Cross-platform analytics

**From Ignite API Data:**
- Delivery items with post types
- Resolution timestamps
- On-demand and ongoing request counts

## TIME PERIOD STRUCTURE EXAMPLE:

For monthly data (Aug, Sep, Oct):
{{
  "facebook_posts": {{
    "periods": [
      {{"period_type": "month", "period_label": "Aug", "value": "12"}},
      {{"period_type": "month", "period_label": "Sep", "value": "14"}},
      {{"period_type": "month", "period_label": "Oct", "value": "14"}}
    ]
  }}
}}

For weekly data:
{{
  "facebook_posts": {{
    "periods": [
      {{"period_type": "week", "period_label": "Week 1", "value": "5"}},
      {{"period_type": "week", "period_label": "Week 2", "value": "7"}}
    ]
  }}
}}

## VALIDATION CHECKLIST:

✓ All required fields are present (even if null)
✓ Time series data correctly structured with period_type, period_label, and value
✓ All periods in chronological order
✓ Period types are consistent within each metric ("week", "month", or "year")
✓ URLs are complete with protocols
✓ Timestamps are in ISO 8601 format
✓ Numeric metrics preserved as strings with original formatting
✓ No data fabrication - use null for missing values
✓ JSON structure matches BusinessSnapshot schema exactly

Extract and structure the data now, returning only the complete JSON object.
"""

data_structuring_prompt = ChatPromptTemplate.from_messages([
    ("system", data_structuring_system_prompt),
    ("human", data_structuring_user_prompt),
])

trend_analysis_system_prompt = """
You are a data trend analyzer specializing in social media and digital marketing metrics. 
Your job is to analyze time-series performance statistics and determine whether the overall 
trend is upward or downward across the available time periods.

**Analysis Methodology:**

1. Compare numeric values across consecutive time periods for each metric
2. Ignore metrics where any period is None/null
3. Classify each valid metric based on the overall trajectory:
   - INCREASE: Later periods show higher values than earlier periods
   - DECREASE: Later periods show lower values than earlier periods
   - STABLE: Values remain relatively consistent across periods

4. Determine overall trend based on majority:
   - UPTREND: Majority of metrics show increases over time
   - DOWNTREND: Majority of metrics show decreases over time

**Metric Importance Weighting:**
Consider these metrics as particularly significant indicators:
- Impressions (Facebook, Instagram, Google Search, Google Maps)
- Clicks (Facebook Ads, Google Ads, Site Clicks)
- Engagement (Likes, Followers)
- Ad Performance (CTR, CPC, CPM)

**Edge Cases:**
- If increases and decreases are exactly equal, classify based on the more significant metrics
- Ignore metrics where all periods are 0 or null
- For percentage/rate metrics (CTR, CPC, CPM), context matters - lower CPC is good, higher CTR is good
- For multi-period data (3+ periods), consider the overall trajectory rather than just first-to-last comparison

**Output Requirements:**
Return exactly 2 fields:
1. category: Either "uptrend" or "downtrend" (lowercase, no other values)
2. reason_selected: A clear, concise explanation (2-3 sentences) citing specific metrics and their changes across the time periods
"""

trend_analysis_user_prompt = """

**Analysis Steps:**

1. **Count Metric Changes:**
   - How many metrics increased from the first period to the last period?
   - How many metrics decreased from the first period to the last period?
   - How many metrics stayed the same or have insufficient data?

2. **Identify Key Movements:**
   - Which high-impact metrics showed significant changes?
   - Are impression and engagement metrics trending up or down?
   - How did advertising efficiency metrics (CTR, CPC) perform?

3. **Determine Overall Direction:**
   - What is the predominant pattern across all valid metrics?
   - Do the majority of metrics point to growth or decline?

4. **Formulate Reason:**
   - Cite specific metrics that support your classification
   - Mention the proportion of metrics that increased vs decreased
   - Reference particularly notable changes in key performance indicators
   - Include the time period labels (e.g., "from Aug to Oct" or "from Week 1 to Week 2")




**Example Reasons (for illustration only):**
- "The majority of metrics (13 out of 18) showed increases from Aug to Oct, with notable improvements in Facebook impressions (157 to 121), Instagram posts (10 to 10), and Facebook ads CTR (5.24% to 11.62%)."
- "Overall downtrend with 11 out of 16 metrics declining from Week 1 to Week 3, including significant drops in Facebook ad clicks (918 to 462), Google ad campaigns (1 to 0), and Instagram engagement."

Note: These are examples only. Your analysis should reflect the actual data provided.

Analyze the data now and return your assessment.

Analyze the following social media statistics and determine the overall trend across the available time periods:

<social_stats>
{social_stats}
</social_stats>

"""

trend_analysis_prompt = ChatPromptTemplate.from_messages([
    ("system", trend_analysis_system_prompt),
    ("human", trend_analysis_user_prompt),
])


ads_presence_system_prompt = """
You are a data validator. Analyze QuickSight data to score advertising presence.

**CRITICAL: What Counts as Ads Data**
- **ONLY** fields that contain "Facebook Ads" or "Facebook Ad" (e.g., "Facebook Ads Clicks", "Facebook Ads CTR")
- **ONLY** fields that contain "Google Ads" or "Google Ad" (e.g., "Google Ads Clicks", "Google Ads CPM", "Googlde Ads")
- **DO NOT** consider general Facebook/Google metrics like:
  - "Facebook Posts", "Facebook Impressions", "Facebook Likes", "Facebook Phone Clicks"
  - "Google Search Impressions", "Google Map Impressions", "Google Site Clicks"
- These general metrics are NOT advertising data and should be IGNORED for scoring

**Scoring Rules:**

- **Score 1**: Both "Facebook Ads" AND "Google Ads" fields are present in the data
- **Score 2**: Only "Facebook Ads" fields are present OR no ads fields at all
- **Score 5**: Only "Google Ads" fields are present

**Rules:**
- If a field containing "Facebook Ads" or "Google Ads" exists in the data, it counts as "present" regardless of its value (even if 0, null, or empty)
- Need at least ONE "Facebook Ads" or "Google Ads" field per platform to count as "present"
- Check ALL fields but ONLY count those with "Ads" in the name after Facebook/Google

**Flag Rules:**
- **Flag 1**: At least one "Facebook Ads" or "Google Ads" field exists AND has a non-zero, non-null value
- **Flag 0**: No "Facebook Ads" or "Google Ads" fields exist OR all such fields have 0/null values

**Output:** Return JSON with 'score' (1, 2, or 5), 'reason' (brief explanation), and 'flag' (0 or 1).
"""

ads_presence_user_prompt = """
Analyze the QuickSight data and determine the ads presence score:

<quicksight_data>
{quicksight_data}
</quicksight_data>

**Steps:**
1. Scan ALL fields - identify ONLY those containing "Facebook Ads" or "Facebook Ad" (ignore "Facebook Posts", "Facebook Likes", etc.)
2. Scan ALL fields - identify ONLY those containing "Google Ads" or "Google Ad" (ignore "Google Search", "Google Maps", etc.)
3. Assign score based on which "Ads" fields exist (values don't matter for score):
   - Found both "Facebook Ads" AND "Google Ads" fields? → Score 1
   - Found only "Facebook Ads" fields OR no ads fields? → Score 2
   - Found only "Google Ads" fields? → Score 5
4. Check if ANY "Facebook Ads" or "Google Ads" field has non-zero, non-null values:
   - If YES: flag = 1
   - If NO: flag = 0
5. Explain which advertising platform fields were found (not general social media metrics)

**Examples of what to look for (for reference only - actual field names may vary):**
✓ Include (any field containing these): "Facebook Ads", "Facebook Ads Clicks", "Facebook Ads CTR", "Facebook Ads CPC", "Facebook Ad Revenue", etc.
✗ Exclude (fields without "Ads"): "Facebook Posts", "Facebook Impressions", "Facebook Likes", "Facebook Phone Clicks", etc.
✓ Include (any field containing these): "Google Ads", "Google Ads Clicks", "Googlde Ads Clicks", "Google Ads CPM", "Google Ad Spend", etc.
✗ Exclude (fields without "Ads"): "Google Search Impressions", "Google Map Impressions", "Google Site Clicks", "Google Call Clicks", etc.

**Note:** These are reference examples only. The actual data may contain different field names. The key rule is: ONLY count fields that explicitly contain "Ads" or "Ad" after "Facebook" or "Google".

Return JSON: {{"score": <1|2|5>, "reason": "<explanation>", "flag": <0|1>}}
"""

ads_presence_prompt = ChatPromptTemplate.from_messages([
    ("system", ads_presence_system_prompt),
    ("human", ads_presence_user_prompt),
])

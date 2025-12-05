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

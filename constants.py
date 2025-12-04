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

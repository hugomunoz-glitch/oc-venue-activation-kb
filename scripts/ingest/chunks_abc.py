"""
Structured chunk + fee data for California ABC (Alcoholic Beverage Control)
temporary/one-day alcohol permit reference data. State-level source - applies
uniformly across all cities in this KB's scope, not just Fullerton, but is
associated with the Fullerton city_id for now since the schema requires one
and the KB is currently single-city. Flag this explicitly if the KB expands
to multiple cities (see Phase 4 notes in the instructions doc).
"""

CITY = "Fullerton"

DOCUMENTS = [
    {
        "title": "ABC-221: Daily License Application (nonprofit temporary alcohol permit)",
        "source_type": "website",
        "source_name": "California Department of Alcoholic Beverage Control (abc.ca.gov)",
        "source_key": "https://www.abc.ca.gov/wp-content/uploads/forms/ABC-221.pdf",
        "retrieved_date": "2026-08-20",
        "effective_date": "2023-11-01",
        "effective_date_confidence": "confirmed",
        "notes": "Form revision date printed as 'ABC-221 (Rev.11/2023)'. Fee amounts on the form cross-checked against the Application Fee Schedules page (non-profit temporary licenses, effective 2019-07-01). ELIGIBILITY LIMIT: only available to qualifying nonprofit/charitable/civic/fraternal/political/religious/social organizations - NOT directly available to a for-profit wedding venue or gym.",
        "chunks": [
            ("Daily License - Eligibility", "The Daily License (Form ABC-221) is available only to qualifying organizations: amateur sports organizations, charitable organizations, civic organizations, cultural organizations, fraternal organizations in existence over five years with regular membership, political organizations (including parties/affiliates supporting a candidate or ballot measure), religious organizations, social organizations, nonprofit corporations, television stations (for specific statutory purposes), persons conducting an estate wine sale, and women's educational/charitable organizations. A private for-profit wedding venue or gym does NOT itself qualify - it would need a genuine qualifying nonprofit to be the licensed organization, or must instead use a Catering/Event Authorization (Form ABC-218) via a properly licensed caterer."),
            ("Daily License - Fees", "Daily License (Form ABC-221) fees, per day: Special Daily Beer and Wine = $50.00; Daily General (beer, wine and distilled spirits) = $75.00; Special Temporary License (television station, nonprofit corporation, estate wine sale, women's educational/charitable org, or other per statute) = $100.00; Vessel per Section 24045.10 B&P = $50.00. Fees are non-refundable once the license is issued. Payment by cashier's check or money order payable to ABC."),
            ("Daily License - Process", "Form ABC-221 requires: organization name and Tax ID, event address and dates, estimated attendance, whether the event is outdoors (requires a site diagram if so), property owner approval signature, and (per Business and Professions Code Section 25682(c)) a designated RBS-certified person who must remain on-site for the duration of the event. The license may be revoked summarily if deemed necessary to protect public safety, welfare, health, peace or morals."),
        ],
    },
    {
        "title": "ABC-218: Catering Authorization Application (event alcohol service via licensed caterer)",
        "source_type": "website",
        "source_name": "California Department of Alcoholic Beverage Control (abc.ca.gov)",
        "source_key": "https://www.abc.ca.gov/wp-content/uploads/forms/ABC-218.pdf",
        "retrieved_date": "2026-08-20",
        "effective_date": "2024-01-01",
        "effective_date_confidence": "confirmed",
        "notes": "Form revision date printed as 'ABC-218 (Rev. 01/2024)'; instructions document 'ABC-218 INSTR (Rev. 02/2024)'. Fee tiers not printed on the form itself - cross-checked against the Application Fee Schedules page (Catering and Event Authorizations, effective 2022-01-01). This is the realistic path for a private (non-nonprofit) wedding venue or gym wanting one-day alcohol service, since it requires hiring an already-licensed caterer rather than the venue holding its own license.",
        "chunks": [
            ("Catering Authorization - Who Applies", "Form ABC-218 (Catering Authorization Application) is filed by an existing ABC licensee (e.g. a caterer holding a Type 58 Caterer's Permit, a Type 91 Beer Manufacturer's Caterer's Permit, a Type 77 Event Permit, or a Type 93 Estate Tasting Event Permit) to extend their existing license to a specific off-site event - it is not something a venue with no existing ABC license applies for directly. A private wedding venue or gym without its own liquor license would need to hire such a licensed caterer to serve alcohol at an activation, rather than obtaining a license itself."),
            ("Catering Authorization - Fees", "Catering and Event Authorization fees (effective 2022-01-01), charged per day: 0 to 999 attendance = $100; 1,000 to 4,999 attendance = $325; 5,000 or more attendance = $1,000; Invitation Only Events (per Business and Professions Code Section 25600.5) = $250; Estate Tasting Event Permit = $100. For a typical small-to-mid-size wedding or activation (well under 1,000 guests), the applicable fee is $100/day."),
            ("Catering Authorization - Process and Limits", "Form ABC-218 must be submitted at least three days before the event (or at least five days if applying online at services.abc.ca.gov) and no more than 30 days before the event; late or early submissions may not be processed. There is a limit of 36 catered events per year at any single location. Multi-day events must have consecutive dates with identical attendance and hours each day, or must be filed as separate single-day events. The event may require operating conditions, property owner approval, law enforcement agency approval, or a supplemental site diagram (Form ABC-253)."),
        ],
    },
]

FEE_ROWS = [
    {
        "permit_type": "ABC Daily License (nonprofit temporary alcohol permit)",
        "fee_name": "Special Daily Beer and Wine",
        "amount_usd": 50, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat_per_day", "code_section": "Form ABC-221",
        "applies_to_track": "statewide_nonprofit_only",
        "effective_date": "2019-07-01",
        "notes": "Nonprofit/qualifying-organization eligibility only.",
    },
    {
        "permit_type": "ABC Daily License (nonprofit temporary alcohol permit)",
        "fee_name": "Daily General (beer, wine, distilled spirits)",
        "amount_usd": 75, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat_per_day", "code_section": "Form ABC-221",
        "applies_to_track": "statewide_nonprofit_only",
        "effective_date": "2019-07-01",
        "notes": "Nonprofit/qualifying-organization eligibility only.",
    },
    {
        "permit_type": "ABC Daily License (nonprofit temporary alcohol permit)",
        "fee_name": "Special Temporary License",
        "amount_usd": 100, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat_per_day", "code_section": "Form ABC-221",
        "applies_to_track": "statewide_nonprofit_only",
        "effective_date": "2019-07-01",
        "notes": "Covers Special Daily On-Sale, Off-Sale, and Auction variants per the Application Fee Schedules page.",
    },
    {
        "permit_type": "ABC Catering/Event Authorization (via licensed caterer)",
        "fee_name": "0 to 999 attendance",
        "amount_usd": 100, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat_per_day", "code_section": "Form ABC-218",
        "applies_to_track": "statewide_private_venue_path",
        "effective_date": "2022-01-01",
        "notes": "The realistic tier for a typical wedding/gym activation. Requires hiring a caterer who already holds a Type 58/91/77/93 license.",
    },
    {
        "permit_type": "ABC Catering/Event Authorization (via licensed caterer)",
        "fee_name": "1,000 to 4,999 attendance",
        "amount_usd": 325, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat_per_day", "code_section": "Form ABC-218",
        "applies_to_track": "statewide_private_venue_path",
        "effective_date": "2022-01-01",
        "notes": None,
    },
    {
        "permit_type": "ABC Catering/Event Authorization (via licensed caterer)",
        "fee_name": "5,000 or more attendance",
        "amount_usd": 1000, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat_per_day", "code_section": "Form ABC-218",
        "applies_to_track": "statewide_private_venue_path",
        "effective_date": "2022-01-01",
        "notes": None,
    },
    {
        "permit_type": "ABC Catering/Event Authorization (via licensed caterer)",
        "fee_name": "Invitation Only Events",
        "amount_usd": 250, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat_per_day", "code_section": "Form ABC-218 / B&P Section 25600.5",
        "applies_to_track": "statewide_private_venue_path",
        "effective_date": "2022-01-01",
        "notes": None,
    },
]

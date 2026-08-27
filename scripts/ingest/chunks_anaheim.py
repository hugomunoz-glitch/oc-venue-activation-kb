"""
Phase 4, Anaheim: document-upload source - the City of Anaheim Planning &
Zoning Fee Schedule (effective August 2026, anaheim.net/DocumentCenter/View/22436).
Confirmed fetchable (unlike Anaheim's municipal code, which amlegal.com
blocks the same way it blocked Fullerton's in Phase 1) - real, current,
primary-sourced fee figures, not inferred.

Municipal code chunks (special event permit / temporary use requirements)
are added separately once the user supplies the text manually (amlegal.com
returns 403 to automated fetches).
"""

CITY = "Anaheim"

DOCUMENTS = [
    {
        "title": "City of Anaheim Planning & Zoning Fee Schedule",
        "source_type": "fee_schedule",
        "code_chapter": None,
        "source_name": "City of Anaheim Planning Services Division (anaheim.net)",
        "source_file": None,
        "source_key": "https://anaheim.net/DocumentCenter/View/22436/Planning-and-Zoning-Fees",
        "retrieved_date": "2026-08-27",
        "effective_date": "2026-08-01",
        "effective_date_confidence": "stated_on_document",
        "notes": "Effective August 2026 per the document's own cover page (Z677). Administrative and Discretionary case fee tables; special-event and CUP lines are what this KB cares about.",
        "chunks": [
            (
                "Special Event Permit fees (Administrative)",
                "Anaheim's Planning Services Division charges these administrative special-event fees: Special Event Permit - Flags & Banners, Sidewalk Sales: $100 per event. Special Event Permit - Outdoor Activity: $362 per event. Special Event Permit - Post Inspection Fee for Carnivals, Circuses, Pumpkin Patches and Tree Lots: $259 per event. Special Events - Special Circumstance Waiver (and Wayfinding Sign Program Permit - Administrative Review): $857 per event. These are flat administrative-review fees, separate from any Conditional Use Permit process. Effective August 2026.",
            ),
            (
                "Conditional Use Permit (CUP) fees (Discretionary)",
                "Anaheim's Conditional Use Permit fees vary by project type: CUP - New Construction: $220/hr, $11,255 minimum initial deposit, $2,813 minimum balance. CUP - No New Construction: $9,893 flat fee. Minor Conditional Use Permit (MCUP): $6,816 flat fee. CUP - Amendment, Minor by Planning Commission: $8,121 flat fee. CUP Amendment for Large Projects: $13,408 flat fee. Density Bonus: $220/hr, $11,255 deposit, $2,813 minimum balance. Flat-fee CUP cases may be subject to an additional 20% fee for each secondary case if multiple cases are filed or processed concurrently, and to the Resubmittal Flat Fee ($2,250) for multiple revisions. Effective August 2026.",
            ),
            (
                "Appeals and other related fees",
                "An appeal to Anaheim City Council costs $5,515 flat fee for cases on the flat-fee list (applicant pays all fees, except a $450 fee paid to the City Clerk if appealed by a non-applicant); other appeals are charged the same as the underlying permit fee. A Zoning Verification Letter costs $320 per request. Effective August 2026.",
            ),
        ],
    },
]

# Structured fee rows for the `fee_schedules` table - mirrors the chunk text
# above but as typed numeric data joinable by city_id.
FEE_ROWS = [
    {
        "permit_type": "special_event_permit",
        "fee_name": "Special Event Permit - Flags & Banners, Sidewalk Sales",
        "amount_usd": 100, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat", "code_section": None, "applies_to_track": None,
        "notes": "City of Anaheim Planning & Zoning Fee Schedule, effective August 2026.",
    },
    {
        "permit_type": "special_event_permit",
        "fee_name": "Special Event Permit - Outdoor Activity",
        "amount_usd": 362, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat", "code_section": None, "applies_to_track": None,
        "notes": "City of Anaheim Planning & Zoning Fee Schedule, effective August 2026.",
    },
    {
        "permit_type": "special_event_permit",
        "fee_name": "Special Event Permit - Post Inspection Fee (Carnivals, Circuses, Pumpkin Patches, Tree Lots)",
        "amount_usd": 259, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat", "code_section": None, "applies_to_track": None,
        "notes": "City of Anaheim Planning & Zoning Fee Schedule, effective August 2026.",
    },
    {
        "permit_type": "special_event_permit",
        "fee_name": "Special Events - Special Circumstance Waiver",
        "amount_usd": 857, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat", "code_section": None, "applies_to_track": None,
        "notes": "City of Anaheim Planning & Zoning Fee Schedule, effective August 2026.",
    },
    {
        "permit_type": "conditional_use_permit",
        "fee_name": "CUP - No New Construction",
        "amount_usd": 9893, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat", "code_section": None, "applies_to_track": None,
        "notes": "City of Anaheim Planning & Zoning Fee Schedule, effective August 2026. May be subject to +20% for concurrent secondary cases.",
    },
    {
        "permit_type": "conditional_use_permit",
        "fee_name": "Minor Conditional Use Permit (MCUP)",
        "amount_usd": 6816, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat", "code_section": None, "applies_to_track": None,
        "notes": "City of Anaheim Planning & Zoning Fee Schedule, effective August 2026.",
    },
    {
        "permit_type": "conditional_use_permit",
        "fee_name": "CUP - Amendment, Minor by Planning Commission",
        "amount_usd": 8121, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat", "code_section": None, "applies_to_track": None,
        "notes": "City of Anaheim Planning & Zoning Fee Schedule, effective August 2026.",
    },
    {
        "permit_type": "conditional_use_permit",
        "fee_name": "CUP Amendment for Large Projects",
        "amount_usd": 13408, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat", "code_section": None, "applies_to_track": None,
        "notes": "City of Anaheim Planning & Zoning Fee Schedule, effective August 2026.",
    },
    {
        "permit_type": "conditional_use_permit",
        "fee_name": "CUP - New Construction",
        "amount_usd": None, "amount_usd_min": 11255, "amount_usd_max": None,
        "amount_type": "hourly_plus_deposit", "code_section": None, "applies_to_track": None,
        "notes": "$220/hr against an $11,255 minimum initial deposit, $2,813 minimum balance. City of Anaheim Planning & Zoning Fee Schedule, effective August 2026.",
    },
]

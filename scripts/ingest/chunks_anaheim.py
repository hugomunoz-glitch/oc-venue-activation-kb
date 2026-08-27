"""
Phase 4, Anaheim: two document-upload sources.

1. City of Anaheim Planning & Zoning Fee Schedule (effective August 2026,
   anaheim.net/DocumentCenter/View/22436) - confirmed fetchable directly.
2. Anaheim Municipal Code Ch. 18.38/18.118 special-event and temporary-use
   sections - amlegal.com confirmed 403s automated fetches (same block
   Fullerton's code hit in Phase 1), so the user retrieved and supplied this
   text manually (a saved PDF of the code pages, not paraphrased).
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
    {
        "title": "Anaheim Municipal Code Ch. 18.38/18.118: Special Events, Festival Permit, Temporary Uses",
        "source_type": "municipal_code",
        "code_chapter": "18.38 / 18.118",
        "source_name": "Anaheim Municipal Code (codelibrary.amlegal.com)",
        "source_file": None,
        "source_key": "https://codelibrary.amlegal.com/codes/anaheim/latest/anaheim_ca/0-0-0-80504",
        "retrieved_date": "2026-08-27",
        "effective_date": "2026-01-13",
        "effective_date_confidence": "stated_in_ordinance_history",
        "notes": "amlegal.com returns 403 to automated fetches (same as Fullerton's code in Phase 1). Text manually retrieved and supplied by the user; §18.38.230's most recent amendment is Ord. 6620, effective January 13, 2026.",
        "chunks": [
            (
                "§18.38.230 - Special Events, Outdoor Activity: definition and permit requirement",
                "Anaheim requires a special event permit before conducting a 'Special Events - Outdoor Activity': any event, promotion, or sale sponsored by a business, shopping center, or organization (or a school/charitable-nonprofit fundraiser), held outside a building but on the same property, which may include outdoor display of merchandise, rides, games, booths, or similar amusement devices - whether or not admission is charged. This is the section that covers a typical one-day activation at an existing business property (e.g. a gym hosting a promotional pop-up on its own lot). Exceptions not requiring a permit: compliant holiday decorations, up to three national/state/local/religious/fraternal flags, and private occasional parties not open to the public.",
            ),
            (
                "§18.38.230 - Where it's allowed",
                "A Special Events - Outdoor Activity permit may be issued for: any property with a conditional use permit authorizing a use permitted or conditionally permitted in a commercial zone; any public or private elementary, junior high, or senior high school; any location with a conditional use permit for community and religious assembly; and, with additional restrictions, certain large auto dealerships adjacent to a freeway. Special events on the Center Street Promenade follow a separate approval path (Planning and Building Director), not the standard requirements of this section.",
            ),
            (
                "§18.38.230 - Duration and frequency limits",
                "A Special Events - Outdoor Activity permit may not be issued for more than nine (9) consecutive calendar days. No business or organization may be issued more than four (4) such special event permits in any calendar year - using multiple addresses for one business, or a change of business ownership at an address, does not create additional permits beyond that four-per-year limit.",
            ),
            (
                "§18.38.230 - Conduct requirements (hours, structures, parking, signs)",
                "Special event sales/displays must be directly related to the business on the same property and constitute at least 25% of that business's total gross receipts. Structures (including tents and amusement-device structures) require approval from the Building Division, Fire Department, and Electrical Engineering Division before erection; no structure, amusement device, or fixed balloon may exceed 50 feet in height. Hours are confined to the business's normal operating hours, and in no event before 7:00 a.m. or after 10:00 p.m. Live/amplified music must comply with Chapter 6.70 (Sound Pressure Levels). One sign advertising the event is permitted, removed at the event's conclusion. A site plan is required if parking areas will be used.",
            ),
            (
                "§18.38.230 - Application, fee, and special circumstances waiver",
                "A special event permit application must be filed with the Planning Department at least 14 days before the opening date for events involving rides, games, booths, or amusement devices (temporary signs/flags/banners/balloons/trailers/tree-lot/pumpkin-patch-only applications may be filed any time before display). A fee is charged per Chapter 18.80 (Fees) - charitable, nonprofit organizations recognized by the State of California are exempt from this fee, except for carnivals, circuses, Christmas tree lots, or pumpkin patches. The Planning Director may issue a 'special circumstances waiver' to modify or waive any regulation in this section if it would serve the public interest, safety, or general welfare, or if extraordinary circumstances exist - petitions for this waiver require their own fee (also set in Chapter 18.80) and receive a decision within 14 days of a complete application.",
            ),
            (
                "§18.38.135 - Festival Permit: large-scale events only, not a typical one-day activation",
                "Anaheim's separate Festival Permit (Ch. 18.38.135) governs large-scale events only: a 'Festival' is defined as an event expected to draw 35,000+ people to two or more designated City Venues (the Anaheim Convention Center, Honda Center, and Angel Stadium of Anaheim) within the designated Festival Districts, across two or more public event days, generating a peak hotel room block of at least 500 rooms. This permit - and its far more extensive application requirements (security/medical/traffic/sanitation plans, $5,000,000+ liability insurance, performance bonds) - does not apply to a typical one-day gym or wedding-venue activation; that falls under the much simpler §18.38.230 Special Events - Outdoor Activity process instead.",
            ),
            (
                "§18.118.080 - Permitted Temporary Uses (Commercial-Recreation zone)",
                "In Anaheim's Commercial-Recreation (CR) zone, temporary special events and temporary flags/banners/balloons are permitted subject to compliance with the Special Events provisions (Chapter 18.38, Supplemental Use Regulations) and the Temporary Signs - Special Event Permit provisions (Section 18.44.170, Signs) - the same permit process described above, not a separate CR-zone-specific permit. This section also permits temporary contractor offices/storage during construction (up to 1 year) and temporary paved parking on vacant land as a hotel accessory use (up to 2 years), each requiring separate approval.",
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

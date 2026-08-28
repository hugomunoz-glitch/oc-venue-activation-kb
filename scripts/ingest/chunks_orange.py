"""
Phase 4, Orange (the ninth and final city in this plan): one document-
upload source, confirmed directly fetchable. The City of Orange's actual
code (Ch. 17.46, Special Events) is on ecode360.com and confirmed 403s
automated fetches - the seventh confirmed block of a code-hosting platform
in this project, and the only one hit on every single try.

Same honest-gap approach as Stanton: only the directly-verified Master
Schedule of Fees is ingested. The ordinance's own event-duration/hours
thresholds (a 9-consecutive-day cap and an 11 p.m. cutoff appeared in
search-engine summaries) are NOT included as verified fact, since they were
never independently confirmed against primary text - consistent with this
project's own standing lesson (La Habra's CUP fee) about not trusting
secondhand paraphrases of a blocked source.
"""

CITY = "Orange"

DOCUMENTS = [
    {
        "title": "City of Orange Master Schedule of Fees and Charges (Res. No. 11517, Jan. 2024)",
        "source_type": "fee_schedule",
        "code_chapter": None,
        "source_name": "City of Orange (cityoforange.org)",
        "source_file": None,
        "source_key": "https://citydocs.cityoforange.org/WebLink/edoc/244320376/RES-11517 AMENDED MASTER SCHEDULE OF FEES AND CHARGES VARIOUS SERVICES AND LOBBYIST REGISTRATION - JAN 9, 2024.pdf",
        "retrieved_date": "2026-08-27",
        "effective_date": "2024-01-09",
        "effective_date_confidence": "stated_on_document",
        "notes": "Read directly via pdftotext, from the Community Development - Planning Division section. This is the most recent comprehensive Community Development fee schedule found; a separate, narrower Res. No. 11665 (effective July 2026) updates only Community Services & Library facility-rental fees, not Planning fees.",
        "chunks": [
            (
                "Special Event and Temporary Use Permit fees (Community Development - Planning Division)",
                "Per the City of Orange's Master Schedule of Fees and Charges: Special Event Application/Permit - $110 each, plus actual cost. Special Promotion (Banner) Permit - $110 each. Temporary Use Permit (recurring uses) - $387 each. Temporary Use Permit (non-recurring uses) - $1,000 each. These are separate from the Community Services Department's own Special Event Park Permit (a $60 application fee, for events specifically held in a City park - a different track from a private-property activation at an existing business).",
            ),
            (
                "Conditional Use Permit, Variance, and Zoning Verification fees",
                "Per the same fee schedule: CUP/Variance - Zoning Administrator - $3,000 deposit, billed at actual cost. CUP/Variance - Planning Commission - $3,000 deposit, billed at actual cost. Planning Commission Modification to CUP, Major Site Plan, or Variance - $3,000 deposit. Minor Site Plan Review (Staff) - $1,000 deposit. Zoning Verification Letter - $332 each. Zone Clearance, Over-the-Counter Review - $42 each.",
            ),
        ],
    },
]

FEE_ROWS = [
    {
        "permit_type": "special_event_permit", "fee_name": "Special Event Application/Permit",
        "amount_usd": 110, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat_plus_cost", "code_section": None, "applies_to_track": None,
        "notes": "City of Orange Master Schedule of Fees, Res. No. 11517 (Jan. 2024). Plus actual cost.",
    },
    {
        "permit_type": "special_event_permit", "fee_name": "Temporary Use Permit (recurring uses)",
        "amount_usd": 387, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat", "code_section": None, "applies_to_track": None,
        "notes": "City of Orange Master Schedule of Fees, Res. No. 11517 (Jan. 2024).",
    },
    {
        "permit_type": "special_event_permit", "fee_name": "Temporary Use Permit (non-recurring uses)",
        "amount_usd": 1000, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat", "code_section": None, "applies_to_track": None,
        "notes": "City of Orange Master Schedule of Fees, Res. No. 11517 (Jan. 2024).",
    },
    {
        "permit_type": "conditional_use_permit", "fee_name": "CUP/Variance - Zoning Administrator",
        "amount_usd": None, "amount_usd_min": 3000, "amount_usd_max": None,
        "amount_type": "deposit", "code_section": None, "applies_to_track": None,
        "notes": "City of Orange Master Schedule of Fees, Res. No. 11517 (Jan. 2024). Billed at actual cost.",
    },
    {
        "permit_type": "conditional_use_permit", "fee_name": "CUP/Variance - Planning Commission",
        "amount_usd": None, "amount_usd_min": 3000, "amount_usd_max": None,
        "amount_type": "deposit", "code_section": None, "applies_to_track": None,
        "notes": "City of Orange Master Schedule of Fees, Res. No. 11517 (Jan. 2024). Billed at actual cost.",
    },
]

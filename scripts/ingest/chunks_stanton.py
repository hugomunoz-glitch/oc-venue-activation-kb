"""
Phase 4, Stanton: one document-upload source, confirmed directly
fetchable. Stanton's actual code (Ch. 20.540, Temporary Use Permits,
Annual Advertising Permits and Special Event Permits) is on ecode360.com
and confirmed 403s automated fetches - the sixth confirmed block of a
code-hosting platform in this project.

Deliberately NOT ingested this round: the actual TUP/Special-Event
definitional thresholds (event duration limits, car-wash/entertainment-
event day counts, etc.) - only search-engine paraphrases of the blocked
ordinance were found, no genuine primary-sourced application form or
directly-fetchable code text. Encoding a secondhand paraphrase as if it
were verified ordinance text is exactly the mistake this project already
caught once (La Habra's CUP fee, $5,385 quoted by a search summary vs.
$6,759 in the actual fee schedule PDF) - so this is left as an honest gap
pending either a working direct source or manual retrieval, not guessed at.
"""

CITY = "Stanton"

DOCUMENTS = [
    {
        "title": "City of Stanton Community Development Fee Schedule (effective 7/1/2026)",
        "source_type": "fee_schedule",
        "code_chapter": None,
        "source_name": "City of Stanton (stantonca.gov)",
        "source_file": None,
        "source_key": "http://www.stantonca.gov/2026 CD FEE SCHEDULE EFFECTIVE 7-1-2026.pdf",
        "retrieved_date": "2026-08-27",
        "effective_date": "2026-07-01",
        "effective_date_confidence": "stated_on_document",
        "notes": "Read directly via pdftotext. Shows both the prior fee and the new fee effective 7/1/2026 for each line item.",
        "chunks": [
            (
                "Special Event and Temporary Use Permit fees",
                "Per Stanton's Community Development Fee Schedule, effective 7/1/2026: Special Events Permit - $199 (up from $193). Temporary Use Permit - $1,180 (up from $1,146). Temporary Sign - $108 (up from $105). Note: this knowledge base has the fee amounts but not the underlying ordinance's event-duration/frequency thresholds for these permits - Stanton's code (Ch. 20.540) is on ecode360.com, which blocks automated access; that text has not yet been independently retrieved.",
            ),
            (
                "Conditional Use Permit, Variance, and related discretionary fees",
                "Per the same fee schedule, effective 7/1/2026: Conditional Use Permit - $2,972 (up from $2,885). Conditional Use Permit - Major/Amendment - $3,153 (up from $3,061). Variance - $2,508 (up from $2,435). Zone Change - $10,230 (up from $9,932). Administrative Review (Minor Site Plan/Design Review, Minor CUP, Minor Variance) - $1,757 (up from $1,706). Appeal to Planning Commission - $3,076 (up from $2,986). Sign Program - $1,615 (up from $1,568).",
            ),
        ],
    },
]

FEE_ROWS = [
    {
        "permit_type": "special_event_permit", "fee_name": "Special Events Permit",
        "amount_usd": 199, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat", "code_section": None, "applies_to_track": None,
        "notes": "City of Stanton Community Development Fee Schedule, effective 7/1/2026.",
    },
    {
        "permit_type": "special_event_permit", "fee_name": "Temporary Use Permit",
        "amount_usd": 1180, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat", "code_section": None, "applies_to_track": None,
        "notes": "City of Stanton Community Development Fee Schedule, effective 7/1/2026.",
    },
    {
        "permit_type": "conditional_use_permit", "fee_name": "Conditional Use Permit",
        "amount_usd": 2972, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat", "code_section": None, "applies_to_track": None,
        "notes": "City of Stanton Community Development Fee Schedule, effective 7/1/2026.",
    },
    {
        "permit_type": "conditional_use_permit", "fee_name": "Variance",
        "amount_usd": 2508, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat", "code_section": None, "applies_to_track": None,
        "notes": "City of Stanton Community Development Fee Schedule, effective 7/1/2026.",
    },
]

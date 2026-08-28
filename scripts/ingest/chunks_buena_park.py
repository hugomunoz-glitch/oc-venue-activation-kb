"""
Phase 4, Buena Park: two document-upload sources, both confirmed directly
fetchable. Buena Park's actual code (Ch. 19.1004, Temporary Uses and
Special Permits) is on ecode360.com and confirmed 403s automated fetches -
the fifth code-hosting platform (amlegal.com, ecode360.com x2, municode.com
x2) this project has hit the same wall on.

1. City of Buena Park Temporary Use Permit Application - real, current,
   and (unlike Brea/Tustin) its $545 fee agrees exactly with the separate
   Planning Department fee schedule - no discrepancy to flag this time.
2. City of Buena Park Planning Department Schedule of Fees (effective
   July 1, 2022, per City Council Resolution No. 14482) - read directly
   via pdftotext.
"""

CITY = "Buena Park"

DOCUMENTS = [
    {
        "title": "City of Buena Park Temporary Use Permit Application",
        "source_type": "permit_application",
        "code_chapter": "19.1004 (referenced)",
        "source_name": "City of Buena Park Community Development Department (buenapark.com)",
        "source_file": None,
        "source_key": "https://www.buenapark.com/departments/Building/TEMPORARY USE PERMIT APPLICATION.pdf",
        "retrieved_date": "2026-08-27",
        "effective_date": "2023-07-19",
        "effective_date_confidence": "stated_on_document",
        "notes": "Buena Park's actual code (Ch. 19.1004, Temporary Uses and Special Permits) is on ecode360.com and confirmed 403s automated fetches - this current, city-issued application form is used instead. Its $545 fee matches the separate Planning Department fee schedule exactly.",
        "chunks": [
            (
                "Temporary Use Permit: fee, deadline, and requirements",
                "A Buena Park Temporary Use Permit costs a $545.00 non-refundable filing fee. Applications must be submitted to the Director of Community Development a minimum of 30 days before the event date - incomplete applications cannot be accepted. The application asks whether the applicant has conducted the same type of activity/event in this or any neighboring city within the past six months, and requires two sets of site plans showing buildings, parking, and other site uses, with dimensions from the proposed use to the nearest building.",
            ),
        ],
    },
    {
        "title": "City of Buena Park Planning Department Schedule of Fees",
        "source_type": "fee_schedule",
        "code_chapter": None,
        "source_name": "City of Buena Park (buenapark.com)",
        "source_file": None,
        "source_key": "https://cms7files1.revize.com/buenaparkca/Document_center/City%20Departments/Community%20development/Form/PLANNING%20DIVISION%20SCHEDULE%20OF%20FEES%202022.pdf",
        "retrieved_date": "2026-08-27",
        "effective_date": "2022-07-01",
        "effective_date_confidence": "stated_on_document",
        "notes": "Read directly via pdftotext. Effective July 1, 2022 per City Council Resolution No. 14482 - the most current version findable; several fees (marked with footnote 1-3) are deposits covering a set number of planner hours, billed further if exceeded.",
        "chunks": [
            (
                "Conditional Use Permit and Variance fees",
                "Per Buena Park's Planning Department Schedule of Fees: Conditional Use Permit (Major) - $4,575 (a deposit covering up to 15 hours of planner time; additional hours billed at the fully-burdened hourly rate). Conditional Use Permit (Minor) - $2,885. Variance - $3,030. Zone Changes (map/text amendment) - $4,620 (deposit covering up to 18 hours). Zoning Verification Letter - $190.",
            ),
            (
                "Temporary use and miscellaneous fees",
                "Per the same fee schedule: Temporary Use Permit - $545 (matches the dedicated TUP application form exactly). Pennant and Banner Permit - $45. Fireworks Temporary Stand Permit - $1,010. Sign Permit - $255 (includes planning plan check). Short Term Rental Permit - $445 (3-year term), plus a $105 annual inspection fee.",
            ),
        ],
    },
]

FEE_ROWS = [
    {
        "permit_type": "special_event_permit", "fee_name": "Temporary Use Permit",
        "amount_usd": 545, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat", "code_section": "19.1004", "applies_to_track": None,
        "notes": "City of Buena Park - both the dedicated TUP application form and the Planning Department fee schedule agree on this figure.",
    },
    {
        "permit_type": "conditional_use_permit", "fee_name": "Conditional Use Permit (Major)",
        "amount_usd": None, "amount_usd_min": 4575, "amount_usd_max": None,
        "amount_type": "deposit", "code_section": None, "applies_to_track": None,
        "notes": "City of Buena Park Planning Department Schedule of Fees, effective July 1, 2022. Deposit covers up to 15 hours of planner time.",
    },
    {
        "permit_type": "conditional_use_permit", "fee_name": "Conditional Use Permit (Minor)",
        "amount_usd": 2885, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat", "code_section": None, "applies_to_track": None,
        "notes": "City of Buena Park Planning Department Schedule of Fees, effective July 1, 2022.",
    },
    {
        "permit_type": "conditional_use_permit", "fee_name": "Variance",
        "amount_usd": 3030, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat", "code_section": None, "applies_to_track": None,
        "notes": "City of Buena Park Planning Department Schedule of Fees, effective July 1, 2022.",
    },
]

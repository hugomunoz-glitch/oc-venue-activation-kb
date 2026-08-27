"""
Phase 4, La Habra: two document-upload sources, both confirmed directly
fetchable (unlike La Habra's actual municipal code, Ch. 18.65 Special Event
Permits, which is on ecode360.com and confirmed 403s automated fetches -
same story as amlegal.com elsewhere in this project).

1. City of La Habra Special Event Permit application, revised 1/21/26 -
   a genuinely rich primary source: clear numeric thresholds for what makes
   an event "large" vs "small," annual event-count caps, and structure/sign
   size limits, not just a bare form.
2. City of La Habra Master Schedule of Fees - confirmed via direct
   pdftotext extraction (not just a search-engine summary) for CUP/Variance/
   Zoning Verification Letter figures. Real finding: the search-engine
   summary quoted a CUP fee of $5,385, but the actual current master fee
   schedule states $6,759 - the primary-source PDF is used, not the
   secondhand summary.
"""

CITY = "La Habra"

DOCUMENTS = [
    {
        "title": "City of La Habra Special Event Permit Application",
        "source_type": "permit_application",
        "code_chapter": "18.65 (referenced)",
        "source_name": "City of La Habra Planning Division (lahabraca.gov)",
        "source_file": None,
        "source_key": "https://www.lahabraca.gov/DocumentCenter/View/209",
        "retrieved_date": "2026-08-27",
        "effective_date": "2026-01-21",
        "effective_date_confidence": "stated_on_document",
        "notes": "Revised 1/21/26 per the form's own header. La Habra's actual code chapter (18.65, Special Event Permits) is on ecode360.com and confirmed 403s automated fetches - this current, city-issued application form is used instead, since it states real operative thresholds directly.",
        "chunks": [
            (
                "Large vs. Small event classification and thresholds",
                "La Habra classifies a temporary outdoor special event as 'Large' if it meets ANY of: 250+ anticipated attendees, a duration of 5+ days, temporary removal of more than 25% of on-site parking, closure of one or more public streets, or use of an inflatable structure (e.g. a bounce house) larger than 200 square feet. Large events require a 90-day advance application, a $517 nonrefundable processing fee, and Planning Commission approval via public hearing. Anything not meeting those thresholds is a 'Small' event: a 30-day advance application and a $32 nonrefundable processing fee, approvable by city staff directly. Seasonal commercial sales like pumpkin patches and Christmas tree lots are governed separately under Municipal Code Section 5.04.610, not this permit.",
            ),
            (
                "Annual event-count restrictions",
                "No property in La Habra may host more than twelve (12) special events per calendar year, with a minimum of 30 days between each event. Special events that include outdoor sales are limited to four (4) per calendar year (also 30 days apart). A property owner wanting to exceed either limit must first obtain Conditional Use Permit approval from the Planning Commission.",
            ),
            (
                "Structure, sign, and other permit triggers",
                "Tents/canopies brought onto the property may require a separate temporary building permit depending on size - contact the Chief Building Official before submitting the Special Event Permit application. Advertising the event requires a temporary sign permit; signage is capped at a collective 45 square feet, or an inflatable sign up to 200 square feet with inspection - no human signs are permitted at any time. Applicants must show proof of ability to meet the insurance requirements in Municipal Code Section 18.65.100 (not itself part of this application form). Large events specifically require a list of every property owner within 300 feet of the event site.",
            ),
        ],
    },
    {
        "title": "City of La Habra Master Schedule of Fees",
        "source_type": "fee_schedule",
        "code_chapter": None,
        "source_name": "City of La Habra (lahabraca.gov)",
        "source_file": None,
        "source_key": "https://lahabraca.gov/DocumentCenter/View/11612/City-of-La-Habra-Master-Schedule-of-Fees-Adopted-6523",
        "retrieved_date": "2026-08-27",
        "effective_date": None,
        "effective_date_confidence": None,
        "notes": "Read directly via pdftotext, not summarized secondhand - a search-engine result had quoted a $5,385 CUP fee, which does not match this document's actual $6,759 figure. This fee schedule does not separately list special-event permit fees (those are set on the application form itself, referencing Account 113000-4409).",
        "chunks": [
            (
                "Conditional Use Permit and related discretionary planning fees",
                "Per La Habra's Master Schedule of Fees: Conditional Use Permit - $6,759. Condominium Conversion - $6,759. Zone Variance (Major) - $6,759. Zone Change - $8,293. Certificate of Compatibility - $6,759. CEQA Exemption - $458. Continuance (staff-requested additional review) - $563. Transportation Demand Management (Planning Commission) - $2,487. Zoning Verification Letter - $192/hour. Preliminary plan review - $192/hour.",
            ),
        ],
    },
]

# Structured fee rows for the `fee_schedules` table - the clean, unambiguous
# figures only (unlike Brea, there's no conflicting pair to flag here).
FEE_ROWS = [
    {
        "permit_type": "special_event_permit", "fee_name": "Special Event Permit - Small event",
        "amount_usd": 32, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat", "code_section": None, "applies_to_track": None,
        "notes": "City of La Habra Special Event Permit application, revised 1/21/26.",
    },
    {
        "permit_type": "special_event_permit", "fee_name": "Special Event Permit - Large event",
        "amount_usd": 517, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat", "code_section": None, "applies_to_track": None,
        "notes": "City of La Habra Special Event Permit application, revised 1/21/26. Also requires 90-day advance notice and Planning Commission public hearing approval.",
    },
    {
        "permit_type": "conditional_use_permit", "fee_name": "Conditional Use Permit",
        "amount_usd": 6759, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat", "code_section": "18.70.010", "applies_to_track": None,
        "notes": "City of La Habra Master Schedule of Fees.",
    },
    {
        "permit_type": "conditional_use_permit", "fee_name": "Zone Variance (Major)",
        "amount_usd": 6759, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat", "code_section": "18.70.010", "applies_to_track": None,
        "notes": "City of La Habra Master Schedule of Fees.",
    },
    {
        "permit_type": "conditional_use_permit", "fee_name": "Zone Change",
        "amount_usd": 8293, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat", "code_section": "18.70.010", "applies_to_track": None,
        "notes": "City of La Habra Master Schedule of Fees.",
    },
]

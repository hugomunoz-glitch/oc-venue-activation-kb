"""
Phase 4, Brea: two document-upload sources.

1. City of Brea Temporary Use Permit (TUP) Application, last updated April
   2026 (cityofbrea.gov/DocumentCenter/View/10707) - confirmed fetchable
   directly. Unlike Fullerton/Anaheim, Brea's actual municipal code chapter
   (20.72, Temporary Use Permit) is ALSO on amlegal.com and confirmed 403s
   automated fetches the same way - but this current, city-issued
   application form is a genuine primary source in its own right, with real
   procedural thresholds (insurance requirements, tent/generator/stage
   size triggers), so it's used here instead of requiring manual retrieval.
2. City of Brea planning/special-event fee pages (cityofbrea.gov/1363/Fees
   and /141/Planning-Fees) - confirmed fetchable directly.

Real, worth flagging: the general Fees page lists a "$55 Special
Event/Temporary Use Permit" fee, while the TUP Application form itself
(the more current, explicitly-dated April 2026 primary source) states an
$850 fee/deposit for a Temporary Use Permit specifically. These are kept
as two separate, honestly-labeled figures rather than silently reconciled -
Brea appears to run two tiers (a simpler "Special Events Permit" for
smaller events like company picnics, and the more involved TUP process for
larger ones), and which applies to a given activation depends on facts this
KB doesn't have a firm rule for yet.
"""

CITY = "Brea"

DOCUMENTS = [
    {
        "title": "City of Brea Temporary Use Permit (TUP) Application",
        "source_type": "permit_application",
        "code_chapter": "20.72 (referenced)",
        "source_name": "City of Brea Planning Division (cityofbrea.gov)",
        "source_file": None,
        "source_key": "https://cityofbrea.gov/DocumentCenter/View/10707/Temporary-Use-Permit-Application-PDF",
        "retrieved_date": "2026-08-27",
        "effective_date": "2026-04-01",
        "effective_date_confidence": "stated_on_document",
        "notes": "Last updated April 1, 2026 per the form's own footer. Brea's municipal code Chapter 20.72 (Temporary Use Permit) is hosted on amlegal.com and confirmed 403s automated fetches, same as Fullerton/Anaheim's code - this current, city-issued application form is used as the primary source instead, since it states real operative thresholds and requirements directly.",
        "chunks": [
            (
                "TUP application deadline and fee",
                "A Temporary Use Permit (TUP) application must be submitted to Brea's Planning Division at least 45 days before the proposed event date. There is a deposit of $850 for large events and a flat fee of $850 for small events (other fees may apply). A complete application requires the application form, a separate event description, and a site plan; it is not considered submitted until required fees are paid. Note: Brea's general city fee schedule separately lists a $55 'Special Event/Temporary Use Permit' fee, which appears to apply to a simpler, distinct 'Special Events Permit' track (e.g. company picnics, car shows) rather than this TUP process - this KB does not have a firm rule for which category a given event falls into.",
            ),
            (
                "TUP insurance requirements",
                "For a Brea TUP event located on public property (e.g. a public street or sidewalk), the applicant must provide a certificate of insurance naming the City of Brea as an additional insured, with coverage stated as primary and non-contributory and a waiver of subrogation rights. Required coverage: Commercial General Liability (always required) - $1,000,000 per occurrence / $2,000,000 aggregate for bodily injury, personal injury, and property damage. Workers' Compensation and Employer's Liability (if employees are working the event) - $1,000,000 per occurrence for employer's liability, plus statutory California workers' comp. Liquor Liability (if alcohol is supplied/sold) - $1,000,000 per occurrence / $2,000,000 aggregate. Automobile Liability (if automobiles are part of the event) - $2,000,000 per occurrence / $2,000,000 aggregate.",
            ),
            (
                "TUP thresholds requiring additional permits: structures, tents, generators",
                "Brea's TUP application flags several size/type thresholds that trigger additional permits beyond the TUP itself. Stages taller than 30 inches require a building permit plus structural design/calculations from a licensed CA engineer, submitted at least 3 weeks before the event. Tents/canopies larger than 120 square feet need anchorage details; tents with support posts 12+ feet apart, 10+ feet high, and 600+ square feet require full structural design/calculations and a building permit. Tents/canopies over 400 total square feet separately require a Fire Department permit and inspection. Generators with a fuel supply over 5 gallons require a Fire Department Special Events Permit. On-site cooking always requires a Fire Department Special Events Permit. Installing a temporary power pole requires a building permit. All of these sub-permits must be applied for at least 3 weeks before the event date.",
            ),
            (
                "TUP requirements: business license, alcohol, public property, food donation",
                "Every vendor a Brea TUP applicant hires must obtain a City of Brea business license tax certificate before the TUP can be approved. Alcohol service requires an alcohol management plan, security information, and the applicant's own ABC permit(s) from the California Department of Alcoholic Beverage Control. Any use of public property (street, alley, sidewalk) requires a separate Public Works Encroachment Permit, applied for at least 30 days before the event with a site plan and traffic control plan. Events expecting to serve edible food to over 2,000 people per day must have an agreement with an edible food recovery organization and donate edible food per SB 1383.",
            ),
        ],
    },
    {
        "title": "City of Brea Planning and Special Event Fees",
        "source_type": "fee_schedule",
        "code_chapter": None,
        "source_name": "City of Brea (cityofbrea.gov)",
        "source_file": None,
        "source_key": "https://www.cityofbrea.gov/1363/Fees",
        "retrieved_date": "2026-08-27",
        "effective_date": None,
        "effective_date_confidence": None,
        "notes": "General city fee schedule page, cross-referenced against the separate Planning Fees page (cityofbrea.gov/141/Planning-Fees) for discretionary planning fees.",
        "chunks": [
            (
                "Special event / inspection fees (general fee schedule)",
                "Per Brea's general city fee schedule: Special Event/Temporary Use Permit fee: $55. Special Event Inspection Fee: $111 per hour. Special Event After Hours Inspection Fee: $167 per hour. Annual & Operational Fire Permit: $55 per permit. See the separate TUP Application chunk for the $850 fee/deposit stated on the actual current Temporary Use Permit form - these two figures are not reconciled in this KB (see that chunk's note).",
            ),
            (
                "Discretionary planning fees (deposit-based)",
                "Brea's discretionary planning applications are billed as minimum deposits against actual staff time, not flat fees: Conditional Use Permit - $2,000 minimum deposit. Zone Variance - $2,000 minimum deposit. Zoning Verification Letter - $327 minimum deposit. Staff time is billed at $175/hour for Management staff and $109/hour for Technical staff; unused deposit funds are returned after project completion.",
            ),
        ],
    },
]

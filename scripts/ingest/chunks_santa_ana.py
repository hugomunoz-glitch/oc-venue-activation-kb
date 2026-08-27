"""
Phase 4, Santa Ana: two document-upload sources, both confirmed directly
fetchable. Santa Ana's actual municipal code (Ch. 41, Article V - CUPs,
Variances) is on municode.com and confirmed 403s automated fetches - the
same pattern seen on every other code-hosting platform in this project so
far (amlegal.com, ecode360.com, now municode.com). City-issued PDFs
substitute again.

1. City of Santa Ana Event Permit Application (posted 2025, referencing a
   2023 form revision still in current use) - real event-size tiers,
   advance-notice windows, and insurance requirements.
2. City of Santa Ana Planning Division FY 2026-2027 Fee Schedule - read
   directly via pdftotext, current and comprehensive (CUP, Variance,
   Zoning Verification, and dozens of other planning fees).

Real, worth flagging: unlike Anaheim/Brea/La Habra, Santa Ana's Special
Event Permit fee is NOT a fixed published number - the application form's
own fee section is blank, filled in per-application by city staff
(reviewed by Police, Reservations Admin/Athletics, and Parks Facility/Film
departments). Treated as a genuine case-by-case gap, same honesty
precedent as Fullerton's OCFA chunk, rather than forcing in an estimated
range some third-party site quoted.
"""

CITY = "Santa Ana"

DOCUMENTS = [
    {
        "title": "City of Santa Ana Event Permit Application",
        "source_type": "permit_application",
        "code_chapter": None,
        "source_name": "City of Santa Ana Special Events Office (santa-ana.gov)",
        "source_file": None,
        "source_key": "https://storage.googleapis.com/proudcity/santaanaca/2022/03/2023_Event-Permit-Application_Fillable.pdf",
        "retrieved_date": "2026-08-27",
        "effective_date": None,
        "effective_date_confidence": None,
        "notes": "Santa Ana's actual code (Ch. 41, special event provisions) is on municode.com and confirmed 403s automated fetches - this current, city-issued application form is used instead. The fee section on this form is blank (filled in per-application by staff), not a fixed published number - see the fee chunk for why that's treated as a genuine gap, not guessed at.",
        "chunks": [
            (
                "Event size tiers and application deadlines",
                "Santa Ana classifies events into three tiers: Minor (up to 100 attendees), Moderate (101-1,000 attendees), and Major (1,001+ attendees). Minor and Moderate events require applications and site plans submitted 45 business days to 6 months before the first event date. Major events require 90 business days to 1 year before the first event date. Late or incomplete applications are not accepted. Applications go to specialevents@santa-ana.org.",
            ),
            (
                "Insurance requirements",
                "Santa Ana requires the permittee to maintain commercial general liability insurance naming the City of Santa Ana, its officers, employees, agents, volunteers, and representatives as additional insureds, covering bodily/personal injury and property damage arising from the permittee's event operations (including vehicle-related acts). The City's Risk Management office reviews each application individually and determines the required coverage amount - stated as 'likely to be in the vicinity of $1,000,000 to $5,000,000 per occurrence,' with the City reserving the right to adjust based on the specific risk, prior events, or other circumstances. This insurance must be primary and non-contributing with any other coverage.",
            ),
            (
                "Event Permit fee: determined per-application, not a fixed published amount",
                "Santa Ana's Event Permit Application itself does not state a fixed fee amount - the fee section (Security Deposit, Permit Fee(s), Police Overtime Fees, Meter Parking Fees, Other) is left blank on the form, to be filled in per-application after review by the Santa Ana Police Department, Reservations Admin/Athletics, and Parks Facility/Film divisions as applicable to the specific event. This is a genuine case-by-case determination, not a published number this knowledge base can cite - do not present any third-party estimate of this fee as if it were an official published figure.",
            ),
        ],
    },
    {
        "title": "City of Santa Ana Planning Division Fee Schedule (FY 2026-2027)",
        "source_type": "fee_schedule",
        "code_chapter": None,
        "source_name": "City of Santa Ana Planning Division (santa-ana.gov)",
        "source_file": None,
        "source_key": "https://storage.googleapis.com/proudcity/santaanaca/2026/03/planning-division-fees-fy-2026-2027-b085a783.pdf",
        "retrieved_date": "2026-08-27",
        "effective_date": "2026-07-01",
        "effective_date_confidence": "stated_on_document",
        "notes": "Read directly via pdftotext. Note: a 7% technology fee applies per transaction on top of these figures, and a separate 2.5% card-processing fee applies to credit/debit payments starting July 1, 2026 - neither is baked into the amounts below.",
        "chunks": [
            (
                "Conditional Use Permit and related discretionary planning fees",
                "Per Santa Ana's FY 2026-2027 Planning Division Fee Schedule: Conditional Use Permit (General) - $7,485. Conditional Use Permit - ABC License (with public notice/comment included) - $6,687. Conditional Use Permit - Planned Residential Development - $11,769. Variance Application - $7,269. Minor Exception Application - $3,579. Zone Change (Amendment Application) - $6,978. Zoning Verification Letter - $784. Zoning Interpretation Letter - $696. Appeal (Applicant) - $5,637; Appeal (Non-Applicant) - $763. A 7% technology fee applies per transaction on top of these figures.",
            ),
            (
                "Temporary/seasonal use and sign-related fees",
                "Per the same fee schedule: Land Use Certificate - Seasonal/Temporary Event (covers fiesta & rummage sales, parking lot sales, auctions) - $539 per certificate. Land Use Certificate - Carnival, Music, Arcade, ABC, Category 3 & 4 Entertainment Permit - $963 per certificate. Temporary Sign (Banner) Permit - $220. Temporary Trailer Permit - $843. Entertainment Permit (Category 2, amplified music/no dancing, ends by midnight) - $539; Category 3 (with dancing, ends by midnight) - $963; Category 4 (with dancing, past midnight) - $963.",
            ),
        ],
    },
]

FEE_ROWS = [
    {
        "permit_type": "conditional_use_permit", "fee_name": "Conditional Use Permit (General)",
        "amount_usd": 7485, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat", "code_section": None, "applies_to_track": None,
        "notes": "City of Santa Ana Planning Division Fee Schedule, FY 2026-2027. Plus 7% technology fee per transaction.",
    },
    {
        "permit_type": "conditional_use_permit", "fee_name": "Variance Application",
        "amount_usd": 7269, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat", "code_section": None, "applies_to_track": None,
        "notes": "City of Santa Ana Planning Division Fee Schedule, FY 2026-2027. Plus 7% technology fee per transaction.",
    },
    {
        "permit_type": "special_event_permit", "fee_name": "Land Use Certificate - Seasonal/Temporary Event",
        "amount_usd": 539, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat", "code_section": None, "applies_to_track": None,
        "notes": "City of Santa Ana Planning Division Fee Schedule, FY 2026-2027. This is distinct from the Event Permit Application's own fee, which is determined case-by-case (not fixed) by the Special Events Office.",
    },
]

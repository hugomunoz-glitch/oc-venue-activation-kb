"""
Phase 4, Tustin: three document-upload sources, all confirmed directly
fetchable from tustinca.org (Tustin's actual municipal code, on
municode.com, confirmed 403s automated fetches - the fourth code-hosting
platform in this project to do so, after amlegal.com/ecode360.com/an
earlier municode.com hit for Santa Ana).

1. Temporary Use Permit application - a real, current city-issued form.
2. Large Gathering Use Permit application - same, for bigger events.
3. 2026-2027 Comprehensive Schedule of Fees - the city's general fee
   resolution.

Real, worth flagging: the Large Gathering Use Permit's own fee (stated on
the application form itself, printed directly on the form) is $1,103
deposit, but the Comprehensive Fee Schedule's own line for "Large Gathering
Permit" states $2,243 deposit. Both are genuine, current, city-issued
documents - this is kept as an unreconciled discrepancy (same precedent as
Brea's $55/$850 pair) rather than silently picking one.
"""

CITY = "Tustin"

DOCUMENTS = [
    {
        "title": "City of Tustin Temporary Use Permit Application",
        "source_type": "permit_application",
        "code_chapter": None,
        "source_name": "City of Tustin Community Development Department (tustinca.org)",
        "source_file": None,
        "source_key": "https://www.tustinca.org/DocumentCenter/View/633/Temporary-Use-Permit--General-PDF",
        "retrieved_date": "2026-08-27",
        "effective_date": None,
        "effective_date_confidence": None,
        "notes": "Tustin's actual code (municode.com) confirmed 403s automated fetches. The form itself shows a crossed-out $263.00 fee replaced by $709.00 - treated as the current fee, matching the $709 figure in the separate Comprehensive Fee Schedule.",
        "chunks": [
            (
                "Temporary Use Permit: fee and processing time",
                "A Tustin Temporary Use Permit costs $709 (this figure appears on both the application form itself, which shows a corrected/updated fee, and the city's separate Comprehensive Schedule of Fees). Allow a minimum of 10 business days for processing. The completed application, including a site plan showing all tables, booths, tents, rides, and other items with their locations, goes to the Community Development Department (300 Centennial Way, Tustin, CA 92780).",
            ),
            (
                "Temporary Use Permit: standard conditions (tents, alcohol, food, noise)",
                "Standard conditions on a Tustin Temporary Use Permit: all merchandise/equipment/displays must be removed and the site restored by midnight on the permit's expiration date. Tents over 200 square feet must be flame retardant; tents over 400 square feet require Orange County Fire Authority approval and inspection, and tents must maintain a minimum 20-foot fire lane between rows of parking. On-site food service needs Orange County Environmental Health approval. No alcohol may be served without both a City of Tustin permit and a State ABC permit. A valid City of Tustin business license is required for any business operating under the permit. All activity must comply with the Tustin Noise Ordinance - no amplified speaking, music, or singing unless specifically approved. The permit is discretionary, not a right, and may be revoked or the event ended at the discretion of the Police Watch Commander or Community Development Director.",
            ),
        ],
    },
    {
        "title": "City of Tustin Large Gathering Use Permit Application",
        "source_type": "permit_application",
        "code_chapter": None,
        "source_name": "City of Tustin Community Development Department (tustinca.org)",
        "source_file": None,
        "source_key": "https://www.tustinca.org/DocumentCenter/View/627/Large-Gathering-Use-Permit-PDF",
        "retrieved_date": "2026-08-27",
        "effective_date": None,
        "effective_date_confidence": None,
        "notes": "The application form itself states a $1,103 deposit fee, but the city's separate Comprehensive Schedule of Fees states $2,243 deposit for the same permit - both are genuine, current, city-issued figures, kept unreconciled rather than guessed at (same precedent as Brea's $55 vs. $850 special-event fee pair).",
        "chunks": [
            (
                "Large Gathering Use Permit: fee, insurance, and processing time",
                "A Tustin Large Gathering Use Permit's fee is stated as a $1,103 deposit directly on the application form - but the city's separate Comprehensive Schedule of Fees lists the same 'Large Gathering Permit' line at $2,243 deposit. Both figures are genuine and current; this knowledge base does not have a rule for which one actually applies at time of filing. The application requires a Certificate of Insurance naming the City of Tustin as additionally insured for $1,000,000. Allow a minimum of 10 business days for processing.",
            ),
            (
                "Large Gathering Use Permit: same standard conditions as Temporary Use Permit",
                "The Large Gathering Use Permit carries the same standard conditions as Tustin's Temporary Use Permit: removal/restoration by midnight on the expiration date, tent size thresholds (200 sq ft flame-retardant, 400 sq ft needs OCFA approval/inspection, 20-foot fire lane), Orange County Health Care Agency approval for food stands, no alcohol without City + State ABC permits, valid business license required, compliance with the Noise Ordinance, and discretionary revocation authority for the Police Watch Commander or Community Development Director.",
            ),
        ],
    },
    {
        "title": "City of Tustin Comprehensive Schedule of Fees (2026-2027)",
        "source_type": "fee_schedule",
        "code_chapter": None,
        "source_name": "City of Tustin (tustinca.org)",
        "source_file": None,
        "source_key": "https://www.tustinca.org/DocumentCenter/View/19836/2026-Comprehensive-Schedule-of-Fees",
        "retrieved_date": "2026-08-27",
        "effective_date": "2026-01-01",
        "effective_date_confidence": "inferred_from_document_title",
        "notes": "Read directly via pdftotext. Nearly all Planning Division fees here are structured as deposits against actual staff time, not flat fees.",
        "chunks": [
            (
                "Discretionary planning fees",
                "Per Tustin's 2026-2027 Comprehensive Schedule of Fees: Conditional Use Permit (Planning Commission) - $5,875 deposit. Variance (Planning Commission) - $5,875 deposit; Variance (Zoning Administrator) - $1,175 deposit. Zone Change - $11,749 deposit. Master Sign Plan - Conditional Use Permit - $2,937 deposit. Use Determination - $587 deposit. Temporary Sign Permit - $129 (flat request fee). Time Extension (for temporary use permits) - $182 request fee.",
            ),
        ],
    },
]

FEE_ROWS = [
    {
        "permit_type": "special_event_permit", "fee_name": "Temporary Use Permit",
        "amount_usd": 709, "amount_usd_min": None, "amount_usd_max": None,
        "amount_type": "flat", "code_section": None, "applies_to_track": None,
        "notes": "City of Tustin Temporary Use Permit application / Comprehensive Schedule of Fees - both agree on this figure.",
    },
    {
        "permit_type": "conditional_use_permit", "fee_name": "Conditional Use Permit (Planning Commission)",
        "amount_usd": None, "amount_usd_min": 5875, "amount_usd_max": None,
        "amount_type": "deposit", "code_section": None, "applies_to_track": None,
        "notes": "City of Tustin Comprehensive Schedule of Fees, 2026-2027 - deposit against actual staff time.",
    },
    {
        "permit_type": "conditional_use_permit", "fee_name": "Variance (Planning Commission)",
        "amount_usd": None, "amount_usd_min": 5875, "amount_usd_max": None,
        "amount_type": "deposit", "code_section": None, "applies_to_track": None,
        "notes": "City of Tustin Comprehensive Schedule of Fees, 2026-2027 - deposit against actual staff time.",
    },
]

"""
Structured, section-aware chunk data for Fullerton Phase 1 ingestion.

Chunking rule (per the project's instructions doc): split municipal code by
section heading (each numbered section = one chunk), and split fee tables by
row (each fee line item = one chunk) rather than by raw character count, so a
dollar amount never gets separated from the permit type and city it belongs to.

Each document dict below becomes one row in `documents`; each entry in its
"chunks" list becomes one row in `chunks`, tagged with document_id + city_id
by the generator script.
"""

CITY = "Fullerton"

DOCUMENTS = [
    {
        "title": "Chapter 15.58: Special Events on Private Property",
        "source_type": "municipal_code",
        "code_chapter": "15.58",
        "source_name": "Fullerton Municipal Code",
        "source_file": "source-docs/fullerton/municipal-code/chapter-15.58-special-events-private-property.pdf",
        "retrieved_date": "2026-08-14",
        "effective_date": None,
        "effective_date_confidence": None,
        "notes": "Functions as Fullerton's private-property TUP-equivalent chapter. Cross-references Chapter 8.71 (public property) and Chapter 9.12 (public parks).",
        "chunks": [
            ("§15.58.010", "INTENT AND PURPOSE. The intent of this chapter is to identify special events and to specify the requirements and provisions for their approval regardless of the proposed location or zone classification. The requirements and provisions established for each special event are intended to ensure the general safety, health and welfare of the community and to ensure that the temporary operation of the special event will be a compatible activity for the neighborhood in which it is located. (Ord. 2982, passed 2001)"),
            ("§15.58.020", "DEFINITIONS. SPECIAL EVENT (PRIVATE PROPERTY): An event that is conducted outdoors on private property by a private entity and is open to the general public (admitted or invited). Examples include: carnivals, festivals, car show, circus, auction or a similar kind of temporary outdoor exhibition or performance. SPECIAL EVENT (PUBLIC PROPERTY): An event that is conducted outdoors on public streets, public parking lots, public parks or public facilities. (Ord. 2982, passed 2001; Ord. 3232, passed 2016)"),
            ("§15.58.025", "APPLICABILITY. (A) Special events (private property) shall be subject to the review and approval process specified in this chapter. (B) Special events (public property) shall be subject to review and approval from the Public Works Department and/or Parks and Recreation Department. (C) A temporary commercial activity, such as a sidewalk or parking lot sale, shall be subject to the provisions of §15.58.095 and shall not be considered a special event for purposes of this chapter. (Ord. 3232, passed 2016)"),
            ("§15.58.030", "PERMIT REQUIRED. (A) A special event shall be prohibited on private property unless a properly issued special event permit is first issued to the applicant. An application for a special event on private property shall be filed with the Community and Economic Development Department. (B) An application for a special event in a public park shall be filed with the Director of Parks and Recreation in accordance with Chapter 9.12 of this code. (C) An application for a special event using a public street and/or a public facility shall be filed with the Director of Public Works in accordance with Chapter 8.71 of this code. (Ord. 2982, passed 2001; Ord. 3232, passed 2016)"),
            ("§15.58.040", "APPLICATION FOR PERMIT AND FEES. (A) A complete application for a special event permit must be received by the Community and Economic Development Department no later than 30 days before the scheduled special event. The City Council may, by resolution, set appropriate fees for the filing of the application. (B) An application shall be on a form provided by the city and shall provide, at minimum: (1) the applicant's identity and a responsible contact person; (2) a site plan showing event boundaries, temporary buildings/structures (stages, tents, canopies, toilets, vendor's booths), adjacent land uses, fire hydrants and fire access lanes, toilets/trash/water facilities, and on-site parking; (3) a description of the event including hours of operation, expected number of participants/assistants/workers/spectators, security measures, parking management/signage, and setup/cleanup plan; (4) written owner approval if off-site parking is proposed. (Ord. 2982, passed 2001; Ord. 3232, passed 2016)"),
            ("§15.58.050", "REQUIREMENTS AND PROVISIONS FOR APPROVAL OF PERMIT. Minimum conditions include: boundary signage; a 20-foot setback from residential property lines for loud equipment/stages/rides; maintained on-site circulation and parking access; sanitation/trash cleanup within one day of event completion; hours of operation limited to 10:00 a.m.-11:00 p.m. Monday-Saturday and 11:00 a.m.-9:00 p.m. Sunday; construction/dismantling/delivery noise prohibited between 8:00 p.m. and 7:00 a.m.; documentation that required building/electrical/plumbing permits and inspections are complete; adequate parking arrangements; and compliance with any additional city-specified conditions. (Ord. 2982, passed 2001; Ord. 3232, passed 2016)"),
            ("§15.58.060", "PROCEDURE FOR REVIEW OF APPLICATION. (A) A decision to approve a special event permit on private property is made by the Director of Community and Economic Development or their designee. (B) Before acting, the Director shall consult other city departments, review compliance history at the location, and mail notification to adjacent properties no later than five days before the event (including off-site parking locations if applicable), containing a map, event description, and contact information for comments before/during/after the event. (Ord. 2982, passed 2001; Ord. 3232, passed 2016)"),
            ("§15.58.070", "DECISION ON THE APPLICATION AND APPEAL OF DECISION. Within ten business days after receipt of a complete application, the Director of Community and Economic Development or their designee shall notify the applicant in writing of a decision to approve, conditionally approve, or deny the request (with reasons stated if denied). (Ord. 2982, passed 2001; Ord. 3232, passed 2016)"),
            ("§15.58.080", "SUSPENSION OF PERMIT. The Director of Community and Economic Development and/or the Chief of Police shall suspend a special event permit if the applicant violated a permit condition or law, or threatened public peace/safety/welfare or unreasonably interfered with nearby property use/enjoyment. Written notice of suspension is final and conclusive; all permitted activity must cease immediately upon notice. (Ord. 2982, passed 2001; Ord. 3232, passed 2016)"),
            ("§15.58.090", "BUSINESS LICENSES. A special event permit under this chapter controls over any business licenses issued under Chapter 4.02. Only vendors with prior written approval from the special event permit holder may operate within the event venue (approval shall not be unreasonably withheld). The permit holder may charge vendors a reasonable registration fee. (Ord. 2982, passed 2001)"),
            ("§15.58.095", "TEMPORARY COMMERCIAL USE ON PRIVATE PROPERTY. Covers intermittent/seasonal/promotional temporary commercial uses (e.g. Christmas tree lot, pumpkin patch, agricultural stand, sidewalk/parking-lot sale) as distinct from a 'special event' under this chapter. Key limits: maximum 90 calendar days from setup to full removal/cleanup (extension requires Planning Commission approval per Chapter 15.76); not allowed on R-1/R-1P zoned property with a habitable structure; must front an arterial or collector street, no residential-street access; requires written property-owner consent; requires Community and Economic Development and/or Fire Department permits plus a business license; at least six off-street patron parking spaces required; signage capped at 50 sq ft total, 8 ft max height. Open-air marketing activities (sidewalk/parking-lot sales) by an existing on-site merchant are capped at 5 days in duration and one such activity per 30-day period. (Ord. 3232, passed 2016)"),
        ],
    },
    {
        "title": "Chapter 8.71: Special Events on Public Streets and Public Facilities",
        "source_type": "municipal_code",
        "code_chapter": "8.71",
        "source_name": "Fullerton Municipal Code",
        "source_file": "source-docs/fullerton/municipal-code/chapter-8.71-special-events-public-property.pdf",
        "retrieved_date": "2026-08-14",
        "effective_date": None,
        "effective_date_confidence": None,
        "notes": "Parallel track to Chapter 15.58 for events on public streets/facilities, administered by Public Works (or Parks & Recreation for public parks, per Chapter 9.12). Cross-referenced by 15.58.030(C) and 15.58.025(B).",
        "chunks": [
            ("§8.71.010", "INTENT AND PURPOSE. Identifies special events and specifies requirements/provisions for their approval when the proposed location is on a public street or public facility, to ensure general safety, health and welfare of the community and compatibility with the surrounding neighborhood. (Ord. 2972, passed 2000)"),
            ("§8.71.020", "DEFINITIONS. BLOCK PARTY: an event where all or part of a public residential street is temporarily closed to normal vehicular traffic (a type of SPECIAL EVENT). PUBLIC FACILITY: any city-maintained/owned facility other than a city park or open space area (a public parking area/structure qualifies; public schools are exempt except for non-school-related programs). PUBLIC STREET: any publicly maintained street, road, highway, alley, sidewalk, parkway, bridge, culvert drain, right-of-way, etc. SPECIAL EVENT: an outdoor event open to the general public (admitted or invited), e.g. carnival, festival, tent/car show, circus, parade, auction, rally, or similar temporary outdoor exhibition/performance. (Ord. 2972, passed 2000)"),
            ("§8.71.030", "PERMIT REQUIRED. (A) A special event on a public street/facility requires a permit filed with the Director of Public Works. (B) A special event in a city park/open space area is filed with the Director of Parks and Recreation under Chapter 9.12. (C) A special event on private property is filed with the Director of Development Services under Chapter 15.58. (D) No permit is required for events the city/Redevelopment Agency co-sponsors, subject to findings: the organization is IRS-recognized nonprofit; a majority of its members/officers are city residents (waivable for other local-government co-sponsors); the organization agrees to pay at least half of extra costs (including extra police); adequate city/Agency funds are budgeted; and the event is compatible with the Redevelopment Agency's Central Business District goals. (Ord. 2972, passed 2000)"),
            ("§8.71.040", "APPLICATION FOR PERMIT AND FEES. (A) Application must be on file with the Director of Public Works at least 90 days before the event (waivable at the Director's discretion, or referable to City Council). (B) The City Council may, by resolution, set appropriate filing fees. (C) The application (on a city-provided form) must include, at minimum: applicant/responsible-contact identity; a venue diagram showing boundaries and temporary structures/stages/booths; event type and duration; expected participant/assistant/worker/spectator counts; security measures and directional devices; toilets/trash/water facilities; and a petition with adjacent business-owner/resident signatures showing support. (Ord. 2972, passed 2000)"),
            ("§8.71.050", "REQUIREMENTS AND PROVISIONS FOR APPROVAL OF PERMIT. Minimum provisions: (1) a refundable security deposit and filing fee per City Council resolution; (2) event confined to a signed, bounded area; (3) traffic control/detour plans as Public Works requires; (4) sanitation/trash cleanup immediately after the event; (5) compatible duration/hours; (6) Public Works approval of temporary structure locations; (7) adequate attendee parking; (8) agreed noise restrictions; (9) liability insurance/bonds satisfactory to the city plus an indemnification clause; (10) a Police Chief determination of whether police attendance is needed (officer costs borne by the applicant if so, based on attendee count/age, activity nature, site, conflict potential, and department experience with similar events); (11) if alcohol is served/sold, Police Chief satisfaction with security measures plus a State ABC daily license and host liquor liability insurance per city Risk Management; (12) if food is prepared/sold, a commercial temporary food permit (or nonprofit exemption) from the OC Health Care Agency, Environmental Health division. (Ord. 2654, passed 1988; Ord. 2972, passed 2000)"),
            ("§8.71.060", "PROCEDURE FOR REVIEW OF APPLICATION. Decided by the Director of Public Works after consulting other city departments; adjacent owners/residents may be notified. If the venue is within a parking district, the Board of Parking Place Commissioners holds a public hearing and may impose conditions; otherwise the application is routed to the Chief of Police, Fire Chief, and Director of Development Services for review/recommended conditions. Approval findings: the event is run by a nonprofit/community organization/local business based in the city; it promotes the city, residents, or businesses; it's consistent with public peace/health/safety; and it won't unreasonably interfere with adjacent property use. Permit issuance requires fees paid, bonds posted, and insurance certificates on file. (Ord. 2972, passed 2000)"),
            ("§8.71.070", "DECISION ON APPLICATION AND APPEAL OF DECISION. Director-level decisions: written response within 15 days (approve/conditionally approve/deny with reasons); appeal within 10 days goes to the Board of Parking Place Commissioners (hearing within 30 days), then to City Council/City Clerk within 10 more days if still contested. Board-level decisions (parking-district venues): review within 45 days of submittal, appeal within 10 days to City Council. City Council appeal hearings occur within 30 days of the written appeal and are final. (Ord. 2972, passed 2000)"),
            ("§8.71.080", "SUSPENSION OF PERMIT. The Director of Public Works and/or Chief of Police shall suspend a special event permit for violation of permit conditions or law, or if the event's conduct threatens public peace/safety/welfare or unreasonably interferes with nearby property use. Suspension notice is final and conclusive; all permitted activity must cease immediately. (Ord. 2972, passed 2000)"),
            ("§8.71.090", "BUSINESS LICENSES. A special event permit under this chapter controls over business licenses issued under §4.02.010. Only vendors with prior written approval from the permit holder may operate within the venue (approval not to be unreasonably withheld); the permit holder may charge vendors a reasonable registration fee. (Ord. 2972, passed 2000)"),
        ],
    },
    {
        "title": "Chapter 15.70: Conditional Use Permits",
        "source_type": "municipal_code",
        "code_chapter": "15.70",
        "source_name": "Fullerton Municipal Code",
        "source_file": "source-docs/fullerton/municipal-code/chapter-15.70-conditional-use-permits.pdf",
        "retrieved_date": "2026-08-14",
        "effective_date": None,
        "effective_date_confidence": None,
        "notes": "Relevant to whether a venue exceeding its currently-approved event count needs a CUP amendment rather than relying on repeated Special Event Permits (test question 1/7 territory).",
        "chunks": [
            ("§15.70.010", "INTENT AND PURPOSE. The Planning Commission may grant a conditional use permit (CUP) for matters this title requires to be reviewed, but only if findings under §15.70.040(D) can be made. Purpose: ensure compatibility between the proposed use and other existing/potential uses in the area, and account for variations in noise, smoke, dust, fumes, vibration, odors and hazards. (Ord. 2982, passed 2001; Ord. 3026, passed 2003; Ord. 3232, passed 2016)"),
            ("§15.70.020", "APPLICATION AND FEES. A CUP application may be filed only by (or with written authorization from) the legal property owner. It must be made on a Community and Economic Development Department form and include: a completed preliminary environmental description form; maps/drawings/plans/tabulations describing the request; and the required fee, as prescribed by resolution of the City Council. NOTE: no dollar amount for this fee appears in the ordinance text itself - it is set by a separate City Council fee resolution not yet located in this knowledge base. (Ord. 2982, passed 2001; Ord. 3131, passed 2009; Ord. 3232, passed 2016)"),
            ("§15.70.030", "PUBLIC NOTIFICATION OF PLANNING COMMISSION HEARING. Public hearing notice for a CUP is provided in accordance with §15.76.040. (Ord. 2982, passed 2001; Ord. 3131, passed 2009; Ord. 3232, passed 2016)"),
            ("§15.70.040", "PLANNING COMMISSION DECISION AND REQUIRED FINDINGS. Decided by majority vote (a tie denies the CUP); the order becomes final 10 days after the resolution unless appealed under §15.70.060. The Commission may impose conditions covering yards/buffers, fences/walls, parking/ingress-egress, street dedications, landscaping, noise/nuisance regulation, operating-hours regulation, signage, bonding for removal, and other orderly-development conditions. Required findings to grant: (1) the use is conditionally permitted in the zone and meets zoning standards; (2) it's consistent with the General Plan/applicable specific plan; (3) as conditioned, it won't be detrimental to health/safety/welfare of nearby residents/workers; (4) it demonstrates compliance with the design criteria in §15.47.060. A CUP tied to a vesting tentative map is processed concurrently and runs with the map's life. (Ord. 2982, passed 2001; Ord. 3232, passed 2016)"),
            ("§15.70.050", "TIME LIMITS. A CUP order becomes final 10 working days after the resolution unless appealed under §15.70.060. A CUP isn't valid until all approval conditions are met and released by the Director of Community and Economic Development. It automatically becomes void after 24 months from approval if the owner hasn't acted to erect/build/alter/move/maintain the use (or after 24 consecutive months of inactivity) - preparation of plans, financing, or ownership changes don't count as 'action.' Extensions may be granted at the initial hearing or requested per §15.76.120. (Ord. 2982, passed 2001; Ord. 3232, passed 2016)"),
            ("§15.70.060", "APPEALS. An appeal of a Planning Commission CUP decision must be filed with Community and Economic Development within 10 working days (next working day if the deadline falls on a weekend/holiday), with a letter stating reasons and an appeal fee per City Council resolution. Filing an appeal stays the Commission's order. The City Council must hold a public hearing within 60 days of the appeal, announce its decision by resolution within 20 days of the hearing, and mail the resolution within 10 days of adoption. City Council acts by majority vote of the full Council (a tie denies the CUP). (Ord. 2982, passed 2001; Ord. 3026, passed 2003; Ord. 3131, passed 2009; Ord. 3232, passed 2016)"),
            ("§15.70.070-080", "RESERVED. Both sections repealed by Ord. 3131."),
            ("§15.70.090", "REVOCATION. If a CUP condition is violated, the use becomes a nuisance, or the use is abandoned for 6 months, Community and Economic Development serves the owner a notice of intent to revoke, detailing the property, owner/occupants, CUP file number and issuance date, authorized use, the specific non-compliance, and hearing/appearance rights. The Planning Commission then holds a hearing and must find: (1) specific conditions weren't complied with by a certain date/period; and (2) the non-compliance was knowing/intentional/reckless, or (if not) wasn't corrected by the hearing date. (Ord. 2982, passed 2001; Ord. 3232, passed 2016)"),
        ],
    },
    {
        "title": "Application for a Special Event Permit - Fee Schedule (Private Property and/or Public Property)",
        "source_type": "fee_schedule",
        "code_chapter": None,
        "source_name": "City of Fullerton Special Event Permit Application",
        "source_file": "source-docs/fullerton/permit-applications/special-event-permit-application-with-fees.pdf",
        "retrieved_date": "2026-08-14",
        "effective_date": "2026-03-10",
        "effective_date_confidence": "inferred_from_form_footer",
        "notes": "Form footer reads 'UPDATED 03-10-26'; treated as the fee table's effective/last-updated date until a more authoritative fee resolution date is found. Jointly administered: Community Development handles the private-property track (Ch. 15.58), Public Works Engineering handles the public-property track (Ch. 8.71).",
        "chunks": [
            ("Fee: Community Development Permit Issuance Fee", "Community Development Permit Issuance Fee: $100 flat fee. Applies to the private-property Special Event Permit track under Fullerton Municipal Code §15.58.040. Account code 10345-4614 (3221)."),
            ("Fee: Public Works Engineering Permit Issuance Fee", "Public Works Engineering Permit Issuance Fee: $1,000 or $2,000 (two-tier flat fee - the form doesn't state the criteria distinguishing which events fall in which tier). Applies to the public-property Special Event Permit track under Fullerton Municipal Code §8.71.040. Account code 10322-4260 (E2020E/E2020D)."),
            ("Fee: Public Works Engineering Inspection and Plan Check Fee", "Public Works Engineering Inspection and Plan Check Fee: $161 flat fee. Applies to the public-property Special Event Permit track under Fullerton Municipal Code §8.71.040. Account code 10322-4614 (E2030A)."),
            ("Fee: Joint Fire Dept. & Building Dept. Inspection (business hours)", "Joint Inspection from Fire Department and Building Department, during business hours: $300 flat fee. Applies to both the private-property and public-property Special Event Permit tracks. Split 50% to account 10345-4220 (3210) and 50% to account 10251-4640 (7037)."),
            ("Fee: Joint Fire Dept. & Building Dept. Inspection (after-hours/weekends)", "Joint Inspection from Fire Department and Building Department, after-hours or on weekends: $450 flat fee. Applies to both the private-property and public-property Special Event Permit tracks."),
            ("Fee: Police Department Staffing", "Police Department Staffing: billed hourly after the event, only if police officers are determined necessary per Fullerton Municipal Code §8.71.050(A)(10). No flat rate is given on this form for the hourly rate. Applies to both permit tracks, situationally. Account code 10277-4730 (7253)."),
            ("Fee: Refundable Deposit", "Refundable Deposit: $1,000 or $2,000, required for the public-property Special Event Permit track under Fullerton Municipal Code §8.71.050(A)(1), except waived for block parties. Account code 10-2420 (2000)."),
        ],
    },
]

# Structured fee rows for the `fee_schedules` table - mirrors the chunk text
# above but as queryable numeric data for exact-amount lookups.
FEE_ROWS = [
    {
        "permit_type": "Special Event Permit (private property)",
        "fee_name": "Community Development Permit Issuance Fee",
        "amount_usd": 100,
        "amount_usd_min": None,
        "amount_usd_max": None,
        "amount_type": "flat",
        "code_section": "FMC 15.58.040",
        "applies_to_track": "private_property",
        "notes": "Account code 10345-4614 (3221).",
    },
    {
        "permit_type": "Special Event Permit (public property)",
        "fee_name": "Public Works Engineering Permit Issuance Fee",
        "amount_usd": None,
        "amount_usd_min": 1000,
        "amount_usd_max": 2000,
        "amount_type": "tiered_flat",
        "code_section": "FMC 8.71.040",
        "applies_to_track": "public_property",
        "notes": "Two-tier amount; tier-determining criteria not stated on the form. Account code 10322-4260 (E2020E/E2020D).",
    },
    {
        "permit_type": "Special Event Permit (public property)",
        "fee_name": "Public Works Engineering Inspection and Plan Check Fee",
        "amount_usd": 161,
        "amount_usd_min": None,
        "amount_usd_max": None,
        "amount_type": "flat",
        "code_section": "FMC 8.71.040",
        "applies_to_track": "public_property",
        "notes": "Account code 10322-4614 (E2030A).",
    },
    {
        "permit_type": "Special Event Permit (both tracks)",
        "fee_name": "Joint Inspection from Fire Dept. & Building Dept. (business hours)",
        "amount_usd": 300,
        "amount_usd_min": None,
        "amount_usd_max": None,
        "amount_type": "flat",
        "code_section": None,
        "applies_to_track": "both",
        "notes": "Split 50% to 10345-4220 (3210); 50% to 10251-4640 (7037).",
    },
    {
        "permit_type": "Special Event Permit (both tracks)",
        "fee_name": "Joint Inspection from Fire Dept. & Building Dept. (after-hours/weekends)",
        "amount_usd": 450,
        "amount_usd_min": None,
        "amount_usd_max": None,
        "amount_type": "flat",
        "code_section": None,
        "applies_to_track": "both",
        "notes": None,
    },
    {
        "permit_type": "Special Event Permit (both tracks)",
        "fee_name": "Police Department Staffing",
        "amount_usd": None,
        "amount_usd_min": None,
        "amount_usd_max": None,
        "amount_type": "hourly_billed_after_event",
        "code_section": "FMC 8.71.050(A)(10)",
        "applies_to_track": "both",
        "notes": "Only charged if police officers are determined necessary. No flat/hourly rate given on this form. Account code 10277-4730 (7253).",
    },
    {
        "permit_type": "Special Event Permit (public property)",
        "fee_name": "Refundable Deposit",
        "amount_usd": None,
        "amount_usd_min": 1000,
        "amount_usd_max": 2000,
        "amount_type": "refundable_deposit",
        "code_section": "FMC 8.71.050(A)(1)",
        "applies_to_track": "public_property",
        "notes": "Waived for block parties. Account code 10-2420 (2000).",
    },
]

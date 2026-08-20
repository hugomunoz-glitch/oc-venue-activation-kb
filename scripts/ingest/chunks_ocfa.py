"""
Live-website source: OC Fire Authority's Special Event Permit page. This is
the KB's "live website" ingestion method (re-fetchable, changes over time),
distinct from the document-upload PDFs and the Google Places API pull.

No fee_schedules rows here: OCFA's own page states fees "vary based on event
type, size, public safety impact" with no fixed schedule published - that's
a genuine unknown, not a number to force into a structured table. Captured
in the chunk text instead, matching the project's honesty-about-gaps rule.
"""

CITY = "Fullerton"

DOCUMENTS = [
    {
        "title": "OC Fire Authority: Special Event Permits (Prevention Field Services)",
        "source_type": "website",
        "source_name": "Orange County Fire Authority (ocfa.org)",
        "source_key": "https://ocfa.org/about-us/departments/community-risk-reduction/prevention-field-services/",
        "retrieved_date": "2026-08-20",
        "effective_date": None,
        "effective_date_confidence": None,
        "notes": "Live page content, re-fetchable on a schedule per the project's live-website ingestion method. Applies county-wide, including Fullerton, per the instructions doc's note that OCFA 'interacts differently with each city's own process' rather than being uniform.",
        "chunks": [
            ("Overview and activities requiring a permit", "OC Fire Authority (OCFA) Prevention Field Services manages special event permits for temporary activities or equipment presenting elevated hazards, for events with invited guests or the general public on public or private property. Activities requiring a permit include: tents and canopies; carnivals and fairs; haunted houses and mazes; fireworks and special effects; open flames (bonfires, pit barbecues, candles); and non-primary facility uses (e.g. a warehouse hosting a concert). This directly covers an outdoor wedding reception tent or a gym hosting a non-primary-use pop-up event."),
            ("Application timeline and expedite fee", "Applications must be submitted at least two weeks in advance through OCFA's online Public Services Portal (publicservices.ocfa.org). An additional 50% expedite fee charge applies if the complete application package arrives fewer than 10 working days before the event. OCFA does not state a base fee amount on this page - total fees are determined case by case after evaluation (see Costs)."),
            ("Costs", "OCFA states that special event permit fees vary based on event type, size, public safety impact, and whether fire code permits apply - the total fee is determined only after OCFA evaluates the specific application, with no fixed published base rate. Payment (credit card, electronic check, or cash at OCFA Headquarters) is due before the event date, the first inspection, or within six weeks of invoicing, whichever comes first."),
            ("Guideline S-01 and event-type attachments", "Guideline S-01 governs special event permit processing and generic information requirements. Event-specific attachments exist for: Attachment A - tents, canopies, and membrane structures (the one most relevant to an outdoor wedding reception); Attachment B - fireworks displays; Attachment C - haunted houses and grad night events; Attachment D - pumpkin patches and tree lots; Attachment E - parades and races; Attachment F - mall and vehicle displays; Attachment G - bonfires and pit barbecues; Attachment H - carnivals and fairs. All documents are available through OCFA's online portal."),
            ("Regional contact", "OCFA Prevention Field Services maintains five regional offices; general information line is (714) 573-6254."),
        ],
    },
]

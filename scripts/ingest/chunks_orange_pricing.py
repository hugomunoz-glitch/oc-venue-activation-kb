"""
Phase 4, Orange: real venue pricing via Zola. Unlike several other cities in
this phase, Orange's own Zola search actually surfaced many genuine local
results - consistent with Old Towne Orange being a real, active wedding-
venue district (part of why Orange was proposed as the ninth city in the
first place). One worth a specific double-check: "Hotel Fera Anaheim, a
DoubleTree by Hilton" is branded with Anaheim's name but is confirmed via
multiple independent sources to actually be at 100 The City Dr S, Orange,
CA - a useful reminder that a venue's own brand name doesn't tell you its
city any more than the search query does.
"""

CITY = "Orange"

VENUES = [
    {
        "name": "The Estate OC",
        "slug": "the-estate-oc",
        "starting_price": 13000,
        "capacity_min": None,
        "capacity_max": None,
        "tier": "All-inclusive",
    },
    {
        "name": "The Vintage Rose",
        "slug": "the-vintage-rose",
        "starting_price": 10000,
        "capacity_min": None,
        "capacity_max": None,
        "tier": "All-inclusive",
    },
    {
        "name": "Hotel Fera Anaheim, a DoubleTree by Hilton",
        "slug": "hotel-fera-anaheim-a-doubletree-by-hilton",
        "starting_price": 7000,
        "capacity_min": None,
        "capacity_max": None,
        "tier": "All-inclusive",
    },
    {
        "name": "Fletcher Courtyards at American Family Living Ministries",
        "slug": "fletcher-courtyards-at-american-family-living-ministries",
        "starting_price": 6000,
        "capacity_min": None,
        "capacity_max": None,
        "tier": "Select services",
    },
    {
        "name": "La Petite Rose",
        "slug": "la-petite-rose",
        "starting_price": 6000,
        "capacity_min": None,
        "capacity_max": None,
        "tier": "Select services",
    },
    {
        "name": "The Villa | Weddings & Events",
        "slug": "the-villa-weddings-and-events",
        "starting_price": 5325,
        "capacity_min": None,
        "capacity_max": None,
        "tier": "Select services",
    },
    {
        "name": "The French Estate",
        "slug": "the-french-estate",
        "starting_price": 4500,
        "capacity_min": None,
        "capacity_max": None,
        "tier": "Select services",
    },
    {
        "name": "Fireside Farm OC",
        "slug": "fireside-farm-oc",
        "starting_price": 1500,
        "capacity_min": None,
        "capacity_max": None,
        "tier": "Raw space",
    },
    {
        "name": "Orange Hill Restaurant",
        "slug": "orange-hill-restaurant",
        "starting_price": 1500,
        "capacity_min": None,
        "capacity_max": None,
        "tier": "Raw space",
    },
]


def _content(v: dict) -> str:
    price_str = f"Starting price: ${v['starting_price']:,}." if v["starting_price"] else "No starting price published."
    cap_str = f"Guest capacity: up to {v['capacity_max']}." if v["capacity_max"] else ""
    return (
        f"{v['name']} (Orange, CA) - wedding/event venue. {price_str} {cap_str} "
        f"Service tier: {v['tier']}. Source: Zola marketplace listing (\"starting at\" price - "
        f"a real market signal, not a guaranteed quote; actual cost varies by date, season, and "
        f"negotiated add-ons)."
    )


DOCUMENTS = [
    {
        "title": f"{v['name']} - Zola Venue Listing",
        "source_type": "website",
        "source_name": "Zola (zola.com)",
        "source_key": f"https://www.zola.com/wedding-vendors/wedding-venues/{v['slug']}",
        "retrieved_date": "2026-08-27",
        "effective_date": "2026-08-27",
        "effective_date_confidence": "inferred_from_retrieval",
        "notes": "Marketplace listing price - re-fetchable, but should be treated as a snapshot. Address-verified as located in Orange.",
        "chunks": [(v["name"], _content(v))],
    }
    for v in VENUES
]

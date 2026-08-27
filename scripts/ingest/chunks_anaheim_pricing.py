"""
Phase 4, Anaheim: real venue pricing via Zola, same role as chunks_zola.py
played for Fullerton in Phase 3 - fills the market-rate benchmark gap.

Zola's Anaheim search pulls in the same cross-city contamination risk
already seen twice in this project (chunks_zola.py's own docstring, and the
Phase 2 Google Places bug found and fixed in Phase 4): each venue below was
individually address-verified as actually in Anaheim before inclusion.
"White House Banquets & Event Center" also appears in this KB's Google
Places pull (rating/category only, no price) - this listing is what
supplies its actual starting price.
"""

CITY = "Anaheim"

VENUES = [
    {
        "name": "White House Banquets & Event Center",
        "slug": "the-white-house-event-center",
        "starting_price": 9500,
        "capacity_min": None,
        "capacity_max": None,
        "tier": "All-inclusive",
    },
    {
        "name": "The Grand Theater",
        "slug": "the-grand-theater",
        "starting_price": 10676,
        "capacity_min": None,
        "capacity_max": 600,
        "tier": "All-inclusive",
    },
    {
        "name": "The Anaheim Hotel",
        "slug": "the-anaheim-hotel",
        "starting_price": 3500,
        "capacity_min": None,
        "capacity_max": None,
        "tier": "Select services",
    },
    {
        "name": "The Westin Anaheim Resort",
        "slug": "the-westin-anaheim-resort",
        "starting_price": 8000,
        "capacity_min": None,
        "capacity_max": None,
        "tier": "All-inclusive",
    },
    {
        "name": "Anaheim Hills Golf Course",
        "slug": "anaheim-hills-golf-course",
        "starting_price": 9999,
        "capacity_min": None,
        "capacity_max": None,
        "tier": "Select services",
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
        "name": "Anaheim Marriott Suites",
        "slug": "anaheim-marriott-suites",
        "starting_price": 99,
        "capacity_min": None,
        "capacity_max": None,
        "tier": "Select services",
    },
]


def _content(v: dict) -> str:
    price_str = f"Starting price: ${v['starting_price']:,}." if v["starting_price"] else "No starting price published."
    cap_str = f"Guest capacity: up to {v['capacity_max']}." if v["capacity_max"] else ""
    caveat = ""
    if v["name"] == "Anaheim Marriott Suites":
        caveat = (" Note: this figure is unusually low relative to comparable full-service venues here - "
                   "likely a per-person or off-peak minimum rather than a comparable base venue rental rate; "
                   "treat this one price with extra caution rather than as a like-for-like comparison.")
    return (
        f"{v['name']} (Anaheim, CA) - wedding/event venue. {price_str} {cap_str} "
        f"Service tier: {v['tier']}. Source: Zola marketplace listing (\"starting at\" price - "
        f"a real market signal, not a guaranteed quote; actual cost varies by date, season, and "
        f"negotiated add-ons).{caveat} This is the market-rate benchmark data referenced when comparing "
        f"activation revenue to permit/insurance/staffing costs."
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
        "notes": "Marketplace listing price - re-fetchable, but should be treated as a snapshot; prices/availability change. Address-verified as located in Anaheim (Zola's search radius includes neighboring cities).",
        "chunks": [(v["name"], _content(v))],
    }
    for v in VENUES
]

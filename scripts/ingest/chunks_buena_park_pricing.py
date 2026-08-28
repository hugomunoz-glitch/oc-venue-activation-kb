"""
Phase 4, Buena Park: real venue pricing via Zola. Two address-verified
genuine Buena Park venues found: Claim Jumper - Buena Park (7971 Beach
Blvd) and Los Coyotes Country Club (8888 Los Coyotes Dr).
"""

CITY = "Buena Park"

VENUES = [
    {
        "name": "Los Coyotes Country Club",
        "slug": "los-coyotes-country-club",
        "starting_price": 7500,
        "capacity_min": None,
        "capacity_max": None,
        "tier": "Select services",
    },
    {
        "name": "Claim Jumper - Buena Park",
        "slug": "claim-jumper-buena-park",
        "starting_price": 1000,
        "capacity_min": None,
        "capacity_max": None,
        "tier": "Raw space",
    },
]


def _content(v: dict) -> str:
    price_str = f"Starting price: ${v['starting_price']:,}." if v["starting_price"] else "No starting price published."
    cap_str = f"Guest capacity: up to {v['capacity_max']}." if v["capacity_max"] else ""
    return (
        f"{v['name']} (Buena Park, CA) - wedding/event venue. {price_str} {cap_str} "
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
        "notes": "Marketplace listing price - re-fetchable, but should be treated as a snapshot. Address-verified as located in Buena Park.",
        "chunks": [(v["name"], _content(v))],
    }
    for v in VENUES
]

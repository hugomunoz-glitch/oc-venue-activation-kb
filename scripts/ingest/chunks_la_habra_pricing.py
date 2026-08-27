"""
Phase 4, La Habra: real venue pricing. Zola's "La Habra, CA" search mostly
returned neighboring-city venues (Irvine, Costa Mesa, Whittier, Fullerton,
Buena Park, Rancho Santa Fe, San Clemente); a second candidate, "The Garden
Room," had an address conflict across sources (La Habra in one listing,
Garden Grove in another) and was excluded rather than guessed at. Only
Westridge Golf Club had a clean, consistently-confirmed La Habra address
across multiple independent sources.
"""

CITY = "La Habra"

VENUES = [
    {
        "name": "Westridge Golf Club",
        "slug": "westridge-golf-club",
        "starting_price": 7230,
        "capacity_min": None,
        "capacity_max": 300,
        "tier": "Select services",
    },
]


def _content(v: dict) -> str:
    price_str = f"Starting price: ${v['starting_price']:,} (for 50 guests; a separate $1,700 ceremony setup fee applies)." if v["starting_price"] else "No starting price published."
    cap_str = f"Guest capacity: up to {v['capacity_max']}." if v["capacity_max"] else ""
    return (
        f"{v['name']} (La Habra, CA) - country club wedding/event venue. {price_str} {cap_str} "
        f"Service tier: {v['tier']}. Source: marketplace listing (\"starting at\" price - "
        f"a real market signal, not a guaranteed quote; actual cost varies by date, season, and "
        f"negotiated add-ons). Note: this is the only address-verified wedding/event venue found "
        f"actually within La Habra's city limits - most marketplace searches for \"La Habra\" wedding "
        f"venues surface venues in neighboring cities instead."
    )


DOCUMENTS = [
    {
        "title": f"{v['name']} - Venue Listing",
        "source_type": "website",
        "source_name": "Wedding marketplace listing",
        "source_key": f"https://www.zola.com/wedding-vendors/wedding-venues/{v['slug']}",
        "retrieved_date": "2026-08-27",
        "effective_date": "2026-08-27",
        "effective_date_confidence": "inferred_from_retrieval",
        "notes": "Marketplace listing price - re-fetchable, but should be treated as a snapshot. Address confirmed as 1400 S La Habra Hills Dr, La Habra, CA 90631 across multiple independent sources.",
        "chunks": [(v["name"], _content(v))],
    }
    for v in VENUES
]

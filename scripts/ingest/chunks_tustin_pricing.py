"""
Phase 4, Tustin: real venue pricing. Another extreme case, same as Brea:
Zola's "Tustin, CA" search returned zero venues actually in Tustin - every
result was in Orange, Santa Ana, Irvine, Costa Mesa, Rancho Santa Fe, or
San Clemente. A separate marketplace (Wedding Spot) surfaced exactly one
genuine Tustin venue, address-verified: Prego Mediterranean, 2409 Park Ave,
Tustin, CA 92782 (The District at Tustin Legacy).
"""

CITY = "Tustin"

VENUES = [
    {
        "name": "Prego Mediterranean",
        "slug": "prego-mediterranean-tustin",
        "starting_price": 2462,
        "capacity_min": None,
        "capacity_max": None,
        "tier": "Select services",
    },
]


def _content(v: dict) -> str:
    price_str = f"Starting price: ${v['starting_price']:,} (for 50 guests)." if v["starting_price"] else "No starting price published."
    cap_str = f"Guest capacity: up to {v['capacity_max']}." if v["capacity_max"] else ""
    return (
        f"{v['name']} (Tustin, CA) - restaurant event space, at The District at Tustin Legacy. "
        f"{price_str} {cap_str} Service tier: {v['tier']}. Source: Wedding Spot marketplace listing "
        f"(\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by "
        f"date, season, and negotiated add-ons). Note: this is the only address-verified wedding/event "
        f"venue found actually within Tustin's city limits - Zola's own \"Tustin\" search returned zero "
        f"venues actually located in Tustin, all in neighboring cities instead."
    )


DOCUMENTS = [
    {
        "title": f"{v['name']} - Venue Listing",
        "source_type": "website",
        "source_name": "Wedding Spot (wedding-spot.com)",
        "source_key": f"https://www.wedding-spot.com/venue/{v['slug']}",
        "retrieved_date": "2026-08-27",
        "effective_date": "2026-08-27",
        "effective_date_confidence": "inferred_from_retrieval",
        "notes": "Marketplace listing price - re-fetchable, but should be treated as a snapshot. Address confirmed as 2409 Park Ave, Tustin, CA 92782 across multiple independent sources.",
        "chunks": [(v["name"], _content(v))],
    }
    for v in VENUES
]

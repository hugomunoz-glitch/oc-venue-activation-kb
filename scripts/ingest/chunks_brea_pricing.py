"""
Phase 4, Brea: real venue pricing. Worth stating plainly rather than
padding the count: Brea is a small city with very little dedicated
wedding/event venue inventory of its own. Zola's "Brea, CA" search returned
zero venues actually located in Brea - every single result was in a
neighboring city (Fullerton, Anaheim, Orange, Yorba Linda, Buena Park,
Costa Mesa, and further out) - the most extreme case of the cross-city
search-radius contamination seen anywhere in this project so far. Eventective's
listing had the same problem (179 of 180 "Brea, CA" results were actually
elsewhere). Only one address-verified, genuinely-in-Brea venue with a
published price was found: Embassy Suites by Hilton Brea - North Orange
County (900 E Birch St, Brea, CA 92821).
"""

CITY = "Brea"

VENUES = [
    {
        "name": "Embassy Suites by Hilton Brea - North Orange County",
        "slug": "embassy-suites-brea-north-orange-county",
        "starting_price": 2000,
        "capacity_min": None,
        "capacity_max": 400,
        "tier": "Select services",
    },
]


def _content(v: dict) -> str:
    price_str = f"Starting price: ${v['starting_price']:,} (for 50 guests; scales up to ${5500:,} depending on guest count)." if v["starting_price"] else "No starting price published."
    cap_str = f"Guest capacity: up to {v['capacity_max']}." if v["capacity_max"] else ""
    return (
        f"{v['name']} (Brea, CA) - hotel event space, one of the only address-verified "
        f"wedding/event venues actually located within Brea's city limits. {price_str} {cap_str} "
        f"Service tier: {v['tier']}. Source: Eventective marketplace listing (\"starting at\" price - "
        f"a real market signal, not a guaranteed quote; actual cost varies by date, season, and "
        f"negotiated add-ons). Note: Brea has very little dedicated wedding/event venue inventory "
        f"of its own - most marketplace searches for \"Brea\" wedding venues actually surface venues "
        f"in neighboring cities (Fullerton, Anaheim, Orange, Yorba Linda), which are excluded here."
    )


DOCUMENTS = [
    {
        "title": f"{v['name']} - Eventective Venue Listing",
        "source_type": "website",
        "source_name": "Eventective (eventective.com)",
        "source_key": f"https://www.eventective.com/brea-ca/wedding-venues/{v['slug']}",
        "retrieved_date": "2026-08-27",
        "effective_date": "2026-08-27",
        "effective_date_confidence": "inferred_from_retrieval",
        "notes": "Marketplace listing price - re-fetchable, but should be treated as a snapshot. Address-verified as located in Brea; this is the only venue found actually within Brea's city limits after excluding neighboring-city results.",
        "chunks": [(v["name"], _content(v))],
    }
    for v in VENUES
]

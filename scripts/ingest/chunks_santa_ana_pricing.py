"""
Phase 4, Santa Ana: real venue pricing via Zola. Santa Ana's own search
radius still pulled in Irvine/Costa Mesa/Orange/Anaheim/Fountain Valley/
Garden Grove/Rancho Santa Fe/San Clemente results - each of the 7 kept here
was individually address-verified, including two that needed real
double-checking despite their Santa Ana price-list placement: "Tustin
Hills Racquet Club" (name suggests Tustin, confirmed address is actually
11782 Simon Ranch Rd, Santa Ana) and "Orange County Mining Co." (confirmed
10000 Crawford Canyon Rd, Santa Ana, not Orange).
"""

CITY = "Santa Ana"

VENUES = [
    {
        "name": "Ebell Club of Santa Ana",
        "slug": "ebell-club-of-santa-ana",
        "starting_price": 15000,
        "capacity_min": None,
        "capacity_max": None,
        "tier": "All-inclusive",
    },
    {
        "name": "Hotel Zessa, a DoubleTree by Hilton",
        "slug": "hotel-zessa-a-doubletree-by-hilton",
        "starting_price": 5000,
        "capacity_min": None,
        "capacity_max": None,
        "tier": "All-inclusive",
    },
    {
        "name": "Heritage Museum of Orange County",
        "slug": "heritage-museum-of-orange-county",
        "starting_price": 3000,
        "capacity_min": None,
        "capacity_max": None,
        "tier": "Raw space",
    },
    {
        "name": "Lakeside Orange County Airport Hotel",
        "slug": "lakeside-orange-county-airport-hotel",
        "starting_price": 1799,
        "capacity_min": None,
        "capacity_max": None,
        "tier": "Select services",
    },
    {
        "name": "McFadden Public Market",
        "slug": "mcfadden-public-market",
        "starting_price": 1500,
        "capacity_min": None,
        "capacity_max": None,
        "tier": "Raw space",
    },
    {
        "name": "Tustin Hills Racquet Club",
        "slug": "tustin-hills-racquet-club",
        "starting_price": 1000,
        "capacity_min": None,
        "capacity_max": None,
        "tier": "Raw space",
    },
    {
        "name": "Orange County Mining Co.",
        "slug": "orange-county-mining-co",
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
        f"{v['name']} (Santa Ana, CA) - wedding/event venue. {price_str} {cap_str} "
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
        "notes": "Marketplace listing price - re-fetchable, but should be treated as a snapshot. Address-verified as located in Santa Ana (Zola's search radius includes neighboring cities).",
        "chunks": [(v["name"], _content(v))],
    }
    for v in VENUES
]

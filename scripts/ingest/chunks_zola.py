"""
Live-website source: Zola's Fullerton wedding-venue marketplace pages -
real starting prices, guest capacity, and service tier. This fills the
market-rate gap flagged in the Phase 3 baseline evaluation (Q8) after the
originally-planned Peerspace/Splacer source turned out to be bot-blocked.

Zola's Fullerton search returns venues from neighboring cities too (its
search radius, not a strict city filter) - each one below was individually
address-verified as actually located in Fullerton before inclusion, per
this project's city-scoped-retrieval principle. Excluded on verification:
University Club (Irvine), The Harper (Costa Mesa), The Colony House,
The Wooden Pearl, The Stuffed Potato, The Ebell Club (all Anaheim), The
Secret Garden At Rancho Santa Fe, San Clemente Shore (not Fullerton at all).

source_confidence is "medium" throughout: marketplace "starting at" prices
are a real signal but not a guaranteed quote (venues negotiate, seasons/
dates vary) - same caveat the instructions doc's data model calls for.
"""

CITY = "Fullerton"

VENUES = [
    {
        "name": "The Muckenthaler Mansion",
        "slug": "muckenthaler-mansion",
        "starting_price": 23000,
        "capacity_min": None,
        "capacity_max": 1500,
        "tier": "All-inclusive",
    },
    {
        "name": "Summit House Restaurant",
        "slug": "summit-house-restaurant",
        "starting_price": 7000,
        "capacity_min": None,
        "capacity_max": 250,
        "tier": "All-inclusive",
    },
    {
        "name": "The Villa Del Sol",
        "slug": "the-villa-del-sol",
        "starting_price": 4950,
        "capacity_min": None,
        "capacity_max": 200,
        "tier": "Select services",
    },
    {
        "name": "Fullerton Community Center",
        "slug": "fullerton-community-center",
        "starting_price": 2200,
        "capacity_min": None,
        "capacity_max": 300,
        "tier": "Raw space",
    },
    {
        "name": "Golleher Alumni House at Cal State Fullerton",
        "slug": "golleher-alumni-house-at-cal-state-fullerton",
        "starting_price": 1400,
        "capacity_min": None,
        "capacity_max": 250,
        "tier": "Raw space",
    },
    {
        "name": "City of Fullerton - Hunt Branch Library",
        "slug": "city-of-fullerton-hunt-branch-library",
        "starting_price": 1199,
        "capacity_min": None,
        "capacity_max": 200,
        "tier": "Raw space",
    },
    {
        "name": "Coyote Hills Golf Course",
        "slug": "coyote-hills-golf-course",
        "starting_price": None,
        "capacity_min": None,
        "capacity_max": 275,
        "tier": "Select services",
    },
]


def _content(v: dict) -> str:
    price_str = f"Starting price: ${v['starting_price']:,}." if v["starting_price"] else "No starting price published."
    cap_str = f"Guest capacity: up to {v['capacity_max']}." if v["capacity_max"] else ""
    return (
        f"{v['name']} (Fullerton, CA) - wedding/event venue. {price_str} {cap_str} "
        f"Service tier: {v['tier']}. Source: Zola marketplace listing (\"starting at\" price - "
        f"a real market signal, not a guaranteed quote; actual cost varies by date, season, and "
        f"negotiated add-ons). This is the market-rate benchmark data referenced when comparing "
        f"activation revenue to permit/insurance/staffing costs."
    )


DOCUMENTS = [
    {
        "title": f"{v['name']} - Zola Venue Listing",
        "source_type": "website",
        "source_name": "Zola (zola.com)",
        "source_key": f"https://www.zola.com/wedding-vendors/wedding-venues/{v['slug']}",
        "retrieved_date": "2026-08-20",
        "effective_date": "2026-08-20",
        "effective_date_confidence": "inferred_from_retrieval",
        "notes": "Marketplace listing price - re-fetchable, but should be treated as a snapshot; prices/availability change. Address-verified as located in Fullerton (Zola's search radius includes neighboring cities).",
        "chunks": [(v["name"], _content(v))],
    }
    for v in VENUES
]

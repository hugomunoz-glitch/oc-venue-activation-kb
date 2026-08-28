"""
Phase 4, Stanton: real venue pricing. A third extreme case (after Brea and
Tustin): Zola's "Stanton, CA" search returned zero venues actually in
Stanton. A second candidate found via a different search ("Diamond Seafood
Palace") had a conflicting address across sources (Stanton in one listing,
Garden Grove in Google Places' own data) and was excluded, same as La
Habra's "Garden Room" case. The one genuine, unambiguous Stanton venue
found is the city's own Civic Center/City Hall (7800 Katella Ave), which
rents its ~4,000 sq ft ballroom for private events - but no published
starting price was found. Recorded honestly as a real venue with a real
gap, not a guessed number.
"""

CITY = "Stanton"

VENUES = [
    {
        "name": "Stanton Civic Center (City Hall Ballroom)",
        "slug": None,
        "starting_price": None,
        "capacity_min": None,
        "capacity_max": None,
        "square_footage": 4000,
        "tier": "Raw space",
    },
]


def _content(v: dict) -> str:
    return (
        f"{v['name']} (Stanton, CA) - a city-owned facility at 7800 Katella Ave available for private "
        f"event rental, with a ballroom of approximately {v['square_footage']:,} square feet. "
        f"No starting price is published online; contact the city's Community Services division "
        f"(CommunityServices@StantonCA.gov, (714) 890-4270) for current rental rates. This is the only "
        f"address-verified event venue found actually within Stanton's city limits - marketplace "
        f"searches for \"Stanton\" wedding/event venues (Zola, Eventective) return zero results "
        f"genuinely located in Stanton, and one other candidate found (Diamond Seafood Palace) had a "
        f"conflicting address across sources (Stanton vs. Garden Grove) and was excluded rather than "
        f"guessed at."
    )


DOCUMENTS = [
    {
        "title": f"{v['name']} - Facility Rental",
        "source_type": "website",
        "source_name": "City of Stanton (stantonca.gov)",
        "source_key": "https://www.stantonca.gov/business_detail_T14_R81.php",
        "retrieved_date": "2026-08-27",
        "effective_date": "2026-08-27",
        "effective_date_confidence": "inferred_from_retrieval",
        "notes": "City-owned facility, not a marketplace listing - no 'starting at' price was found published anywhere; treated as a genuine gap, not estimated.",
        "chunks": [(v["name"], _content(v))],
    }
    for v in VENUES
]

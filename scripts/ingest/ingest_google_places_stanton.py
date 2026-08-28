"""
Phase 4 API ingestion: Stanton wedding-venue and gym listings from Google
Places API (New). Mirrors the established address-verification filter.

Usage:
    source .venv/bin/activate
    python ingest_google_places_stanton.py
    psql "$DATABASE_URL" -f ingest_google_places_stanton.sql
"""

import datetime
import os
import sys

import requests

from common import embed, sql_literal, vector_literal

GOOGLE_PLACES_API_KEY = os.environ["GOOGLE_PLACES_API_KEY"]

CITY = "Stanton"
RETRIEVED_DATE = datetime.date.today().isoformat()

SEARCH_QUERIES = [
    "wedding venue Stanton CA",
    "gym Stanton CA",
    "banquet hall event venue Stanton CA",
]


def search_places(query: str) -> list[dict]:
    resp = requests.post(
        "https://places.googleapis.com/v1/places:searchText",
        headers={
            "Content-Type": "application/json",
            "X-Goog-Api-Key": GOOGLE_PLACES_API_KEY,
            "X-Goog-FieldMask": (
                "places.id,places.displayName,places.formattedAddress,"
                "places.rating,places.userRatingCount,places.priceLevel,places.types"
            ),
        },
        json={"textQuery": query},
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json().get("places", [])


def summarize(place: dict) -> str:
    name = place.get("displayName", {}).get("text", "Unknown")
    address = place.get("formattedAddress", "address unknown")
    types = ", ".join(place.get("types", [])) or "uncategorized"
    rating = place.get("rating")
    rating_count = place.get("userRatingCount")
    price_level = place.get("priceLevel")

    parts = [f"{name} is located at {address}. Google Places categories: {types}."]
    if rating is not None:
        rating_str = f"Google rating: {rating}/5"
        if rating_count:
            rating_str += f" ({rating_count} ratings)"
        parts.append(rating_str + ".")
    if price_level:
        parts.append(f"Google price level: {price_level}.")
    parts.append(
        "Source: Google Places API (New), a venue-directory signal only - "
        "ratings and category tags, not an actual rental rate or activation fee."
    )
    return " ".join(parts)


def main():
    by_place_id: dict[str, dict] = {}
    skipped = []
    for query in SEARCH_QUERIES:
        print(f"Searching: {query}", file=sys.stderr)
        for place in search_places(query):
            place_id = place["id"]
            if place_id in by_place_id:
                continue
            address = place.get("formattedAddress", "")
            if f", {CITY}," not in address and not address.startswith(f"{CITY},"):
                skipped.append((place.get("displayName", {}).get("text", "?"), address))
                continue
            by_place_id[place_id] = place

    print(f"Found {len(by_place_id)} unique places across {len(SEARCH_QUERIES)} queries", file=sys.stderr)
    if skipped:
        print(f"Skipped {len(skipped)} places not actually in {CITY}:", file=sys.stderr)
        for name, address in skipped:
            print(f"  - {name}: {address}", file=sys.stderr)

    statements = []
    for place_id, place in by_place_id.items():
        name = place.get("displayName", {}).get("text", "Unknown venue")
        content = summarize(place)
        vec = embed(content)
        source_key = f"google_places:{place_id}"

        statements.append(f"""
with target_city as (
  select id from cities where name = {sql_literal(CITY)}
),
upserted_doc as (
  insert into documents (city_id, title, source_type, source_name, source_key, retrieved_date, notes)
  select id, {sql_literal(name)}, {sql_literal('api')}, {sql_literal('Google Places API (New)')},
         {sql_literal(source_key)}, {sql_literal(RETRIEVED_DATE)}::date,
         {sql_literal('Venue-directory signal only (ratings, category tags) - not a rental-rate source.')}
  from target_city
  on conflict (source_key) do update set
    title = excluded.title,
    retrieved_date = excluded.retrieved_date
  returning id, city_id
),
cleared_chunks as (
  delete from chunks where document_id in (select id from upserted_doc)
)
insert into chunks (document_id, city_id, chunk_index, section_reference, content, embedding)
select upserted_doc.id, upserted_doc.city_id, 0, {sql_literal(name)}, {sql_literal(content)}, {vector_literal(vec)}
from upserted_doc;
""")

    out_path = os.path.join(os.path.dirname(__file__), "ingest_google_places_stanton.sql")
    with open(out_path, "w") as f:
        f.write("\n\n".join(statements))

    print(f"Wrote {out_path} ({len(statements)} places)", file=sys.stderr)


if __name__ == "__main__":
    main()

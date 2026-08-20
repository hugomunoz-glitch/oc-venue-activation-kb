"""
Phase 2 API ingestion: pulls Fullerton wedding-venue and gym listings from
Google Places API (New), embeds a one-chunk summary of each via the deployed
`embed` Edge Function, and writes ingest_google_places.sql - one idempotent
upsert-by-source_key statement (source_key = "google_places:{place_id}"),
same pattern as the document-upload ingestion in generate_sql.py.

Usage:
    source .venv/bin/activate   # or: pip install -r requirements.txt
    python ingest_google_places.py

Requires GOOGLE_PLACES_API_KEY (see .env.example) in addition to the
SUPABASE_URL / SUPABASE_ANON_KEY already used by generate_sql.py.
"""

import datetime
import json
import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"].rstrip("/")
SUPABASE_ANON_KEY = os.environ["SUPABASE_ANON_KEY"]
GOOGLE_PLACES_API_KEY = os.environ["GOOGLE_PLACES_API_KEY"]
EMBED_URL = f"{SUPABASE_URL}/functions/v1/embed"

CITY = "Fullerton"
RETRIEVED_DATE = datetime.date.today().isoformat()

# Distinct queries to cover both venue_types this KB cares about, plus the
# "hybrid/flex space" category (banquet halls etc. that Google doesn't tag
# as wedding_venue but that function the same way for activation purposes).
SEARCH_QUERIES = [
    "wedding venue Fullerton CA",
    "gym Fullerton CA",
    "banquet hall event venue Fullerton CA",
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


def embed(text: str) -> list[float]:
    resp = requests.post(
        EMBED_URL,
        headers={
            "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
            "Content-Type": "application/json",
        },
        json={"input": text},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        raise RuntimeError(f"embed function error: {data['error']}")
    return data["embedding"]


def sql_literal(value) -> str:
    if value is None:
        return "null"
    return f"$q${value}$q$"


def vector_literal(vec: list[float]) -> str:
    return "'[" + ",".join(f"{x:.8f}" for x in vec) + "]'::extensions.vector(384)"


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
    for query in SEARCH_QUERIES:
        print(f"Searching: {query}", file=sys.stderr)
        for place in search_places(query):
            place_id = place["id"]
            if place_id not in by_place_id:
                by_place_id[place_id] = place

    print(f"Found {len(by_place_id)} unique places across {len(SEARCH_QUERIES)} queries", file=sys.stderr)

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

    out_path = os.path.join(os.path.dirname(__file__), "ingest_google_places.sql")
    with open(out_path, "w") as f:
        f.write("\n\n".join(statements))

    print(f"Wrote {out_path} ({len(statements)} places)", file=sys.stderr)


if __name__ == "__main__":
    main()

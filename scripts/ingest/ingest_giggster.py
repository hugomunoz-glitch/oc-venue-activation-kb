"""
New source, new goal: Giggster (giggster.com) - an hourly/short-term space
rental marketplace, not a full-event marketplace like Zola. This exists
specifically to support the "few hours at a time" activation-rental pitch:
Zola/Eventective/Wedding Spot only ever gave full-event "starting at"
prices, which can't be compared against per-hour permit/insurance/staffing
costs the way an hourly rate can.

Unlike Zola (which tags every result with the searched city regardless of
actual location), Giggster's own search results display each listing's real
city directly - a much stronger signal than anything the Zola/Eventective/
Wedding Spot sources ever gave. That per-listing city label is what was used
to build the VENUES lists below (any listing whose displayed city didn't
match the target city was excluded, not silently kept).

Coverage is genuinely uneven, matching a pattern already seen across every
other source in this project: only 4 of the 9 cities have a dedicated
Giggster city page (Fullerton, Anaheim, Santa Ana, and city-tagged results
surfaced via the Anaheim/Orange County searches for Orange). Buena Park and
Brea only surface via search-radius spillover from neighboring cities' pages
(one listing each). La Habra, Tustin, and Stanton have no confirmed Giggster
inventory at all - a genuine gap, consistent with those same three cities'
thin coverage in every other market-pricing source used so far, not
something worth forcing.

All 6 covered cities are ingested here in one pass (rather than one file per
city, unlike the Phase 4 city-by-city rollout) because this is a single
coordinated data-source rollout, not organic city-by-city growth over
separate sessions - there's no reason to split files for that.

Writes to both chunks (so retrieval/chat can cite it, same as every other
source) AND revenue_benchmarks (so a future revenue-math calculator can do
real arithmetic against a numeric column) - explicitly tagged
price_unit='per_hour' and activation_type='hourly_rental' so it can never
get silently averaged or compared against Zola's per_event/wedding rows.

Usage:
    source .venv/bin/activate
    python ingest_giggster.py
"""

import datetime
import os
import re
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"].rstrip("/")
SUPABASE_ANON_KEY = os.environ["SUPABASE_ANON_KEY"]
EMBED_URL = f"{SUPABASE_URL}/functions/v1/embed"

RETRIEVED_DATE = datetime.date.today().isoformat()

CITY_IDS = {
    "Anaheim": "bbabbd2d-a9f1-4e12-91dc-e2740e55fcdd",
    "Brea": "65cbb336-720b-4fc9-ba7e-a5fd257a2018",
    "Buena Park": "d8613625-1703-43f9-b3de-d39d1ab240ff",
    "Fullerton": "b05d2af8-ff6f-44dd-a10f-25d106a40c04",
    "Orange": "7b2db04f-a202-48d9-93b2-f584100361b3",
    "Santa Ana": "c89552ab-c1df-4f52-b737-d727af63aebb",
}

# (name, hourly_price, venue_type) - venue_type kept close to Giggster's own
# category rather than forced into "wedding_venue", since most of these are
# not wedding venues at all - that's the point of this source.
VENUES_BY_CITY = {
    "Anaheim": [
        ("Air-Conditioned Creator Space for Photo/Video", 40, "creator_space"),
        ("Urban Photo Studio with Ample Natural Light", 110, "photo_studio"),
        ("Tasting Room & Bar in Anaheim", 150, "bar_event_space"),
        ("Elegant Wine Bar, Restaurant, Boutique", 300, "bar_restaurant"),
        ("Unique Malaysian Cuisine Restaurant in Anaheim", 50, "restaurant"),
    ],
    "Fullerton": [
        ("California Hills Ranch House - Dream Kitchen", 125, "residential"),
        ("Vintage Lounge in Historic Downtown", 100, "lounge"),
        ("Modern/Industrial Airport Hangar", 200, "industrial"),
        ("Beautiful Outdoor Space with Pool & Pool House", 225, "residential"),
        ("Country Garden Home", 55, "residential"),
        ("Spacious Outdoor Filming & Recording Space", 100, "residential"),
        ("Fitness & Dance, Makeup & Massage Studio", 80, "gym_studio"),
        ("Event Space / Open Studio Multipurpose Room(s)", 49, "studio"),
        ("Neon Dreams at the Holiday Escape", 150, "event_space"),
        ("Roomy Urban Space (Casa 723 Fullerton)", 150, "commercial"),
        ("Car Photography Studio", 85, "photo_studio"),
    ],
    "Santa Ana": [
        ("Spacious and Fully-Equipped Private Photo Studio", 39, "photo_studio"),
        ("Professional White Wall Photo & Video Studio (Downtown)", 35, "photo_studio"),
        ("New York Style Vintage/Modern Studio", 175, "studio"),
        ("6000 Sq. Ft. Open Space Gym", 75, "gym"),
        ("Exotic Bar Atmosphere in Santa Ana", 145, "bar_event_space"),
        ("Retro-Inspired Arcade and Full Bar", 50, "bar_event_space"),
        ("Speakeasy Style, Tiki, Hawaiian Island Themed Bar", 50, "bar_event_space"),
        ("Vibrant Patio Space for Private Events", 135, "patio_event_space"),
        ("Versatile Live Music Venue with 2 Stages, Bar & Patio", 140, "music_venue"),
        ("Versatile and Spacious New York Style Loft in OC", 150, "loft"),
    ],
    "Orange": [
        ("Cyclorama Wall and 50+ Backdrops, Natural Daylight", 49, "photo_studio"),
        ("Multi-Set Studio - Tile Backdrops, Ultrafragola!", 39, "photo_studio"),
        ("Warm 1920's Craftsman w/ Amazing OC Views", 105, "historic_home"),
        ("1920's Mission Home w/ Desert Landscape", 85, "historic_home"),
        ("Mid-Century Luxury Kitchen, Dining & Living Areas", 72, "studio"),
        ("Cyclorama Studio with Bathroom and Living Spaces", 60, "studio"),
        ("Orange Circle Modern Industrial Venue Space", 200, "event_space"),
    ],
    "Buena Park": [
        ("Stunning Backyard Pool on the Luxurious Golf Course", 100, "residential"),
    ],
    "Brea": [
        ("Artist Retreat Home with Great Energy", 38, "residential"),
    ],
}


def embed(text: str) -> list[float]:
    resp = requests.post(
        EMBED_URL,
        headers={"Authorization": f"Bearer {SUPABASE_ANON_KEY}", "Content-Type": "application/json"},
        json={"input": text},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        raise RuntimeError(f"embed function error: {data['error']}")
    return data["embedding"]


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def sql_literal(value) -> str:
    if value is None:
        return "null"
    return f"$q${value}$q$"


def vector_literal(vec: list[float]) -> str:
    return "'[" + ",".join(f"{x:.8f}" for x in vec) + "]'::extensions.vector(384)"


def content_for(name: str, city: str, hourly_price: int, venue_type: str) -> str:
    type_label = venue_type.replace("_", " ")
    return (
        f"{name} ({city}, CA) - {type_label}, available for short-term hourly rental. "
        f"Hourly rate: ${hourly_price}/hr. Source: Giggster marketplace listing (an hourly rental "
        f"platform, not a full-event venue marketplace - this figure is a per-hour rate, not a "
        f"per-event starting price, and should never be compared directly against Zola/Eventective/"
        f"Wedding Spot full-event prices without converting to the same basis). Real market signal, "
        f"not a guaranteed quote; actual cost varies by date, duration, and negotiated add-ons."
    )


DOC_NOTES = (
    "Hourly rental marketplace listing - city taken directly from Giggster's own "
    "per-listing display, not the searched city (unlike Zola). Re-fetchable, treat as a snapshot."
)

BENCHMARK_NOTES = "City confirmed via Giggster's own per-listing display, not the searched city."


def main():
    statements = []
    benchmark_statements = []

    for city, venues in VENUES_BY_CITY.items():
        city_id = CITY_IDS[city]
        for name, hourly_price, venue_type in venues:
            content = content_for(name, city, hourly_price, venue_type)
            vec = embed(content)
            source_key = f"giggster:{slugify(city)}:{slugify(name)}"
            price_note = f"${hourly_price}/hr, Giggster marketplace \"starting at\" rate"

            statements.append(f"""
with target_city as (
  select id from cities where id = '{city_id}'
),
upserted_doc as (
  insert into documents (city_id, title, source_type, source_name, source_key, retrieved_date, notes)
  select id, {sql_literal(name + ' - Giggster Hourly Listing')}, {sql_literal('website')}, {sql_literal('Giggster (giggster.com)')},
         {sql_literal(source_key)}, {sql_literal(RETRIEVED_DATE)}::date,
         {sql_literal(DOC_NOTES)}
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

            benchmark_statements.append(f"""
insert into revenue_benchmarks (
  city_id, venue_name, venue_type, activation_type, starting_price_usd, price_unit,
  price_note, source_confidence, effective_date, notes
)
values (
  '{city_id}', {sql_literal(name)}, {sql_literal(venue_type)}, {sql_literal('hourly_rental')},
  {hourly_price}, {sql_literal('per_hour')},
  {sql_literal(price_note)},
  {sql_literal('medium')}, {sql_literal(RETRIEVED_DATE)}::date,
  {sql_literal(BENCHMARK_NOTES)}
);
""")
            print(f"OK: {name} ({city}) - ${hourly_price}/hr", file=sys.stderr)

    out_path = os.path.join(os.path.dirname(__file__), "ingest_giggster.sql")
    with open(out_path, "w") as f:
        f.write("\n\n".join(statements))
        f.write("\n\n-- revenue_benchmarks rows\n")
        f.write("\n\n".join(benchmark_statements))

    total = sum(len(v) for v in VENUES_BY_CITY.values())
    print(f"\nWrote {out_path} ({total} venues across {len(VENUES_BY_CITY)} cities)", file=sys.stderr)
    print("No confirmed Giggster inventory found for: La Habra, Tustin, Stanton", file=sys.stderr)


if __name__ == "__main__":
    main()

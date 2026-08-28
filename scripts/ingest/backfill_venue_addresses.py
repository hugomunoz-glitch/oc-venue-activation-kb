"""
One-time backfill: the market-rate venue-pricing chunks (Zola, Eventective,
Wedding Spot, and one generic "Wedding marketplace listing") never carried a
street address - only "(City, CA)" - unlike the Google Places-sourced venue
chunks, which have always included the full formattedAddress. Looks up each
one via Google Places Text Search, inserts the verified address right after
the "(City, CA)" tag, re-embeds the updated chunk, and writes an
UPDATE-by-chunk_id SQL file.

Also re-verifies city placement using the real formattedAddress (a stronger
signal than the "(City, CA)" label the original ingestion trusted) and flags
any mismatch instead of silently keeping or auto-fixing it - same discipline
as every other address-verification pass in this project. Two mismatches
were already suspected before running this: "Hotel Fera Anaheim" (chunk text
already said "(Orange, CA)" while tagged to Anaheim) and "Tustin Hills
Racquet Club" (tagged to Santa Ana).

Usage:
    source .venv/bin/activate
    python backfill_venue_addresses.py
"""

import json
import os
import sys
import time
from typing import Optional

import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"].rstrip("/")
SUPABASE_ANON_KEY = os.environ["SUPABASE_ANON_KEY"]
GOOGLE_PLACES_API_KEY = os.environ["GOOGLE_PLACES_API_KEY"]
EMBED_URL = f"{SUPABASE_URL}/functions/v1/embed"

# (chunk_id, venue name, tagged city, exact current chunk content) - pulled
# directly from documents/chunks for every market-pricing source lacking an
# address: source_name in ('Zola (zola.com)', 'Eventective (eventective.com)',
# 'Wedding Spot (wedding-spot.com)', 'Wedding marketplace listing').
VENUES = [
    ("bfdd1ced-92e5-46b9-8fcc-45de337bc54b", "Anaheim Hills Golf Course", "Anaheim",
     "Anaheim Hills Golf Course (Anaheim, CA) - wedding/event venue. Starting price: $9,999.  Service tier: Select services. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons). This is the market-rate benchmark data referenced when comparing activation revenue to permit/insurance/staffing costs."),
    ("2d2d325e-f81d-4ae2-a4f1-2bd33d2a815c", "Anaheim Marriott Suites", "Anaheim",
     "Anaheim Marriott Suites (Anaheim, CA) - wedding/event venue. Starting price: $99.  Service tier: Select services. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons). Note: this figure is unusually low relative to comparable full-service venues here - likely a per-person or off-peak minimum rather than a comparable base venue rental rate; treat this one price with extra caution rather than as a like-for-like comparison. This is the market-rate benchmark data referenced when comparing activation revenue to permit/insurance/staffing costs."),
    ("1e000a79-3236-48aa-8779-947bdb383b5b", "Hotel Fera Anaheim, a DoubleTree by Hilton", "Anaheim",
     "Hotel Fera Anaheim, a DoubleTree by Hilton (Orange, CA) - wedding/event venue. Starting price: $7,000.  Service tier: All-inclusive. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons)."),
    ("baa7e699-2cf5-4533-8763-272d927461f0", "The Anaheim Hotel", "Anaheim",
     "The Anaheim Hotel (Anaheim, CA) - wedding/event venue. Starting price: $3,500.  Service tier: Select services. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons). This is the market-rate benchmark data referenced when comparing activation revenue to permit/insurance/staffing costs."),
    ("89f52690-d8e2-437e-aaf2-f58edfdd464a", "The Grand Theater", "Anaheim",
     "The Grand Theater (Anaheim, CA) - wedding/event venue. Starting price: $10,676. Guest capacity: up to 600. Service tier: All-inclusive. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons). This is the market-rate benchmark data referenced when comparing activation revenue to permit/insurance/staffing costs."),
    ("46d34732-3311-4827-acf4-f0b44fa97122", "The Westin Anaheim Resort", "Anaheim",
     "The Westin Anaheim Resort (Anaheim, CA) - wedding/event venue. Starting price: $8,000.  Service tier: All-inclusive. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons). This is the market-rate benchmark data referenced when comparing activation revenue to permit/insurance/staffing costs."),
    ("cf660cf7-0c4a-4a74-b46d-5795b0b018be", "White House Banquets & Event Center", "Anaheim",
     "White House Banquets & Event Center (Anaheim, CA) - wedding/event venue. Starting price: $9,500.  Service tier: All-inclusive. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons). This is the market-rate benchmark data referenced when comparing activation revenue to permit/insurance/staffing costs."),
    ("d0410b98-1fea-4a01-9bfc-0c0ebfeb09d6", "Claim Jumper - Buena Park", "Buena Park",
     "Claim Jumper - Buena Park (Buena Park, CA) - wedding/event venue. Starting price: $1,000.  Service tier: Raw space. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons)."),
    ("1b4c03f8-4ad3-4af3-8c36-d619c925c5c7", "Los Coyotes Country Club", "Buena Park",
     "Los Coyotes Country Club (Buena Park, CA) - wedding/event venue. Starting price: $7,500.  Service tier: Select services. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons)."),
    ("2b7ce147-6d23-4589-98e2-97a4799c325f", "City of Fullerton - Hunt Branch Library", "Fullerton",
     "City of Fullerton - Hunt Branch Library (Fullerton, CA) - wedding/event venue. Starting price: $1,199. Guest capacity: up to 200. Service tier: Raw space. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons). This is the market-rate benchmark data referenced when comparing activation revenue to permit/insurance/staffing costs."),
    ("690391ba-8f36-4910-a83f-6be9b4912124", "Coyote Hills Golf Course", "Fullerton",
     "Coyote Hills Golf Course (Fullerton, CA) - wedding/event venue. No starting price published. Guest capacity: up to 275. Service tier: Select services. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons). This is the market-rate benchmark data referenced when comparing activation revenue to permit/insurance/staffing costs."),
    ("c307ef48-8e36-4e9b-8045-31a66b3e45df", "Fullerton Community Center", "Fullerton",
     "Fullerton Community Center (Fullerton, CA) - wedding/event venue. Starting price: $2,200. Guest capacity: up to 300. Service tier: Raw space. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons). This is the market-rate benchmark data referenced when comparing activation revenue to permit/insurance/staffing costs."),
    ("8f082dde-27ba-4132-872e-9c3290a333f4", "Golleher Alumni House at Cal State Fullerton", "Fullerton",
     "Golleher Alumni House at Cal State Fullerton (Fullerton, CA) - wedding/event venue. Starting price: $1,400. Guest capacity: up to 250. Service tier: Raw space. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons). This is the market-rate benchmark data referenced when comparing activation revenue to permit/insurance/staffing costs."),
    ("5822cf1c-8615-4285-96ff-9aee902d7e70", "Summit House Restaurant", "Fullerton",
     "Summit House Restaurant (Fullerton, CA) - wedding/event venue. Starting price: $7,000. Guest capacity: up to 250. Service tier: All-inclusive. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons). This is the market-rate benchmark data referenced when comparing activation revenue to permit/insurance/staffing costs."),
    ("95057d9b-2132-4281-b060-747f5b9cd635", "The Muckenthaler Mansion", "Fullerton",
     "The Muckenthaler Mansion (Fullerton, CA) - wedding/event venue. Starting price: $23,000. Guest capacity: up to 1500. Service tier: All-inclusive. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons). This is the market-rate benchmark data referenced when comparing activation revenue to permit/insurance/staffing costs."),
    ("7bdbf2f6-b312-4e63-be09-043318832e61", "The Villa Del Sol", "Fullerton",
     "The Villa Del Sol (Fullerton, CA) - wedding/event venue. Starting price: $4,950. Guest capacity: up to 200. Service tier: Select services. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons). This is the market-rate benchmark data referenced when comparing activation revenue to permit/insurance/staffing costs."),
    ("fe2a1df6-4281-463a-b73a-b9d80621fbe6", "Fireside Farm OC", "Orange",
     "Fireside Farm OC (Orange, CA) - wedding/event venue. Starting price: $1,500.  Service tier: Raw space. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons)."),
    ("aa28e880-bfb3-40d4-8671-25fab86e151b", "Fletcher Courtyards at American Family Living Ministries", "Orange",
     "Fletcher Courtyards at American Family Living Ministries (Orange, CA) - wedding/event venue. Starting price: $6,000.  Service tier: Select services. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons)."),
    ("e880500f-7cbc-4292-bfc7-74501bf5ad00", "La Petite Rose", "Orange",
     "La Petite Rose (Orange, CA) - wedding/event venue. Starting price: $6,000.  Service tier: Select services. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons)."),
    ("bc26f3ad-762d-466f-b585-d63b5c9aaa07", "Orange Hill Restaurant", "Orange",
     "Orange Hill Restaurant (Orange, CA) - wedding/event venue. Starting price: $1,500.  Service tier: Raw space. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons)."),
    ("551b3b4e-ebbc-4406-bb33-0c86c99a8b87", "The Estate OC", "Orange",
     "The Estate OC (Orange, CA) - wedding/event venue. Starting price: $13,000.  Service tier: All-inclusive. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons)."),
    ("dc10a0c4-a126-4310-bf85-86e47d9133a1", "The French Estate", "Orange",
     "The French Estate (Orange, CA) - wedding/event venue. Starting price: $4,500.  Service tier: Select services. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons)."),
    ("0c82fb5a-8ba9-4d1e-8ce8-4eb48cfc2910", "The Villa | Weddings & Events", "Orange",
     "The Villa | Weddings & Events (Orange, CA) - wedding/event venue. Starting price: $5,325.  Service tier: Select services. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons)."),
    ("e0287a0e-93e5-4957-8f50-1fadbd731cb9", "The Vintage Rose", "Orange",
     "The Vintage Rose (Orange, CA) - wedding/event venue. Starting price: $10,000.  Service tier: All-inclusive. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons)."),
    ("b10cd560-6b40-4d77-bce8-447b865ff0a0", "Ebell Club of Santa Ana", "Santa Ana",
     "Ebell Club of Santa Ana (Santa Ana, CA) - wedding/event venue. Starting price: $15,000.  Service tier: All-inclusive. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons)."),
    ("c514ceb6-b663-46dd-a8aa-d8f496369d75", "Heritage Museum of Orange County", "Santa Ana",
     "Heritage Museum of Orange County (Santa Ana, CA) - wedding/event venue. Starting price: $3,000.  Service tier: Raw space. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons)."),
    ("52e53075-944f-43c4-960b-70a625891b3d", "Hotel Zessa, a DoubleTree by Hilton", "Santa Ana",
     "Hotel Zessa, a DoubleTree by Hilton (Santa Ana, CA) - wedding/event venue. Starting price: $5,000.  Service tier: All-inclusive. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons)."),
    ("659be37f-6d0a-4f90-8138-ea79659224b5", "Lakeside Orange County Airport Hotel", "Santa Ana",
     "Lakeside Orange County Airport Hotel (Santa Ana, CA) - wedding/event venue. Starting price: $1,799.  Service tier: Select services. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons)."),
    ("dcca44ea-76d4-491e-a042-ddfcb1565c72", "McFadden Public Market", "Santa Ana",
     "McFadden Public Market (Santa Ana, CA) - wedding/event venue. Starting price: $1,500.  Service tier: Raw space. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons)."),
    ("1360b0ba-b41f-4cb5-93a6-fd5df57c6520", "Orange County Mining Co.", "Santa Ana",
     "Orange County Mining Co. (Santa Ana, CA) - wedding/event venue. Starting price: $1,000.  Service tier: Raw space. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons)."),
    ("1b1b5708-d132-41d1-abd9-de2e5407195f", "Tustin Hills Racquet Club", "Santa Ana",
     "Tustin Hills Racquet Club (Santa Ana, CA) - wedding/event venue. Starting price: $1,000.  Service tier: Raw space. Source: Zola marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons)."),
    ("751dad0f-86eb-49c8-b0f1-faed0217bd54", "Embassy Suites by Hilton Brea - North Orange County", "Brea",
     "Embassy Suites by Hilton Brea - North Orange County (Brea, CA) - hotel event space, one of the only address-verified wedding/event venues actually located within Brea's city limits. Starting price: $2,000 (for 50 guests; scales up to $5,500 depending on guest count). Guest capacity: up to 400. Service tier: Select services. Source: Eventective marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons). Note: Brea has very little dedicated wedding/event venue inventory of its own - most marketplace searches for \"Brea\" wedding venues actually surface venues in neighboring cities (Fullerton, Anaheim, Orange, Yorba Linda), which are excluded here."),
    ("86cf9eb8-256c-406d-a194-8568db417008", "Westridge Golf Club", "La Habra",
     "Westridge Golf Club (La Habra, CA) - country club wedding/event venue. Starting price: $7,230 (for 50 guests; a separate $1,700 ceremony setup fee applies). Guest capacity: up to 300. Service tier: Select services. Source: marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons). Note: this is the only address-verified wedding/event venue found actually within La Habra's city limits - most marketplace searches for \"La Habra\" wedding venues surface venues in neighboring cities instead."),
    ("5b493604-c41d-4399-8592-6ae939d3ee88", "Prego Mediterranean", "Tustin",
     "Prego Mediterranean (Tustin, CA) - restaurant event space, at The District at Tustin Legacy. Starting price: $2,462 (for 50 guests).  Service tier: Select services. Source: Wedding Spot marketplace listing (\"starting at\" price - a real market signal, not a guaranteed quote; actual cost varies by date, season, and negotiated add-ons). Note: this is the only address-verified wedding/event venue found actually within Tustin's city limits - Zola's own \"Tustin\" search returned zero venues actually located in Tustin, all in neighboring cities instead."),
]


def embed(text: str) -> list[float]:
    last_err = None
    for attempt in range(3):
        try:
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
        except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as e:
            last_err = e
            time.sleep(2 * (attempt + 1))
    raise last_err


def search_place(name: str, city: str) -> Optional[dict]:
    resp = requests.post(
        "https://places.googleapis.com/v1/places:searchText",
        headers={
            "Content-Type": "application/json",
            "X-Goog-Api-Key": GOOGLE_PLACES_API_KEY,
            "X-Goog-FieldMask": "places.id,places.displayName,places.formattedAddress",
        },
        json={"textQuery": f"{name} {city} CA"},
        timeout=20,
    )
    resp.raise_for_status()
    places = resp.json().get("places", [])
    return places[0] if places else None


def sql_literal(value: str) -> str:
    return f"$q${value}$q$"


def vector_literal(vec: list[float]) -> str:
    return "'[" + ",".join(f"{x:.8f}" for x in vec) + "]'::extensions.vector(384)"


def main():
    mismatches = []
    not_found = []
    updated = []

    out_sql = os.path.join(os.path.dirname(__file__), "backfill_venue_addresses.sql")
    sql_file = open(out_sql, "w")

    for chunk_id, name, city, content in VENUES:
        place = search_place(name, city)
        if not place:
            not_found.append({"name": name, "city": city})
            print(f"NOT FOUND: {name} ({city})", file=sys.stderr)
            continue

        address = place.get("formattedAddress", "")
        if city.lower() not in address.lower():
            mismatches.append({"name": name, "tagged_city": city, "real_address": address, "chunk_id": chunk_id})
            print(f"MISMATCH: {name} tagged {city}, real address: {address}", file=sys.stderr)
            continue

        marker = f"({city}, CA)"
        if marker not in content:
            print(f"SKIP (marker not found): {name}", file=sys.stderr)
            continue

        new_content = content.replace(marker, f"({city}, CA), located at {address}", 1)
        vec = embed(new_content)

        sql_file.write(f"""
update chunks set content = {sql_literal(new_content)}, embedding = {vector_literal(vec)}
where id = {sql_literal(chunk_id)};

""")
        sql_file.flush()
        updated.append({"name": name, "city": city, "address": address})
        print(f"OK: {name} ({city}) -> {address}", file=sys.stderr)

    sql_file.close()
    print(f"\nWrote {out_sql} ({len(updated)} updates)", file=sys.stderr)

    out_report = os.path.join(os.path.dirname(__file__), "backfill_venue_addresses_report.json")
    with open(out_report, "w") as f:
        json.dump({"updated": updated, "mismatches": mismatches, "not_found": not_found}, f, indent=2)
    print(f"Wrote {out_report}: {len(updated)} updated, {len(mismatches)} mismatches, {len(not_found)} not found", file=sys.stderr)


if __name__ == "__main__":
    main()

# Phase 4: Multi-City Expansion

## The nine-city list

Anaheim, Fullerton, Brea, La Habra, Santa Ana, Tustin, Buena Park, Stanton, **Orange**.

The first eight came directly from the project owner. There's no single
official "Central Orange County" designation — Orange County's own Service
Planning Area boundaries group Anaheim/Brea/Buena Park/Fullerton/La
Habra/Stanton under "North SPA," while Santa Ana/Tustin fall in a more
central/south grouping — so this list is a practical one, not a bureaucratic
one. Orange was added as the ninth: it borders four of the other eight
(Anaheim, Santa Ana, Tustin, Villa Park), sits geographically between the
northern cluster and the Santa Ana/Tustin pair, and Old Towne Orange is a
real, active wedding/event venue district (unlike a redundant pick like
Villa Park, a small residential enclave with little activation-venue
activity). Garden Grove is the clear runner-up if a different ninth city is
wanted later.

**Status: Fullerton (Phase 1-3), Anaheim, Brea, and La Habra are ingested.
The other five (Santa Ana, Tustin, Buena Park, Stanton, Orange) are planned,
not started.**

## Architecture decisions (apply once, benefit every future city)

### City scoping is a metadata filter, not an embedding trick

This was decided back in Phase 1 planning, before a second city ever
existed: `chunks.city_id` and `hybrid_search`'s `match_city_id` parameter
were built in from the start, specifically because nine cities' fee
ordinances are structurally near-identical ("a special event permit fee of
$X shall be set by resolution," repeated per city) — semantic similarity
alone risks matching the right *kind* of fact to the wrong city. Phase 4
is where that banked decision finally gets exercised with more than one row
in `cities`.

### Regional/state sources use `city_id = NULL`, not per-city duplication

Some sources genuinely aren't city-specific — OCFA (serves most of Orange
County) and California's ABC alcohol-permit forms (state-level) were
originally tagged to Fullerton's `city_id` simply because Fullerton was the
only city that existed yet. Re-ingesting them per city would be wasteful and
would risk drift between copies. Instead:

- `chunks.city_id` and `documents.city_id` are nullable (they were `NOT
  NULL` until this phase — a real constraint that had to be relaxed).
- `hybrid_search`'s `WHERE` clause treats `city_id IS NULL` as "matches
  every city's queries," not just "matches when no city filter is given."
- When ingesting a new city, check whether an existing regional/state
  source already covers it before writing a new ingestion script for
  something that isn't actually city-specific.

### City detection is a keyword match, not an LLM call

`answer/index.ts` fetches `cities(id, name)` once per request and does a
case-insensitive substring match against the question text. City names are
explicit, distinctive tokens — this is free, instant, and exactly as
reliable as the reranker already assumes a clean retrieval input is. Zero
matches or multiple matches both return an honest "which city?" response
rather than guessing or searching unscoped across cities — silently
defaulting to one city, or dropping the filter entirely, is precisely the
cross-city contamination this whole design exists to prevent.

### One ingestion script set per city, not a generalized multi-city refactor

`chunks_anaheim.py` / `ingest_anaheim.py` (fee schedule) and
`chunks_anaheim_pricing.py` / `ingest_anaheim_pricing.py` (venue pricing)
are their own files, mirroring the pattern `chunks_zola.py`/`chunks_ocfa.py`
already established — not a refactor of the working Fullerton scripts into
a parameterized multi-city version. Consistent with this project's existing
preference for not retrofitting abstractions onto working code.

## The per-city ingestion recipe (what Anaheim's addition actually looked like)

1. **Insert the city.** One row in `cities`.
2. **Source research, verified not assumed.** Search for the city's actual
   municipal code (special event / temporary use permit chapters), fee
   schedule, and any live-website equivalent. Confirm each URL is actually
   fetchable before committing to it as a source — Anaheim's municipal code
   (hosted on `codelibrary.amlegal.com`, the same host that blocked
   Fullerton's in Phase 1) returned a confirmed 403; its fee-schedule PDF
   (`anaheim.net`) was confirmed fetchable.
3. **Document upload: fee schedule.** A `chunks_<city>.py` +
   `ingest_<city>.py` pair, reusing `common.py`'s `build_document_sql`,
   populating both `documents`/`chunks` (for citations) and structured
   `fee_schedules` rows (numeric, joinable). Watch for the all-NULL-column
   typing bug (Postgres infers `text` for a VALUES column that's `null` in
   every row) — cast explicitly (`null::numeric`), don't assume the
   generated SQL will just work.
4. **API: Google Places venues/gyms.** A `ingest_google_places_<city>.py`
   variant. **Critical: filter results by the place's actual address
   containing the target city, not by which city was in the search query.**
   Google's search radius pulls in neighboring cities regardless of query
   wording — a third of Anaheim's raw pull (18 of 54 places) were actually
   in Orange, Santa Ana, Fullerton, Downey, or Buena Park. This exact check
   also surfaced a real, previously-undetected Phase 2 bug: 10 of Fullerton's
   existing Google Places documents were mistagged the same way (3 actually
   in Anaheim, retagged; 7 in cities not yet tracked, removed rather than
   left wrong — they'll come back correctly tagged when those cities are
   added).
5. **Market-rate pricing: Zola-style venue pricing.** Same address-
   verification discipline as step 4, applied to a marketplace pricing pull
   (`chunks_<city>_pricing.py` + `ingest_<city>_pricing.py`, mirroring
   `chunks_zola.py`) - one document+chunk per venue plus a structured
   `revenue_benchmarks` row.
6. **Document upload: municipal code, once available.** If the city's code
   host blocks automated access (check directly, don't assume it will or
   won't), the fallback is the same one used in Phase 1: ask the user to
   manually retrieve the relevant chapter text.
7. **Verify, don't just ingest.** Query `hybrid_search` scoped to the new
   city's `city_id` and confirm it returns the new content; scoped to an
   existing city's `city_id`, confirm nothing new leaked in.

## La Habra: complete

Same recipe, same pattern: the actual code chapter (ecode360.com) is
confirmed-blocked, but the city's own current Special Event Permit
application and Master Schedule of Fees were rich, real, directly-fetchable
primary sources. This round's real finding: a search-engine summary quoted
a $5,385 CUP fee that turned out to be wrong — the actual fee schedule PDF
(read directly via `pdftotext`, not a secondhand summary) states $6,759.
Worth remembering for every remaining city: verify fee figures against the
primary document itself, not a search engine's paraphrase of it.

## Brea: complete

All four sources ingested, with two real findings worth carrying forward
into later cities: (1) a city's actual municipal code host isn't always the
blocker — Brea's own current TUP application PDF was a richer, directly-
fetchable primary source than the amlegal.com-blocked code chapter would
have been; (2) when a fee figure conflicts across two of a city's own pages,
surface both clearly rather than silently pick one — Brea's general fee
schedule and its TUP application state different numbers for what sounds
like the same fee. Also confirmed the most extreme cross-city contamination
case yet: Zola's "Brea, CA" search returned zero venues actually in Brea.

## Anaheim: complete

All four planned sources are ingested: the fee schedule, the municipal code
(§18.38.230 Special Events - Outdoor Activity, §18.38.135 Festival Permit,
§18.118.080 Permitted Temporary Uses - manually retrieved by the user and
supplied as a saved PDF, since `amlegal.com` confirmed-blocked automated
fetches the same way it blocked Fullerton's in Phase 1), Google Places
venues/gyms, and market-rate venue pricing. Verified end-to-end: a gym
pop-up question correctly cites §18.38.230 (not the large-events-only
Festival Permit), and a duration/frequency question correctly returns the
real 9-day/4-per-year limits.

**Still open:** a small Anaheim-specific evaluation pass (not the full
13-question Fullerton set) checking both "Anaheim questions get Anaheim
answers" and "a Fullerton question still only returns Fullerton content."

## What's still open for Phase 4 overall

- Seven more cities (Brea, La Habra, Santa Ana, Tustin, Buena Park, Stanton,
  Orange), each following the recipe above.
- `supabase/migrations/` still has no local file history for this project's
  schema (it exists as a tracked migration history inside the live Supabase
  project itself, just never pulled down into this repo) — worth closing
  before the schema accumulates further multi-city changes.

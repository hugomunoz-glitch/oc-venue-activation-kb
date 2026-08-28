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

**Status: complete. All nine cities (Fullerton, Anaheim, Brea, La Habra,
Santa Ana, Tustin, Buena Park, Stanton, Orange) are ingested and verified.**

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

## Orange: complete (the ninth and final city)

Confirms this project's biggest architectural risk from this phase paid
off in reverse, too: naming Orange as the ninth city meant its name
collides with "Orange County," the region this whole knowledge base
covers - a real bug, not a hypothetical one, since generic "Orange County"
mentions are common in this domain. Caught and fixed before it shipped
(strip the phrase before matching), verified live that it doesn't silently
misresolve. Also the richest Google Places pull of the whole phase (33
venues) and the first city where Zola's own search actually surfaced
mostly-genuine local results, confirming Old Towne Orange's real
wedding-venue activity - the reasoning that got Orange chosen as the ninth
city in the first place held up against real data.

## Stanton: complete

A real limit surfaced this round, not just a finding: no genuine primary-
sourced application form existed for Stanton's TUP/Special Event ordinance,
only search-engine paraphrases of the blocked code text. Rather than
encode those as verified fact, only the directly-fetched fee schedule was
ingested and the ordinance thresholds left as an honest, stated gap - the
right call given this project's own prior lesson (La Habra's CUP fee) about
not trusting secondhand summaries. Third "Zola returns zero genuine local
venues" case; the one real venue found (the city's own Civic Center) has no
published price, recorded as a gap rather than guessed.

## Buena Park: complete

ecode360.com confirmed-blocked again (fifth code-hosting platform, second
time for this specific host after Brea). Notably, no fee discrepancy this
round - the TUP application form's fee matched the general schedule
exactly, a useful reminder that the Brea/Tustin discrepancies are real
findings, not something to expect by default every time.

## Tustin: complete

Municode.com now confirmed-blocked for the second city (after Santa Ana) -
combined with amlegal.com and ecode360.com, every code-hosting platform
this project has touched blocks automated fetches. A second genuine,
unreconciled fee discrepancy this round (Large Gathering Permit: $1,103 on
the application form vs. $2,243 on the general fee schedule) - two
discrepancies in six cities suggests this is a real, recurring pattern in
how cities publish fees across multiple documents, not a one-off. Also a
second "Zola returns zero genuine local venues" case (after Brea) - worth
checking a second marketplace (Wedding Spot, in this case) when Zola comes
up empty, rather than concluding the city has no venues at all.

## Santa Ana: complete

Confirms the code-hosting-platform block is universal so far (amlegal.com,
ecode360.com, and now municode.com all 403 automated fetches) - worth
assuming for every remaining city rather than re-testing the assumption
each time, though still worth a quick direct check before committing to the
manual-retrieval fallback. New honest-gap case: Santa Ana's own Event Permit
Application leaves its fee section blank, determined per-application by
city staff - a third-party site's "$120-$2400" estimate was deliberately
not used as if it were an official number.

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

## Follow-up work completed after all nine cities shipped

Three items were flagged as open once ingestion finished; here's what
happened on each.

**Schema pulled into local migration files.** `supabase/migrations/` now
has all 7 real migrations, as exact original SQL - not reconstructed from
introspection. Supabase's own migration history table stores the full
statement text alongside each tracked version, not just a version/name
pair, so this was a direct, verbatim pull rather than a best-effort rebuild.

**Missing ordinance thresholds (Stanton, Orange, part of Buena Park):
genuinely revisited, still open.** Beyond the original ecode360.com/
municode.com attempts, tried three more channels specifically to see if a
working source existed: the Wayback Machine (blocked entirely - Claude Code
cannot fetch web.archive.org), two third-party code-mirror sites
(us.citylaws.org and zoneomics.com - both load, but neither exposes the
actual chapter text, only tables of contents or unrelated derived articles),
and a direct search for a city-hosted PDF of Buena Park's zoning ordinance
(none exists - `buenapark.com`'s own zoning page links straight back to the
blocked ecode360 mirror). This remains a genuine gap pending manual
retrieval, the same fallback that worked for Fullerton, Anaheim, and La
Habra - not something more automated searching was able to close.

**Per-city evaluation pass: done.** 40 questions (5 per new city, mirroring
Fullerton's original categories - permit classification, fee, duration/
frequency threshold, insurance, market pricing) run against the live
system. Full results and grading in
[`scripts/eval/phase4_city_evaluation.md`](../scripts/eval/phase4_city_evaluation.md).
Headline: **40/40 correct city routing** (zero cross-contamination across
all nine cities tested together for the first time), 38 correct answers,
and 2 correct honest refusals on genuine source gaps - no incorrect
answers.

The two genuine, unreconciled fee discrepancies (Brea's $55 vs. $850;
Tustin's $1,103 vs. $2,243) remain by design - both are real, current,
city-issued figures with no rule in this knowledge base for which applies
at filing time, and the evaluation confirmed the system surfaces both
honestly without being asked to.

## Post-launch fixes: latency regression and venue addresses

Two issues surfaced after the Railway deploy was already live and verified.

**Every answer had gone from ~5s to 60-98s.** Root cause, found by
instrumenting the `answer` function with per-step timing and one Gemini
response-metadata log line: `gemini-flash-latest` is a moving alias, and
Google had silently repointed it to a newer model (`gemini-3.7-flash`,
confirmed via the response's own `modelVersion` field) with extended
"thinking" on by default (`thoughtsTokenCount` present in `usageMetadata`)
- adding 30-40s of pure deliberation to a call that only ever needed
structured classification/generation, no reasoning. Retrieval itself
(embed, hybrid_search, title fetch) was never the problem - all three
stayed under 200ms throughout. Fix: `thinkingConfig: { thinkingBudget: 0 }`
on both Gemini calls in `supabase/functions/answer/index.ts`, cutting
latency back to single digits to low teens of seconds.

**Venue-pricing chunks had no street address.** The Google Places-sourced
venue chunks always included a full address, but the market-rate pricing
chunks (Zola across five cities, plus one Eventective/Wedding
marketplace/Wedding Spot listing each for Brea/La Habra/Tustin) only ever
carried "(City, CA)" - never verified against an actual address, just
trusted from the marketplace listing's own city label. Backfilled by
looking up all 34 of these venues via Google Places Text Search
(`scripts/ingest/backfill_venue_addresses.py`), inserting the verified
address into each chunk, and re-embedding.

That lookup also re-ran the address-verification check this project applies
everywhere else, and it caught 4 real mismatches the original "(City, CA)"
label had missed:

- **Hotel Fera Anaheim** - tagged to Anaheim, real address is in Orange
  (Orange is a tracked city) - retagged rather than deleted.
- **Anaheim Marriott Suites** - real address is in Garden Grove (not a
  tracked city) - excluded, same as the untracked-city exclusions from the
  original Fullerton/Zola pull.
- **Fireside Farm OC** - tagged to Orange, real address is in Costa Mesa
  (not tracked) - excluded.
- **Orange County Mining Co.** - tagged to Santa Ana, real address is in
  North Tustin, an unincorporated community distinct from the City of
  Tustin (not the same jurisdiction, so not a safe retag either) - excluded.

30 of the 34 venues checked out clean on the first pass. The 4 mismatches
were real gaps in the original "trust the marketplace's own city label"
verification - not something the address backfill was expected to find,
but a direct benefit of doing it properly.

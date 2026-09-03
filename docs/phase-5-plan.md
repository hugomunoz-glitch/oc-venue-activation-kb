# Phase 5: Hourly Activation-Rental Pricing

## Why this phase exists

The stated goal behind this whole knowledge base surfaced explicitly for the
first time in this phase: the user wants a database to bring to
conversations with venue owners, making the case for renting out their
space for a few hours at a time (an "activation") as a new revenue stream -
and helping them do the actual math on whether it's worth it.

Every piece of market-pricing data ingested through Phase 4 (Zola,
Eventective, Wedding Spot, one generic "Wedding marketplace listing") was a
**full-event "starting at" price** - the kind of number a wedding books
against, not something a few-hours activation can be priced against. That's
not a data gap so much as a wrong unit: you can't build a "does renting out
4 hours make sense" pitch out of numbers that only exist as whole-day
minimums.

## What was evaluated

Peerspace was the original candidate for hourly pricing back in Phase 2 -
already confirmed bot-blocked then, and still the case now. Giggster
(giggster.com), an hourly/short-term space rental marketplace, was
identified and verified reachable this phase: real, per-listing hourly
prices, fetchable via WebFetch, with genuine coverage in Orange County.

One structural advantage over every prior market-pricing source: Giggster's
own search results display each listing's **real city** directly, not just
the searched city. Zola, Eventective, and Wedding Spot all required trusting
either a marketplace's own city label or a follow-up address lookup (see the
false-positive incident below); Giggster's per-listing city field let a
single Fullerton search correctly separate results into Fullerton, Brea, La
Habra, Buena Park, Anaheim, and Placentia listings in one page - a much
stronger native signal.

## Coverage: genuinely uneven, same pattern as every other source

Only 4 of the 9 cities have a dedicated Giggster city page (Fullerton,
Anaheim, Santa Ana; Orange's listings were pulled from spillover on
Anaheim's and the county-wide page rather than a working dedicated page -
`/find/orange--ca` did not actually resolve despite appearing in a city
directory listing). Buena Park and Brea surface only via search-radius
spillover from neighboring cities (one listing each). **La Habra, Tustin,
and Stanton have no confirmed Giggster inventory at all** - consistent with
those same three cities' thin coverage in every other market-pricing source
used across this project (Eventective/Wedding Spot/Wedding-marketplace each
found exactly one real local venue for Brea/La Habra/Tustin; Stanton has
never had any confirmed market-pricing venue). This is treated as a genuine
gap, not something to force by loosening the city-verification bar.

**Result: 35 hourly-rate venues ingested across 6 cities** (Anaheim 5,
Fullerton 11, Santa Ana 10, Orange 7, Buena Park 1, Brea 1). Types range
from event/party spaces and bars to a couple of directly on-scope gym
listings (a "6000 Sq. Ft. Open Space Gym" in Santa Ana at $75/hr, a
"Fitness & Dance, Makeup & Massage Studio" in Fullerton at $80/hr) - a
useful, unplanned bonus given this KB's scope explicitly includes gyms
hosting one-day fitness pop-ups, not just wedding venues.

## Schema change: `price_unit`

`revenue_benchmarks` already existed (populated with 32 rows from Phase 3/4)
but had no column distinguishing a full-event price from an hourly one -
every row implicitly assumed "starting price for the whole event." Mixing a
$40/hr rate into the same numeric column as a $23,000/event rate with no
unit marker would corrupt any future revenue-math calculator the moment
someone queried across both. Added a single migration
(`20260828231640_add_price_unit_to_revenue_benchmarks.sql`):
`price_unit text not null default 'per_event'` - the default correctly
backfills every existing row (they were all genuinely per-event prices), and
all 35 new Giggster rows are explicitly `per_hour`. Also tagged
`activation_type = 'hourly_rental'` (distinct from the existing `'wedding'`
value) so the two categories can never get silently averaged together.

Chunk content for every Giggster listing also states in plain language that
it's a per-hour rate, not a per-event price, and warns against comparing the
two without converting to the same basis - verified live: a generic
"typical venue rental rate in Fullerton" question correctly returned two
clearly separated sections (`Full-event starting prices` vs. `Hourly
short-term spaces`) rather than blending them.

## What's deliberately not built yet

Per explicit scope decision for this pass: **data only, no calculator.**
The actual "does renting out 4 hours make the math work" synthesis - hourly
rate minus permit fee minus insurance cost minus staffing, amortized per
activation - is a distinct, well-defined follow-up now that real numbers
exist for it to run on. Building it before the data existed would have
meant guessing at the shape of a calculation that didn't have real inputs
yet.

## Ingestion script

`scripts/ingest/ingest_giggster.py` covers all 6 cities in one file, unlike
the one-file-per-city convention used for Phase 4's city-by-city rollout -
justified here because this was a single coordinated data-source rollout
done in one pass, not organic growth spread across separate sessions the
way each Phase 4 city was.

## A verification lesson from earlier this phase, still relevant here

Right before this phase started, an automated Google Places re-verification
pass produced two false-positive city mismatches (Fireside Farm OC,
Orange County Mining Co.) that led to real data being wrongly deleted -
caught only because the user pushed back on one of them, not because the
automated check itself raised any doubt. The lesson carried directly into
this phase's Giggster ingestion: every included venue's city came from
Giggster's own explicit per-listing display, cross-checked by observing
that a single search page correctly separated multiple distinct cities'
worth of results - a structural signal, not a single fuzzy-matched API
call standing alone.

## Addresses and contact info: not obtainable, and one more real error found

The user asked for street addresses and host contact info for the Giggster
venues, matching what the Google Places-sourced venues already have.
Checked directly against three live Giggster listing pages: none of them
expose a real address ("exact location provided after booking" on every
one) or any direct contact info (phone, email) - contact is routed only
through Giggster's own in-platform messaging, by the platform's own design,
the same reason Airbnb hides addresses until a booking is confirmed. This
isn't a gap more searching can close; it's how the source works for every
private-host listing on it.

Checking those three listing pages individually surfaced a second real
error beyond what the per-listing search-results display had already
caught: the "6000 Sq. Ft. Open Space Gym" venue, ingested as Santa Ana at
$75/hr, is actually in Irvine, CA per its own live listing page - Irvine is
not a tracked city. Removed (`revenue_benchmarks` row, `chunks` row, and
`documents` row all deleted; verified live that the same question now
returns an honest refusal instead of the wrong answer). A second listing
checked the same way, Fullerton's "Event Space / Open Studio Multipurpose
Room(s)" at $49/hr, confirmed correct - genuinely Fullerton, and its
generic-sounding name is verbatim from the listing itself, not a
placeholder; the space simply has no branded business name.

Only these two of the 35 Giggster venues have been individually verified
against their own listing pages so far. The other 33 still rely only on
the per-listing city label from the search-results page, which has now
been shown to disagree with the listing's own page at least once. That risk
is being held, not resolved: nothing else has been changed pending a
decision on whether a full listing-by-listing re-check across all 35 is
worth doing.

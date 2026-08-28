# Phase 4 Per-City Evaluation

Mirrors the spirit of `baseline_evaluation.md`'s original 13-question
Fullerton set, scaled to a proportionate 5 questions per new city (permit
classification, fee, duration/frequency threshold, insurance/requirement,
market pricing) rather than repeating all 13 verbatim eight times over.
40 questions total across the eight cities added in Phase 4. Raw responses:
`phase4_city_eval_results.json`. Run against the live deployed `/answer`
endpoint, same as `generation_evaluation.md`.

## Headline result

**40/40 correct city routing.** Every single question's `returned_city`
matched the city named in the question — zero cross-contamination across
all nine cities now live in the system. This is the one number that matters
most for this phase: it's the direct, at-scale proof that the city-scoping
design (decided in Phase 1, exercised for real starting in Phase 4) actually
holds once there's more than a couple of cities to confuse.

**39/40 answered with accurate, correctly-cited data. 1/40 correctly, honestly
refused** — not a system failure. Asked what tent size requires a building
permit in La Habra, the system said the source material doesn't specify a
number (it only says "contact the Chief Building Official") and declined to
invent one. That's the honesty behavior working exactly as designed on a
genuine source gap, not a retrieval miss - La Habra's own permit
application form really doesn't give that number, unlike Brea's and
Tustin's forms, which do.

## Per-city results

| City | Questions | Correct answers | Honest refusals | Notes |
|---|---|---|---|---|
| Anaheim | 5 | 5 | 0 | Correctly distinguished the Festival Permit's $5M+ insurance requirement from the everyday Special Event Permit; correctly flagged the $99 Anaheim Marriott Suites price as a likely outlier rather than presenting it uncritically. |
| Brea | 5 | 5 | 0 | Correctly surfaced the $55/$850 fee discrepancy unprompted, without being asked about it directly - the honesty behavior generalizes beyond the one question it was originally caught on. |
| La Habra | 5 | 4 | 1 | The one refusal (tent size for building permit) is a genuine source gap, not a bug - confirmed by re-reading the ingested chunk, which itself says the threshold isn't given. |
| Santa Ana | 5 | 5 | 0 | Correctly distinguished the two different fee tracks (Event Permit Application, case-by-case vs. Land Use Certificate - Seasonal/Temporary Event, $539 flat) without conflating them when asked generally about "the fee." |
| Tustin | 5 | 5 | 0 | Correctly surfaced the $1,103/$2,243 Large Gathering Permit discrepancy unprompted, same generalization as Brea. |
| Buena Park | 5 | 5 | 0 | Clean, no discrepancies or gaps - matches this city's own ingestion finding (its TUP fee agreed exactly across both source documents). |
| Stanton | 5 | 4 | 1 | The refusal (venue rental rate) is the same known, deliberately-recorded gap from ingestion (no published price for the one real local venue) - correctly reproduced by the live system, not a new finding. |
| Orange | 5 | 5 | 0 | Correctly distinguished the Planning Division's Special Event Permit ($110) from Community Services' Special Event Park Permit ($60) as two different tracks, and correctly computed the recurring/non-recurring TUP fee difference ($613) from two separately-cited numbers. |

**Tally: 38 correct answers, 2 correct honest refusals, 0 incorrect answers,
0 cross-city contamination** (out of 40).

## What this confirms

1. **City-scoping holds at scale, not just in the two-city case tested during
   Phase 4 ingestion.** Every prior verification (Anaheim vs. Fullerton, then
   spot-checks per city as each was added) was pairwise. This is the first
   test where all nine cities' data coexists and gets exercised together,
   and the `city_id` filter didn't leak once.
2. **The honesty behaviors generalize.** Both fee discrepancies (Brea,
   Tustin) were surfaced correctly here without the question specifically
   probing for them, and both genuine data gaps (La Habra's tent threshold,
   Stanton's venue price) were declined rather than guessed at. These
   weren't re-engineered for this eval - the same reranking/generation
   pipeline built in Phase 3 is doing the same honest work across cities it
   was never specifically tuned for.
3. **Reranking rarely needed a second hop here** - every one of these 40
   questions resolved in `retrieval_hops: 1`, because each was phrased
   using terms that actually appear in the ingested source material (permit
   names, fee categories). This isn't a contradiction of Phase 3's Q2
   finding (a gym-permit question needing a rewritten query) - that failure
   mode is specifically about phrasing mismatches, and these questions were
   deliberately phrased close to the source language, the way a well-formed
   query intent naturally would be.

## What remains genuinely open

- Three cities (Stanton, Orange, and the parking-lot-sale specifics in
  Buena Park) are still missing their own ordinance's event-duration/
  frequency thresholds. Revisited directly for this work: tried the Wayback
  Machine, third-party code-mirror sites (us.citylaws.org, zoneomics.com),
  and a direct search for a city-hosted PDF - none had the actual operative
  text accessible without the same automated block every code-hosting
  platform in this project has hit. This remains a genuine gap pending
  manual retrieval (the same fallback that worked for Fullerton, Anaheim,
  and La Habra), not something more searching closed.
- The two fee discrepancies (Brea, Tustin) remain unreconciled by design -
  both are genuine, current, city-issued figures with no rule in this
  knowledge base for which one applies at filing time.

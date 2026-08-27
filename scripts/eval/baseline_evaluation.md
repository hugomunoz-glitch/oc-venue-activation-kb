# Phase 3 Baseline Evaluation

Retrieval-only (no generation/synthesis layer exists yet — see Phase 3 plan). Each
question run through the live `hybrid_search` RPC, top 5 results, against the
Phase 1+2 corpus (50 documents, 89 chunks). Raw results: `baseline_results.json`.

Grading: **GOOD** (retrieved content directly supports a correct answer) /
**PARTIAL** (right topic surfaced, but the actual numeric answer doesn't exist
in the corpus — a genuine source gap, not a retrieval bug) / **FAIL** (wrong
or misleading content surfaced, or the system should have refused and didn't).

| # | Question (short) | Verdict | Notes |
|---|---|---|---|
| 1 | CUP vs. TUP for exceeding event count | PARTIAL | Correctly surfaces Ch. 15.70 (CUP), but no numeric "how many events" threshold exists anywhere in the ordinance — genuine gap, not a retrieval miss. |
| 2 | Gym pop-up permits | **FAIL** | All 5 hits are Google Places gym *listings* — zero permit/code chunks retrieved. "Gym" in the query pulled toward venue-directory data instead of Ch. 15.58/8.71. |
| 3 | Backyard wedding: SEP vs. TUP by guest count | PARTIAL | Correctly surfaces §15.58.030. No guest-count threshold exists in the ordinance (it's a blanket permit regardless of size) — genuine gap. |
| 4 | Alcohol service added cost | GOOD | Correctly combines Public Works fees + ABC-218's $100/day + police staffing. Missing only the "compare to guest charges" side (no ticket-price data exists). |
| 5 | Fire-marshal/occupancy cap for gym | GOOD | Correctly surfaces OCFA's page. Honestly, no numeric occupancy threshold is published there either (matches OCFA's own stated "case by case" evaluation). |
| 6 | Fullerton insurance/COI limits | **FAIL** | All 5 hits are unrelated Fullerton fee chunks at high similarity (0.85+) — none address insurance at all. Fullerton doesn't publish this (known gap), but retrieval presents confident-looking wrong answers instead of signaling "not found." |
| 7 | CUP filing-count threshold | **FAIL** | Surfaces ABC-218's "36 events/year" catering limit — a *different jurisdiction's unrelated number* — at 0.876 similarity, dangerously close to plausible. Real risk of citation-mixing across permit types. |
| 8 | Market rental rate range | PARTIAL | Correctly surfaces real venue listings, and each chunk's own text already states "not an actual rental rate" — the honesty caveat baked into Phase 2's chunk content earlier is doing real work here. No rate data exists (Peerspace blocked, as documented). |
| 9 | "Is there enough data to know if this breaks even?" | PARTIAL | Retrieves relevant supporting fee data, but answering the meta-question itself ("yes/no, enough data") requires reasoning, not just retrieval. |
| 10 | Change-of-use/building-code inspection | **FAIL** | Retrieves Ch. 15.58/8.71 (zoning) content, but the actual question is a Building Division / Title 14 matter — never ingested. Wrong-title content presented as relevant. |
| 11 | Nonprofit discount margin | PARTIAL | Fee inputs available; no venue revenue data exists to compute a margin against (known gap). Arithmetic itself needs a generation layer regardless. |
| 12 | *(out-of-scope)* Should I buy/lease a property? | **FAIL** | Should refuse. Instead returns real venue listings at 0.85+ similarity — high confidence, wrong response type entirely. |
| 13 | *(out-of-scope)* Next-quarter revenue forecast | **FAIL** | Should refuse. Returns gym listings + an ABC fee chunk at 0.81 similarity — notably lower than every in-scope question's top score. |

**Tally: 3 GOOD, 5 PARTIAL, 5 FAIL** (out of 13).

## Key findings

1. **Two distinct out-of-scope failure modes, needing different fixes.** Q12 and
   Q13 both should have been refused, but they fail differently. Q13's top
   similarity (0.81) sits close to the ~0.74 noise floor we measured earlier
   (a nonsense control query against this corpus) — a similarity threshold
   could plausibly catch this one. Q12's top similarity (0.856) sits solidly in
   the "genuinely relevant" band, because the query literally contains "wedding
   venue in Fullerton" and matches real venue data well — the *content* is
   relevant, but the *question type* (investment advice) is categorically out
   of scope regardless of match quality. **A similarity threshold alone will
   never catch Q12-style failures** — that needs actual question-intent
   classification, which only a generation/reasoning layer can do. This
   directly shapes the Phase 3 chat-layer design: it needs both a low-similarity
   fallback *and* an explicit scope/intent check.

2. **The "confident but wrong" pattern (Q6, Q7) is the most concerning failure
   type**, more than outright misses (Q2, Q10). Retrieval returning nothing
   would at least be honestly empty; instead it returns plausible-looking,
   high-similarity content from the *wrong* source (a different city's fee
   schedule component, a different jurisdiction's numeric limit). Without a
   generation layer that can say "these results don't actually answer your
   question," a user reading raw search results could easily mistake Q7's ABC
   catering limit for Fullerton's own CUP threshold.

3. **Chunk-level honesty caveats work.** Q8 is a real bright spot: because the
   Google Places ingestion script (Phase 2) baked "not an actual rental rate"
   into every venue chunk's own text, even imperfect retrieval still carries
   the correct caveat forward. Worth doing more of this at ingestion time
   rather than relying only on a future generation layer to add disclaimers.

4. **Q2's total miss is a tuning problem, not a data gap** — the permit chunks
   for a gym hosting an event *do* exist (Ch. 15.58/8.71), they just didn't
   surface against this specific phrasing. This is exactly what Phase 3's
   reranking work should target: cases where the right chunk exists in the
   corpus but a different, topically-adjacent chunk out-competes it.

## What this means for Phase 3 priorities

- The generation/chat layer needs to handle **both** failure modes from
  finding 1 — not just "refuse when nothing matches well."
- Reranking should specifically target Q2/Q10-style topic-adjacent misses.
- Before trusting the generation layer's citations, it should be re-evaluated
  against this same 13-question set to measure improvement directly against
  this baseline.

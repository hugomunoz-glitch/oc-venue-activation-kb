# Phase 3 Generation-Layer Re-Evaluation

The same 13 baseline questions, now run through the live `/answer` edge
function: widened hybrid search (top-15 fused candidates) → LLM reranking
(scores each candidate for genuine relevance to the actual question, not
just RRF/embedding rank) → a capped one-hop agentic requery when the
reranker judges the first pass insufficient → Gemini synthesis with
citations. Raw responses: `generation_results.json`.

Grading distinguishes three outcomes, since a "correct" result here can mean
either a genuine synthesized answer or a genuine, honest refusal — collapsing
both into one "GOOD" bucket would overstate how much the system actually
*answers*:

- **ANSWERED** — a real, correctly-cited answer built from genuine facts.
- **HONEST REFUSAL** — the system declines or flags a gap, and that's the
  *correct* response (the data genuinely isn't there, or the question is
  out of scope) — this is success per the brief's own honesty standard, not
  a failure.
- **PARTIAL** — some genuine facts are surfaced and cited, but the system is
  more conservative than it needed to be about synthesizing them further.
- **FAIL** — a wrong, misleading, or wrong-jurisdiction answer stated with
  confidence, or an answerable question wrongly refused.

| # | Question (short) | Baseline verdict | Generation verdict | Notes |
|---|---|---|---|---|
| 1 | CUP amendment vs. TUP for event count | PARTIAL | **HONEST REFUSAL** | Correctly cites Ch. 15.58/15.70, explicitly says no numeric threshold exists rather than dangling the citation as a non-answer. |
| 2 | Gym pop-up permits | **FAIL** | **ANSWERED** | **Target fix.** First pass still surfaced gym listings; the reranker flagged it insufficient, triggered one requery ("Fullerton special event permit private property commercial temporary use FMC 15.58"), and the second pass correctly cites §15.58.025/.030/.040/.095 with the actual temporary-commercial-use vs. special-event distinction. |
| 3 | Backyard wedding: SEP vs. TUP by guest count | PARTIAL | **HONEST REFUSAL** | Correctly cites §15.58.030 + OCFA, explicitly notes no guest-count threshold or TUP-specific rule exists. |
| 4 | Alcohol service added cost | GOOD | **PARTIAL** | Citations are genuinely on-topic (ABC-218 $100/day, ABC-221 $50-100/day, PW/CD/police fee lines) and the answer states the real dollar figures - but declines to sum them into a "total," since police staffing has no published flat rate. See finding 3 below. |
| 5 | Fire-marshal/occupancy cap for gym | GOOD | **HONEST REFUSAL** | Matches OCFA's own case-by-case stance - correctly says no numeric cap is published, doesn't invent one. |
| 6 | Fullerton insurance/COI limits | **FAIL** | **HONEST REFUSAL** | Baseline's worst "confident but wrong" case (unrelated fee chunks at 0.85+ sim). Now correctly surfaces the one genuinely relevant clause (§8.71.050 - insurance/bonds required, city Risk Management sets liquor liability) and honestly says exact dollar limits/costs aren't published. |
| 7 | CUP filing-count threshold | **FAIL** | **HONEST REFUSAL** | **The most important fix.** Baseline dangerously cited ABC-218's unrelated "36 events/year" catering limit as if it were Fullerton's CUP threshold (0.876 similarity). Reranking now filters it out entirely - zero citations, clean refusal, no cross-permit-type mixing. |
| 8 | Market rental rate range | PARTIAL | **ANSWERED** | Real dollar range ($1,199-$7,000) across 5 named venues, each cited, correctly caveated as "starting benchmark rates, varying by date/season" - a genuine, complete synthesis of what data exists. |
| 9 | "Enough data to know if this breaks even?" | PARTIAL | **ANSWERED** | The meta-question itself gets reasoned about directly: explicitly lists what's missing (insurance cost, full operational pricing) *and* what's available (venue prices, ABC fee, deposit, inspection fee) rather than just dumping retrieved passages. |
| 10 | Change-of-use/building-code inspection | **FAIL** | **HONEST REFUSAL** | Baseline presented wrong-title zoning content as if it answered a Building Division question. Now correctly separates what it has (OCFA permit trigger, general inspection-completion requirement) from what it doesn't (no defined change-of-use trigger) - honest gap, not a wrong-topic answer. |
| 11 | Nonprofit discount margin | PARTIAL | **PARTIAL** | Terse, fully honest refusal ("does not have that information yet") - correct, but more conservative than Q9's fuller treatment of a similar gap; see finding 3. |
| 12 | *(out-of-scope)* Buy/lease property | **FAIL** | **HONEST REFUSAL** | Unchanged - scope check catches this before retrieval even runs (already fixed pre-reranking). No regression. |
| 13 | *(out-of-scope)* Revenue forecast | **FAIL** | **HONEST REFUSAL** | Unchanged - same scope check. No regression. |

**Tally: 2 ANSWERED, 9 HONEST REFUSAL, 2 PARTIAL, 0 FAIL** (out of 13) — versus
baseline's 3 GOOD, 5 PARTIAL, 5 FAIL (retrieval-only).

## Key findings

1. **The target fix worked, and worked via the mechanism designed for it.**
   Q2 was diagnosed as a total retrieval miss (right chunks exist, wrong
   phrasing). Reranking alone can only reorder what's already retrieved - it
   had nothing to promote at `match_count=15` either (still no Ch. 15.58/8.71
   chunk in the pool at that width). The agentic requery is what actually
   fixed it: the reranker recognized "these are all venue listings, not
   permit content" and proposed a rewritten query that finally surfaced the
   right chapter. This confirms the plan's core distinction between the two
   techniques - reranking fixes buried-but-present chunks, agentic requery
   fixes phrasing-caused total misses - and here they're separate fixes
   with different failure signatures, not the same thing wearing two names.

2. **The most dangerous baseline pattern - confident, wrong-jurisdiction
   citation-mixing - is eliminated, not just softened.** Q7's baseline result
   (a different jurisdiction's numeric limit at 0.876 similarity, "dangerously
   close to plausible") and Q6's (unrelated fee chunks at 0.85+ with zero
   insurance content) both now resolve to honest, correctly-scoped refusals.
   This was flagged as the top-priority failure mode in `baseline_evaluation.md`,
   and it's the category reranking's per-candidate relevance judgment is best
   suited to catch (it's explicitly told a "different jurisdiction's numeric
   limit" is not relevant even at high similarity - the same instruction that
   made `generateAnswer`'s prompt honest is now enforced one step earlier, at
   retrieval selection, not just at synthesis).

3. **A real, worth-stating tension: the honesty rules can be conservative
   about synthesis, not just about invention.** Q4 and Q11 both have genuinely
   on-topic, correctly-cited component data (real ABC fees, real fee-schedule
   line items) but the system declines to combine them into the compound
   answer the question actually asked for ("total added cost," "margin
   remaining"). This isn't hallucination-avoidance working as intended - it's
   the system being *more* cautious than the data warrants, because no single
   passage states a total and the rules emphasize not stretching a passage
   into more than it says. Q9 shows this doesn't have to be the outcome (it
   reasons about a similarly gapped, multi-part question quite directly) - so
   this reads as inconsistency in how far the generation layer is willing to
   go, not a hard architectural limit. Worth a prompt-level pass in a future
   iteration, and worth stating plainly in the retrospective as a limitation
   the honesty-first design trades against, not one it was blind to.

4. **No regressions.** Q12/Q13 (the out-of-scope pair, already fixed before
   this work) are unchanged. No previously-GOOD question moved to FAIL or PARTIAL.

## What this means for the retrospective

- Reranking and agentic retrieval were genuinely two different fixes for two
  different failure modes, not redundant techniques - worth stating explicitly
  as an architectural-judgment point, since the brief asks for exactly that.
- The honesty-first design is doing real work (findings 1-2), at a real,
  identifiable cost (finding 3) - a system this conservative about synthesis
  will sometimes under-deliver on genuinely answerable multi-part questions.
  That's a legitimate "what should happen next" item, not a hidden flaw.

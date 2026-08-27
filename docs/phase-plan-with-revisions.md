# Phase Plan — With Revisions

The individual pivots below were documented as they happened (in git commits
and in `prompts-that-changed-decisions.md`), but never pulled into one place.
This is that document: each phase's original goal and cut list, what actually
shipped, and the revisions in between — what changed, and what made it change.

A note on dating: git commit timestamps for Phase 1 and Phase 2 are batched
on the same day (2026-08-20) because of a real process gap covered below —
substantial Phase 1 work happened before anything was committed. Where a
specific date matters, it's the date a decision was made in the build
conversation, not the commit date.

---

## Phase 1 — Prove the Pipeline

**Goal (per the task brief's own phase guide):** one source type ingested end
to end — chunk, embed, store in Supabase — with semantic search returning
relevant results and their sources shown. Deployed and demonstrable.

**Not in this phase (as planned):** hybrid search, multiple source types,
re-ingestion safety, a generation/chat layer, a source-management view.

**What shipped:** Fullerton's municipal code chapters on special events
(15.58) and Conditional Use Permits (15.70), plus the actual fee schedule —
4 documents, 35 chunks, embedded with `gte-small` and stored in Supabase
with pgvector. Every chunk carries its source section as metadata. Deployed
on Railway. Tagged `phase-1`.

**Revisions during this phase:**

- **Embedding model: OpenAI `text-embedding` → `gte-small` via a Supabase
  Edge Function.** The original default recommendation was OpenAI's API.
  Pushing on "why" surfaced a real cost and account-setup burden with no
  offsetting benefit at this scale — `gte-small` running inside Supabase is
  free, requires no separate account, and switching later only means
  re-embedding existing chunks, not rearchitecting anything. Decided before
  Phase 1 shipped.
- **Deployment platform: an open Railway-vs-Vercel choice → Railway,
  confirmed as a hard requirement.** Deployment platform had been reasoned
  from a phase-planning doc, not from the actual task brief PDF. Asking
  directly whether the brief required anything specific sent us back to
  read it for the first time — it names Railway as a required deliverable
  three separate times ("a working Railway link" is explicitly listed in
  the final handover package). Without that question, deployment likely
  would have moved to Vercel, technically satisfying "a live app" but not
  the actual assignment. This is the single largest correction in the
  project.
- **Git discipline: no phase-tagging system → tags as permanent snapshots.**
  By the time Phase 2 was ready to start, a check-in surfaced that despite
  substantial Phase 1 work, nothing had actually been committed beyond the
  repo's initial empty commit. This produced the tagging discipline used
  for the rest of the build (`phase-1`, `phase-2`, `phase-3` as permanent
  snapshots, real commits before starting new work) — and, later, the
  actual deployment strategy: one evolving Railway URL plus git tags as the
  durable, presentable record, chosen over the cost and upkeep of running a
  separate live environment per phase.

**Demo:** raw hybrid-search page (`web/search.html`, preserved as the
Phase 1–2 view) returning cited passages for a real Fullerton permit question.

---

## Phase 2 — Widen the Intake

**Goal (per the brief):** all three required ingestion methods working — an
API, a live website, a document upload — with source metadata and citations
throughout, and re-ingestion that doesn't create duplicates.

**Not in this phase (as planned):** hybrid search tuning, a generation/chat
layer, real venue pricing data (the market-rate question was known to be
open but was treated as a Phase 3 concern).

**What shipped:** 50 documents, 89 chunks, three ingestion methods —
Google Places API (43 real Fullerton venues/gyms), the OC Fire Authority's
special-event permit page (live website), and California's ABC alcohol
permit reference forms (document upload, two permit paths with dollar
figures verified against the primary government PDFs). A source-management
view for browsing everything ingested. Idempotent re-ingestion via a
`source_key` unique constraint and an upsert pattern. Tagged `phase-2`.

**Revisions during this phase:**

- **API and live-website sources: Yelp Fusion + Eventbrite → Google Places +
  OCFA.** Both were the original candidates named when the source map was
  first planned. Yelp Fusion turned out not to be free anymore (30-day
  trial, then $229+/month, business email required) — caught by directly
  checking current pricing rather than trusting the assumption. Eventbrite's
  public search API had been retired. Both were swapped for sources that
  actually worked, and — more durably — this established a pattern for the
  rest of the build: verify current pricing and terms before committing,
  rather than trust training data. That pattern caught the same kind of
  staleness again later (Google's own Places pricing model, CA ABC's lack
  of a real open-data API).
- **Market-rate pricing source: Peerspace → blocked, left as an honest gap.**
  Peerspace (a venue marketplace) was the planned source for real rental
  pricing. It bot-blocked automated access. Rather than force a workaround,
  this was left as a documented, known gap through the rest of Phase 2 — the
  Google Places venue chunks got an explicit "not an actual rental rate"
  caveat baked into their own text at ingestion time, so even the honest gap
  carried a correct caveat forward into anything that later retrieved those
  chunks. This gap was closed in Phase 3 (see below), not here.
- **Idempotent ingestion added mid-phase, reactively.** This wasn't in the
  original Phase 2 plan as a distinct line item so much as a lesson learned
  by then: a Phase 1 duplicate-document bug (a subagent delegation attempt
  was rejected mid-run, then re-run from scratch without realizing the
  first attempt had already succeeded, inserting Chapter 15.58 twice) had
  already been fixed by hand once. The `source_key` unique constraint plus
  delete-then-reinsert chunk pattern built for Phase 2 exists specifically
  because that bug shouldn't be possible to repeat.

**Demo:** the source-management view (`web/sources.html`) showing all three
ingestion methods' output side by side, plus safely re-running ingestion on
an already-loaded source with no duplicates appearing.

---

## Phase 3 — Sharpen It

**Goal (per the brief):** hybrid search or reranking, a chat interface with
grounded and cited answers, a knowledge-graph-or-agentic-retrieval
experiment, and evaluation against the question set.

**Not in this phase (as planned):** a knowledge graph (deliberately not
chosen — see below), Phase 4's multi-city expansion, Fullerton
insurance/COI data (never published anywhere by the city itself; left out
on purpose rather than guessing a generic California number).

**What shipped, in the order it actually happened:**

1. **Baseline evaluation first, before touching generation.** Rather than
   building the chat layer and evaluating it after the fact, all 13 test
   questions were run against Phase 2's raw `hybrid_search` first, human-
   graded (3 GOOD / 5 PARTIAL / 5 FAIL), and written up in
   `scripts/eval/baseline_evaluation.md` — a deliberate methodological
   choice so the generation layer would have a real number to be measured
   against, not just a "feels better" impression.
2. **A grounded, cited chat layer (Google Gemini).** Answers only from
   retrieved passages, cites every claim, and explicitly declines rather
   than guessing when passages don't answer the question. Caught one real
   bug along the way: an initial regex-based refusal check
   (`/doesn'?t have.../i` on Gemini's free-text output) false-positived on a
   genuinely good, well-cited answer whose text happened to contain a
   caveat phrase. Fixed by switching to structured JSON output with an
   explicit `has_answer` boolean, instead of parsing prose for signals.
3. **Real market-rate data (closing the Phase 2 gap).** Direct pushback —
   "what was the actual purpose of including all those [Google Places]
   venues?" — surfaced that the `revenue_benchmarks` table had existed in
   the data model since Phase 1 planning but was never actually populated.
   Seven Fullerton venues' real starting prices were sourced from Zola,
   each individually address-verified (the initial pull included venues
   actually in Irvine, Costa Mesa, and Anaheim, since Zola's default search
   radius isn't city-scoped — five were excluded once checked).
4. **Reranking + an agentic-retrieval experiment**, chosen over a knowledge
   graph. `fee_schedules` and `revenue_benchmarks` are already relational
   (FKs to `cities` and `documents`, typed numeric columns) — this corpus
   is fee/permit/pricing facts, not an entity-relationship network a graph
   would meaningfully improve on. Combined with the brief's own warning that
   knowledge-graph pipelines "have a special talent for eating weekends,"
   agentic retrieval was the better-fitted experiment — and it directly
   targeted a diagnosed failure (a gym-permit question whose correct answer
   existed in the corpus but never matched that phrasing). The two
   techniques target genuinely different failure modes: reranking promotes
   a correct-but-buried chunk that's already been retrieved; the agentic
   requery step rewrites the search itself when nothing retrieved is
   actually relevant. A first version of the reranker's "is this enough to
   answer" threshold was miscalibrated — too strict, triggering unnecessary
   second searches (and once, a wrongly-conservative refusal on an already-
   good answer) — caught by testing a previously-good question against the
   new code before trusting it, and fixed before it shipped.
5. **Full re-evaluation against the finished chat layer.** All 13 questions
   re-run end to end: **0 FAIL**, down from the baseline's 5 — including
   eliminating the two most dangerous baseline failures (a different
   jurisdiction's permit fee presented as Fullerton's own threshold at 0.876
   similarity; an unrelated fee chunk presented as an insurance answer).
   Full grading in `scripts/eval/generation_evaluation.md`.

Tagged `phase-3`.

**Demo:** the chat interface (`web/index.html`) — a gym-permit question that
visibly triggers the "search refined" indicator and returns a correctly
cited answer, next to an out-of-scope question that's honestly declined.

---

## What this leaves for Phase 4 (not started, by design)

One decision is already banked for when the nine-city Central Orange County
expansion starts: **city disambiguation has to be a metadata filter (`city_id`)
applied before vector ranking, not left to embeddings to disambiguate.**
Nine cities' fee ordinances are structurally near-identical — "a special
event permit fee of $X shall be set by resolution," repeated per city — so
similarity search alone risks matching the right *kind* of fact to the wrong
city. This surfaced from asking "will this be an issue if I scale to Orange
County?" early on, well before Phase 4 planning was otherwise underway, and
is saved in both this plan and persistent project memory so it isn't lost
before that work starts.

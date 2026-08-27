# Prompts That Genuinely Changed the Architecture

Per the task brief's research-methodology guidance ("keep a record of the
prompts that genuinely changed your decisions"). These are pulled from the
actual build conversation with Claude across Phases 1–3, in chronological
order. Each entry: what was asked, what decision it actually changed, and
why it mattered.

---

### "Why do you recommend the OpenAI text-embedding?"

Pushed for a justification instead of accepting the default recommendation.
The follow-up questions this opened up ("How much can I expect to spend on
OpenAI?", "Is the Supabase gte-small option free? ... Can I switch later?")
led directly to choosing **gte-small running locally in a Supabase Edge
Function** over a paid third-party embedding API — zero cost, zero account
setup, and confirmed as a low-risk choice since switching later only means
re-embedding existing chunks, not rearchitecting anything.

### "Will this be an issue if I scale to Orange County?"

This single question produced the most important architectural principle in
the whole project: **city disambiguation has to be a metadata filter, not an
embedding-model choice.** Nine cities' ordinances are structurally
near-identical ("a special event permit fee of $X shall be set by
resolution," repeated per city) — embedding similarity alone risks matching
the right *kind* of fact to the wrong city. The fix (filter by `city_id`
before ranking by vector similarity) got written directly into the
instructions doc's Phase 4 section and saved to persistent memory so it
wouldn't get lost before Phase 4 actually starts.

### "How do you know it's a weak match? It shows a 77.8% similarity."

Refused to accept "it's weak" as an assertion. This forced an actual
empirical test — embedding a nonsense control query ("What is the capital of
France?") and running it through the same search — which revealed this
corpus's real similarity floor (~0.74, versus ~0.90 for genuinely relevant
matches). That floor number became a load-bearing fact later: it's exactly
what explained *why* the two out-of-scope baseline questions (Q12, Q13)
failed for different reasons, and why a similarity threshold alone can't
catch both failure modes.

### "Is Yelp Fusion free? ... I'm seeing different plans." (with screenshot)

Overturned a stale assumption — both mine and the instructions doc's — that
Yelp Fusion was a simple free starting point for the API ingestion
requirement. It isn't anymore (30-day trial, then $229+/month, business
email required). This directly caused the pivot to **Google Places API**,
and more importantly established a pattern for the rest of the build:
verify current pricing/terms before committing, rather than trust training
data. That pattern caught the same kind of staleness later with Eventbrite
(public search retired), CA ABC open data (no real API), and Google's own
Places pricing model (the old $200 pooled credit was replaced by per-SKU
limits in March 2025).

### "Is there anything about the instructions that calls for Railway?" → "I'm referring to the 'Build a Knowledge Base that actually answers questions' document."

The single biggest correction in the project. Up to this point, deployment
platform had been treated as an open choice (Railway vs. Vercel), reasoned
from a document I *had* read (the phase-plan `instructions.md`). This prompt
sent me back to actually read the original task brief PDF for the first
time — which names Railway as a required deliverable three separate times
("A working Railway link" is explicitly listed in the final handover
package). Without this question, the deployment would likely have moved to
Vercel, satisfying the spirit of "a live app" but not the letter of the
actual assignment.

### "Can we begin working on Phase 2 without destroying the Phase 1 demo?"

Surfaced a real gap: despite substantial Phase 1 work, nothing had actually
been committed to git yet — only the repo's original empty initial commit
existed. This produced the git-tagging discipline used for the rest of the
build (`phase-1`, `phase-2` tags as permanent snapshots, real commits before
starting new work) — not just a one-off fix, but the actual answer to "how
do we make phases individually demonstrable" that later shaped the Railway
deployment strategy too (one evolving URL + tags, chosen explicitly over
maintaining multiple live environments).

### "What does it mean that I can 'check out and redeploy an old snapshot on demand?' ... I need to show my work."

Pushed past a vague explanation to name the actual concern: durable,
presentable proof, not just technical recoverability. This is what settled
the "one URL + git tags" vs. "separate persistent URL per phase" decision —
tags plus GitHub's own history were judged sufficient as the durable record,
avoiding the cost/upkeep of running multiple live environments.

### "I would like to include pricing information for the venues... What was the actual purpose of including all those venues?"

Direct, slightly skeptical pushback on a Phase 2 deliverable (the 43 Google
Places venues) that turned out to be well-founded — those venues were
always directory/rating signal only, never pricing, because the originally-
planned pricing source (Peerspace) was bot-blocked back in Phase 2. This
question is what led to actually building the `revenue_benchmarks` table
(present in the original data model since Phase 1 planning, but never
implemented until this prompt) and sourcing real venue pricing from Zola —
closing a gap the Phase 3 baseline evaluation had already flagged (Q8) but
that hadn't been acted on yet.

---

## Pattern across all of these

Almost none of these were "explain this concept to me" questions. They were
either **(a) pushback on an unverified claim** ("how do you know," "is that
free," "is there anything that calls for X") or **(b) a why/what-for
question that exposed a decision made without a clearly articulated reason**
("what was the actual purpose"). Both types were more useful for shaping the
architecture than open-ended requests to proceed — worth keeping in mind for
Phase 4 and beyond.

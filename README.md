# OC Venue Activation Knowledge Base

A grounded, cited question and answer system for hosting one day "activations"
(wedding receptions, fitness pop ups, and similar short term events) across
nine cities in North and Central Orange County, California. Every answer is
generated only from real, cited source material. If the knowledge base does
not have the answer, it says so instead of guessing.

**Live app:** https://oc-venue-activation-kb-production.up.railway.app/

## What it answers

- Which permit applies to a given activity, and what it costs
- Insurance requirements for event permits
- How many events a venue can hold per year before needing a different permit
- Real venue rental pricing, both full event pricing and, as of Phase 5,
  hourly short term rental pricing
- It will not give investment advice, purchase decisions, or revenue
  forecasts. That is out of scope by design.

## Cities covered

Fullerton, Anaheim, Brea, La Habra, Santa Ana, Tustin, Buena Park, Stanton,
and Orange.

City is either auto detected from the question text or chosen directly from
a dropdown in the chat interface.

## How it works

- **Database:** Supabase Postgres with pgvector. Documents are chunked,
  embedded, and stored with source metadata (title, section, retrieval date,
  city).
- **Retrieval:** hybrid search combining full text search and vector
  similarity (reciprocal rank fusion), always filtered by city before
  ranking. This filter is applied at the database query level, not left for
  the embeddings to sort out on their own, so answers for one city cannot
  leak in facts from another.
- **Reranking and agentic retrieval:** a second AI pass scores how relevant
  the retrieved passages actually are, and can trigger one rewritten search
  if the first pass comes back weak.
- **Answer generation:** Google Gemini generates the final answer, citing
  every claim to a specific source passage, and returns a plain yes or no
  signal for whether it actually found an answer.
- **Edge functions:** two Supabase Edge Functions, `embed` (turns text into
  vectors) and `answer` (the full retrieval and generation pipeline), found
  in `supabase/functions/`.
- **Frontend:** a small static site in `web/` (chat interface, a raw
  retrieval view, and a page listing every ingested source), served by a
  minimal Node server and deployed on Railway.

## Data sources

- City municipal codes (permit and event chapters), read from official city
  PDFs where the city's own code hosting platform blocked automated access
- City fee schedule PDFs
- Google Places API, for a directory of real local venues and gyms
- OC Fire Authority and California ABC alcohol permit forms (these apply
  across every city, not just one)
- Zola, Eventective, and Wedding Spot, for real full event wedding venue
  pricing
- Giggster, for real hourly short term rental pricing (added in Phase 5)

## Project history

The project was built in five phases. Each one is tagged in git and written
up in more detail in `docs/`:

1. **Phase 1**, tag `phase-1`: proved the core pipeline on Fullerton alone.
2. **Phase 2**, tag `phase-2`: added all three required ways of bringing in
   data (an API, a live website, and uploaded documents), plus safe re
   ingestion so nothing gets duplicated.
3. **Phase 3**, tag `phase-3`: added the chat interface, hybrid search
   reranking, and a full evaluation against a 13 question test set.
4. **Phase 4**, tag `phase-4`: expanded from one city to nine, with city
   scoped retrieval proven correct at scale (zero cross city mix ups across
   a 40 question evaluation). See `docs/phase-4-plan.md`.
5. **Phase 5**: added real hourly rental pricing to support the actual
   business goal behind this project, helping venues weigh renting out
   space for a few hours at a time against a full day booking. See
   `docs/phase-5-plan.md`.

`docs/phase-plan-with-revisions.md` is a single place that tracks what
changed between the original plan and what actually shipped, phase by
phase, and why.

`docs/prompts-that-changed-decisions.md` records the specific questions
asked during the build that changed the direction of the project, such as
confirming Railway was a hard deployment requirement instead of an open
choice.

## Evaluation

- Baseline retrieval (before the chat layer existed): `scripts/eval/baseline_evaluation.md`
- Full generation evaluation, 13 question set, 0 failures: `scripts/eval/generation_evaluation.md`
- Phase 4 multi city evaluation, 40 questions across all nine cities, 40 out
  of 40 correct city routing: `scripts/eval/phase4_city_evaluation.md`

## Known gaps, on purpose

These are documented rather than hidden or guessed around:

- Exact event length and frequency ordinance thresholds for Stanton,
  Orange, and part of Buena Park could not be found through any working
  source and remain an open gap pending manual retrieval.
- Two real fee figures do not agree with each other: Brea's general fee
  schedule versus its own permit application form, and Tustin's permit
  application versus its comprehensive fee schedule. Both numbers are real
  and current, so both are kept and shown rather than picking one.
- Market rate pricing (both full event and hourly) is thin to nonexistent
  for La Habra, Tustin, and Stanton, since no pricing source checked had
  meaningful real listings for those cities.
- A revenue calculator that would combine rental income against permit,
  insurance, and staffing costs has not been built yet. The data needed for
  it now exists and is clearly labeled by pricing type, but the calculation
  itself is a deliberately separate next step.

## Repository layout

```
docs/               Phase plans, decision log, progress write ups
scripts/ingest/      One script per source per city, used to pull in and
                     embed data (idempotent: safe to re run)
scripts/eval/        Evaluation question sets, run scripts, and results
supabase/functions/  Edge functions: embed, answer
supabase/migrations/ Exact schema history, pulled directly from Supabase
source-docs/         Original source PDFs kept for reference
web/                 Static frontend (chat, raw retrieval view, sources view)
```

## Running it locally

The frontend is a static site with no build step:

```bash
cd web
npm start
```

Ingestion scripts are Python, and each one is self contained:

```bash
cd scripts/ingest
source .venv/bin/activate
python <script_name>.py
```

Most ingestion scripts write a `.sql` file rather than writing to the
database directly, so the SQL can be reviewed before being applied.

## Tech stack

Supabase (Postgres, pgvector, Edge Functions), Google Gemini (reranking and
answer generation), Google Places API, plain HTML and JavaScript for the
frontend, Node for the static server, deployed on Railway.

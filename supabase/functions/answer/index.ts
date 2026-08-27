import "jsr:@supabase/functions-js/edge-runtime.d.ts";

const model = new Supabase.ai.Session("gte-small");

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SUPABASE_ANON_KEY = Deno.env.get("SUPABASE_ANON_KEY")!;
const GEMINI_API_KEY = Deno.env.get("GEMINI_API_KEY")!;
const GEMINI_MODEL = Deno.env.get("GEMINI_MODEL") || "gemini-flash-latest";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

// Baseline-eval-derived scope check, applied before we even bother retrieving:
// these categories are out of scope regardless of how well matched the
// retrieved content ends up being (this is what a similarity threshold alone
// cannot catch - see baseline_evaluation.md finding on Q12 vs Q13).
const OUT_OF_SCOPE_PATTERNS: [RegExp, string][] = [
  [/\b(should i|worth it|good (idea|investment|deal)|buy|lease|invest|purchase)\b.*\b(property|venue|building|deal)\b/i,
    "This looks like an investment or purchase-decision question. This knowledge base provides permit requirements, fees, and cited reference data only - it does not give investment or \"should I do this deal\" advice."],
  [/\b(forecast|predict|next (quarter|year|month)|projected|will (my|the) .*(revenue|income|profit))\b/i,
    "This looks like a revenue forecast or prediction question. This knowledge base reports historical/benchmark data and cost math from cited sources - it does not generate financial forecasts or predictions."],
];

interface Hit {
  id: string;
  document_id: string;
  section_reference: string;
  content: string;
  similarity: number;
}

async function embed(text: string): Promise<number[]> {
  const out = await model.run(text, { mean_pool: true, normalize: true });
  return out as number[];
}

async function hybridSearch(
  queryText: string,
  queryEmbedding: number[],
  cityId: string,
  matchCount = 15
): Promise<Hit[]> {
  const res = await fetch(`${SUPABASE_URL}/rest/v1/rpc/hybrid_search`, {
    method: "POST",
    headers: {
      apikey: SUPABASE_ANON_KEY,
      Authorization: `Bearer ${SUPABASE_ANON_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query_text: queryText,
      query_embedding: JSON.stringify(queryEmbedding),
      match_city_id: cityId,
      match_count: matchCount,
    }),
  });
  if (!res.ok) throw new Error(`hybrid_search failed: ${res.status} ${await res.text()}`);
  return res.json();
}

interface City {
  id: string;
  name: string;
}

async function fetchCities(): Promise<City[]> {
  const res = await fetch(`${SUPABASE_URL}/rest/v1/cities?select=id,name`, {
    headers: { apikey: SUPABASE_ANON_KEY, Authorization: `Bearer ${SUPABASE_ANON_KEY}` },
  });
  if (!res.ok) throw new Error(`cities fetch failed: ${res.status}`);
  return res.json();
}

// City auto-detection: a plain keyword match against the question text,
// deliberately not an LLM call - city names are explicit, distinctive
// tokens, so this is free, instant, and just as reliable as the reranker
// already assumes a clean retrieval input is. Zero or multiple matches are
// both treated as "ask, don't guess" - silently defaulting to one city, or
// searching unscoped across all of them, is exactly the cross-city
// contamination the city_id filter exists to prevent.
function detectCity(question: string, cities: City[]): City[] {
  const lower = question.toLowerCase();
  return cities.filter((c) => lower.includes(c.name.toLowerCase()));
}

async function fetchDocumentTitles(docIds: string[]): Promise<Record<string, string>> {
  const uniqueIds = [...new Set(docIds)];
  if (uniqueIds.length === 0) return {};
  const res = await fetch(
    `${SUPABASE_URL}/rest/v1/documents?id=in.(${uniqueIds.join(",")})&select=id,title`,
    { headers: { apikey: SUPABASE_ANON_KEY, Authorization: `Bearer ${SUPABASE_ANON_KEY}` } }
  );
  if (!res.ok) throw new Error(`documents fetch failed: ${res.status}`);
  const rows = await res.json();
  const map: Record<string, string> = {};
  for (const r of rows) map[r.id] = r.title;
  return map;
}

function checkOutOfScope(question: string): string | null {
  for (const [pattern, message] of OUT_OF_SCOPE_PATTERNS) {
    if (pattern.test(question)) return message;
  }
  return null;
}

interface HitWithTitle extends Hit {
  document_title: string;
}

interface RerankResult {
  included: HitWithTitle[];
  retrievalSufficient: boolean;
  suggestedRequery: string | null;
}

// Reranking + agentic-retrieval-decision in one Gemini call: scores each
// candidate for actual relevance to the question (not just RRF/embedding
// rank), and - since the model already has to judge whether the candidates
// answer the question at all - asks it to propose a better search query when
// they don't. This is what promotes a correct-but-buried chunk (reranking)
// and, separately, catches the case where the right chunk was never
// retrieved for this phrasing at all (agentic requery).
async function rerankAndPlan(
  question: string,
  cityName: string,
  hits: HitWithTitle[],
  allowRequery: boolean
): Promise<RerankResult> {
  const candidates = hits
    .map((h, i) => `[${i}] ${h.document_title} - ${h.section_reference} (similarity ${h.similarity.toFixed(2)})\n${h.content}`)
    .join("\n\n");

  const requeryInstruction = allowRequery
    ? `- "retrieval_sufficient": true if the candidates collectively contain enough genuine, on-topic facts to build a real answer - even a partial one that combines several citations, or one that honestly notes a gap for only part of a multi-part question. Set this false if the candidates are clearly off-topic or the wrong jurisdiction, OR if they are the wrong KIND of information for what's actually being asked - e.g. the question asks what permit/process/approval is required but the candidates only show fee amounts, venue directory listings, or other adjacent-but-non-responsive material with no actual permit/process content; or the question asks about cost but the candidates only describe a process. Do not set this false merely because the answer would be incomplete in degree (missing one sub-part of several) - only when it's the wrong kind of material entirely.
- "suggested_requery": if retrieval_sufficient is false, propose ONE alternative search query (different phrasing, synonyms, or more specific terms) that would more likely retrieve the right material from a permit/fee/venue-pricing knowledge base. Otherwise null.`
    : `- Set "retrieval_sufficient" to true and "suggested_requery" to null always (a second search has already been attempted for this question).`;

  const prompt = `You are judging search results for a knowledge base about event activation permits, fees, and venues in ${cityName}, California.

Question: ${question}

Candidate passages (indexed):
${candidates}

For each candidate, judge whether it is actually relevant to directly answering the question - not just topically adjacent (e.g. a different city's fee, a different permit type, or a venue *listing* when the question asks about *permits* are NOT relevant even if they mention similar words).

Return:
- "scores": an array with one entry per candidate index, each {"index": number, "relevance_score": number between 0 and 1, "include": boolean (true only if genuinely relevant enough to help answer the question)}.
${requeryInstruction}`;

  const res = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json", "x-goog-api-key": GEMINI_API_KEY },
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }],
        generationConfig: {
          temperature: 0,
          responseMimeType: "application/json",
          responseSchema: {
            type: "object",
            properties: {
              scores: {
                type: "array",
                items: {
                  type: "object",
                  properties: {
                    index: { type: "integer" },
                    relevance_score: { type: "number" },
                    include: { type: "boolean" },
                  },
                  required: ["index", "relevance_score", "include"],
                },
              },
              retrieval_sufficient: { type: "boolean" },
              suggested_requery: { type: "string", nullable: true },
            },
            required: ["scores", "retrieval_sufficient"],
          },
        },
      }),
    }
  );
  if (!res.ok) throw new Error(`Gemini rerank error: ${res.status} ${await res.text()}`);
  const data = await res.json();
  const raw = data.candidates?.[0]?.content?.parts?.[0]?.text;
  if (!raw) return { included: hits.slice(0, 6), retrievalSufficient: true, suggestedRequery: null };
  const parsed = JSON.parse(raw);

  const scored = (parsed.scores as { index: number; relevance_score: number; include: boolean }[])
    .filter((s) => s.include && hits[s.index])
    .sort((a, b) => b.relevance_score - a.relevance_score)
    .slice(0, 6)
    .map((s) => hits[s.index]);

  return {
    included: scored,
    retrievalSufficient: Boolean(parsed.retrieval_sufficient),
    suggestedRequery: parsed.suggested_requery ?? null,
  };
}

async function generateAnswer(question: string, cityName: string, hits: (Hit & { document_title: string })[]): Promise<{ answer: string; refused: boolean }> {
  const context = hits
    .map((h, i) => `[${i + 1}] Source: ${h.document_title} - ${h.section_reference} (similarity ${h.similarity.toFixed(2)})\n${h.content}`)
    .join("\n\n");

  const prompt = `You are answering questions for a knowledge base about event activation permits, fees, and venues in ${cityName}, California. You are given retrieved passages below. Follow these rules strictly:

1. Answer ONLY using the passages provided below. Never use outside knowledge.
2. Cite every factual claim with its passage number, like [1] or [2].
3. If the passages do NOT clearly and directly answer the question - even if they are topically related or mention similar terms - say so explicitly instead of stretching a loosely-related passage into an answer. A passage about a different city's fee, a different permit type, or a different jurisdiction's numeric limit must NOT be presented as if it answers the question, even if it looks similar.
4. If the passages don't contain the answer, say plainly that this knowledge base doesn't have that information yet, rather than guessing or inventing a number.
5. This system does not give investment/purchase-decision advice or financial forecasts/predictions, even if relevant-looking data is retrieved. If the question is asking for either of those, decline and explain why, citing only what factual/reference data (if any) is genuinely relevant.
6. Be concise. Do not repeat the passages verbatim; synthesize.
7. Set has_answer to true only if the passages let you give a genuine, directly-responsive answer - even a partial one grounded in real citations. Set it to false if you had to say the information isn't available, or if you declined as out of scope.

Question: ${question}

Retrieved passages:
${context}`;

  const res = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json", "x-goog-api-key": GEMINI_API_KEY },
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }],
        generationConfig: {
          temperature: 0,
          responseMimeType: "application/json",
          responseSchema: {
            type: "object",
            properties: {
              answer: { type: "string" },
              has_answer: { type: "boolean" },
            },
            required: ["answer", "has_answer"],
          },
        },
      }),
    }
  );
  if (!res.ok) throw new Error(`Gemini API error: ${res.status} ${await res.text()}`);
  const data = await res.json();
  const raw = data.candidates?.[0]?.content?.parts?.[0]?.text;
  if (!raw) return { answer: "(no response generated)", refused: true };
  const parsed = JSON.parse(raw);
  return { answer: parsed.answer, refused: !parsed.has_answer };
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const { question } = await req.json();
    if (!question || typeof question !== "string") {
      return new Response(JSON.stringify({ error: "question (string) is required" }), {
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    const scopeRefusal = checkOutOfScope(question);
    if (scopeRefusal) {
      return new Response(
        JSON.stringify({ answer: scopeRefusal, refused: true, citations: [], out_of_scope: true }),
        { headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const cities = await fetchCities();
    const matchedCities = detectCity(question, cities);

    if (matchedCities.length === 0) {
      const cityList = cities.map((c) => c.name).join(", ");
      return new Response(
        JSON.stringify({
          answer: `Which city is this about? This knowledge base currently covers: ${cityList}. Naming the city in your question (e.g. "in Anaheim") gets you a properly scoped answer.`,
          refused: true,
          out_of_scope: false,
          needs_city: true,
          citations: [],
        }),
        { headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }
    if (matchedCities.length > 1) {
      const names = matchedCities.map((c) => c.name).join(" and ");
      return new Response(
        JSON.stringify({
          answer: `This question mentions more than one city (${names}). Please ask about one city at a time - each city's permits and fees are tracked separately, and combining them risks mixing up which rule applies where.`,
          refused: true,
          out_of_scope: false,
          needs_city: true,
          citations: [],
        }),
        { headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const city = matchedCities[0];

    const embedding = await embed(question);
    const hits = await hybridSearch(question, embedding, city.id);
    const titles = await fetchDocumentTitles(hits.map((h) => h.document_id));
    let hitsWithTitles: HitWithTitle[] = hits.map((h) => ({ ...h, document_title: titles[h.document_id] ?? "Unknown source" }));

    let { included, retrievalSufficient, suggestedRequery } = await rerankAndPlan(question, city.name, hitsWithTitles, true);
    let retrievalHops = 1;
    let requeryUsed: string | null = null;

    if (!retrievalSufficient && suggestedRequery) {
      const requeryEmbedding = await embed(suggestedRequery);
      const requeryHits = await hybridSearch(suggestedRequery, requeryEmbedding, city.id);
      const requeryTitles = await fetchDocumentTitles(requeryHits.map((h) => h.document_id));
      const requeryHitsWithTitles: HitWithTitle[] = requeryHits.map((h) => ({
        ...h,
        document_title: requeryTitles[h.document_id] ?? "Unknown source",
      }));

      const seen = new Set(hitsWithTitles.map((h) => h.id));
      const merged = [...hitsWithTitles, ...requeryHitsWithTitles.filter((h) => !seen.has(h.id))];

      const second = await rerankAndPlan(question, city.name, merged, false);
      included = second.included;
      retrievalHops = 2;
      requeryUsed = suggestedRequery;
    }

    const { answer, refused } = await generateAnswer(question, city.name, included);

    return new Response(
      JSON.stringify({
        answer,
        refused,
        out_of_scope: false,
        city: city.name,
        retrieval_hops: retrievalHops,
        requery: requeryUsed,
        citations: included.map((h) => ({
          title: h.document_title,
          section_reference: h.section_reference,
          similarity: h.similarity,
        })),
      }),
      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (error) {
    return new Response(JSON.stringify({ error: (error as Error).message }), {
      status: 500,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }
});

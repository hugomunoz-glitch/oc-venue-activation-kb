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
  document_id: string;
  section_reference: string;
  content: string;
  similarity: number;
}

async function embed(text: string): Promise<number[]> {
  const out = await model.run(text, { mean_pool: true, normalize: true });
  return out as number[];
}

async function hybridSearch(queryText: string, queryEmbedding: number[], matchCount = 6): Promise<Hit[]> {
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
      match_count: matchCount,
    }),
  });
  if (!res.ok) throw new Error(`hybrid_search failed: ${res.status} ${await res.text()}`);
  return res.json();
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

async function generateAnswer(question: string, hits: (Hit & { document_title: string })[]): Promise<{ answer: string; refused: boolean }> {
  const context = hits
    .map((h, i) => `[${i + 1}] Source: ${h.document_title} - ${h.section_reference} (similarity ${h.similarity.toFixed(2)})\n${h.content}`)
    .join("\n\n");

  const prompt = `You are answering questions for a knowledge base about event activation permits, fees, and venues in Fullerton, California. You are given retrieved passages below. Follow these rules strictly:

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
          temperature: 0.1,
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

    const embedding = await embed(question);
    const hits = await hybridSearch(question, embedding);
    const titles = await fetchDocumentTitles(hits.map((h) => h.document_id));
    const hitsWithTitles = hits.map((h) => ({ ...h, document_title: titles[h.document_id] ?? "Unknown source" }));

    const { answer, refused } = await generateAnswer(question, hitsWithTitles);

    return new Response(
      JSON.stringify({
        answer,
        refused,
        out_of_scope: false,
        citations: hitsWithTitles.map((h) => ({
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

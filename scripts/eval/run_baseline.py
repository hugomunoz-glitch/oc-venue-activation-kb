"""
Phase 3 baseline evaluation: runs the 13 test questions from the instructions
doc's problem statement against the live hybrid_search, one-shot retrieval
only (no generation layer exists yet). Writes results to baseline_results.json
for manual grading / writeup.
"""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "ingest"))

import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "ingest", ".env"))

SUPABASE_URL = os.environ["SUPABASE_URL"].rstrip("/")
SUPABASE_ANON_KEY = os.environ["SUPABASE_ANON_KEY"]

QUESTIONS = [
    "Does a Fullerton wedding venue need a Conditional Use Permit (CUP) amendment to host more than its currently-approved number of events per year, or does a Temporary Use Permit (TUP) cover extra one-off events?",
    "What permits does a gym in Fullerton need to host a one-day fitness pop-up in partnership with an outside brand?",
    "Is a backyard/outdoor wedding reception activation in Fullerton covered by a Special Event Permit, a TUP, or neither, depending on guest count?",
    "What is the typical added cost (permit + insurance + staffing + ABC license) of adding alcohol service to a one-day activation in Fullerton, and how does that compare to what a comparable activation charges guests?",
    "Is there an attendance cap that triggers fire-marshal/occupancy review for a temporary event at a gym in Fullerton?",
    "What insurance/Certificate of Insurance (COI) liability limits does Fullerton typically require for a one-day third-party activation, and how much does that coverage typically cost?",
    "How many special-event or TUP filings can one venue submit per year in Fullerton before the city requires a CUP instead?",
    "What's the typical market rental rate range for a mid-size event space (wedding venue or gym floor) in Fullerton for a single-day activation?",
    "For a venue that wants to keep per-guest activation pricing low enough for a local community group, does the knowledge base have enough fee, insurance, and market-rate data to say whether that activation can still break even?",
    "Does temporarily converting gym floor space for a wedding reception or private event trigger a change-of-use or building-code inspection, separate from the event permit itself?",
    "If a venue offers a discounted rate to a local nonprofit renting the space, how much margin is left after permit, insurance, and staffing costs at that discounted price?",
    "Should I buy or lease a specific property to open a wedding venue in Fullerton?",
    "What will my gym's activation revenue be next quarter?",
]


def embed(text: str) -> list[float]:
    resp = requests.post(
        f"{SUPABASE_URL}/functions/v1/embed",
        headers={"Authorization": f"Bearer {SUPABASE_ANON_KEY}", "Content-Type": "application/json"},
        json={"input": text},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["embedding"]


def hybrid_search(query_text: str, query_embedding: list[float], match_count: int = 5) -> list[dict]:
    resp = requests.post(
        f"{SUPABASE_URL}/rest/v1/rpc/hybrid_search",
        headers={
            "apikey": SUPABASE_ANON_KEY,
            "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "query_text": query_text,
            "query_embedding": json.dumps(query_embedding),
            "match_count": match_count,
        },
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json()


def fetch_document_titles(doc_ids: list[str]) -> dict:
    if not doc_ids:
        return {}
    ids = ",".join(set(doc_ids))
    resp = requests.get(
        f"{SUPABASE_URL}/rest/v1/documents?id=in.({ids})&select=id,title",
        headers={"apikey": SUPABASE_ANON_KEY, "Authorization": f"Bearer {SUPABASE_ANON_KEY}"},
        timeout=20,
    )
    resp.raise_for_status()
    return {row["id"]: row["title"] for row in resp.json()}


def main():
    results = []
    for i, q in enumerate(QUESTIONS, 1):
        print(f"[{i}/{len(QUESTIONS)}] {q[:70]}...", file=sys.stderr)
        vec = embed(q)
        hits = hybrid_search(q, vec)
        titles = fetch_document_titles([h["document_id"] for h in hits])
        results.append({
            "n": i,
            "question": q,
            "hits": [
                {
                    "document_title": titles.get(h["document_id"], "?"),
                    "section_reference": h["section_reference"],
                    "similarity": round(h["similarity"], 3),
                    "content": h["content"],
                }
                for h in hits
            ],
        })

    out_path = os.path.join(os.path.dirname(__file__), "baseline_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()

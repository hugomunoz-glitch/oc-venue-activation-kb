"""
Phase 3 generation-layer re-evaluation: runs the same 13 test questions from
run_baseline.py through the live /answer edge function (hybrid search +
reranking + agentic requery + Gemini synthesis), instead of raw retrieval.
Writes results to generation_results.json for grading against baseline_evaluation.md.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import requests
from dotenv import load_dotenv

from run_baseline import QUESTIONS

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "ingest", ".env"))

SUPABASE_URL = os.environ["SUPABASE_URL"].rstrip("/")
SUPABASE_ANON_KEY = os.environ["SUPABASE_ANON_KEY"]


def ask(question: str) -> dict:
    resp = requests.post(
        f"{SUPABASE_URL}/functions/v1/answer",
        headers={"Authorization": f"Bearer {SUPABASE_ANON_KEY}", "Content-Type": "application/json"},
        json={"question": question},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


def main():
    results = []
    for i, q in enumerate(QUESTIONS, 1):
        print(f"[{i}/{len(QUESTIONS)}] {q[:70]}...", file=sys.stderr)
        data = ask(q)
        results.append({
            "n": i,
            "question": q,
            "answer": data.get("answer"),
            "refused": data.get("refused"),
            "out_of_scope": data.get("out_of_scope"),
            "retrieval_hops": data.get("retrieval_hops"),
            "requery": data.get("requery"),
            "citations": data.get("citations", []),
        })

    out_path = os.path.join(os.path.dirname(__file__), "generation_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()

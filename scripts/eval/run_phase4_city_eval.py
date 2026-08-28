"""
Phase 4 per-city evaluation: mirrors the spirit of run_baseline.py's
original 13-question Fullerton set, scaled to a proportionate 5 questions
per new city (permit classification, fee, duration/frequency threshold,
insurance/requirement, market pricing) rather than repeating all 13 verbatim
for all eight new cities. Hits the deployed /answer endpoint directly, same
pattern as run_generation_eval.py.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "ingest", ".env"))

SUPABASE_URL = os.environ["SUPABASE_URL"].rstrip("/")
SUPABASE_ANON_KEY = os.environ["SUPABASE_ANON_KEY"]

QUESTIONS_BY_CITY = {
    "Anaheim": [
        "What permits does a gym in Anaheim need to host a one-day fitness pop-up event on its own property?",
        "What does a Minor Conditional Use Permit cost in Anaheim?",
        "How many special event permits can one business get per year in Anaheim, and how many days can each one last?",
        "What insurance does Anaheim's Festival Permit require?",
        "What is the typical market rental rate for a wedding venue in Anaheim?",
    ],
    "Brea": [
        "How far in advance do I need to apply for a temporary use permit in Brea, and what does it cost?",
        "What insurance does Brea require for an event on public property?",
        "What size tent triggers a Fire Department permit in Brea?",
        "What does a Conditional Use Permit cost in Brea?",
        "What is the typical venue rental rate in Brea?",
    ],
    "La Habra": [
        "How many attendees can I have before my special event in La Habra counts as a large event?",
        "How many special events can one property host per year in La Habra?",
        "What does a Conditional Use Permit cost in La Habra?",
        "What size tent requires a building permit in La Habra?",
        "What is the typical venue rental rate in La Habra?",
    ],
    "Santa Ana": [
        "I expect 300 attendees at my one-day activation in Santa Ana - is that a moderate or major event, and how far ahead do I need to apply?",
        "What is the exact fee for a special event permit in Santa Ana?",
        "What insurance does Santa Ana require for an event permit?",
        "What does a Conditional Use Permit cost in Santa Ana?",
        "What is the typical venue rental rate in Santa Ana?",
    ],
    "Tustin": [
        "What does a Large Gathering Use Permit cost in Tustin?",
        "At what tent size do I need Orange County Fire Authority approval for an event in Tustin?",
        "What insurance does a Large Gathering Use Permit require in Tustin?",
        "What does a Conditional Use Permit cost in Tustin?",
        "What is the typical venue rental rate in Tustin?",
    ],
    "Buena Park": [
        "How far ahead must I apply for a temporary use permit in Buena Park, and what does it cost?",
        "What does a Major Conditional Use Permit cost in Buena Park?",
        "What does a Minor Conditional Use Permit cost in Buena Park?",
        "What does a Variance cost in Buena Park?",
        "What is the typical venue rental rate in Buena Park?",
    ],
    "Stanton": [
        "What does a Temporary Use Permit cost in Stanton?",
        "What is a typical venue rental rate in Stanton?",
        "What does a Special Events Permit cost in Stanton?",
        "What does a Conditional Use Permit cost in Stanton?",
        "What does a Variance cost in Stanton?",
    ],
    "Orange": [
        "What does a special event permit cost in the city of Orange?",
        "What is the typical market rental rate for a wedding venue in Orange?",
        "What is the difference between the Special Event Permit fee and the Special Event Park Permit fee in Orange?",
        "What does a Conditional Use Permit or Variance cost in Orange?",
        "What is the fee difference between a recurring and non-recurring Temporary Use Permit in Orange?",
    ],
}


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
    total = sum(len(qs) for qs in QUESTIONS_BY_CITY.values())
    n = 0
    for city, questions in QUESTIONS_BY_CITY.items():
        for q in questions:
            n += 1
            print(f"[{n}/{total}] ({city}) {q[:60]}...", file=sys.stderr)
            data = ask(q)
            results.append({
                "expected_city": city,
                "question": q,
                "answer": data.get("answer"),
                "refused": data.get("refused"),
                "returned_city": data.get("city"),
                "retrieval_hops": data.get("retrieval_hops"),
                "requery": data.get("requery"),
                "citations": data.get("citations", []),
            })

    out_path = os.path.join(os.path.dirname(__file__), "phase4_city_eval_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()

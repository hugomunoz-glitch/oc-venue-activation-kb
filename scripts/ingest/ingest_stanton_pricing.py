"""
Ingests Stanton venue info (chunks_stanton_pricing.py). No revenue_benchmarks
row this time - there's no actual price or guest-capacity figure to put in
a structured numeric table, just a real venue with a genuine pricing gap
(see the chunk's own content). Document + chunk only, same honesty
precedent as OCFA's case-by-case fee in Fullerton having no fee_schedules
row.

Usage:
    source .venv/bin/activate
    python ingest_stanton_pricing.py
    psql "$DATABASE_URL" -f ingest_stanton_pricing.sql
"""

import sys

from chunks_stanton_pricing import CITY, DOCUMENTS
from common import build_document_sql


def main():
    statements = [build_document_sql(CITY, doc) for doc in DOCUMENTS]

    out_path = "ingest_stanton_pricing.sql"
    with open(out_path, "w") as f:
        f.write("\n\n".join(statements))

    print(f"Wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()

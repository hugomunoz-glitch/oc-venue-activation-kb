"""
Phase 4, Brea: reads chunks_brea.py, embeds each chunk, writes ingest_brea.sql.
No fee_schedules rows this time - the two document/permit fee figures ($55
vs $850) are flagged as an unreconciled discrepancy rather than picked as a
single clean number, so there's no unambiguous value to put in a structured
numeric table (same honesty-about-gaps precedent as OCFA's chunk in Phase 2,
which also had no fee_schedules rows for a fee stated as "case by case").

Usage:
    source .venv/bin/activate
    python ingest_brea.py
    psql "$DATABASE_URL" -f ingest_brea.sql
"""

import sys

from chunks_brea import CITY, DOCUMENTS
from common import build_document_sql


def main():
    statements = [build_document_sql(CITY, doc) for doc in DOCUMENTS]

    out_path = "ingest_brea.sql"
    with open(out_path, "w") as f:
        f.write("\n\n".join(statements))

    print(f"Wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()

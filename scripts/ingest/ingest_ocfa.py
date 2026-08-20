"""
Ingests the OCFA special event permit page (chunks_ocfa.py) - the KB's
"live website" ingestion method.

Usage:
    source .venv/bin/activate
    python ingest_ocfa.py
    psql "$DATABASE_URL" -f ingest_ocfa.sql
"""

import os
import sys

from chunks_ocfa import CITY, DOCUMENTS
from common import build_document_sql


def main():
    statements = [build_document_sql(CITY, doc) for doc in DOCUMENTS]

    out_path = os.path.join(os.path.dirname(__file__), "ingest_ocfa.sql")
    with open(out_path, "w") as f:
        f.write("\n\n".join(statements))

    print(f"Wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()

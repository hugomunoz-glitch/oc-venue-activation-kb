"""
Reads chunks_fullerton.py, embeds each chunk's text via the deployed Supabase
`embed` Edge Function (gte-small, 384-dim), and writes ingest_fullerton.sql -
one self-contained INSERT statement per document (using a CTE so we never
have to hardcode a generated document_id) plus one INSERT for fee_schedules.

Usage:
    pip install -r requirements.txt
    cp .env.example .env   # fill in SUPABASE_URL + SUPABASE_ANON_KEY
    python generate_sql.py

The anon/publishable key is enough here - the embed function only requires a
valid JWT (verify_jwt=true), not elevated privilege. Writing to the database
still requires running the generated SQL with an elevated connection (e.g.
via the Supabase SQL editor, the Supabase MCP `execute_sql` tool, or a
service-role-authenticated client) since RLS only grants public SELECT.
"""

import json
import os
import sys

import requests
from dotenv import load_dotenv

from chunks_fullerton import CITY, DOCUMENTS, FEE_ROWS

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"].rstrip("/")
SUPABASE_ANON_KEY = os.environ["SUPABASE_ANON_KEY"]
EMBED_URL = f"{SUPABASE_URL}/functions/v1/embed"


def embed(text: str) -> list[float]:
    resp = requests.post(
        EMBED_URL,
        headers={
            "Authorization": f"Bearer {SUPABASE_ANON_KEY}",
            "Content-Type": "application/json",
        },
        json={"input": text},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        raise RuntimeError(f"embed function error: {data['error']}")
    return data["embedding"]


def sql_literal(value) -> str:
    """Dollar-quoted string literal - sidesteps apostrophe/quote escaping entirely."""
    if value is None:
        return "null"
    return f"$q${value}$q$"


def vector_literal(vec: list[float]) -> str:
    return "'[" + ",".join(f"{x:.8f}" for x in vec) + "]'::extensions.vector(384)"


def build_document_sql(doc: dict) -> str:
    chunk_rows = []
    print(f"Embedding {len(doc['chunks'])} chunks for: {doc['title']}", file=sys.stderr)
    for idx, (section_reference, content) in enumerate(doc["chunks"]):
        vec = embed(content)
        chunk_rows.append(
            f"({idx}, {sql_literal(section_reference)}, {sql_literal(content)}, {vector_literal(vec)})"
        )

    chunk_values_sql = ",\n".join(chunk_rows)
    return f"""
with target_city as (
  select id from cities where name = {sql_literal(CITY)}
),
new_doc as (
  insert into documents (city_id, title, source_type, code_chapter, source_name, source_file, retrieved_date, effective_date, effective_date_confidence, notes)
  select id, {sql_literal(doc['title'])}, {sql_literal(doc['source_type'])}, {sql_literal(doc['code_chapter'])},
         {sql_literal(doc['source_name'])}, {sql_literal(doc['source_file'])}, {sql_literal(doc['retrieved_date'])}::date,
         {sql_literal(doc['effective_date'])}::date, {sql_literal(doc['effective_date_confidence'])}, {sql_literal(doc['notes'])}
  from target_city
  returning id, city_id
)
insert into chunks (document_id, city_id, chunk_index, section_reference, content, embedding)
select new_doc.id, new_doc.city_id, v.idx, v.section_reference, v.content, v.embedding
from new_doc, (values
{chunk_values_sql}
) as v(idx, section_reference, content, embedding);
"""


def build_fee_schedules_sql() -> str:
    value_rows = []
    for row in FEE_ROWS:
        value_rows.append(
            "(" + ", ".join([
                sql_literal(row["permit_type"]),
                sql_literal(row["fee_name"]),
                str(row["amount_usd"]) if row["amount_usd"] is not None else "null",
                str(row["amount_usd_min"]) if row["amount_usd_min"] is not None else "null",
                str(row["amount_usd_max"]) if row["amount_usd_max"] is not None else "null",
                sql_literal(row["amount_type"]),
                sql_literal(row["code_section"]),
                sql_literal(row["applies_to_track"]),
                sql_literal(row["notes"]),
            ]) + ")"
        )

    fee_values_sql = ",\n".join(value_rows)
    return f"""
with target_city as (
  select id from cities where name = {sql_literal(CITY)}
),
fee_doc as (
  select id from documents where source_file = 'source-docs/fullerton/permit-applications/special-event-permit-application-with-fees.pdf'
  order by created_at desc limit 1
)
insert into fee_schedules (city_id, permit_type, fee_name, amount_usd, amount_usd_min, amount_usd_max, amount_type, code_section, applies_to_track, effective_date, effective_date_confidence, source_document_id, notes)
select target_city.id, v.permit_type, v.fee_name, v.amount_usd, v.amount_usd_min, v.amount_usd_max, v.amount_type, v.code_section, v.applies_to_track,
       '2026-03-10'::date, 'inferred_from_form_footer', fee_doc.id, v.notes
from target_city, fee_doc, (values
{fee_values_sql}
) as v(permit_type, fee_name, amount_usd, amount_usd_min, amount_usd_max, amount_type, code_section, applies_to_track, notes);
"""


def main():
    statements = [build_document_sql(doc) for doc in DOCUMENTS]
    statements.append(build_fee_schedules_sql())

    out_path = os.path.join(os.path.dirname(__file__), "ingest_fullerton.sql")
    with open(out_path, "w") as f:
        f.write("\n\n".join(statements))

    print(f"Wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()

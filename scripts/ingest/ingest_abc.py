"""
Ingests California ABC temporary/one-day alcohol permit reference data
(chunks_abc.py) into Supabase: one document + chunks per ABC form, plus
structured fee_schedules rows tagged with each row's own effective_date
and linked to whichever document it belongs to (unlike the Fullerton
fee data, these two forms have different effective dates and each fee
row belongs to a specific one of the two documents).

Usage:
    source .venv/bin/activate
    python ingest_abc.py
    psql "$DATABASE_URL" -f ingest_abc.sql
"""

import os
import sys

import requests
from dotenv import load_dotenv

from chunks_abc import CITY, DOCUMENTS, FEE_ROWS

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"].rstrip("/")
SUPABASE_ANON_KEY = os.environ["SUPABASE_ANON_KEY"]
EMBED_URL = f"{SUPABASE_URL}/functions/v1/embed"


def embed(text: str) -> list[float]:
    resp = requests.post(
        EMBED_URL,
        headers={"Authorization": f"Bearer {SUPABASE_ANON_KEY}", "Content-Type": "application/json"},
        json={"input": text},
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()
    if "error" in data:
        raise RuntimeError(f"embed function error: {data['error']}")
    return data["embedding"]


def sql_literal(value) -> str:
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
        chunk_rows.append(f"({idx}, {sql_literal(section_reference)}, {sql_literal(content)}, {vector_literal(vec)})")

    chunk_values_sql = ",\n".join(chunk_rows)
    return f"""
with target_city as (
  select id from cities where name = {sql_literal(CITY)}
),
upserted_doc as (
  insert into documents (city_id, title, source_type, source_name, source_key, retrieved_date, effective_date, effective_date_confidence, notes)
  select id, {sql_literal(doc['title'])}, {sql_literal(doc['source_type'])}, {sql_literal(doc['source_name'])},
         {sql_literal(doc['source_key'])}, {sql_literal(doc['retrieved_date'])}::date,
         {sql_literal(doc['effective_date'])}::date, {sql_literal(doc['effective_date_confidence'])}, {sql_literal(doc['notes'])}
  from target_city
  on conflict (source_key) do update set
    title = excluded.title,
    retrieved_date = excluded.retrieved_date,
    effective_date = excluded.effective_date,
    effective_date_confidence = excluded.effective_date_confidence,
    notes = excluded.notes
  returning id, city_id
),
cleared_chunks as (
  delete from chunks where document_id in (select id from upserted_doc)
)
insert into chunks (document_id, city_id, chunk_index, section_reference, content, embedding)
select upserted_doc.id, upserted_doc.city_id, v.idx, v.section_reference, v.content, v.embedding
from upserted_doc, (values
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
                str(row["amount_usd"]) if row["amount_usd"] is not None else "null::numeric",
                str(row["amount_usd_min"]) if row["amount_usd_min"] is not None else "null::numeric",
                str(row["amount_usd_max"]) if row["amount_usd_max"] is not None else "null::numeric",
                sql_literal(row["amount_type"]),
                sql_literal(row["code_section"]),
                sql_literal(row["applies_to_track"]),
                sql_literal(row["effective_date"]) + "::date",
                sql_literal(row["notes"]),
                # source_document_id: pick the ABC-221 doc for nonprofit-track rows, ABC-218 for the caterer-track rows
                "(select id from documents where source_key = "
                + sql_literal(
                    "https://www.abc.ca.gov/wp-content/uploads/forms/ABC-221.pdf"
                    if row["applies_to_track"] == "statewide_nonprofit_only"
                    else "https://www.abc.ca.gov/wp-content/uploads/forms/ABC-218.pdf"
                )
                + ")",
            ]) + ")"
        )

    fee_values_sql = ",\n".join(value_rows)
    return f"""
with target_city as (
  select id from cities where name = {sql_literal(CITY)}
)
insert into fee_schedules (city_id, permit_type, fee_name, amount_usd, amount_usd_min, amount_usd_max, amount_type, code_section, applies_to_track, effective_date, effective_date_confidence, source_document_id, notes)
select target_city.id, v.permit_type, v.fee_name, v.amount_usd, v.amount_usd_min, v.amount_usd_max, v.amount_type, v.code_section, v.applies_to_track,
       v.effective_date, 'confirmed', v.source_document_id, v.notes
from target_city, (values
{fee_values_sql}
) as v(permit_type, fee_name, amount_usd, amount_usd_min, amount_usd_max, amount_type, code_section, applies_to_track, effective_date, notes, source_document_id);
"""


def main():
    statements = [build_document_sql(doc) for doc in DOCUMENTS]
    statements.append(build_fee_schedules_sql())

    out_path = os.path.join(os.path.dirname(__file__), "ingest_abc.sql")
    with open(out_path, "w") as f:
        f.write("\n\n".join(statements))

    print(f"Wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()

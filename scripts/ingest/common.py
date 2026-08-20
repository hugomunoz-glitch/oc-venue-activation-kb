"""
Shared helpers for the ingest_*.py scripts: embedding via the deployed Supabase
`embed` Edge Function, SQL literal formatting, and the idempotent
upsert-by-source_key document+chunks pattern used by every ingestion script.
"""

import os
import sys

import requests
from dotenv import load_dotenv

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
    """Dollar-quoted string literal - sidesteps apostrophe/quote escaping entirely."""
    if value is None:
        return "null"
    return f"$q${value}$q$"


def vector_literal(vec: list[float]) -> str:
    return "'[" + ",".join(f"{x:.8f}" for x in vec) + "]'::extensions.vector(384)"


def build_document_sql(city: str, doc: dict) -> str:
    """
    Idempotent upsert-by-source_key for one document + its chunks.
    `doc` needs: title, source_type, source_name, source_key, retrieved_date,
    chunks (list of (section_reference, content) tuples), and optionally
    source_file, code_chapter, effective_date, effective_date_confidence, notes.
    """
    chunk_rows = []
    print(f"Embedding {len(doc['chunks'])} chunks for: {doc['title']}", file=sys.stderr)
    for idx, (section_reference, content) in enumerate(doc["chunks"]):
        vec = embed(content)
        chunk_rows.append(f"({idx}, {sql_literal(section_reference)}, {sql_literal(content)}, {vector_literal(vec)})")

    chunk_values_sql = ",\n".join(chunk_rows)
    source_key = doc.get("source_key") or doc.get("source_file")
    return f"""
with target_city as (
  select id from cities where name = {sql_literal(city)}
),
upserted_doc as (
  insert into documents (city_id, title, source_type, code_chapter, source_name, source_file, source_key, retrieved_date, effective_date, effective_date_confidence, notes)
  select id, {sql_literal(doc['title'])}, {sql_literal(doc['source_type'])}, {sql_literal(doc.get('code_chapter'))},
         {sql_literal(doc['source_name'])}, {sql_literal(doc.get('source_file'))}, {sql_literal(source_key)}, {sql_literal(doc['retrieved_date'])}::date,
         {sql_literal(doc.get('effective_date'))}::date, {sql_literal(doc.get('effective_date_confidence'))}, {sql_literal(doc.get('notes'))}
  from target_city
  on conflict (source_key) do update set
    title = excluded.title,
    source_type = excluded.source_type,
    code_chapter = excluded.code_chapter,
    source_name = excluded.source_name,
    source_file = excluded.source_file,
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

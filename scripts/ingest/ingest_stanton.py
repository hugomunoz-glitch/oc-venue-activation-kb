"""
Phase 4, Stanton: reads chunks_stanton.py, embeds each chunk, writes
ingest_stanton.sql (documents/chunks + fee_schedules).

Usage:
    source .venv/bin/activate
    python ingest_stanton.py
    psql "$DATABASE_URL" -f ingest_stanton.sql
"""

import sys

from chunks_stanton import CITY, DOCUMENTS, FEE_ROWS
from common import build_document_sql, sql_literal

SOURCE_KEY = "http://www.stantonca.gov/2026 CD FEE SCHEDULE EFFECTIVE 7-1-2026.pdf"


def build_fee_schedules_sql() -> str:
    value_rows = []
    for row in FEE_ROWS:
        value_rows.append(
            "(" + ", ".join([
                sql_literal(row["permit_type"]),
                sql_literal(row["fee_name"]),
                f"{row['amount_usd']}::numeric" if row["amount_usd"] is not None else "null::numeric",
                f"{row['amount_usd_min']}::numeric" if row["amount_usd_min"] is not None else "null::numeric",
                f"{row['amount_usd_max']}::numeric" if row["amount_usd_max"] is not None else "null::numeric",
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
  select id from documents where source_key = {sql_literal(SOURCE_KEY)}
),
cleared_fees as (
  delete from fee_schedules where source_document_id in (select id from fee_doc)
)
insert into fee_schedules (city_id, permit_type, fee_name, amount_usd, amount_usd_min, amount_usd_max, amount_type, code_section, applies_to_track, effective_date, effective_date_confidence, source_document_id, notes)
select target_city.id, v.permit_type, v.fee_name, v.amount_usd, v.amount_usd_min, v.amount_usd_max, v.amount_type, v.code_section, v.applies_to_track,
       '2026-07-01'::date, 'stated_on_document', fee_doc.id, v.notes
from target_city, fee_doc, (values
{fee_values_sql}
) as v(permit_type, fee_name, amount_usd, amount_usd_min, amount_usd_max, amount_type, code_section, applies_to_track, notes);
"""


def main():
    statements = [build_document_sql(CITY, doc) for doc in DOCUMENTS]
    statements.append(build_fee_schedules_sql())

    out_path = "ingest_stanton.sql"
    with open(out_path, "w") as f:
        f.write("\n\n".join(statements))

    print(f"Wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()

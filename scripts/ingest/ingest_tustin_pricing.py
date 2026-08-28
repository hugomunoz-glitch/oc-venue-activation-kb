"""
Ingests Tustin venue pricing (chunks_tustin_pricing.py). Single-venue
structure, same as Brea's.

Usage:
    source .venv/bin/activate
    python ingest_tustin_pricing.py
    psql "$DATABASE_URL" -f ingest_tustin_pricing.sql
"""

import os
import sys

from chunks_tustin_pricing import CITY, DOCUMENTS, VENUES
from common import build_document_sql, sql_literal


def build_revenue_benchmarks_sql() -> str:
    value_rows = []
    for v in VENUES:
        source_key = f"https://www.wedding-spot.com/venue/{v['slug']}"
        value_rows.append(
            "("
            + ", ".join([
                sql_literal(v["name"]),
                sql_literal("wedding_venue"),
                sql_literal("wedding"),
                str(v["starting_price"]) if v["starting_price"] is not None else "null::numeric",
                sql_literal("\"Starting at\" marketplace price, not a guaranteed quote."),
                str(v["capacity_min"]) if v["capacity_min"] is not None else "null::int",
                str(v["capacity_max"]) if v["capacity_max"] is not None else "null::int",
                sql_literal(v["tier"]),
                sql_literal(source_key),
            ])
            + ")"
        )
    values_sql = ",\n".join(value_rows)

    return f"""
with target_city as (
  select id from cities where name = {sql_literal(CITY)}
)
insert into revenue_benchmarks (city_id, venue_name, venue_type, activation_type, starting_price_usd, price_note, guest_capacity_min, guest_capacity_max, service_tier, source_confidence, effective_date, source_document_id, notes)
select target_city.id, v.venue_name, v.venue_type, v.activation_type, v.starting_price_usd, v.price_note, v.guest_capacity_min, v.guest_capacity_max, v.service_tier,
       'medium', '2026-08-27'::date, (select id from documents where source_key = v.source_key), null
from target_city, (values
{values_sql}
) as v(venue_name, venue_type, activation_type, starting_price_usd, price_note, guest_capacity_min, guest_capacity_max, service_tier, source_key);
"""


def main():
    statements = [build_document_sql(CITY, doc) for doc in DOCUMENTS]
    statements.append(build_revenue_benchmarks_sql())

    out_path = os.path.join(os.path.dirname(__file__), "ingest_tustin_pricing.sql")
    with open(out_path, "w") as f:
        f.write("\n\n".join(statements))

    print(f"Wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()

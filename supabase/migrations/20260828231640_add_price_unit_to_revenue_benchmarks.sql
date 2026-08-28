alter table revenue_benchmarks add column price_unit text not null default 'per_event';
comment on column revenue_benchmarks.price_unit is 'per_event (full-day/full-event starting price, e.g. Zola) or per_hour (short-term hourly rental, e.g. Giggster) - required to avoid conflating the two in any future revenue math.';

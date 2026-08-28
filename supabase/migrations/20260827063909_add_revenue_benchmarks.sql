create table revenue_benchmarks (
  id uuid primary key default gen_random_uuid(),
  city_id uuid not null references cities(id),
  venue_name text not null,
  venue_type text,
  activation_type text not null default 'wedding',
  starting_price_usd numeric,
  price_note text,
  guest_capacity_min int,
  guest_capacity_max int,
  service_tier text,
  source_confidence text not null default 'medium',
  effective_date date,
  source_document_id uuid references documents(id),
  notes text,
  created_at timestamptz not null default now()
);

create index revenue_benchmarks_city_id_idx on revenue_benchmarks (city_id);

alter table revenue_benchmarks enable row level security;
create policy "Public read access" on revenue_benchmarks for select using (true);

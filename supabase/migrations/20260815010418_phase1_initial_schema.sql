create extension if not exists vector with schema extensions;

create table cities (
  id uuid primary key default gen_random_uuid(),
  name text not null unique,
  state text not null default 'CA',
  permit_data_freshness date,
  created_at timestamptz not null default now()
);

create table documents (
  id uuid primary key default gen_random_uuid(),
  city_id uuid not null references cities(id),
  title text not null,
  source_type text not null check (source_type in ('municipal_code','fee_schedule','permit_application','submittal_checklist','other')),
  code_chapter text,
  source_name text not null,
  source_file text,
  retrieved_date date not null,
  effective_date date,
  effective_date_confidence text,
  notes text,
  created_at timestamptz not null default now()
);

create table chunks (
  id uuid primary key default gen_random_uuid(),
  document_id uuid not null references documents(id) on delete cascade,
  city_id uuid not null references cities(id),
  chunk_index int not null,
  section_reference text,
  content text not null,
  embedding extensions.vector(384),
  fts tsvector generated always as (to_tsvector('english', content)) stored,
  created_at timestamptz not null default now()
);

create index chunks_embedding_idx on chunks using hnsw (embedding extensions.vector_cosine_ops);
create index chunks_fts_idx on chunks using gin (fts);
create index chunks_city_id_idx on chunks (city_id);
create index chunks_document_id_idx on chunks (document_id);

create table fee_schedules (
  id uuid primary key default gen_random_uuid(),
  city_id uuid not null references cities(id),
  permit_type text not null,
  fee_name text not null,
  amount_usd numeric,
  amount_usd_min numeric,
  amount_usd_max numeric,
  amount_type text,
  code_section text,
  applies_to_track text,
  effective_date date,
  effective_date_confidence text,
  source_document_id uuid references documents(id),
  notes text,
  created_at timestamptz not null default now()
);

create index fee_schedules_city_id_idx on fee_schedules (city_id);

alter table cities enable row level security;
alter table documents enable row level security;
alter table chunks enable row level security;
alter table fee_schedules enable row level security;

create policy "Public read access" on cities for select using (true);
create policy "Public read access" on documents for select using (true);
create policy "Public read access" on chunks for select using (true);
create policy "Public read access" on fee_schedules for select using (true);

insert into cities (name, permit_data_freshness) values ('Fullerton', null);

-- Phase 4: multi-city support.
-- 0. city_id NULL now has a real meaning ("applies to every city, not one
--    specific city") for regional/state-level sources, so both columns need
--    to allow it.
alter table documents alter column city_id drop not null;
alter table chunks alter column city_id drop not null;

-- 1. Retag regional/state-level sources (OCFA, ABC forms) from Fullerton's
--    city_id to NULL, so they surface for every city's questions instead of
--    only Fullerton's.
update chunks
set city_id = null
where document_id in (
  '0fd0ab49-64df-4a20-8b50-47b260f6aed2', -- OC Fire Authority: Special Event Permits
  '89843c36-a882-4a72-8f3c-1d654b1d3f75', -- ABC-218: Catering Authorization Application
  '2c25f34c-5a8a-4c61-8ba0-6500d8b8b655'  -- ABC-221: Daily License Application
);

update documents
set city_id = null
where id in (
  '0fd0ab49-64df-4a20-8b50-47b260f6aed2',
  '89843c36-a882-4a72-8f3c-1d654b1d3f75',
  '2c25f34c-5a8a-4c61-8ba0-6500d8b8b655'
);

-- 2. hybrid_search: treat city_id IS NULL rows as applying to every city,
--    not just when match_city_id itself is null.
create or replace function public.hybrid_search(
  query_text text,
  query_embedding vector,
  match_city_id uuid default null::uuid,
  match_count integer default 8,
  full_text_weight double precision default 1.0,
  semantic_weight double precision default 1.0,
  rrf_k integer default 50
)
returns table(id uuid, document_id uuid, city_id uuid, section_reference text, content text, similarity double precision, rank_score double precision)
language sql
stable
set search_path to 'public', 'extensions'
as $function$
with full_text as (
  select c.id, row_number() over (order by ts_rank_cd(c.fts, websearch_to_tsquery('english', query_text)) desc) as rank_ix
  from chunks c
  where c.fts @@ websearch_to_tsquery('english', query_text)
    and (match_city_id is null or c.city_id = match_city_id or c.city_id is null)
  limit least(match_count, 30) * 2
),
semantic as (
  select c.id, row_number() over (order by c.embedding <=> query_embedding) as rank_ix
  from chunks c
  where (match_city_id is null or c.city_id = match_city_id or c.city_id is null)
  order by c.embedding <=> query_embedding
  limit least(match_count, 30) * 2
)
select
  c.id, c.document_id, c.city_id, c.section_reference, c.content,
  (1 - (c.embedding <=> query_embedding))::float as similarity,
  (coalesce(1.0/(rrf_k + full_text.rank_ix), 0.0) * full_text_weight +
   coalesce(1.0/(rrf_k + semantic.rank_ix), 0.0) * semantic_weight)::float as rank_score
from chunks c
left join full_text on full_text.id = c.id
left join semantic on semantic.id = c.id
where full_text.id is not null or semantic.id is not null
order by rank_score desc
limit match_count;
$function$;

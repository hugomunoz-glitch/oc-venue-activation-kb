create or replace function hybrid_search(
  query_text text,
  query_embedding extensions.vector(384),
  match_city_id uuid default null,
  match_count int default 8,
  full_text_weight float default 1.0,
  semantic_weight float default 1.0,
  rrf_k int default 50
)
returns table (
  id uuid,
  document_id uuid,
  city_id uuid,
  section_reference text,
  content text,
  similarity float,
  rank_score float
)
language sql
stable
as $$
with full_text as (
  select c.id, row_number() over (order by ts_rank_cd(c.fts, websearch_to_tsquery('english', query_text)) desc) as rank_ix
  from chunks c
  where c.fts @@ websearch_to_tsquery('english', query_text)
    and (match_city_id is null or c.city_id = match_city_id)
  limit least(match_count, 30) * 2
),
semantic as (
  select c.id, row_number() over (order by c.embedding <=> query_embedding) as rank_ix
  from chunks c
  where (match_city_id is null or c.city_id = match_city_id)
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
$$;

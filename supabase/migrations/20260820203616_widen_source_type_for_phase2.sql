alter table documents drop constraint documents_source_type_check;
alter table documents add constraint documents_source_type_check
  check (source_type in ('municipal_code','fee_schedule','permit_application','submittal_checklist','api','website','other'));

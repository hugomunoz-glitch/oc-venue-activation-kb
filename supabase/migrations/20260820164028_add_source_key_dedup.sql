alter table documents add column source_key text;
update documents set source_key = source_file where source_key is null;
alter table documents add constraint documents_source_key_unique unique (source_key);

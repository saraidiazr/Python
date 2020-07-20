--adding audit columns table;
alter table validation_checks add column table_name text;
alter table validation_checks add column table_count integer;
alter table validation_checks add column agg_name text;
alter table validation_checks add column agg_count text;
alter table validation_checks add column completeness_check text;
alter table validation_checks add column correctness_check text;
alter table validation_checks add column run_time datetime;

-- updating validation table
	update validation_checks
	set run_time = datetime('now','localtime');
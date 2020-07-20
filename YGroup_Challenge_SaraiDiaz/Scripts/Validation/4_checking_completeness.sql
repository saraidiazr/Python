--validation checks
--completeness
	update validation_checks
	set completeness_check = case when source_count == ifnull(table_count,0) 
									and table_count == ifnull(agg_count,0) then 'complete load'
							 else 'partial load' end
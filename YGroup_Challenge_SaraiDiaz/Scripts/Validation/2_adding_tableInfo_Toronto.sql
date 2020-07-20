--Toronto
with table_validation as (
select 'Toronto' as city,
		substr(trip_start_time,1,4) || ' ' ||
		case when cast(substr(trip_start_time,6,2) as integer) < 4 then 'Q1'
			 when cast(substr(trip_start_time,6,2) as integer) between 3 and 6 then 'Q2'
			 when cast(substr(trip_start_time,6,2) as integer) between 6 and 9 then 'Q3'
			 when cast(substr(trip_start_time,6,2) as integer) > 9 then 'Q4'
		end as date,
		count(1) as trips
from toronto_bikes
group by substr(trip_start_time,1,4) || ' ' ||
		case when cast(substr(trip_start_time,6,2) as integer) < 4 then 'Q1'
			 when cast(substr(trip_start_time,6,2) as integer) between 3 and 6 then 'Q2'
			 when cast(substr(trip_start_time,6,2) as integer) between 6 and 9 then 'Q3'
			 when cast(substr(trip_start_time,6,2) as integer) > 9 then 'Q4'
		end
)
update validation_checks
set  table_name = 'toronto_bikes'
	,table_count = (select trips from table_validation where validation_checks.date = table_validation.date)
where exists (select trips from table_validation where validation_checks.date = table_validation.date);

update validation_checks
set  table_name = 'toronto_stations'
	,table_count = (select count(name) from toronto_stations where validation_checks.date = (select strftime('%Y',datetime('now'))))
where exists (select count(name) from toronto_stations where validation_checks.date = (select strftime('%Y',datetime('now'))));

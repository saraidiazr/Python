--Montreal
with table_validation as(
select 	'Montreal' as city,
		substr(start_date,1,7) as date,
		count(1) as trips
from montreal_bikes
group by substr(start_date,1,7)
)
update validation_checks
set  table_name = 'montreal_bikes'
	,table_count = (select trips from table_validation where validation_checks.date = table_validation.date)
where exists (select trips from table_validation where validation_checks.date = table_validation.date);

with table_validation as(
select 	'Montreal' as city,
		source as date,
		count(1) as trips
from montreal_stations
group by source
)
update validation_checks
set  table_name = 'montreal_stations'
	,table_count = (select trips from table_validation where validation_checks.date = table_validation.date)
where exists (select trips from table_validation where validation_checks.date = table_validation.date);



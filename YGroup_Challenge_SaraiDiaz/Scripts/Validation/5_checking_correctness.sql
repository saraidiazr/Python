--validation checks
--correctness							 
	with missing_stations as (
	select distinct city, date, code 
	from (	select distinct	'Montreal' as city,
					substr(start_date,1,7) as date,
					start_station_code as code
			from montreal_bikes bikes
			left join montreal_stations stations
				on bikes.start_station_code = stations.code
			where stations.code is null
			union all 
			select distinct	'Montreal' as city,
					substr(start_date,1,7) as date,
					end_station_code as code
			from montreal_bikes bikes
			left join montreal_stations stations
				on bikes.end_station_code = stations.code
			where stations.code is null) stations
	)
	update validation_checks
	set correctness_check = 'invalid station code : ' || (select code from missing_stations where date = validation_checks.date)
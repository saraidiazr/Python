-- creating agg tables to make easier data retrieval in the dashboard
create table agg_trips as
	select 	'Montreal' as city,
			case when is_member == 1 then 'Member' else 'Casual' end as user_type, 
			strftime('%Y',start_date) as year,
			strftime('%m',start_date) as month,
			day_of_week as day,
			start_time as hour,
			count(1) as trips
	from montreal_bikes
	group by case when is_member == 1 then 'Member' else 'Casual' end, 
			strftime('%Y',start_date),
			strftime('%m',start_date),
			day_of_week,
			start_time
	union all
	select 	'Toronto' as city,
			user_type,
			substr(trip_start_time,1,4) as year,
			substr(trip_start_time,6,2) as month,
			strftime('%w',trip_start_time) as day,
			substr(trip_start_time,instr(trip_start_time,' ')+1,2) as hour,
			count(1) as trips
	from toronto_bikes
	group by user_type,
			substr(trip_start_time,1,4),
			substr(trip_start_time,6,2),
			strftime('%w',trip_start_time),
			substr(trip_start_time,instr(trip_start_time,' ')+1,2);

	--formatting 		
	update agg_trips
	set day = case cast(day as integer)
				when 0 then 'Sunday'
				when 1 then 'Monday'
				when 2 then 'Tuesday'
				when 3 then 'Wednesday'
				when 4 then 'Thursday'
				when 5 then 'Friday'
				else 'Saturday' 
			end
	where city = 'Toronto';
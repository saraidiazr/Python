-- Distribución de los viajes por tipo de usuario.
	select	city,
			year,
			month,
			day,
			hour,
			user_type,
			sum(record_count) as trips
	from trips_agg
	group by city,
			year,
			month,
			day,
			hour,
			user_type;				
	
-- Estaciones más usadas.


-- Rutas más usadas.
	select 	city,
			start_station,
			end_station,
			record_count		
	from (select 'Montreal' as city,
				(select distinct name from montreal_stations where bikes.start_station_code = code) as start_station,
				(select distinct name from montreal_stations where bikes.end_station_code = code) as end_station,
				count(start_station_code) as record_count
		from montreal_bikes bikes
		group by start_station_code,
				 end_station_code
		order by record_count desc
		limit 5)
	union all
	select 	city,
			start_station,
			end_station,
			record_count	
	from (select 'Toronto' as city,
				from_station_name as start_station,
				to_station_name as end_station,
				count(from_station_name) as record_count
		from toronto_bikes 
		group by from_station_name,
				 to_station_name
		order by record_count desc
		limit 5);
		
-- estaciones cercanas a accidentes registrados 
select distinct name, latitude, longitude, 'Montreal' as city
	, case when name in (select distinct name
						 from montreal_stations s
						 join montreal_collisions c 
						 on abs(s.latitude-c.latitude) < 0.00009
						and abs(s.longitude-c.longitude) < 0.00009
						and s.source = (select max(cast source as integer) from montreal_stations)
	then 1 else 0 end as is_collision_nearby
from montreal_stations
where source = (select max(cast source as integer) from montreal_stations))
union all
select distinct name, lat, lon, 'Toronto' as city
	, case when name in (select distinct name
						 from toronto_stations s
						 join toronto_collisions c 
						 on abs(s.lat-c.latitude) < 0.0009
						and abs(s.lon-c.longitude) < 0.0009)
	then 1 else 0 end as is_collision_nearby
from toronto_stations
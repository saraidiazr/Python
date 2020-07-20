-- Montreal indexes
	drop index if exists idx_montreal_bikes;
	drop index if exists idx_montreal_collisions;
	drop index if exists idx_montreal_stations;

	create index idx_montreal_bikes on montreal_bikes (start_station_code,end_station_code);
	create index idx_montreal_collisions on montreal_collisions (date,hour);
	create index idx_montreal_stations on montreal_stations (code,source);
	
-- Toronto indexes
	drop index if exists idx_toronto_bikes;
	drop index if exists idx_toronto_collisions;
	drop index if exists idx_toronto_stations;

	create index idx_toronto_bikes on toronto_bikes (from_station_name,to_station_name);
	create index idx_toronto_collisions on toronto_collisions (year,hour);
	create index idx_toronto_stations on toronto_stations (station_id);







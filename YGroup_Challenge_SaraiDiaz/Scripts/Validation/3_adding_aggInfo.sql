	with agg_validation as(
	select 	city,
			year || '-' || month as date,
			sum(trips) as trips
	from agg_trips
	where city = 'Montreal'
	group by city,
			year || '-' || month
	union all
	select 	city,
			year || ' ' ||
			case when cast(month as integer) < 4 then 'Q1'
				 when cast(month as integer) between 3 and 6 then 'Q2'
				 when cast(month as integer) between 6 and 9 then 'Q3'
				 when cast(month as integer) > 9 then 'Q4'
			end as date,
			sum(trips) as trips
	from agg_trips
	where city = 'Toronto'
	group by city,
			year || ' ' ||
			case when cast(month as integer) < 4 then 'Q1'
				 when cast(month as integer) between 3 and 6 then 'Q2'
				 when cast(month as integer) between 6 and 9 then 'Q3'
				 when cast(month as integer) > 9 then 'Q4'
			end
	)
	update validation_checks
	set  agg_name = 'agg_trips'
		,agg_count = (select trips from agg_validation where validation_checks.date = agg_validation.date)
	where exists (select trips from agg_validation where validation_checks.date = agg_validation.date);

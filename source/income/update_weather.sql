# heating and cooling points
select @hp:=55, @cp:=80;

# transfer data from weather_copa_hourly
replace into weather_degree_hours
	select posttime, temperature, if(temperature<@hp,@hp-temperature,0), if(temperature>@cp,temperature-@cp,0)
	from weather_copa_hourly;

# transfer heating/cooling degree hours
replace into weather_degree_month
	SELECT year(readtime)*12+month(readtime)-1 as billing_month, 
	  ceil((unix_timestamp(max(readtime))-unix_timestamp(min(readtime)))/86400) as days,
	  sum(hdh) as hdh, 
	  sum(cdh) as cdh
	FROM weather_degree_hours
	group by billing_month;

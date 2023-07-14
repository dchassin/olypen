start transaction;

select @start:='2006-10-01';

update tou_prices set enddate=date_sub(@start,interval 1 day) where enddate is NULL;

select @offpeak:=41.19, @onpeak:=121.50, @critical:=350;

insert into tou_prices (startdate, enddate, hour, price, critical_price, price_unit_code, rec_create_date) values
	(@start, NULL, 0, @offpeak, @critical, 'd/MWh', now()),
	(@start, NULL, 1, @offpeak, @critical, 'd/MWh', now()),
	(@start, NULL, 2, @offpeak, @critical, 'd/MWh', now()),
	(@start, NULL, 3, @offpeak, @critical, 'd/MWh', now()),
	(@start, NULL, 4, @offpeak, @critical, 'd/MWh', now()),
	(@start, NULL, 5, @offpeak, @critical, 'd/MWh', now()),
	(@start, NULL, 6, @onpeak, @critical, 'd/MWh', now()),
	(@start, NULL, 7, @onpeak, @critical, 'd/MWh', now()),
	(@start, NULL, 8, @onpeak, @critical, 'd/MWh', now()),
	(@start, NULL, 9, @offpeak, @critical, 'd/MWh', now()),
	(@start, NULL, 10, @offpeak, @critical, 'd/MWh', now()),
	(@start, NULL, 11, @offpeak, @critical, 'd/MWh', now()),
	(@start, NULL, 12, @offpeak, @critical, 'd/MWh', now()),
	(@start, NULL, 13, @offpeak, @critical, 'd/MWh', now()),
	(@start, NULL, 14, @offpeak, @critical, 'd/MWh', now()),
	(@start, NULL, 15, @offpeak, @critical, 'd/MWh', now()),
	(@start, NULL, 16, @offpeak, @critical, 'd/MWh', now()),
	(@start, NULL, 17, @offpeak, @critical, 'd/MWh', now()),
	(@start, NULL, 18, @onpeak, @critical, 'd/MWh', now()),
	(@start, NULL, 19, @onpeak, @critical, 'd/MWh', now()),
	(@start, NULL, 20, @onpeak, @critical, 'd/MWh', now()),
	(@start, NULL, 21, @offpeak, @critical, 'd/MWh', now()),
	(@start, NULL, 22, @offpeak, @critical, 'd/MWh', now()),
	(@start, NULL, 23, @offpeak, @critical, 'd/MWh', now());

commit;

#!/usr/bin/mysql
# market clearing test 1
# DP Chassin, 08 Dec 2005
# 
# IMPORTANT: You must have customers listed in the customer table for this script to work!!!
#
# Scenario
# Sell		demand*2 kW @ $100/MWh
# Buy		None
# Demand	count(customer)*rand()*10 kW 
#
# Result	market should clear ~ 5*count(customer) kW at $100/MWh
#
use olypen;

# Purge data from last five minutes 
# NEVER DO THIS ON A PRODUCTION DATABASE!!!
#delete from sell where unix_timestamp(posttime) > unix_timestamp(now())-300;
#delete from buy where unix_timestamp(posttime) > unix_timestamp(now())-300;
#delete from meter where read_time > now()-300;

insert into cust_meter_trans (device_rec_id, cust_id, read_time, demand, demand_unit_code, meter_reading, meter_unit_code, rec_create_date)
	select 2, rec_id, now(), rand()*10, "kW", 0, "kWh", now() from customer;
insert into sell (seller_id, posttime, quantity, price) 
	select 1, now(), sum(demand)*2, 100 from cust_meter_trans where read_time > now()-300;

# market must be clear within the next 300 seconds

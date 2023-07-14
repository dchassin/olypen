# name: feeder.sql
# auth: DP Chassin
# date: 12/2005
# desc: Create the bulk power bid for the feeder
# note: Tables (fields) used:
#       * cust_meter_trans (demand, read_time)
#       * buy (quantity, posttime)
#	* midc (price, report_time)
#       * sell (seller_id, quantity, price, posttime)
#
# bugs: 1) this is a testing version, the real version should not deduct bids from the reported load
#
# hist: 2005-12-11: created (DP Chassin)
#       2005-12-15: added test to ensure no negative/zero quantity is bid
#	2005-12-19: removed automatic deduct of uncurtailed load; uncurtailable load must be bid in as such now
#       2006-04-28: fixed problem with placement of ELT in demand query
#

# set the feeder capacity
SELECT @capacity:=capacity from feeder_status where posttime < now() order by posttime desc limit 1;

# get the total customer demand as reported by homes
SELECT @ld:=ifnull(SUM(demand)/elt(field(demand_unit_code,"W","kW","MW"),1000,1,0.001),0) AS Quantity
	FROM cust_meter_trans
	WHERE read_time > DATE_SUB(NOW(),INTERVAL 5 MINUTE) 
# DPC: added this on 3/22 to block error flag from HGW
	and demand<65535;

# get the total responsive demand as bid by homes
SELECT @bid:=ifnull(SUM(quantity),0) AS Quantity
	FROM buy
	WHERE posttime > DATE_SUB(NOW(),INTERVAL 5 MINUTE);

# get the current realtime MIDC price
SELECT @pr:=report_value AS Price
	FROM midc
	WHERE report_time > DATE_SUB(NOW(), INTERVAL 1 HOUR);

# get the current firm power price from MIDC
SELECT @fp:=report_value as Price
	FROM midc
	WHERE report_type = "FP"
	ORDER BY report_time DESC
	LIMIT 1;

# get the current firm off-peak power price from MIDC
SELECT @fop:=report_value as Price
	FROM midc
	WHERE report_type = "FOP"
	ORDER BY report_time DESC
	LIMIT 1;

# build the current feeder bid
# NOTE: the unresponsive demand is the customer demand minus the bids
#       this needs to be changed to an explicit unresponsive bid submitted by the homes that bid responsive demand
#INSERT INTO sell (seller_id, quantity, price) VALUES (1, IF(@ld>@bid,@ld-@bid/2,@bid), IFNULL(@pr,IF(DAYOFWEEK(NOW())=1 OR HOUR(NOW())<=6 OR HOUR(NOW())>=23,@fop,@fp)));

# update 12/19/2005: the metered load is considered unresponsive, later the query for unresponsive load will need to changed
#INSERT INTO buy (buyer_id, quantity, price, posttime, mkt_id) VALUES (0, @ld, 9999, now(), ceiling(unix_timestamp()/300));
#INSERT INTO sell (seller_id, quantity, price, posttime, mkt_id) VALUES (1, @capacity, IFNULL(@pr,IF(DAYOFWEEK(NOW())=1 OR HOUR(NOW())<=6 OR HOUR(NOW())>=23,@fop,@fp)), now(), ceiling(unix_timestamp()/300));
REPLACE INTO buy (buyer_id, quantity, price, posttime, mkt_id) VALUES (0, @ld, 9999, now(), 0);
REPLACE INTO sell (seller_id, quantity, price, posttime, mkt_id) VALUES (1, @capacity, IFNULL(@pr,IF(DAYOFWEEK(NOW())=1 OR HOUR(NOW())<=6 OR HOUR(NOW())>=23,@fop,@fp)), now(), 0);


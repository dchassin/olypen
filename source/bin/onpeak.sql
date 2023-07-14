# name: onpeak.sql
# auth: DP Chassin
# date: 12/2005
# desc: Calculate on-peak midc price
# note: Tables (fields) used:
#	* midc (price, report_time)
#
# bugs: (na)
#
# hist: 2005-12-08: created (DP Chassin)
#
SET @type = "FP";
SELECT @rd:=report_time AS DateTime, @fp1:=report_value AS Price
	FROM midc 
	WHERE report_type=@type AND report_time > DATE_SUB(NOW(), INTERVAL 48 HOUR);
SELECT report_time AS DateTime, @fp0:=report_value AS Price
	FROM midc
	WHERE report_type=@type AND report_time = DATE_SUB(@rd, INTERVAL 1 DAY);
REPLACE INTO midc (report_time, report_type, report_value)
	SELECT DATE_ADD(CURDATE(), INTERVAL HOUR(report_time) HOUR) AS DateTime, "OLYM", report_value-@fp0+@fp1 AS Price
		FROM midc
		WHERE report_type="HRLY" AND HOUR(report_time) = HOUR(DATE_ADD(NOW(), INTERVAL 1 HOUR))
		ORDER BY report_time DESC
		LIMIT 1;

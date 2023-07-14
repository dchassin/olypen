select @fp:=price/1000 from fixed_price where enddate is null;

replace into cust_usage_projection (pnnl_acct_id, billing_month, kwh_expected, deposit)
select cust_usage_model.pnnl_acct_id,
	year(now())*12+cust_billing_history.billing_month%12 as month,
	round(kwh_base+kwh_per_hdh*hdh) as kwh_expected,
	round(((kwh_base+kwh_per_hdh*hdh)*@fp)+(150/12),2) as deposit
from cust_usage_model join cust_billing_history using (pnnl_acct_id)
	join weather_degree_month
		on weather_degree_month.billing_month%12 = cust_billing_history.billing_month%12
group by cust_billing_history.pnnl_acct_id, cust_billing_history.billing_month%12;

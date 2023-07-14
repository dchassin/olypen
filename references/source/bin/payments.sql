# payments.sql
#
# calculate monthly supplier payments
#

SELECT date_format(clear.posttime,"%Y-%m") as 'Period', sell.seller_id as 'Supplier', round(sum(clear.price*sell.quantity / 12000),2) as 'Payment'
FROM sell join clear on sell.posttime between date_sub(clear.posttime,interval 5 minute) and clear.posttime
where sell.price <= clear.price
group by seller_id, year(clear.posttime)+month(clear.posttime)/100;


"""This example plots histograms of payments to participants"""
import os, sys
import olypen
import matplotlib.pyplot as pl
import seaborn as sb

olypen.pandas.options.display.width = None
olypen.pandas.options.display.max_columns = None

db = olypen.Olypen()

payments = db.table("billing_report",index_col=["contract_type_code","customer_id"])

result = olypen.pandas.DataFrame(payments.adjusted.groupby(payments.index.names).mean())
fig = pl.figure(figsize=(10,7))
fig.suptitle('Monthly Bill "Surprise" Distribution')
adj = None
table = {}
for tariff in ['FIXED','TOU','RTP']:#result.index.get_level_values(0).unique():
	data = -result.loc[tariff] # negative "surprise" is savings
	data = data
	if adj == None: 
		adj = -data.mean().tolist()[0]
		mean = 0.0
		print(f"Adjustment is {adj-12.50:.2f}")
	else:
		mean = data.mean().tolist()[0] + adj
	std = data.std().tolist()[0]
	table[tariff] = dict(mean=round(mean,2),stdev=round(std,2))
	sb.distplot(data+adj,label=tariff)
fig.legend()
fig.savefig(sys.argv[0].replace(".py",".png"))

print(olypen.pandas.DataFrame(table).transpose())

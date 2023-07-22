"""This example plots histograms of payments to participants"""
import olypen
import matplotlib.pyplot as pl
import seaborn as sb

olypen.pandas.options.display.width = None
olypen.pandas.options.display.max_columns = None

db = olypen.Olypen()

payments = db.table("billing_report",index_col=["contract_type_code","customer_id"])

result = olypen.pandas.DataFrame(payments.unadjusted.groupby(payments.index.names).mean())
fig = pl.figure(figsize=(24,12))
fig.suptitle('Monthly Bill "Surprise" Distribution')
for tariff in ['FIXED','TOU','RTP']:#result.index.get_level_values(0).unique():
	data = result.loc[tariff]
	mean = data.mean().tolist()[0]
	stdv = data.std().tolist()[0]
	# pl.hist(data,label=f"{tariff} ({mean:.2f}+/-{stdv:.2f})")
	sb.distplot(data,label=tariff)
fig.legend()
fig.savefig("plot_payments.png")

"""Calculate individual and aggregate demand elasticity"""
import sys, pandas, numpy, matplotlib.pyplot as pl
from datetime import datetime

tzoffset = -8

pandas.options.display.width = None
pandas.options.display.max_columns = None

auctions = pandas.read_csv("join_bids.csv.gz",parse_dates=['posttime_clear'])
start = auctions['mkt_id'].min()
stop = auctions['mkt_id'].max()+1

auctions = auctions[auctions.price_clear*auctions.quantity_clear>0] # select positive clearing prices and quantities only
buys = auctions[auctions.quantity_bid>0].drop('supplier_id',axis=1) # select positive buy bid quantities
buys = buys[buys.price_bid>buys.price_clear].copy() # select buys that cleared
buys['dlogq'] = -buys['quantity_bid'] / buys['quantity_clear'] # calculate quantity response
buys['dlogp'] = (buys['price_bid']-buys['price_clear']) / buys['price_clear'] # calculate price response
buys['eta'] =  buys['dlogq'] / buys['dlogp'] # calculate elasticity of demand
buys.set_index(['mkt_id','price_bid'],inplace=True)
buys.sort_index(ascending=[True,False],inplace=True)

def heatmap(map_data,**kwargs):
	fig = pl.figure(**kwargs)
	data = pandas.DataFrame(map_data)
	# diff = map_data.max() - map_data.min()
	# data[map_data.name] = (map_data - map_data.min())/diff*256
	index = data.index.get_level_values(0)+tzoffset*12
	data['interval'] = index%288
	start = (index//288).min()
	data['period'] = index//288-start
	data.set_index(['interval','period'],inplace=True)
	N,M = [x+1 for x in data.index.max()]
	array = numpy.full((N,M+1),float('nan'))
	for index,value in data.to_dict()[map_data.name].items():
		array[index] = value
	fig = pl.imshow(array)
	return fig

heatmap(buys.eta<-1.0)
pl.title('Elastic demand (yellow) vs inelastic demand (blue)')
pl.xlabel('Market day')
pl.ylabel('Market of day (5 minutes)')
pl.savefig('plot_heatmap_eta.png')

heatmap(buys.quantity_clear)
pl.colorbar()
pl.xlabel('Market day')
pl.ylabel('Market of day (5 minutes)')
pl.title('Clearing quantity (kW)')
pl.savefig('plot_heatmap_quantity_clear.png')

heatmap(buys.price_clear)
pl.colorbar()
pl.xlabel('Market day')
pl.ylabel('Market of day (5 minutes)')
pl.title('Clearing price ($/MW)')
pl.savefig('plot_heatmap_price_clear.png')


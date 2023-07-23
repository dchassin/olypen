"""Calculate individual and aggregate demand elasticity"""
import sys, pandas, numpy, matplotlib.pyplot as pl
from datetime import datetime

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

# elasticity duration curve
pl.figure(figsize=(10,7))
pl.plot((-buys.sort_values('eta')['eta']).tolist(),label='Bid elasticities')
pl.plot([0,len(buys)],[1,1],'-k',label='Unitary elasticity')
pl.yscale('log')
pl.grid()
pl.legend()
pl.xlabel('Bids above elasticity')
pl.ylabel('Demand elasticity magnitude')
pl.savefig(sys.argv[0].replace('.py','_duration.png'))

# elasticity timeseries
pl.figure(figsize=(10,7))
buys['log_eta'] = numpy.log(-buys['eta'])
eta = pandas.DataFrame(buys['log_eta'].groupby('mkt_id').max())
eta.index = [datetime.fromtimestamp(x*300) for x in eta.index]
pl.plot(numpy.exp(eta.log_eta),'.',markersize=1,label='Inframarginal demand elasticity')
pl.plot([eta.index.min(),eta.index.max()],[1,1],'-k',label='Unitary elasticity')
pl.ylabel('Demand elasticity magnitude')
pl.xlabel('Date')
pl.grid()
pl.legend()
pl.yscale('log')
pl.savefig(sys.argv[0].replace('.py','_eta.png'))


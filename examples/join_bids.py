"""This example illustrates how to join the buy, sell, and clear tables to from 
a complete bid table
"""
import olypen

data = olypen.Olypen()

print("Loading clear...",flush=True)
clear = data.table('clear',index_col='mkt_id')
print("Loading buy...",flush=True)
buy = data.table('buy',index_col='mkt_id').join(clear,lsuffix='_bid',rsuffix='_clear').reset_index().set_index(['mkt_id','price_bid']).sort_index()
print("Loading sell...",flush=True)
sell = data.table('sell',index_col='mkt_id').join(clear,lsuffix='_bid',rsuffix='_clear').reset_index().set_index(['mkt_id','price_bid'])
sell.quantity_bid = -sell.quantity_bid
sell.sort_index(inplace=True)

print("Saving bids...",flush=True)
olypen.pandas.concat([buy,sell]).reset_index().set_index(['mkt_id','price_bid']).sort_index().to_csv("join_bids.csv",header=True,index=True,compression='gzip')

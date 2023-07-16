# importing matplot lib
import os, sys
import olypen
import matplotlib.pyplot as pl
import numpy as np
import pandas as pd
import datetime as dt
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage

pd.options.display.width = None
pd.options.display.max_columns = None

db = olypen.Olypen()

# get the metered loads
loads = pd.read_csv('metered_load.csv.gz',index_col='mkt_id')

# get the bids
bids = pd.read_csv("join_bids.csv.gz",index_col=['mkt_id'])
index = bids.index.get_level_values(0).unique()

# generate frames
fig, ax = pl.subplots()
fps = 12*6 # 6 hours/second at 12 frames/hour
start_frame = 60000 # late october
duration = 1000 # number of frames
def make_frame(t):
	try:
		mkt_id = index[int(t*fps+start_frame)]
		data = bids.loc[mkt_id]
		
		sells = (data.quantity_bid<0).tolist()
		sell = data[sells if type(sells) is list else [sells]].sort_values('price_bid',ascending=True)
		sell_quantities = (-sell.quantity_bid).cumsum().to_list()
		sell_prices = sell.price_bid.to_list()
		sell_quantities.insert(0,0)
		sell_quantities.append(9999)
		sell_prices.append(9999)

		buys = (data.quantity_bid>0).tolist()
		buy = data[buys if type(buys) is list else [buys]].sort_values('price_bid',ascending=False)
		demand = loads.loc[mkt_id]['demand']
		buy_quantities = (buy.quantity_bid.cumsum() + demand).to_list()
		buy_quantities.insert(0,demand)
		buy_prices = buy.price_bid.to_list()
		buy_prices.insert(0,9999)
		buy_quantities.insert(0,0)

		ax.clear()
		ax.stairs(buy_prices,buy_quantities)		
		ax.stairs(sell_prices,sell_quantities)
		ax.set_title(data.iloc[0].posttime_clear)
		ax.plot(data.iloc[0].quantity_clear,data.iloc[0].price_clear,'*')
		ax.set_xlabel('Quantity (kW)')
		ax.set_ylabel('Price ($/MWh)')
		ax.set_xlim([0,1750])
		ax.set_ylim([0,1500])
	except:
		raise
		pass
	return mplfig_to_npimage(fig)

# creating animation
animation = VideoClip(make_frame, duration = duration/fps)

# displaying animation with auto play and looping
animation.write_videofile("animate_market.mp4", fps=fps)

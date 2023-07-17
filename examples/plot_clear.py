"""This example illustrates plotting the clearing history, scatter, and
histogram for price and quantity.
"""
from olypen import Olypen
import matplotlib.pyplot as pl
import matplotlib.gridspec as gs
import numpy as np

data = Olypen()

data.clear.reset_index(inplace=True)
data.clear.set_index('posttime',inplace=True)

fig = pl.figure(figsize=(24,12))
fig.suptitle('Clear')
gs = gs.GridSpec(2,4)

ax = fig.add_subplot(gs[0,0:2])
ax.plot(data.clear.quantity,data.clear.price,'.')
ax.grid()
ax.set_ylabel('Quantity (kW)')
ax.set_xlabel('Price ($/MWh)')
ax.set_ylim([0,500])

ax = fig.add_subplot(gs[0,2:4])
ax.plot(data.clear.price)
ax.set_ylim([0,500])
ax.set_ylabel('Quantity (kW)')
ax.grid()

ax = fig.add_subplot(gs[1,0:2])
ax.plot(data.clear.quantity)
ax.set_xlabel('Price ($/MWh)')
ax.grid()

ax = fig.add_subplot(gs[1,2])
positive = (data.clear.price>0)
hist, bins = np.histogram(data.clear.price[positive])
logbins = np.logspace(np.log10(bins[0]),np.log10(bins[-1]),len(bins))
ax.hist(data.clear.price, bins=logbins, density=True)
ax.set_xscale('log')
ax.set_xlabel('Price ($/MWh)')
ax.set_ylabel('Probability density')
ax.grid()

ax = fig.add_subplot(gs[1,3])
ax.hist(data.clear.quantity,density=True)
ax.set_xlabel('Quantity (kW)')
ax.grid()

fig.savefig(__file__.replace(".py",".png"))

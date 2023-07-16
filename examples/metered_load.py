import olypen
import pandas as pd
import numpy as np

db = olypen.Olypen()

meters = db.table('cust_meter_trans',index_col=None)
meters['mkt_id'] = [int(x) for x in meters['read_time'].values.astype(np.int64)/300e9]
meters.set_index('mkt_id',inplace=True)
loads = pd.DataFrame(meters['demand'].groupby('mkt_id').sum()/1000).dropna()
loads.to_csv('metered_load.csv.gz',compression='gzip',header=True,index=True)

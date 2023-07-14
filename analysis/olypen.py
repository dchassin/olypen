"""Olympic Peninsula Demonstration Project data accessor

Example
-------

>>> import olypen
>>> d = olypen.Olypen()
>>> d.directory
['billing', 'billing_report', 'billing_trans', 'buy', 'clear',
 'contract_type', 'critical_prices', 'cust_billed_meter_usage',
 'cust_billing_history', 'cust_contract_history', 'cust_device',
 'cust_dryer_config', 'cust_dryer_trans', 'cust_meter_trans',
 'cust_tstat_config', 'cust_tstat_trans', 'cust_usage_projection',
 'cust_wh_config', 'cust_wh_trans', 'customer', 'dashboard_data',
 'dev_type_comfort_level', 'device_type', 'experiment',
 'experiment_participant', 'fixed_price', 'home_mode_type',
 'invensys_meter', 'invensys_weather', 'midc', 'noaa_weather_station',
 'prices', 'sell', 'supplier', 'supplier_feeder_limit',
 'supplier_feeder_status', 'supplier_type', 'tou_prices', 'unit_type',
 'weather', 'weather_copa_hourly', 'weather_degree_hours',
 'weather_degree_month', 'weather_sites', 'weathernoaa']
>>> d['clear']
                    posttime  quantity  price  avg24  std24  avg168  std168
mkt_id                                                                     
3812928  2006-04-01 00:00:00   140.183  33.77  43.07  21.02   43.73   14.50
3812929  2006-04-01 00:05:00   143.299  41.09  43.04  21.03   43.72   14.50
3812930  2006-04-01 00:10:00   151.827  41.09  43.03  21.03   43.72   14.50
3812931  2006-04-01 00:15:00   151.333  41.09  43.03  21.03   43.72   14.50
3812932  2006-04-01 00:20:00   149.231  41.09  43.02  21.03   43.72   14.50
...                      ...       ...    ...    ...    ...     ...     ...
3918032  2007-03-31 23:40:00    81.562   4.19  10.54   8.78   19.58   25.11
3918033  2007-03-31 23:45:00    75.376   4.19  10.49   8.78   19.58   25.11
3918034  2007-03-31 23:50:00   108.532   4.19  10.43   8.77   19.58   25.11
3918035  2007-03-31 23:55:00    97.156   4.19  10.38   8.76   19.58   25.11
3918036  2007-04-01 00:00:00    87.457   4.19  10.33   8.75   19.58   25.11

[103843 rows x 7 columns]
"""

import sys, os
import pandas as pd
import datetime as dt
import requests

DATASRC = "https://olypen.s3.us-west-2.amazonaws.com/data"
DATADIR = "../data"

class OlypenException(Exception):
	pass

DATETIMEFORMAT = "%Y-%m-%d %H:%M:%S"
DATEFORMAT = "%Y-%m-%d"
TZNAME = "America/Los Angeles"
TZOFFSET = -8
TZSPEC = dt.timezone(dt.timedelta(hours=TZOFFSET),TZNAME)

def datetime(str):
	try:
		return dt.datetime.strptime(str,DATETIMEFORMAT)
	except:
		return float('NaN')

def date(str):
	try:
		return dt.datetime.strptime(str,DATEFORMAT).date()
	except:
		return float('NaN')

def boolstr(str):
	try:
		return bool(int(str))
	except:
		return float('NaN')

class Olypen:

	VERBOSE = False
	CONVERTERS = {
		# only needed it any fields are not int, float, or str
		"billing_trans" : {
			"billing_trans_id" : int,
			"customer_id" : int,
			"trans_type_code" : str,
			"stmt_start_date" : date,
			"stmt_end_date" : date,
			"billing_trans_date" : date,
			"trans_amount" : float,
			"rec_create_date" : datetime,
			"rec_last_update_date" : datetime,
		},
		"cust_billed_meter_usage" : {
			"customer_id" : int,
			"start_time" : datetime,
			"end_time" : datetime,
			"meter_usage" : float,
			"unit_type_code" : str,
			"rec_create_date" : datetime,
			"rec_last_update_date" : datetime,
		},
		"cust_contract_history" : {
			"cust_contract_history_id" : int,
			"customer_id" : int,
			"contract_type_code" : str,
			"start_date" : date,
			"end_date" : date,
			"rec_create_date" : datetime,
			"rec_last_update_date" : datetime,
		},
		"cust_device" : {
			"cust_device_id" : int, 
			"customer_id" : int, 
			"device_type_id" : int, 
			"instance_id" : int,
			"rec_last_update_date" : datetime, 
			"rec_create_date" : datetime,
		},
		"cust_dryer_config" : {
			"cust_dryer_config_id" : int,
			"cust_device_id" : int,
			"kfactor" : float,
			"rec_create_date" : datetime,
			"rec_last_update_date" : datetime,
		},
		"cust_dryer_trans" : {
			"cust_dryer_trans_id" : int,
			"cust_dryer_config_id" : int,
			"meter_unit_type_code" : str,
			"demand_unit_type_code" : str,
			"read_time" : datetime,
			"demand" : float,
			"meter_reading" : float,
			"is_overridden" : boolstr,
			"is_on" : boolstr,
			"rec_create_date" : datetime,
			"rec_last_update_date" : datetime,
		},
		"cust_meter_trans" : {
			"cust_meter_trans_id" : int,
			"cust_meter_config_id" : int,
			"meter_unit_type_code" : str,
			"demand_unit_type_code" : str,
			"read_time" : datetime,
			"demand" : float,
			"meter_reading" : float,
			"rec_create_date" : datetime,
			"rec_last_update_date" : datetime,
		},
		"cust_meter_trans" : {
			"cust_meter_trans_id" : int,
			"cust_device_id" : int,
			"meter_unit_type_code" : str,
			"demand_unit_type_code" : str,
			"read_time" : datetime,
			"demand" : float,
			"meter_reading" : float,
			"rec_create_date" : datetime,
			"rec_last_update_date" : datetime,
		},
		"cust_tstat_config" : {
			"cust_tstat_config_id": int,
			"cust_device_id": int,
			"home_mode_type_id": int,
			"cooling_temp_set": float,
			"cooling_temp_max": float,
			"cooling_temp_min": float,
			"heating_temp_set": float,
			"heating_temp_max": float,
			"heating_temp_min": float,
			"kts": float,
			"rec_create_date" : datetime,
			"rec_last_update_date" : datetime,
		},
		"cust_tstat_trans" : {
			"cust_tstat_trans_id" : int,
			"cust_tstat_config_id" : int,
			"meter_unit_type_code" : str,
			"demand_unit_type_code" : str,
			"heat_cool_mode_id" : int,
			"read_time" : datetime,
			"temp_current" : float,
			"demand" : float,
			"meter_reading" : float,	
			"rec_create_date" : datetime,
			"rec_last_update_date" : datetime,
		},
	}
	INDEXCOLS = {
		# only needed if indexing is desired by default
		"billing" : ["customer_id","period","mkt_id"],
		"billing_report" : ["customer_id","year","month"],
		"billing_trans" : ["customer_id","billing_trans_date"],
		"buy" : ["mkt_id","price"],
		"clear" : ["mkt_id"],
		"contract_type" : ["contract_type_code"],
		"critical_prices" : ["cpp_date","cpp_hour"],
		"cust_billed_meter_usage" : ["customer_id"],
		"cust_billing_history" : ["billing_month","customer_id"],
		"cust_contract_history" : ["customer_id","start_date"],
		"cust_device" : ["cust_device_id"],
		"cust_dryer_config" : ["cust_dryer_config_id"],
		"cust_dryer_trans" : ["cust_dryer_trans_id"],
		"cust_meter_trans" : ["cust_meter_trans_id"],
		"cust_tstat_config" : ["cust_tstat_config_id"],
		"cust_tstat_trans" : ["cust_tstat_trans_id"],
		"cust_usage_projection" : ["customer_id"],
		"cust_wh_config" : ["cust_wh_config_id"],
		"cust_wh_trans" : ["cust_wh_trans_id"],
		"customer" : ["customer_id"],
		"dashboard_data" : None,
		"dev_type_comfort_level" : None,
		"device_type" : None,
		"experiment" : None,
		"experiment_participant" : None,
		"fixed_price" : None,
		"home_mode_type" : None,
		"invensys_meter" : None,
		"invensys_weather" : None,
		"midc" : None,
		"noaa_weather_station" : None,
		"prices" : None,
		"sell" : None,
		"supplier" : None,
		"supplier_feeder_limit" : None,
		"supplier_feeder_status" : None,
		"supplier_type" : None,
		"tou_prices" : None,
		"unit_type" : None,
		"weather" : None,
		"weather_copa_hourly" : None,
		"weather_degree_hours" : None,
		"weather_degree_month" : None,
		"weather_sites" : None,
		"weathernoaa" : None,	
		}
	
	def __init__(self,datadir=None):
		"""Olypen class constructor
		Parameters:
		  datadir (str) - path to data directory
		"""
		self.datadir = DATADIR if datadir is None else datadir
		if not os.path.exists(self.datadir):
			os.makedirs(self.datadir,exist_ok=True)
		self.tables = {}
		self.directory = self._directory()

	def __getitem__(self,name):
		"""Get a data table"""
		if not name in self.tables:
			return self.table(name)
		else:
			return self.tables[name]

	def _verbose(self,msg):
		if self.VERBOSE:
			print(msg,file=sys.stderr,flush=True)

	def _directory(self):
		"""Get a list of available tables
		Returns:
		  list - List of tables
		"""
		files = list(self.INDEXCOLS.keys())
		names = [os.path.splitext(os.path.splitext(file)[0])[0]
			for file in files]
		self.files = dict(zip(names,files))
		return names

	def table(self,name,**kwargs):
		"""Load a data table
		Parameters:
			name (str) - Name of table 
			kwargs - pandas.read_csv() options
		Returns:
			dataframe - Data
		"""
		file = os.path.join(self.datadir,name+".csv.gz")
		if not os.path.exists(file):
			self._verbose(f"Downloading {name}")
			r = requests.get(os.path.join(DATASRC,name+".csv.gz"),
				stream=True)
			if r.status_code != 200:
				msg = f"{file} not found (HTTP code {r.status_code})"
				raise OlypenException(msg)
			with open(file, 'wb') as f:
			    for chunk in r.iter_content(chunk_size=1024*1024): 
			        if chunk: # filter out keep-alive new chunks
			            f.write(chunk)
		else:
			self._verbose(f"Loading {name}")

		default_kwds = {
			"low_memory" : False,
			"converters" : self.CONVERTERS[name] if name in self.CONVERTERS else None,
			"index_col" : self.INDEXCOLS[name] if name in self.INDEXCOLS else None,
			"na_values" : ['\\N'],
		}
		for item,value in default_kwds.items():
			if not item in kwargs:
				kwargs[item] = value
		data = pd.read_csv(file,**kwargs)
		self._verbose(f"{len(data)} records loaded")
		self.tables[name] = data
		return data

if __name__ == "__main__":
	olypen = Olypen()
	for name in olypen.directory:
		print(name,end='... ',file=sys.stderr,flush=True)
		tic = dt.datetime.now()
		data = olypen[name]
		toc = dt.datetime.now()
		t = (toc-tic).total_seconds()
		n = len(data)
		print(f"{n} records loaded in {t:.1f} seconds ({(n/t):.0f} records/second)",flush=True)

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
>>> d.clear
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
import pandas
import datetime
import requests

DATASRC = "https://olypen.s3.us-west-2.amazonaws.com/data"
DATADIR = ".olypen_data"

class OlypenException(Exception):
	pass

DATETIMEFORMAT = "%Y-%m-%d %H:%M:%S"
DATEFORMAT = "%Y-%m-%d"
TZNAME = "America/Los Angeles"
TZOFFSET = -8
TZSPEC = datetime.timezone(datetime.timedelta(hours=TZOFFSET),TZNAME)
NAN = float('NaN')

def _datetime_na(str):
	try:
		return datetime.datetime.strptime(_str_na,DATETIMEFORMAT)
	except:
		return NAN

def _date_na(str):
	try:
		return datetime.datetime.strptime(_str_na,DATEFORMAT).date()
	except:
		return NAN

def _bool_na(str):
	try:
		return bool(int(str))
	except:
		return NAN

def _float_na(str):
	try:
		return float(str)
	except:
		return NAN

def _int_na(str):
	try:
		return int(str)
	except:
		return NAN

def _str_na(str):
	return str if str != "\\N" else float('NaN')

class Olypen:

	VERBOSE = False
	CONVERTERS = {
		# only needed it any fields are not _int_na, _float_na, or str
		"billing_trans" : {
			"billing_trans_id" : _int_na,
			"customer_id" : _int_na,
			"trans_type_code" : _str_na,
			"stmt_start_date" : _date_na,
			"stmt_end_date" : _date_na,
			"billing_trans_date" : _date_na,
			"trans_amount" : _float_na,
		},
		"cust_billed_meter_usage" : {
			"customer_id" : _int_na,
			"start_time" : _datetime_na,
			"end_time" : _datetime_na,
			"meter_usage" : _float_na,
			"unit_type_code" : _str_na,
		},
		"cust_contract_history" : {
			"cust_contract_history_id" : _int_na,
			"customer_id" : _int_na,
			"contract_type_code" : _str_na,
			"start_date" : _date_na,
			"end_date" : _date_na,
		},
		"cust_device" : {
			"cust_device_id" : _int_na, 
			"customer_id" : _int_na, 
			"device_type_id" : _int_na, 
			"instance_id" : _int_na,
		},
		"cust_dryer_config" : {
			"cust_dryer_config_id" : _int_na,
			"cust_device_id" : _int_na,
			"kfactor" : _float_na,
		},
		"cust_dryer_trans" : {
			"cust_dryer_trans_id" : _int_na,
			"cust_dryer_config_id" : _int_na,
			"meter_unit_type_code" : _str_na,
			"demand_unit_type_code" : _str_na,
			"read_time" : _datetime_na,
			"demand" : _float_na,
			"meter_reading" : _float_na,
			"is_overridden" : _bool_na,
			"is_on" : _bool_na,
		},
		"cust_meter_trans" : {
			"cust_meter_trans_id" : _int_na,
			"cust_meter_config_id" : _int_na,
			"meter_unit_type_code" : _str_na,
			"demand_unit_type_code" : _str_na,
			"read_time" : _datetime_na,
			"demand" : _float_na,
			"meter_reading" : _float_na,
		},
		"cust_meter_trans" : {
			"cust_meter_trans_id" : _int_na,
			"cust_device_id" : _int_na,
			"meter_unit_type_code" : _str_na,
			"demand_unit_type_code" : _str_na,
			"read_time" : _datetime_na,
			"demand" : _float_na,
			"meter_reading" : _float_na,
		},
		"cust_tstat_config" : {
			"cust_tstat_config_id": _int_na,
			"cust_device_id": _int_na,
			"home_mode_type_id": _int_na,
			"cooling_temp_set": _float_na,
			"cooling_temp_max": _float_na,
			"cooling_temp_min": _float_na,
			"heating_temp_set": _float_na,
			"heating_temp_max": _float_na,
			"heating_temp_min": _float_na,
			"kts": _float_na,
		},
		"cust_tstat_trans" : {
			"cust_tstat_trans_id" : _int_na,
			"cust_tstat_config_id" : _int_na,
			"meter_unit_type_code" : _str_na,
			"demand_unit_type_code" : _str_na,
			"heat_cool_mode_id" : _int_na,
			"read_time" : _datetime_na,
			"temp_current" : _float_na,
			"demand" : _float_na,
			"meter_reading" : _float_na,	
		},
		"dashboard_data" : {
			"readtime" : _datetime_na,
			"loadqty" : _float_na,
			"temperature" : _float_na,
		},
		"dev_type_comfort_level" : {
			"dev_type_comfort_level_id" : _int_na,
			"device_type_id" : _int_na,
			"comfort_level_desc" : _str_na,
			"comfort_value" : _float_na,
		},
		"device_type" : {
			"device_type_id" : _int_na,
			"device_type_code" : _str_na,
			"device_type_desc" : _str_na,
		},
		"experiment" : {
		    "experiment_code" : _str_na,
		    "experiment_desc" : _str_na,
		    "start_date" : _datetime_na,
		},
		"experiment_participant" : {
		    "experiment_participant_id" : _int_na,
		    "customer_id" : _int_na,
		    "experiment_code" : _str_na,
		    "signup_date" : _date_na,
		    "participation_start_date" : _date_na,
		},
		"fixed_price" : {
		    "fixed_price_id" : _int_na,
		    "startdate" : _date_na,
		    "enddate" : _date_na,
		    "price" : _float_na,
		    "unit_type_code" : _str_na,
		},
		"home_mode_type" : {
		    "home_mode_type_id" : _int_na,
		    "home_mode_type_code" : _str_na,
		    "home_mode_type_desc" : _str_na,
		},
		"invensys_meter" : {
		    "customer_id" : _int_na,
		    "read_time" : _datetime_na,
		    "meter_id" : _int_na,
		    "meter_reading" : _float_na,
		},
		"invensys_weather" : {
		    "invensys_acct_id" : _int_na,
		    "zipcode" : _int_na,
		    "read_time" : _datetime_na,
		    "temperature" : _float_na,
		},
		"midc" : {
		    "report_time" : _datetime_na,
		    "report_type" : _str_na,
		    "report_value" : _float_na,
		},
		"noaa_weather_station" : {
		    "noaacode" : _str_na,
		    "state" : _str_na,
		    "location" : _str_na,
		},
		"prices" : {
		    "mkt_id" : _int_na,
		    "posttime" : _datetime_na,
		    "wholesale" : _float_na,
		    "ctrl_price" : _float_na,
		    "fixed_price" : _float_na,
		    "tou_price" : _float_na,
		    "rtp_price" : _float_na,
		},
		"sell" : {
		    "supplier_id" : _int_na,
		    "posttime" : _datetime_na,
		    "mkt_id" : _int_na,
		    "quantity" : _float_na,
		    "price" : _float_na,
		},
		"supplier" : {
		    "supplier_id" : _int_na,
		    "supplier_type_code" : _str_na,
		    "supplier_name" : _str_na,
		    "is_active" : _bool_na,
		    "capacity_kw" : _float_na,
		    "fuel_price" : _float_na,
		    "fuel_price_unit_code" : _str_na,
		    "license_start" : _datetime_na,
		    "license_end" : _datetime_na,
		    "license_hours" : _float_na,
		    "run_hours" : _float_na,
		    "annual_cost" : _float_na,
		    "startup_cost" : _float_na,
		    "shutdown_cost" : _float_na,
		    "state_type_code" : _str_na,
		    "state_type_desc" : _str_na,
		    "statechange_time" : _datetime_na,
		    "dg_updatetime" : _datetime_na,
		},
		"supplier_feeder_limit" : {
		    "supplier_id" : _int_na,
		    "start_date" : _datetime_na,
		    "end_date" : _datetime_na,
		    "capacity" : _float_na,
		},
		"supplier_feeder_status" : {
		    "supplier_id" : _int_na,
		    "posttime" : _datetime_na,
		    "updatetime" : _datetime_na,
		    "status" : _str_na,
		    "capacity" : _float_na,
		},
		"supplier_type" : {
		    "supplier_type_code" : _str_na,
		    "supplier_type_desc" : _str_na,
		},
		"tou_prices" : {
		    "tou_prices_id" : _int_na,
		    "startdate" : _date_na,
		    "enddate" : _date_na,
		    "hour" : _int_na,
		    "critical_price" : _float_na,
		    "price" : _float_na,
		    "unit_type_code" : _str_na,
		},
		"unit_type" : {
		    "unit_type_code" : _str_na,
		    "unit_type_abbrev" : _str_na,
		    "unit_type_desc" : _str_na,
		},
		"weather" : {
		    "zipcode" : _int_na,
		    "readtime" : _datetime_na,
		    "posttime" : _datetime_na,
		    "temperature" : _float_na,
		    "humidity" : _float_na,
		    "dewpoint" : _float_na,
		    "windvel" : _float_na,
		    "winddir" : _str_na,
		    "barometer" : _float_na,
		    "visibility" : _float_na,
		},
		"weather_copa_hourly" : {
		    "Posttime" : _datetime_na,
		    "Temperature" : _float_na,
		},
		"weather_degree_hours" : {
		    "readtime" : _datetime_na,
		    "temp" : _float_na,
		    "hdh" : _float_na,
		    "cdh" : _float_na,
		},
		"weather_degree_month" : {
		    "billing_month" : _int_na,
		    "days" : _int_na,
		    "hdh" : _float_na,
		    "cdh" : _float_na,
		},
		"weather_sites" : {
		    "zipcode" : _int_na,
		    "city_st" : _str_na,
		    "noaacode" : _str_na,
		},
		"weathernoaa" : {
		    "noaacode" : _str_na,
		    "readtime" : _datetime_na,
		    "posttime" : _datetime_na,
		    "temperature" : _float_na,
		    "humidity" : _float_na,
		    "dewpoint" : _float_na,
		    "windvel" : _float_na,
		    "winddir" : _float_na,
		    "barometer" : _float_na,
		    "visibility" : _float_na,
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
		"dashboard_data" : ["readtime"],
		"dev_type_comfort_level" : ['dev_type_comfort_level_id'],
		"device_type" : ["device_type_id"],
		"experiment" : ["experiment_code"],
		"experiment_participant" : ["experiment_participant_id"],
		"fixed_price" : ["fixed_price_id"],
		"home_mode_type" : ["home_mode_type_id"],
		"invensys_meter" : ["customer_id"],
		"invensys_weather" : ["invensys_acct_id"],
		"midc" : ["report_time"],
		"noaa_weather_station" : ["noaacode"],
		"prices" : ["mkt_id"],
		"sell" : ["mkt_id","price"],
		"supplier" : ["supplier_id"],
		"supplier_feeder_limit" : ["supplier_id"],
		"supplier_feeder_status" : ["supplier_id"],
		"supplier_type" : ["supplier_type_code"],
		"tou_prices" : ["startdate","hour"],
		"unit_type" : ["unit_type_code"],
		"weather" : ["zipcode","readtime"],
		"weather_copa_hourly" : ["Posttime"],
		"weather_degree_hours" : ["readtime"],
		"weather_degree_month" : ["billing_month"],
		"weather_sites" : ["zipcode"],
		"weathernoaa" : ["noaacode","readtime"],		
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

	def __getattr__(self,name):
		"""Get a data table"""
		if not name in self.tables:
			return self.table(name)
		else:
			return self.tables[name]

	def __delitem__(self,name):
		del self.tables[name]
		
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
		data = pandas.read_csv(file,**kwargs)
		self._verbose(f"{len(data)} records loaded")
		self.tables[name] = data
		return data

if __name__ == "__main__":
	repo = Olypen()
	for name in repo.directory:
		print(name,end='... ',file=sys.stderr,flush=True)
		tic = datetime.datetime.now()
		data = repo[name]
		toc = datetime.datetime.now()
		t = (toc-tic).total_seconds()
		n = len(data)
		print(f"{n} records loaded in {t:.1f} seconds ({(n/t):.0f} records/second)",file=sys.stderr,flush=True)
		del repo[name]

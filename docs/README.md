# Welcome

This repository contains the source to a Python module that can be used to access the Olympic Peninsula Gridwise Demonstration Project data.

See [references](references) for project details, including [implementation source code](references/source), the [data dictionary](references/data_dictionary.csv), and [participant survey results](references/surveys). 

## Installation

Do the following to install this module:

~~~
git clone https://github.com/dchassin/olypen
python3 -m pip install olypen
~~~

## Example

Python code to get a directory of tables:
~~~
import olypen
d = olypen.Olypen()
d.directory
d['clear']
~~~

Output:
~~~
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
~~~

Additional examples are available in the [`examples` folder](examples).

## Citation

Chassin, David P, "Olympic Peninsula Demonstration Testbed Data Accessor", SLAC National Accelerator Laboratory, Menlo Park, California (2023). URL: https://github.com/dchassin/olypen.

## References

* Chassin, David P., "Olympic Peninsula Demonstration Testbed Results", PNNL-SA-70980, Pacific Northwest National Laboratory, Richland, Washington (2010). URL: https://svn.pnl.gov/olypen.

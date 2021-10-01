# dte-usage-plotter
Parse data and generate graph from DTE Energy customer data

## Usage example

```sh
python c:\src\dte_usage_plotter\dtefeed.py --days 14 https://usagedata.dteenergy.com/link/000000-000-00000-0000000-0000
```

Get link here: https://usage.dteenergy.com/

## Command line parameters

```
-h, --hours INTEGER  Get data for last x hours
--days INTEGER       Get data for last x days
--days_cost INTEGER  Get cost data for last x days
--hdist              Hourly distribution
--night              Night hourly distribution
-d, --debug          Debug mode
--help               Show this message and exit.
```
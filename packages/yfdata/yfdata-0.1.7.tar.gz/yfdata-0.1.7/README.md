# yf-data

![application-build](https://github.com/caps6/yf-data/actions/workflows/python-build.yml/badge.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/yfdata)

A simple-but-working python module that returns data from Yahoo Finance.

Current Version: 0.1.7


### Features

Data include:
- OHLC values for stocks and exchange rates
- dividends
- financial data of companies (income and balance sheets).

All data are returned as [Pandas Dataframe](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html).

### Usage

```python

from yfdata import YahooProvider

yp = YahooProvider()

# Frequency for prices and exchange rates can be daily ("1D") or 1-minute ("1m").
 
# Get daily OHLC data.
df = yp.get_prices(["aapl"], "1D")

# Get exchange rates with frequency of 1 minute.
df = yp.get_rates("usd", "eur", freq="1m")

# Get company dividends.
df = yp.get_dividends(["aapl", "msft"])


# Frequency for income data can be annual ("A"), quarterly ("Q") or 
# trailing twelwe months ("TTM").

# Frequency for balance data can be annual ("A") or quarterly ("Q"). 

# Get annual income data.
df = yp.get_income(["aapl", "msft"], freq="A")

# Get quarterly balance data.
df = yp.get_balance(["aapl", "msft"], freq="Q")

# Define a list of specific metrics for income data.
metrics = ["total_revenue", "ebitda"]
df = yp.get_income(["aapl", "msft"], freq="A", metrics=metrics)

```

### Output examples

An excerpt from 1-minute OHLC price data:

| ticker | ts                  | o          | h          | l          | c          | v         |
|--------|---------------------|------------|------------|------------|------------|-----------|
| aapl   | 2024-07-26 13:30:00 | 218.850006 | 219.149902 | 218.089996 | 218.740005 | 1170434.0 |
| aapl   | 2024-07-26 13:31:00 | 218.389999 | 218.470001 | 218.000000 | 218.020004 | 382342.0  |
| aapl   | 2024-07-26 13:32:00 | 218.054993 | 218.740005 | 218.020004 | 218.481903 | 227239.0  |
| aapl   | 2024-07-26 13:33:00 | 218.479996 | 218.539993 | 217.669998 | 217.669998 | 263403.0  |
| aapl   | 2024-07-26 13:34:00 | 217.630005 | 217.630005 | 217.119995 | 217.160004 | 241679.0  |

An excerpt from annual balance data:

| ticker | metric                 | freq | date       | value       |
|--------|------------------------|------|------------|-------------|
| aapl   | total_assets           | A    | 2020-09-30 | 3.23888e+11 |
| aapl   | total_assets           | A    | 2021-09-30 | 3.51002e+11 |
| aapl   | total_assets           | A    | 2022-09-30 | 3.52755e+11 |
| aapl   | total_assets           | A    | 2023-09-30 | 3.52583e+11 |
| aapl   | ordinary_shares_number | A    | 2020-09-30 | 1.69768e+10 |
| aapl   | ordinary_shares_number | A    | 2021-09-30 | 1.64268e+10 |
| aapl   | ordinary_shares_number | A    | 2022-09-30 | 1.59434e+10 |
| aapl   | ordinary_shares_number | A    | 2023-09-30 | 1.55501e+10 |

### Financial metrics

Available metrics for income sheet are:
- total_revenue
- cost_of_revenue
- gross_profit
- operating_expense
- operating_income
- non_operating_interest_income_expense
- other_income_expense
- basic_eps
- diluted_eps
- basic_average_shares
- total_expense
- normalized_income
- ebit
- ebitda

Available metrics for balance sheet are:
- total_assets
- total_liabilities_net_minority_interest
- total_equity_gross_minority_interest
- total_capitalization
- common_stock_equity
- capital_lease_obligations
- net_tangible_assets
- working_capital
- invested_capital
- tangible_book_value
- total_debt
- net_debt
- share_issued
- ordinary_shares_number
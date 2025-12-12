# -*- coding: utf-8 -*-
import random

from .constants import (
    FREQ_DAILY,
    MAPPING_INCOME_METRICS,
    MAPPING_BALANCE_METRICS,
    BROWSERS,
)
from yfdata import urls
from . import parsing

import pandas as pd
from pandas import DataFrame
from curl_cffi import requests


class YahooProvider:
    """Provides data from Yahoo Finance.

    Data include OHLC values for stocks and exchange rates, and dividends and
    financial (income and balance) data of companies.

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

    Examples:
        Create the provider e get some daily stock prices.

        >>> from yfdata import YahooProvider
        >>> yp = YahooProvider()
        >>> df = yp.get_prices(["aapl"], "1D")

        Get exchange rates with frequency of 1 minute.
        >>> df = yp.get_rates("usd", "eur", freq="1m")

        Get company dividends.
        >>> df = yp.get_dividends(["aapl", "msft"])

        Get annual income data.
        >>> df = yp.get_income(["aapl", "msft"], freq="A")

        Get quarterly balance data.
        >>> df = yp.get_balance(["aapl", "msft"], freq="Q")

        Define specific income metrics to retrieve.
        >>> metrics = ["revenue", "ebitda"]
        >>> df = yp.get_income(["aapl", "msft"], freq="A", metrics=metrics)

    """

    def get_prices(self, tickers: list, freq: str = FREQ_DAILY) -> DataFrame:
        """Gets OHLC price data for multiple tickers.

        Args:
            tickers: List of company tickers.
            freq: Data sampling, can be ``1D`` (daily) or ``1m`` (1 minute).

        Returns:
            A DataFrame with OHLC data for prices.

        """

        if isinstance(tickers, str):
            tickers = [tickers]

        dfs = []
        for ticker in tickers:

            url = urls.build_url_prices(ticker, freq)

            # Execute request and parse results.
            r = requests.get(url, impersonate=random.choice(BROWSERS))

            # Parse results.
            df = parsing.parse_prices_or_rates(r.json(), ticker)

            # Append dataframe.
            dfs.append(df)

        df = pd.concat(dfs, ignore_index=True)

        return df

    def get_rates(self, base: str, quote: str, freq: str = FREQ_DAILY) -> DataFrame:
        """Gets OHLC exchange rates for multiple tickers.

        Args:
            base: Currency base.
            quote: Currency quote.
            freq: Data sampling, can be ``1D`` (daily) or ``1m`` (1 minute).

        Returns:
            A DataFrame with OHLC data for exchange rates.

        """

        pair = f"{quote}/{base}"

        url = urls.build_url_rates(base, quote, freq)

        # Execute request and parse results.
        r = requests.get(url, impersonate=random.choice(BROWSERS))
        df = parsing.parse_prices_or_rates(r.json(), pair)

        return df

    def get_income(self, tickers: list, freq: str, metrics: list = None) -> DataFrame:
        """Gets income data for a list of companies.

        Args:
            tickers: List of company tickers.
            freq: Period of data, can be quarterly (Q), annual (A) or trailing
                twelwe months (TTM).
            metrics: List of specific metrics to retrieve. If None, it returns
                all metrics available for income sheet.
        Returns:
            DataFrame with financial data.

        """

        if isinstance(tickers, str):
            tickers = [tickers]

        if metrics is None:
            metrics = list(MAPPING_INCOME_METRICS.keys())

        # Mapping filtered by metrics to retrieve and its inverse mapping.
        mapping = {
            k: v[freq] for k, v in MAPPING_INCOME_METRICS.items() if k in metrics
        }
        inv_mapping = {v: k for k, v in mapping.items()}

        dfs = []

        for ticker in tickers:

            url = urls.build_url_financials(ticker, freq, mapping)

            # Execute request and parse results.
            r = requests.get(url, impersonate=random.choice(BROWSERS))
            df = parsing.parse_financials(r.json(), ticker, freq, inv_mapping)

            dfs.append(df)

        df_full = pd.concat(dfs, ignore_index=True)

        return df_full

    def get_balance(self, tickers: list, freq: str, metrics: list = None) -> DataFrame:
        """Gets income data for a list of companies.

        Args:
            tickers: List of company tickers.
            freq: Period of data, can be quarterly (Q) or annual (A).
            metrics: List of specific metrics to retrieve. If None, it returns
                all metrics available for balance sheet.
        Returns:
            DataFrame with financial data.

        """

        if isinstance(tickers, str):
            tickers = [tickers]

        if metrics is None:
            metrics = list(MAPPING_BALANCE_METRICS.keys())

        # Mapping filtered by metrics to retrieve and its inverse mapping.
        mapping = {
            k: v[freq] for k, v in MAPPING_BALANCE_METRICS.items() if k in metrics
        }
        inv_mapping = {v: k for k, v in mapping.items()}

        dfs = []

        for ticker in tickers:

            url = urls.build_url_financials(ticker, freq, mapping)

            # Execute request and parse results.
            r = requests.get(url, impersonate=random.choice(BROWSERS))
            df = parsing.parse_financials(r.json(), ticker, freq, inv_mapping)

            dfs.append(df)

        df_full = pd.concat(dfs, ignore_index=True)

        return df_full

    def get_dividends(self, tickers: list) -> DataFrame:
        """Gets dividend data of a company.

        Args:
            tickers: List of company tickers.

        Returns:
            DataFrame with dividend data.

        """

        if isinstance(tickers, str):
            tickers = [tickers]

        dfs = []

        for ticker in tickers:

            url = urls.build_url_dividends(ticker)

            # Execute request and parse results.
            r = requests.get(url, impersonate=random.choice(BROWSERS))

            df = parsing.parse_dividends(r.json(), ticker)

            # Append dataframe.
            dfs.append(df)

        df = pd.concat(dfs, ignore_index=True)

        return df

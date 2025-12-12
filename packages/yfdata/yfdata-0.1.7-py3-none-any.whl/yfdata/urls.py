# -*- coding: utf-8 -*-
"""Module with helpers for building URLs of Yahoo Finance API endpoints.
"""

from .constants import (
    T1W,
    T1M,
    T5Y,
    FREQ_DAILY,
    FREQ_MINUTE,
    FREQ_QUARTERLY,
    FREQ_ANNUAL,
    TTM,
)
from yfdata import utils

# Base URLs.
URL_BASE_CHART = "https://query1.finance.yahoo.com/v8/finance/chart"
URL_BASE_FIN_1 = (
    "https://query1.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries"
)
URL_BASE_FIN_2 = (
    "https://query2.finance.yahoo.com/ws/fundamentals-timeseries/v1/finance/timeseries"
)


def build_url_prices(ticker: str, freq: str) -> str:
    """Build URL for price data.

    Args:
        ticker: Stock code.
        freq: Data sampling, can be ``1D`` (daily) or ``1m`` (1 minute).

    Returns:
        String of the endpoint URL.

    """

    if freq not in (FREQ_DAILY, FREQ_MINUTE):
        raise ValueError("Frequency not supported.")

    url = f"{URL_BASE_CHART}/{ticker.upper()}"

    if freq == FREQ_DAILY:
        date_1 = utils.eval_past_dt(T1M)
        url += "?interval=1d&range=1mo"
    else:
        date_1 = utils.eval_past_dt(T1W)
        url += "?interval=1m&range=1w"

    # Add periods to endpoint url.
    period_1 = utils.datetime2timestamp(date_ref=date_1)
    period_2 = utils.datetime2timestamp()
    url += f"&period1={period_1}&period2={period_2}"

    url = finalize_url(url)

    return url


def build_url_rates(base: str, quote: str, freq: str) -> str:
    """Build URL for exchange rates.

    Args:
        base: Currency base.
        quote: Currency quote.
        freq: Data sampling, can be ``1D`` (daily) or ``1m`` (1 minute).

    Returns:
        String of the endpoint URL.

    """

    if freq not in (FREQ_DAILY, FREQ_MINUTE):
        raise ValueError("Frequency not supported.")

    url = f"{URL_BASE_CHART}/{base.upper()}{quote.upper()}=X"

    if freq == FREQ_DAILY:
        date_1 = utils.eval_past_dt(T1M)
        url += "?interval=1d&range=1mo"
    else:
        date_1 = utils.eval_past_dt(T1W)
        url += "?interval=1m&range=1w"

    url += "&includePrePost=false"

    # Add periods to endpoint url.
    period_1 = utils.datetime2timestamp(date_ref=date_1)
    period_2 = utils.datetime2timestamp()
    url += f"&period1={period_1}&period2={period_2}"

    url = finalize_url(url)

    return url


def build_url_financials(ticker: str, freq: str, mapping: dict) -> str:
    """Build URL for financial data.

    Args:
        ticker: Stock code.
        freq: Data sampling, can be ``Q`` (quarterly) or ``A`` (annual).
        mapping: Mapping from names of metrics to retrieve and their yahoo names.

    Returns:
        String of the endpoint URL.

    """

    if freq not in (FREQ_QUARTERLY, FREQ_ANNUAL, TTM):
        raise ValueError("Frequency of financial metrics not supported.")

    url = f"{URL_BASE_FIN_1}/{ticker.upper()}"

    # Add time periods to endpoint url.
    date_1 = utils.eval_past_dt(T5Y)
    period_1 = utils.datetime2timestamp(date_ref=date_1)
    period_2 = utils.datetime2timestamp()
    url += f"?period1={period_1}&period2={period_2}"
    url += "&padTimeSeries=true&merge=false"

    # Add financial metrics to retrieve.
    url += "&type=" + ",".join([mapping[m] for m in mapping])

    url = finalize_url(url)

    return url


def build_url_dividends(ticker: str) -> str:
    """Build URL for dividends.

    Args:
        ticker: Stock code.

    Returns:
        String of the endpoint URL.

    """

    url = f"{URL_BASE_CHART}/{ticker.upper()}"

    # Evaluate periods.
    date_1 = utils.eval_past_dt(T5Y)
    period_1 = utils.datetime2timestamp(date_ref=date_1)
    period_2 = utils.datetime2timestamp()

    # Compose endpoint url.
    url += f"?period1={period_1}&period2={period_2}"
    url += "&interval=1d&events=div"

    url = finalize_url(url)

    return url


def finalize_url(url: str) -> str:

    url += "&lang=en-US&region=US"
    url += "&corsDomain=finance.yahoo.com"

    return url

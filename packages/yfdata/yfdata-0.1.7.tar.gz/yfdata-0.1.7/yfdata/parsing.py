# -*- coding: utf-8 -*-
"""Module with helpers for parsing API content returned by Yahoo API endpoints.
"""
from yfdata import utils

import pandas as pd
from pandas import DataFrame


def parse_prices_or_rates(body: dict, ticker_or_pair: str) -> DataFrame:
    """Parse OHLC data for stock prices and exchange rates.

    Args:
        body: Body response from API.
        ticker_or_pair: Ticker or currency pair.

    Returns:
        DataFrame with OHLC data.

    """

    df = None

    result = body["chart"]["result"]

    if isinstance(result, list) and len(result) > 0:

        data = body["chart"]["result"][0]

        metadata = data["meta"]
        if (
            metadata["instrumentType"] == "EQUITY"
            or metadata["instrumentType"] == "ETF"
        ):
            code_name = "ticker"
        elif metadata["instrumentType"] == "CURRENCY":
            code_name = "pair"
        else:
            raise ValueError("Instrument type not supported.")

        if isinstance(data, dict) and "timestamp" in data and "indicators" in data:

            ts = data["timestamp"]
            quotes = data["indicators"]["quote"][0]

            df = DataFrame(
                data={
                    "ts": ts,
                    "o": quotes["open"],
                    "h": quotes["high"],
                    "l": quotes["low"],
                    "c": quotes["close"],
                    "v": quotes["volume"],
                }
            )

    if df is None:
        code_name = "instrument"
        df = DataFrame(
            data={
                "ts": [],
                "o": [],
                "h": [],
                "l": [],
                "c": [],
                "v": [],
            }
        )

    df[code_name] = ticker_or_pair.lower()
    df["ts"] = pd.to_datetime(df["ts"], unit="s")

    # Reorder the columns.
    df = df[[code_name, "ts", "o", "h", "l", "c", "v"]]

    return df


def parse_financials(body: dict, ticker: str, freq: str, mapping: dict) -> DataFrame:
    """Parse financials data of a company.

    Args:
        body: Body response from API.
        ticker: Ticker of the company.
        freq: Period of data, can be quarterly or annual.
        mapping: Mapping from Yahoo metric names to their canonical names.

    Returns:
        DataFrame with retrieved financial data.

    """

    dfs = []

    # Parse results.
    res = body["timeseries"]["result"]

    for r in res:

        yahoo_metric_name = r["meta"]["type"][0]

        dates = []
        values = []

        if yahoo_metric_name in r:

            for item in r[yahoo_metric_name]:

                if item is not None:
                    dates.append(item["asOfDate"])
                    values.append(float(item["reportedValue"]["raw"]))

        df = DataFrame(
            data={
                "date": dates,
                "value": values,
            }
        )

        df["metric"] = mapping[yahoo_metric_name]
        dfs.append(df)

        df = pd.concat(dfs, ignore_index=True)
        df["ticker"] = ticker.lower()
        df["freq"] = freq

    df = df[["ticker", "metric", "freq", "date", "value"]]

    return df


def parse_dividends(body: dict, ticker: str) -> DataFrame:
    """Parse dividend data of a company.

    Args:
        body: Body response from API.
        ticker: Ticker of company.

    Returns:
        DataFrame with dividend data.

    """

    dates = []
    dividends = []

    result = body["chart"]["result"]

    if isinstance(result, list) and len(result) > 0:

        data = result[0]

        if isinstance(data, dict) and "events" in data:

            dict_dividends = data["events"]["dividends"]

            for uts in dict_dividends:

                if "amount" in dict_dividends[uts]:

                    ts = utils.timestamp2datetime(int(uts))
                    dates.append(ts)
                    dividends.append(dict_dividends[uts]["amount"])

    df = DataFrame(
        data={
            "ts": dates,
            "dividend": dividends,
        }
    )

    df["ticker"] = ticker.lower()

    df["ts"] = pd.to_datetime(df["ts"], unit="s").dt.date

    df = df[["ticker", "ts", "dividend"]]

    return df

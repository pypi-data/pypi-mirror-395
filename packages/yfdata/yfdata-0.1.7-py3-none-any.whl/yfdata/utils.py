# -*- coding: utf-8 -*-
"""Module for utility functions."""
from datetime import datetime, timezone, timedelta

from .constants import CURRENCY_EUR, T1W, T1M, T5Y


def eval_past_dt(timeframe: str, date_ref: datetime = None) -> datetime:
    """Computes a datetime in the past according to a given timeframe or to
    given number of minutes. All datetimes are in UTC zone.

    Allowed values for timeframe are:
    - '1D' (1 day ago),
    - '1M' (1 month ago),

    """

    if date_ref is None:
        date_ref = datetime.now(timezone.utc).replace(tzinfo=None)

    if timeframe is not None:
        if timeframe == T1W:
            dt = date_ref - timedelta(days=7)
        elif timeframe == T1M:
            dt = date_ref - timedelta(days=30)
        elif timeframe == T5Y:
            dt = date_ref - timedelta(days=1826)
        else:
            raise ValueError("Timeframe not supported.")

    else:
        raise ValueError("A value for timeframe or minutes must be defined.")

    return dt


def datetime2timestamp(date_ref: datetime = None) -> int:

    if date_ref is None:
        date_ref = datetime.now()

    unix_timestamp = int(datetime.timestamp(date_ref.replace(tzinfo=None)))

    return unix_timestamp


def timestamp2datetime(timestamp: int) -> datetime:

    dt = datetime.fromtimestamp(timestamp).replace(tzinfo=None)

    return dt

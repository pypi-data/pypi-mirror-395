# -*- coding: utf-8 -*-
"""
Helper functions for visualization data preparation.

This module provides utility functions for date calculations and prediction formatting
used by the web application's visualization system.
"""

import torch
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
import datetime


def is_bank_holiday(date, calendar):
    """
    Identifies dates of bank holidays.

    Args:
        date (TimeStamp): last available date in the dataset.

    Returns:
        (bool): True if the date is a bank holiday.
    """
    # Get the list of bank holidays for the year of the given date
    holidays = calendar.holidays(
        start=date.replace(month=1, day=1), end=date.replace(month=12, day=31)
    )
    return date in holidays


def weekend_eraser(input_date, calendar):
    """
    If the last available date in the dataset is Friday,
    it returns the date of the next Monday.

    Args:
        input_date (TimeStamp): last available date in the dataset.

    Returns:
        input_date (next_monday_date): date for predicted value.
    """
    while True:
        # Check if the input date is a Saturday or a bank holiday
        if input_date.weekday() in [5, 6] or is_bank_holiday(input_date, calendar):
            # Move to next day, then check again
            input_date += datetime.timedelta(days=1)
        else:
            return input_date


def day_fw(df):
    """
    Computes the next date the stock market is open, that is,
    the date the prediction corresponds to.

    Args:
        df (DataFrame): dataframe with predicted values.

    Returns:
        (TimeStamp): date corresponding to the
        last predicted value.
    """
    calendar = USFederalHolidayCalendar()
    date = pd.to_datetime(df.index[-1])
    next_date = weekend_eraser(date + pd.DateOffset(days=1), calendar)
    return (
        next_date.strftime("%Y-%m-%d %H:%M:%S%z")
        if next_date.tz
        else next_date.strftime("%Y-%m-%d")
    )


def aux_plot_func(pred_prob, next_index):
    """
    Extracts the predicted probability of the last date
    and its timestamp.

    Args:
        pred_prob (Tensor or array): dataset of predicted probabilities
        next_index (TimeStamp): data of last prediction

    Returns:
        future_day (string): data of last prediction
        last_pred_prob (float): predicted probability on last date
    """
    future_day = next_index.strftime("%Y-%m-%d")
    if isinstance(pred_prob, torch.Tensor):
        last_pred_prob = (pred_prob[-1].numpy() * 100).round(2)
    else:
        last_pred_prob = (pred_prob[-1] * 100).round(2)
    return future_day, last_pred_prob

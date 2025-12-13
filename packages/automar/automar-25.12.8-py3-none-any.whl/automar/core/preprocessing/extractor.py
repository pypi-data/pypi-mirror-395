# -*- coding: utf-8 -*-
import contextlib
import os
import requests
from io import StringIO
import pandas as pd
import yfinance as yf
import warnings


def custom_warning_handler(message, category, filename, lineno, file=None, line=None):
    # Print only the warning message
    print(f"{category.__name__}: {message}")


warnings.showwarning = custom_warning_handler

GICStoYF = {
    "Materials": "Basic Materials",
    "Industrials": "Industrials",
    "Financials": "Financial Services",
    "Energy": "Energy",
    "Consumer Discretionary": "Consumer Cyclical",
    "Information Technology": "Technology",
    "Communication Services": "Communication Services",
    "Real Estate": "Real Estate",
    "Health Care": "Healthcare",
    "Consumer Staples": "Consumer Defensive",
    "Utilities": "Utilities",
}

GICSbrief = {
    "Materials": "M",
    "Industrials": "I",
    "Financials": "F",
    "Energy": "E",
    "Consumer Discretionary": "CD",
    "Information Technology": "IT",
    "Communication Services": "CS",
    "Real Estate": "RE",
    "Health Care": "HC",
    "Consumer Staples": "CS",
    "Utilities": "U",
}


def naremove(x):
    """
    Replaces missing values with the average between the two
    closest actual values before and after the null observation.

    Args:
        x (dictionary or dataframe): object potentially containing missing values.

    Returns:
        x (dictionary or dataframe): updated object with missing values
        replaced, if any existed, identical to the input otherwise.
    """
    if type(x) == dict:
        nalist = []
        for key, value in x.items():
            x[key] = pd.DataFrame(x[key])
            if None in value:
                nalist.append(1)
        nanum = sum(nalist)
        if nanum > 0:
            for key, value in x.items():
                x[key].ffill().add(x[key].bfill()).div(2)
    else:
        nanum = x.isna().sum().sum()
        if nanum > 0:
            for key in x.keys():
                if pd.isna(x[key].iloc[0]):
                    x[key].iloc[0] = x[key].bfill().iloc[0]
                if pd.isna(x[key].iloc[-1]):
                    x[key].iloc[-1] = x[key].ffill().iloc[-1]
                x[key] = x[key].ffill().add(x[key].bfill()).div(2)

    if nanum == 1:
        print(
            f"A non assigned value was identified and replaced by its closest values average."
        )
    elif nanum > 1:
        print(
            f"{nanum} non assigned values were identified and replaced by their closest values averages."
        )
    else:
        pass

    return x


def tick_func(tick_input, period, datest=None, datend=None):
    """
    Processes the Yahoo Finance query as a dataframe.

    Args:
        tick_input (str): ticker of the requested company.
        period (str): number and type of periods.
        date (str, optional): End date for data extraction.

    Returns:
        (dataframe): panel of opening, closing, highest and lowest price and
        volume of stock of the requested company for the requested period (see
        :func: 'naremove' )
    """
    tick1 = yf.Ticker(tick_input)
    if not datest:
        histrain = tick1.history(period=period, actions=False)
    else:
        histrain = tick1.history(
            actions=False,
            start=pd.to_datetime(datest, format="%Y-%m-%d"),
            end=pd.to_datetime(datend, format="%Y-%m-%d"),
        )
    if histrain.empty:
        raise ValueError(
            f"Not enough data available for {tick_input}, please reduce the number of periods."
        )
    return naremove(pd.DataFrame(histrain))


def sectconv(x):
    """
    Matches a Yahoo Finance styled industry name with the GICS conventional
    industry name.

    Args:
        x (str): name of the industry (Yahoo Finance)

    Returns:
        GICS (str): name of the industry (GICS)
    """
    for GICS, YF in GICStoYF.items():
        if x == YF:
            return GICS
        elif x not in GICStoYF.values():
            return "Sector not available"


def sectbrf(s):
    """
    Matches a GICS industry name with its conventional acronym.

    Args:
        s (str): name of the industry (GICS).

    Returns:
        brief (str): a string, acronym of the industry.
    """
    for GICS, brief in GICSbrief.items():
        if s == GICS:
            return brief


def ind_func(tick_input):
    """
    Extracts industry name out of the Yahooquery query.

    Args:
        tick_input (str): ticker of the requested company.

    Returns:
        GICSindustry (str): GICS style name of the requested
        industry (see :func: 'setconv')
    """
    tick = yf.Ticker(tick_input)
    YFindustry = tick.info["sector"]
    GICSindustry = sectconv(YFindustry)
    return GICSindustry


def symbols_func(
    tick_input, period, ind_input=None, skip=True, datest=None, datend=None
):
    """
    Generates a dictionary with the requested industry name and
    a dictionary of dataframes for each company in the requested indutry
    based on the Yahoo Finance queries.

    Args:
        tick_input (str): ticker of the requested company.
        period (str): number and type of requested periods.
        ind_input (str or None, optional): name of the requested industry. If
            None uses the same industry the requested company belongs
            in. Defaults to None.
        skip (bool, optional): Whether to skip or not companies with less
            available data than requested. Defaults to True.
        date (str, optional): End date for data extraction.

    Returns:
        ind_dic (dict): the key 'data' is a dictionary of dataframes with
        the opening, closing, highest and lowest price and volume of stock of
        the companies in the requested industry for the requested period, the
        key 'name' is a string, the name of the requested industry.
    """
    spdata = {}
    site = StringIO(
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    ).getvalue()
    rr = requests.get(
        site,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        },
    )

    sp500 = pd.read_html(StringIO(rr.text))

    # Find the correct S&P 500 table (Wikipedia may have warning tables before it)
    sp500_table = None
    for table in sp500:
        if "Symbol" in table.columns and "GICS Sector" in table.columns:
            sp500_table = table
            break

    if sp500_table is None:
        raise ValueError("Could not find S&P 500 constituents table in Wikipedia page")

    if tick_input is not None and str(tick_input) not in sp500_table["Symbol"].values:
        raise ValueError(
            f"Please input the ticker of a company included in the S&P 500 list, [{tick_input}] is not found"
        )
    if not ind_input:
        industry = ind_func(tick_input)
    else:
        industry = ind_input

    spsymbols = list(sp500_table.loc[sp500_table["GICS Sector"] == industry]["Symbol"])

    if tick_input in spsymbols:  # List reordered for efficiency in arriving to error
        spsymbols.remove(tick_input)
        spsymbols.insert(0, tick_input)

    for ii in spsymbols:
        ticks = yf.Ticker(ii)
        with open(os.devnull, "w") as devnull:
            with contextlib.redirect_stderr(devnull):
                if datest:
                    hists = ticks.history(
                        actions=False,
                        start=pd.to_datetime(datest, format="%Y-%m-%d"),
                        end=pd.to_datetime(datend, format="%Y-%m-%d"),
                    )
                else:
                    hists = ticks.history(period=period, actions=False)

        if hists.empty:
            # If this is the explicitly requested ticker, raise error
            # Otherwise, warn and skip (regardless of skip parameter)
            if ii == tick_input:
                raise ValueError(
                    f"Not enough data available for {ii}, please reduce the number of periods."
                )
            # For industry downloads, always skip tickers with no data
            warnings.warn(f"Not enough data available for {ii}, skipping.")
            continue

        spdata[ii] = hists
    ind_dic = {"data": naremove(spdata), "name": industry}
    return ind_dic


def ind_avg_func(input_dic, ref_df):
    """
    Generates a dataframe with industry wide average values.

    Args:
        input_dic (dict): contains dataframes with the queries' variables
            opening, closing, lowest and highest price and volume of stock (see
            the output of :func: 'symbols_func').
        ref_df (dataframe): dataframe whose index will be copied by the output.

    Returns:
        MeansDF (dataframe): dataframe containing the industry average values
        of the opening, closing, lowest and highest price and volume of stock
        for every observation.
    """
    spdataOpen = []
    spdataHigh = []
    spdataLow = []
    spdataClose = []
    spdataVolume = []

    for key, value in input_dic.items():
        spdataOpen.append(input_dic[key].Open)
        spdataHigh.append(input_dic[key].High)
        spdataLow.append(input_dic[key].Low)
        spdataClose.append(input_dic[key].Close)
        spdataVolume.append(input_dic[key].Volume)

    MeansDF = pd.DataFrame(
        {
            "Open": pd.Series(index=ref_df.index),
            "High": pd.Series(index=ref_df.index),
            "Low": pd.Series(index=ref_df.index),
            "Close": pd.Series(index=ref_df.index),
            "Volume": pd.Series(index=ref_df.index),
        }
    )

    MeansDF["Open"] = pd.DataFrame(spdataOpen).mean()
    MeansDF["High"] = pd.DataFrame(spdataHigh).mean()
    MeansDF["Low"] = pd.DataFrame(spdataLow).mean()
    MeansDF["Close"] = pd.DataFrame(spdataClose).mean()
    MeansDF["Volume"] = pd.DataFrame(spdataVolume).mean()

    return MeansDF


def df_industry_split(df, industry=None, ticker=None):
    if ticker and not industry:
        tick_df = df[df["Company"] == ticker]
        ind_df = df[df["Company"] != ticker]
    if not ticker and industry:
        tick_df = None
        ind_df = df
    if ticker and industry:
        if df[df["Company"] == ticker].iloc[0]["Industry"] == industry:
            ind_df = df
            tick_df = df[df["Company"] == ticker]
        else:
            tick_df = df[df["Company"] == ticker]
            ind_df = df[df["Industry"] == industry]

    return tick_df, ind_df


def df_industry_avg(df, ticker=1):
    if ticker == 1:
        return df.drop(["Company", "Industry", "Labels"], axis=1).groupby("Date").mean()
    else:
        return df.drop(["Company", "Industry"], axis=1).groupby("Date").mean()

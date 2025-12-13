# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def labeler(input_df):
    """
    Classifies the quantitative difference between subsequent observations of
    the opening stock price as either an increase (1) or a decrease (0).

    Args:
        input_df (dataframe): contains the opening stock price in 'Open'
            column.

    Returns:
        labelvector (series): classification of 'Open' differences.
    """
    labelvector = pd.Series(index=input_df.index, dtype="float64")
    labelvector.iloc[0] = 1.0
    for ii in range(1, len(input_df)):
        labelvector.iloc[ii] = (
            0.0 if input_df.Open.iloc[ii] < input_df.Open.iloc[ii - 1] else 1.0
        )
    return labelvector


def MA_func(input_df, n):
    """
    Calculates moving averages of the closing stock price.

    Args:
        input_df (dataframe): dataframe containing the 'Close' column
        n (float): number of periods included in each rolling window

    Returns:
        Series of moving averages of the 'Close' column
    """
    return input_df.Close.rolling(n).mean()


def RSVKD(input_df):
    """
    Calculates the relative strength value (RSV) in order to derive the fast
    stochastic indicator K and the slow stochastic indicator D.

    Args:
        input_df (dataframe): dataframe containing the closing, lowest and
            highest stock prices in columns 'Close', 'Low' and 'High'.

    Returns:
        RSVdic (dict): contains the aforementioned stochastic indicators under
        keys 'K' and 'D'.
    """
    high, low, close = input_df["High"], input_df["Low"], input_df["Close"]
    rng = high - low

    # RSV undefined when range==0 -> NaN, then forward-fill (causal)
    rsv = ((close - low) / rng * 100).where(rng.ne(0)).ffill()

    # K_t = (1/3) * RSV_t + (2/3) * K_{t-1}
    K = rsv.ewm(alpha=1 / 3, adjust=False).mean()
    # D is the same smoothing over K
    D = K.ewm(alpha=1 / 3, adjust=False).mean()

    # keep values in-bounds (protect against tiny float drift)
    K = K.clip(0, 100)
    D = D.clip(0, 100)

    return {"K": K, "D": D}


def DIFFDEAMACD(input_df):
    """
    Calculates the difference between the twelve and twenty-six period
    exponential moving averages (DIFF), the signal line DEA, and the moving
    average convergence divergence MACD.

    Args:
        input_df (dataframe): contains the closign stock price in column
            'Close'

    Returns:
        DIFFDEAMACDdic (dict): contains the aforementioned technical indicators
        under the respective 'DIFF', 'DEA' and 'MACD' keys
    """
    EMA12 = input_df["Close"].ewm(span=12, min_periods=12).mean()
    EMA26 = input_df["Close"].ewm(span=26, min_periods=26).mean()
    DIFF = EMA12 - EMA26
    DEA = DIFF.ewm(span=9, min_periods=9).mean()

    MACD = DEA.shift() * 0.8 + DIFF * 0.2

    DIFFDEAMACDdic = {"DIFF": DIFF, "DEA": DEA, "MACD": MACD}
    return DIFFDEAMACDdic


def DIFavg(input_df):
    """
    Calculates the aggregated relative value of all the positive quantitative
    differences between subsequent observations of the opening stock price and
    that of all the negative ones.

    Args:
        input_df (dataframe): contains the opening stock price in column
            'Open'.
    Returns:
        UPDW (dict): contains the value of the positive variations under key
        'UP' and that of the negative under 'DW'.
    """
    UP = (input_df.Open.diff() / input_df.Open.shift()).clip(lower=0)
    DW = abs((input_df.Open.diff() / input_df.Open.shift()).clip(upper=0))

    UPDW = {"UP": UP, "DW": DW}
    return UPDW


def ReStIn(input_df):
    """
    Calculates the relative strength index with nine and fourteen periods.

    Args:
        input_df (dataframe): dataframe containing the opening
            stock price in column 'Open' (see :func: DIFavg).

    Returns:
        RSIdic (dict): contains the RSI for nine periods
        under key 'RSI1' and that of fourteen under 'RSI2'.
    """
    updw = DIFavg(input_df)

    upsmavg9 = updw["UP"].rolling(9).mean()
    dwsmavg9 = updw["DW"].rolling(9).mean()
    upsmavg14 = updw["UP"].rolling(14).mean()
    dwsmavg14 = updw["DW"].rolling(14).mean()

    RSI9 = 100 - 100 / (1 + upsmavg9 / dwsmavg9)
    RSI14 = 100 - 100 / (1 + upsmavg14 / dwsmavg14)

    RSIdic = {"RSI1": RSI9, "RSI2": RSI14}
    return RSIdic


def WiR(input_df):
    """
    Calculates the William's indicator for six periods and for ten.

    Args:
        input_df (dataframe): contains the closing, lowest and highest stock
            price series in columns 'Close', 'Low' and 'High'.

    Returns:
        WRdic (dict): contains the William's indicator
        for six periods under the key 'WR1' and that for ten
        under 'WR2'.
    """
    high = input_df["High"]
    low = input_df["Low"]
    close = input_df["Close"]

    hh6 = high.rolling(6, min_periods=6).max()
    ll6 = low.rolling(6, min_periods=6).min()
    hh10 = high.rolling(10, min_periods=10).max()
    ll10 = low.rolling(10, min_periods=10).min()

    den6, den10 = hh6 - ll6, hh10 - ll10
    wr6 = (hh6 - close) * 100 / den6
    wr10 = (hh10 - close) * 100 / den10

    # zero-range -> undefined -> NaN, then forward-fill (causal)
    wr6 = wr6.mask(den6.eq(0)).ffill()
    wr10 = wr10.mask(den10.eq(0)).ffill()

    return {"WR1": wr6, "WR2": wr10}


def CoChIn(input_df):
    """
    Calculates the commodity channel index with seven and fourteen periods.

    Args:
        input_df (dataframe): contains the closing, lowest and highest stock
            price in columns 'Close', 'Low' and 'High' respectively.

    Returns:
        CCIdic (dict): contains the commodity channel index
        for seven periods under the key 'CCI1' and for fourteen
        under 'CCI2'.
    """
    M = (input_df.High + input_df.Low + input_df.Close) / 3

    SM7 = M.rolling(7).mean()
    SM14 = M.rolling(14).mean()

    D7 = (M - SM7).abs().rolling(7).mean()
    D14 = (M - SM14).abs().rolling(14).mean()

    CCI7 = (M - SM7) / (0.015 * D7)
    CCI14 = (M - SM14) / (0.015 * D14)

    CCIdic = {"CCI1": CCI7, "CCI2": CCI14}
    return CCIdic


def total_dic_func(single, average=None, drop=True):
    """
    Builds a dataframe joining the data from the query (opening, closing,
    highest, lowest price and volume of stock) with the indicators calculated
    with the functions defined above (see :func: RSVKD, DIFFDEAMACD, ReStIn,
    WiR, CoChIn), a second such dataframe is built with the data and indicators
    relative to the industry-wide averages.

    Args:
        single (dataframe): containing the preprocessed query data for the
            requested company.
        average (dataframe, optional): containing the preprocessed average data
            obtained from the query data ran for each company in the requested
            industry.

    Returns:
        DF1 (dataframe): contains all data relative to the requested company
            that will be used to train, validate and test the models.
        DF2 (dataframe): contains all data relative to the requested industry
            that will be used to train, validate and test the models.
    """
    RSVKNDSNG = RSVKD(single)
    DIFFDEAMACDSNG = DIFFDEAMACD(single)
    RSISNG = ReStIn(single)
    WRSNG = WiR(single)
    CCISNG = CoChIn(single)

    DF1 = pd.DataFrame(
        {
            "Open": single["Open"],
            "High": single["High"],
            "Low": single["Low"],
            "Close": single["Close"],
            "Volume": single["Volume"],
            "Labels": labeler(single),
            "MA1": MA_func(single, 1),
            "MA2": MA_func(single, 2),
            "MA3": MA_func(single, 3),
            "MA4": MA_func(single, 4),
            "K": RSVKNDSNG["K"],
            "D": RSVKNDSNG["D"],
            "DIFF": DIFFDEAMACDSNG["DIFF"],
            "DEA": DIFFDEAMACDSNG["DEA"],
            "MACD": DIFFDEAMACDSNG["MACD"],
            "RSI1": RSISNG["RSI1"],
            "RSI2": RSISNG["RSI2"],
            "WR1": WRSNG["WR1"],
            "WR2": WRSNG["WR2"],
            "CCI1": CCISNG["CCI1"],
            "CCI2": CCISNG["CCI2"],
        }
    )

    if average is not None:
        RSVKNDMEAN = RSVKD(average)
        DIFFDEAMACDMEAN = DIFFDEAMACD(average)
        RSIMEAN = ReStIn(average)
        WRMEAN = WiR(average)
        CCIMEAN = CoChIn(average)

        DF2 = pd.DataFrame(
            {
                "Open_AVG": average["Open"],
                "High_AVG": average["High"],
                "Low_AVG": average["Low"],
                "Close_AVG": average["Close"],
                "Volume_AVG": average["Volume"],
                "MA1_AVG": MA_func(average, 1),
                "MA2_AVG": MA_func(average, 2),
                "MA3_AVG": MA_func(average, 3),
                "MA4_AVG": MA_func(average, 4),
                "K_AVG": RSVKNDMEAN["K"],
                "D_AVG": RSVKNDMEAN["D"],
                "DIFF_AVG": DIFFDEAMACDMEAN["DIFF"],
                "DEA_AVG": DIFFDEAMACDMEAN["DEA"],
                "MACD_AVG": DIFFDEAMACDMEAN["MACD"],
                "RSI1_AVG": RSIMEAN["RSI1"],
                "RSI2_AVG": RSIMEAN["RSI2"],
                "WR1_AVG": WRMEAN["WR1"],
                "WR2_AVG": WRMEAN["WR2"],
                "CCI1_AVG": CCIMEAN["CCI1"],
                "CCI2_AVG": CCIMEAN["CCI2"],
            }
        )
        if drop:
            return DF1.dropna(), DF2.dropna()
        else:
            return DF1, DF2

    if drop:
        return DF1.dropna()
    else:
        return DF1


def PCA_func(input_df, default_components, cutoff_var, scaler=None):
    """
    Performs a principal component analysis in order to reduce the dimension of
    the dataset of industry-wide average values for the requested variables.

    Args:
        input_df (dataframe): contains the relevant data panel.
        default_components (float): number of principal components the analysis
            extracts.
        cutoff_var (float): significance criterion to decide which principal
            components must be kept after the reduction.

    Returns:
        Dataframe of the principal components that comply with the selection
            criterion.
        pcatest (PCA): object generated by the scikit-learn function containing
            all the principal components the analysis produces.
        pcadef (PCA): object generated by the scikit-learn function containing
            all the principal components that comply with the selection
            criterion.
        scaler (function): If specified, the provided scaler will be used to
            transform the data. If not specified, a StandardScaler will be used
            to train and transform the data.
    """
    pcatest_vars = []
    pcadef_cols = []
    if default_components == 0:
        default_components = None

        pcatest = PCA(default_components)
        if scaler is not None:
            pcatest.fit_transform(scaler.transform(input_df))
        else:
            pcatest.fit_transform(StandardScaler().fit_transform(input_df))

        optimal_components = 0
        for ii in range(0, pcatest.n_components_):
            pcatest_vars.append(pcatest.explained_variance_ratio_[ii])
        for ii in range(0, pcatest.n_components_):
            if pcatest_vars[ii] < cutoff_var:
                optimal_components = ii
                break
    else:
        optimal_components = default_components
        pcatest = None

    pcadef = PCA(optimal_components)
    if scaler is not None:
        pcadef_feat = pcadef.fit_transform(scaler.transform(input_df))
    else:
        pcadef_feat = pcadef.fit_transform(StandardScaler().fit_transform(input_df))

    for ii in range(0, optimal_components):
        pcadef_cols.append(f"Industry{ii + 1}")

    return (
        pd.DataFrame(pcadef_feat, index=input_df.index, columns=pcadef_cols),
        pcatest,
        pcadef,
    )

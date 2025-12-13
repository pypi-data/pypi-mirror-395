# -*- coding: utf-8 -*-
import sqlite3
from functools import partial
import datetime
import time
from pathlib import Path
import warnings

import pandas as pd
from tqdm import tqdm
from automar.core.preprocessing.stats import total_dic_func
from automar.core.preprocessing.extractor import (
    GICStoYF,
    ind_func,
    symbols_func,
    tick_func,
)

from automar.shared.persistence.library import (
    DATABASE_NAME,
    TABLE_NAME,
    check_dates,
    convert_datetime,
    DataKind,
    date_ender,
    gen_filter_company_smartcase,
    get_dirs,
    gen_filename,
    load,
    FinderSt,
    ValidFormats,
    Periods,
    read_df,
    write_df,
    load_sql,
)

# Indicator buffer configuration
# Technical indicators (especially MACD) require historical data to avoid NA values.
# MACD calculation chain:
#   - EMA26: 26 days (rows 0-25 are NA)
#   - DIFF = EMA12 - EMA26: 26 days (rows 0-25 are NA)
#   - DEA = DIFF.ewm(span=9, min_periods=9): needs 9 valid DIFF values (rows 0-33 are NA)
#   - MACD = DEA.shift() * 0.8 + DIFF * 0.2: shift adds 1 more NA (rows 0-34 are NA)
#   Total: 35 trading days lost
# We use 52 calendar days to ensure we get at least 35+ trading days (accounts for weekends/holidays)
# 35 trading days × (7 calendar days / 5 trading days) ≈ 49 days, rounded up to 52 for safety
INDICATOR_BUFFER_CALENDAR_DAYS = 52


def validate_inputs(ticker, industry, history, format):
    """Validate the inputs for ticker, industry, history, and format."""
    if not ticker and not industry:
        raise ValueError("Please input a valid ticker or industry name as a string.")

    if industry and industry not in GICStoYF:
        raise KeyError(
            f"Please input one of the following sectors as a string: {', '.join(GICStoYF.keys())}"
        )

    if history not in Periods:
        raise ValueError(
            f"Please input one of the following periods as a string: {', '.join(Periods)}"
        )

    if format not in ValidFormats:
        raise ValueError(
            f"Please input one of the following formats as a string: {', '.join(ValidFormats)}"
        )


def determine_industry(ticker, industry):
    """Determine the industry based on the ticker or provided industry and if
    the industry provided and the ticker industry are the same."""
    if industry is not None:
        return industry
    elif ticker is not None:
        return ind_func(ticker)
    else:
        raise ValueError("Industry cannot be determined from the provided inputs.")


def fetch_specific_companies(
    company_tickers, industry, history, skip, datend_act, datest=None, datend=None
):
    """
    Fetch data for a specific list of company tickers.

    DEPRECATED: This function is now a wrapper around UnifiedDataAcquisition
    for backward compatibility. New code should use UnifiedDataAcquisition directly.

    Args:
        company_tickers: List of ticker symbols to fetch
        industry: Industry name for metadata
        history: History period
        skip: Whether to skip companies with insufficient data
        datend_act: Actual end date
        datest: Start date (optional)
        datend: End date (optional)

    Returns:
        DataFrame with data for specified companies
    """
    from automar.shared.services.data_acquisition import (
        UnifiedDataAcquisition,
        DataAcquisitionRequest,
        AcquisitionMode,
    )
    from automar.shared.config.path_resolver import get_output_dir

    # Convert date parameters
    start_date = None
    end_date = None
    if datest:
        if isinstance(datest, str):
            start_date = convert_datetime(datest)
        else:
            start_date = datest
    if datend_act:
        if isinstance(datend_act, str):
            end_date = convert_datetime(datend_act)
        else:
            end_date = datend_act

    print(
        f"[INFO] Downloading {len(company_tickers)} missing companies: {company_tickers}"
    )

    # Create acquisition request
    request = DataAcquisitionRequest(
        mode=AcquisitionMode.MISSING_COMPANIES,
        industry=industry,
        companies=company_tickers,
        start_date=start_date,
        end_date=end_date,
        skip=skip,
        history=history,
    )

    # Execute acquisition with progress callback
    db_file = get_output_dir("data") / DATABASE_NAME
    acquisition = UnifiedDataAcquisition(
        db_file,
        progress_callback=lambda msg: print(f"  {msg}"),
    )

    result = acquisition.acquire(request)

    # Print summary compatible with old interface
    if result.success:
        if result.companies_downloaded:
            print(
                f"[INFO] Successfully downloaded {len(result.companies_downloaded)} companies "
                f"with {result.rows_added} new rows"
            )
        if result.companies_failed:
            print(
                f"[WARNING] Failed to download {len(result.companies_failed)} companies: "
                f"{', '.join(result.companies_failed)}"
            )

        # Return DataFrame by reading from database
        # This maintains backward compatibility with code expecting a DataFrame
        import sqlite3

        conn = sqlite3.connect(str(db_file))
        query = """
            SELECT * FROM data
            WHERE Company IN ({})
            AND Date >= ? AND Date <= ?
        """.format(
            ",".join(["?"] * len(company_tickers))
        )
        params = company_tickers + [
            start_date.isoformat() if start_date else None,
            end_date.isoformat() if end_date else None,
        ]
        df = pd.read_sql(query, conn, params=params)
        conn.close()
        return df
    else:
        print(f"[WARNING] No data downloaded: {result.error}")
        return pd.DataFrame()


def fetch_and_process_data(
    ticker, industry, history, skip, datend_act, datest=None, datend=None
):
    """Fetch data for the given ticker or industry and process it."""
    company_list = []

    if datest and datend:
        datest = convert_datetime(datest)
        datend = convert_datetime(datend)

    data_dic = symbols_func(
        ticker, history, ind_input=industry, skip=skip, datest=datest, datend=datend_act
    )

    ind_name = data_dic["name"]

    # Process each company's data
    for company_ticker, data in tqdm(
        data_dic["data"].items(), desc="Processing company histories"
    ):
        processed_data = total_dic_func(data, drop=False)
        processed_data["Date"] = processed_data.index.date
        processed_data["Company"] = company_ticker
        processed_data["Industry"] = ind_name
        company_list.append(processed_data)

    # Include specific ticker if not already in data_dic
    if ticker is not None and ticker not in data_dic["data"]:
        ticker_industry = ind_func(ticker)
        if (industry is not None) and (ticker_industry != industry):
            ticker_data = tick_func(ticker, history, datest=datest, datend=datend_act)
            processed_data = total_dic_func(ticker_data)
            processed_data["Date"] = processed_data.index.date
            processed_data["Company"] = ticker.upper()
            processed_data["Industry"] = ticker_industry
            company_list.append(processed_data)
            ind_name += f"({ticker})"

    # Concatenate all company data into a single DataFrame
    df = pd.concat(company_list, ignore_index=True)
    return df


def load_or_extract(
    datest=None,
    datend=None,
    ticker=None,
    industry=None,
    history="10y",
    skip=True,
    dir_path=None,
    file_path=None,
    format="feather",
    ensure_combined_dataset=False,
):
    """Load data for the given ticker or industry, extracting it if necessary.

    Files are automatically saved when newly extracted. If a file already exists,
    it is loaded and returned without re-saving."""

    # Validate inputs
    validate_inputs(ticker, industry, history, format)

    # Validate that we have either history OR both datest and datend
    if not history and not (datest and datend):
        raise ValueError(
            "Please specify either 'history' period OR both 'datest' and 'datend'."
        )

    # Store original requested start date for filtering later
    datest_original = None

    if datest and datend:
        # Both dates provided - validate them
        datest = date_ender(datest)  # Returns string in 'YYYY-MM-DD' format
        check_dates(datest, datend)

        # Apply buffer for technical indicators
        # This ensures that technical indicators (especially MACD which needs 34 trading days)
        # have enough historical data and don't produce NAs at the requested start date
        datest_original = datest  # Store user's requested start date (string)

        # Convert to datetime, apply buffer, convert back to string
        datest_dt = convert_datetime(datest)
        datest_with_buffer_dt = datest_dt - datetime.timedelta(
            days=INDICATOR_BUFFER_CALENDAR_DAYS
        )
        datest_with_buffer = datest_with_buffer_dt.strftime("%Y-%m-%d")

        print(
            f"[INFO] Applying {INDICATOR_BUFFER_CALENDAR_DAYS}-day buffer for technical indicators"
        )
        print(f"[INFO] Downloading data from {datest_with_buffer} (buffer) to {datend}")
        print(
            f"[INFO] Final dataset will contain {datest_original} onwards (as requested)"
        )

        datest = datest_with_buffer  # Use buffered date for downloading
    elif history:
        # History provided - check for conflicting parameters
        if datest:
            raise ValueError(
                "Please input either 'history' or 'datest' and 'datend', but not both methods to define the range of data to extract."
            )
        # When using history, datend can be any date (including today)
        # The actual end date will be determined by what data is available

    datend, datend_actual = date_ender(datend, end=True)

    # Resolve industry when users provide only a ticker.
    # SQLite lookups need the industry upfront to evaluate coverage
    # and naming logic also expects a concrete value.
    resolved_industry = industry
    if resolved_industry is None and ticker:
        try:
            resolved_industry = determine_industry(ticker, resolved_industry)
        except Exception as exc:  # pragma: no cover - surfaced to API/CLI
            raise ValueError(
                f"Could not determine industry for ticker '{ticker}': {exc}"
            ) from exc
    industry = resolved_industry

    if file_path and (file_format := file_path.suffix.lstrip(".")):
        if file_format in ValidFormats:
            format = file_format

    if file_path is not None and format == ValidFormats.SQLITE:
        file_path = Path(file_path)
        if not file_path.suffix:
            file_path = file_path.with_suffix("." + format)
        elif file_path.suffix.lstrip(".") not in ValidFormats:
            raise ValueError(
                f"Wrong file format, please use one of these: {', '.join(ValidFormats)}"
            )
        if file_path.exists():
            df = read_df(file_path)
            ignored_args = []

            if ticker is not None:
                ignored_args.append("ticker")
            if industry is not None:
                ignored_args.append("industry")
            if ignored_args:
                warnings.warn(
                    f"""File loaded from inputted path, the following
                    arguments have been ignored: {', '.join(ignored_args)}."""
                )
            df.attrs["file_path"] = str(file_path)
            return df, FinderSt.SUCCESS
        else:
            if (ticker is not None) or (industry is not None):
                warnings.warn(
                    f"""No file was found in the provided path. 
                              Data retrieval will be attempted using the other arguments."""
                )
            else:
                raise ValueError(
                    "No file was found in the provided path, please review it."
                )

    # Try loading the file
    if format == ValidFormats.SQLITE:
        if file_path is None:
            from automar.shared.persistence.library import DEFAULT_TREE

            file_path = (
                get_dirs(root=None, create_dirs=True, end=dir_path or DEFAULT_TREE)
                / DATABASE_NAME
            )
        df, status, load_joined = load_sql(
            db_path=file_path,
            date=datend,
            datest=datest,
            datend=datend,
            ticker=ticker,
            industry=industry,
            history=history,
            dir_path=dir_path,
            ensure_combined_dataset=ensure_combined_dataset,
            skip=skip,
        )
    else:
        df, status, load_joined = load(
            date=datend,
            datest=datest,
            ticker=ticker,
            industry=industry,
            history=history,
            dir_path=dir_path,
            ensure_combined_dataset=ensure_combined_dataset,
        )

    data_changed = ensure_combined_dataset and load_joined

    # Handle find status
    # Keep track of original status for return value
    original_status = status

    fetch_fn = partial(
        fetch_and_process_data,
        skip=skip,
        history=history,
        datest=datest,
        datend=datend,
        datend_act=datend_actual,
    )

    match status:
        case FinderSt.INCOMPLETE:
            # Download only missing companies
            gap_info = df.attrs.get("gap_info", {})
            missing_companies = gap_info.get("missing_companies", [])

            if missing_companies:
                print(
                    f"[INFO] Downloading {len(missing_companies)} missing S&P 500 companies"
                )
                missing_df = fetch_specific_companies(
                    missing_companies,
                    industry,
                    history,
                    skip,
                    datend_actual,
                    datest,
                    datend,
                )
                if not missing_df.empty:
                    df = pd.concat([df, missing_df], axis=0)
                    data_changed = True
                else:
                    print(
                        "[WARNING] Failed to download missing companies - no new data acquired"
                    )
            else:
                print("[WARNING] INCOMPLETE status but no gap_info found")

        case FinderSt.MISSING_ALL | FinderSt.MISSING_INDUSTRY:
            # Extract data and then read it
            df = fetch_fn(ticker=ticker, industry=industry)
            data_changed = True
        case FinderSt.MISSING_INDUSTRY_TO_JOIN:
            # Download only missing companies from the industry, not the entire sector
            gap_info = df.attrs.get("gap_info", {}) if df is not None else {}
            missing_companies = gap_info.get("missing_companies", [])

            if missing_companies:
                print(
                    f"[INFO] Downloading {len(missing_companies)} missing companies from {industry} sector"
                )
                missing_df = fetch_specific_companies(
                    missing_companies,
                    industry,
                    history,
                    skip,
                    datend_actual,
                    datest,
                    datend,
                )
                if not missing_df.empty:
                    if df is not None:
                        df = pd.concat([df, missing_df], axis=0)
                    else:
                        df = missing_df
                    data_changed = True
                else:
                    print("[WARNING] Failed to download missing companies")
            else:
                # No gap info available - fall back to old behavior as safety net
                print(
                    "[WARNING] MISSING_INDUSTRY_TO_JOIN but no gap_info - using fallback"
                )
                df_ind = fetch_fn(ticker=None, industry=industry)
                ticker_exists = (
                    df is not None and gen_filter_company_smartcase(df, ticker).any()
                )
                if ticker_exists:
                    # Always combine ticker with industry when both are requested
                    # The ticker data must be preserved even if ensure_combined_dataset=False
                    df = pd.concat([df_ind, df], axis=0)
                    data_changed = True
                else:
                    df = pd.concat([df_ind, df], axis=0)
                    data_changed = True
        case FinderSt.MISSING_TICKER:
            # Download ONLY the single ticker, not its entire industry
            # This handles: user requested specific industry + ticker from different industry
            from automar.core.preprocessing.stats import total_dic_func
            from automar.core.preprocessing.extractor import tick_func, ind_func

            ticker_data = tick_func(
                ticker, history, datest=datest, datend=datend_actual
            )
            processed_data = total_dic_func(ticker_data, drop=False)
            processed_data["Date"] = processed_data.index.date
            processed_data["Company"] = ticker.upper()
            processed_data["Industry"] = ind_func(ticker)
            df = pd.concat([df, processed_data], axis=0, ignore_index=True)
            data_changed = True
        case FinderSt.SUCCESS:
            if not skip:
                # Force re-extraction even if file exists (skip=False)
                df = fetch_fn(ticker=ticker, industry=industry)
                data_changed = True
            elif not data_changed:
                # File already exists and was successfully loaded with requested context
                from automar.shared.persistence.library import DEFAULT_TREE

                if file_path is None:
                    if format == "sqlite":
                        file_path = (
                            get_dirs(
                                root=None,
                                create_dirs=False,
                                end=dir_path or DEFAULT_TREE,
                            )
                            / DATABASE_NAME
                        )
                    else:
                        # Reconstruct filename based on loaded data
                        industry_for_filename = industry
                        if industry_for_filename is None:
                            industry_for_filename = df[
                                gen_filter_company_smartcase(df, ticker)
                            ]["Industry"].iloc[0]

                        ticker_for_filename = ticker
                        if df["Industry"].nunique() == 1:
                            # Single industry in file - don't include ticker in filename
                            ticker_for_filename = None

                        datest_for_filename = None
                        if datest:
                            datest_for_filename = df["Date"].min().strftime("%Y-%m-%d")

                        file_path = get_dirs(
                            root=None, create_dirs=False, end=dir_path or DEFAULT_TREE
                        ) / gen_filename(
                            industry=industry_for_filename,
                            history=history,
                            date=df["Date"].max().strftime("%Y-%m-%d"),
                            kind=DataKind.DATA,
                            datest=datest_for_filename,
                            ticker=ticker_for_filename,
                            format=format,
                        )

                df.attrs["file_path"] = str(file_path)
                return df, FinderSt.SUCCESS

    if df is None:
        # Unreachable
        raise ValueError("Dataframe not generated. Something went terribly wrong.")

    # Filter to originally requested date range if buffer was applied
    # This removes the buffer period used for technical indicator calculation,
    # ensuring the final dataset contains only the requested date range
    if datest_original is not None:
        # Convert Date column to datetime for comparison if needed
        if df["Date"].dtype == object:
            df["Date"] = pd.to_datetime(df["Date"])

        rows_before = len(df)
        df = df[df["Date"] >= pd.Timestamp(datest_original)].copy()
        rows_after = len(df)

        # Reset index so it starts from 0 (not from the buffer offset)
        df = df.reset_index(drop=True)

        print(f"[INFO] Filtered to requested date range: {datest_original} onwards")
        print(
            f"[INFO] Removed {rows_before - rows_after} buffer rows (kept {rows_after} rows)"
        )

    # Store original ticker for filename generation
    ticker_for_filename = ticker

    if industry is None:
        industry = df[gen_filter_company_smartcase(df, ticker)]["Industry"].iloc[0]

    # Determine if ticker should be included in filename:
    # - Include ticker ONLY if dataframe contains multiple industries (ticker from different industry was merged)
    # - Exclude ticker if dataframe contains only one industry (standard industry download)
    # This logic ensures:
    #   - "data_Communication_Services_3y.feather" when user requests TTWO (belongs to Communication Services)
    #   - "data_Communication_Services(BALL)_3y.feather" when user requests BALL from Financials + Communication Services industry
    if df["Industry"].nunique() == 1:
        # Dataframe contains only one industry - don't include ticker in filename
        ticker_for_filename = None
    # If df has multiple industries, keep ticker_for_filename to indicate which ticker triggered the download

    if file_path is None:
        from automar.shared.persistence.library import DEFAULT_TREE

        if format == "sqlite":
            file_path = (
                get_dirs(root=None, create_dirs=True, end=dir_path or DEFAULT_TREE)
                / DATABASE_NAME
            )
        else:
            # Use original requested date for filename (not the buffered date)
            datest_for_filename = None
            if datest_original:
                datest_for_filename = (
                    datest_original  # Already a string in 'YYYY-MM-DD' format
                )
            elif datest:
                datest_for_filename = df["Date"].min().strftime("%Y-%m-%d")

            file_path = get_dirs(
                root=None, create_dirs=True, end=dir_path or DEFAULT_TREE
            ) / gen_filename(
                industry=industry,
                history=history,
                date=df["Date"].max().strftime("%Y-%m-%d"),
                kind=DataKind.DATA,
                datest=datest_for_filename,
                ticker=ticker_for_filename,
                format=format,
            )

    from pathlib import Path

    if not isinstance(file_path, Path):
        file_path = Path(file_path)

    should_write = data_changed or not file_path.exists()

    if should_write:
        # Force overwrite if skip=False (force re-download mode)
        actually_wrote = write_df(df, file_path, force_overwrite=not skip)
        # Only print "File saved" if data was actually written (not skipped duplicates)
        if actually_wrote is not False:  # True or None (for non-SQLite formats)
            print(f"File saved as: {file_path}")

    # Store file path in dataframe metadata for later retrieval
    df.attrs["file_path"] = str(file_path)

    # Return tuple (df, status) - status indicates what was found before extraction
    return df, original_status

# -*- coding: utf-8 -*-
import datetime
from enum import auto, Enum, StrEnum
from pathlib import Path

DATABASE_NAME = "data.sqlite"
TABLE_NAME = "data"
DEFAULT_TREE = Path("out/data")
VALID_INDUSTRY = (
    "Materials",
    "Industrials",
    "Financials",
    "Energy",
    "Consumer Discretionary",
    "Information Technology",
    "Communication Services",
    "Real Estate",
    "Health Care",
    "Consumer Staples",
    "Utilities",
)


class ValidFormats(StrEnum):
    PKL = auto()
    CSV = auto()
    PARQUET = auto()
    FEATHER = auto()
    XLSX = auto()
    SQLITE = auto()


class Periods(StrEnum):
    Y1 = "1y"
    Y2 = "2y"
    Y3 = "3y"
    Y4 = "4y"
    Y5 = "5y"
    Y6 = "6y"
    Y7 = "7y"
    Y8 = "8y"
    Y9 = "9y"
    Y10 = "10y"


class DataKind(StrEnum):
    DATA = "data"
    PCA = "pca"


class FinderSt(Enum):
    """Status codes for data finder operations."""

    SUCCESS = 0
    MISSING_TICKER = 1
    MISSING_INDUSTRY = 2
    MISSING_INDUSTRY_TO_JOIN = 3
    MISSING_ALL = 4
    # Consolidated: INCOMPLETE_COMPANIES, INCOMPLETE_DATES, INCOMPLETE_BOTH -> INCOMPLETE
    # Use GapAnalyzer for detailed gap analysis instead
    INCOMPLETE = 5  # Data exists but is incomplete (companies or dates)


class DiscontinuousDataError(Exception):
    """
    Raised when SQLite data contains significant gaps (5+ consecutive trading days)
    in the requested date range.

    This prevents model training/analysis on incomplete data that would produce
    misleading results due to missing date ranges.
    """

    def __init__(self, gap_info):
        self.gap_info = gap_info

        # Build user-friendly message with details about affected companies
        companies_affected = gap_info["companies_with_gaps"]
        total_companies = gap_info["total_companies"]
        start_date, end_date = gap_info["requested_range"]

        # Show up to 3 companies with their gaps
        company_details = []
        for company, details in list(companies_affected.items())[:3]:
            gaps_str = ", ".join(
                [
                    f"{g['start']} to {g['end']} ({g['trading_days_missing']} days)"
                    for g in details["gaps"]
                ]
            )
            company_details.append(
                f"  • {company}: {gaps_str} [Coverage: {details['coverage_pct']:.1f}%]"
            )

        if len(companies_affected) > 3:
            company_details.append(
                f"  • ... and {len(companies_affected) - 3} more companies"
            )

        companies_str = "\n".join(company_details)

        message = f"""
Discontinuous data detected in SQLite database for date range {start_date} to {end_date}.

{len(companies_affected)} out of {total_companies} companies have significant gaps (5+ consecutive trading days missing):

{companies_str}

This usually happens when you downloaded separate date ranges with gaps between them.
For example: downloading Jan-March, then separately downloading June-Dec, leaving April-May empty.

Solutions:
1. Adjust your date range to avoid the gap(s) - select only continuous periods
2. Use the Extract tab with "Force re-download" checkbox to rebuild the data as continuous
3. Download the missing date ranges using the Extract tab to fill the gaps

Note: Training models or running analysis on discontinuous data would produce unreliable results.
"""
        super().__init__(message)


def find_continuous_gaps(missing_days, expected_trading_days):
    """
    Group consecutive missing trading days into continuous gap ranges.

    Args:
        missing_days: DatetimeIndex of missing trading days
        expected_trading_days: DatetimeIndex of all expected trading days

    Returns:
        list: List of tuples (gap_start, gap_end) for each continuous gap
    """
    if len(missing_days) == 0:
        return []

    gaps = []
    gap_start = missing_days[0]
    prev_day = missing_days[0]

    for day in missing_days[1:]:
        # Check if this day is the next expected trading day after prev_day
        try:
            prev_index = expected_trading_days.get_loc(prev_day)
            current_index = expected_trading_days.get_loc(day)

            # If indices are NOT consecutive, we have a new gap
            if current_index != prev_index + 1:
                gaps.append((gap_start, prev_day))
                gap_start = day
        except KeyError:
            # Day not in expected_trading_days, skip
            pass

        prev_day = day

    # Add the last gap
    gaps.append((gap_start, prev_day))

    return gaps


def detect_date_gaps_per_company(df, start_date, end_date, gap_threshold_days=5):
    """
    Detect significant gaps (5+ consecutive trading days) in data for EACH company.

    This ensures we catch gaps even when only one company has them, preventing
    silent date range adjustments that could mislead users about data continuity.

    Args:
        df: DataFrame with 'Date' and 'Company' columns
        start_date: Start of requested range (str in ISO format or datetime)
        end_date: End of requested range (str in ISO format or datetime)
        gap_threshold_days: Number of consecutive missing trading days to flag as significant (default: 5)

    Returns:
        tuple: (has_gaps: bool, gap_details: dict or None)
            - has_gaps: True if any company has gaps >= threshold
            - gap_details: Dictionary with detailed gap information per company
    """
    import pandas as pd
    import pandas_market_calendars as mcal

    # Get NYSE calendar
    nsq = mcal.get_calendar("NYSE")
    nsq_holidays = nsq.holidays().holidays

    # Generate expected trading days for the requested range
    start_ts = pd.Timestamp(start_date)
    end_ts = pd.Timestamp(end_date)

    filtered_holidays = [
        hd for hd in nsq_holidays if start_ts <= pd.Timestamp(hd) <= end_ts
    ]

    expected_trading_days = pd.date_range(start=start_ts, end=end_ts, freq="B").drop(
        filtered_holidays
    )

    # Check EACH company individually for gaps
    companies_with_gaps = {}

    for company in df["Company"].unique():
        company_df = df[df["Company"] == company]
        company_dates = pd.to_datetime(company_df["Date"]).unique()
        company_dates = pd.DatetimeIndex(company_dates).sort_values()

        if len(company_dates) == 0:
            continue  # No data for this company

        # CRITICAL: Only check for gaps WITHIN the company's actual date range
        # This prevents false positives for companies that:
        # - Weren't publicly traded during the full requested range (IPOs, spinoffs)
        # - Joined/left the sector during the period
        # - Have legitimately shorter trading histories
        #
        # We only care about gaps WITHIN their trading period, not before/after
        company_start = company_dates.min()
        company_end = company_dates.max()

        # Filter expected trading days to only the range where this company actually trades
        company_expected_days = expected_trading_days[
            (expected_trading_days >= company_start)
            & (expected_trading_days <= company_end)
        ]

        # Find missing trading days WITHIN this company's actual trading period
        missing_days = company_expected_days[~company_expected_days.isin(company_dates)]

        if len(missing_days) == 0:
            continue  # Company has complete data within its trading period

        # Find continuous gap ranges for this company
        gaps = find_continuous_gaps(missing_days, company_expected_days)

        # Check if any gaps exceed the threshold (5+ consecutive trading days)
        significant_gaps = []
        for gap_start, gap_end in gaps:
            gap_length = len(
                expected_trading_days[
                    (expected_trading_days >= gap_start)
                    & (expected_trading_days <= gap_end)
                ]
            )

            if gap_length >= gap_threshold_days:
                significant_gaps.append(
                    {
                        "start": gap_start.date(),
                        "end": gap_end.date(),
                        "trading_days_missing": gap_length,
                    }
                )

        if significant_gaps:
            companies_with_gaps[company] = {
                "gaps": significant_gaps,
                "total_missing": len(missing_days),
                "coverage_pct": (len(company_dates) / len(expected_trading_days)) * 100,
            }

    has_gaps = len(companies_with_gaps) > 0

    gap_info = {
        "companies_with_gaps": companies_with_gaps,
        "total_companies_affected": len(companies_with_gaps),
        "total_companies": df["Company"].nunique(),
        "requested_range": (str(start_date), str(end_date)),
        "expected_trading_days": len(expected_trading_days),
    }

    return has_gaps, gap_info


def get_dirs(root=None, create_dirs=False, end=DEFAULT_TREE):
    if root is None:
        from automar.shared.config.path_resolver import get_project_root

        root = get_project_root()
    else:
        Path(root)

    folder = root / end
    if create_dirs:
        folder.mkdir(exist_ok=True, parents=True)
    return folder


def get_datend_from_filename(filename):
    import re

    pattern = r"_(\d{4}-\d{2}-\d{2})\.(" + "|".join(ValidFormats) + r")$"
    match = re.search(pattern, filename)
    if match:
        try:
            return datetime.datetime.strptime(match.group(1), "%Y-%m-%d")
        except ValueError:
            return None
    return None


def sort_most_recent_dataset(dir_path, industry):
    dir_name = get_dirs(root=dir_path, create_dirs=False)
    if not dir_name.is_dir():
        return None

    glob_pattern = f"data_{ind_under_name(industry)}*"

    datasets = [
        (file_path, get_datend_from_filename(file_path.name))
        for file_path in dir_name.glob(glob_pattern)
        if file_path.suffix.lstrip(".").lower() in ValidFormats
    ]

    datasets = [(fp, dt) for fp, dt in datasets if dt is not None]
    sorted_datasets = sorted(datasets, key=lambda x: x[1], reverse=True)
    sorted_files = tuple(fp for fp, _ in sorted_datasets)

    return sorted_files if sorted_files else None


def write_df(df, path, force_overwrite=False):
    """
    Write DataFrame to various file formats.

    For SQLite databases, uses new transaction-safe implementation with:
    - PRIMARY KEY constraint enforcement
    - Transaction management
    - Proper connection handling
    - Data validation
    - Optional force overwrite for duplicate handling

    Args:
        df: DataFrame to write
        path: Output file path
        force_overwrite: If True, overwrite duplicates in SQLite (INSERT OR REPLACE)
                        If False, skip duplicates (INSERT OR IGNORE)

    Returns:
        For SQLite: bool (True if data written, False if all duplicates)
        For other formats: None
    """
    path = Path(path)
    match path.suffix:
        case ".csv":
            df.to_csv(path, index=True)
        case ".xlsx":
            df.to_excel(path, index=True)
        case ".parquet":
            df.to_parquet(path, index=True)
        case ".feather":
            df.to_feather(path, compression="zstd")
        case ".pkl":
            df.to_pickle(path)
        case ".sqlite3" | ".sqlite" | ".db":
            # Use new transaction-safe implementation
            from .database import write_df_safe

            result = write_df_safe(
                df, TABLE_NAME, path, validate=True, force_overwrite=force_overwrite
            )

            # Print status messages for backward compatibility
            if result.success:
                if result.rows_invalid > 0:
                    print(
                        f"[INFO] Removed {result.rows_invalid} invalid rows during validation"
                    )
                if result.rows_skipped > 0:
                    print(
                        f"[INFO] Skipped {result.rows_skipped} duplicate rows (already in database)"
                    )
                if result.rows_written > 0:
                    print(f"[INFO] Writing {result.rows_written} new rows to database")
                else:
                    total_input = (
                        result.rows_written + result.rows_skipped + result.rows_invalid
                    )
                    print(
                        f"[INFO] No new data to write (all {total_input} rows already exist or invalid)"
                    )

                return result.rows_written > 0  # True if data was written
            else:
                print(f"[ERROR] Failed to write to database: {result.error}")
                return False
        case _:
            raise ValueError(f"Unsupported file format: {path}")


def read_df(path):
    import pandas as pd

    path = Path(path)
    match path.suffix:
        case ".csv":
            return pd.read_csv(path)
        case ".xlsx":
            return pd.read_excel(path)
        case ".parquet":
            return pd.read_parquet(path)
        case ".feather":
            return pd.read_feather(path)
        case ".pkl":
            return pd.read_pickle(path)
        case ".sqlite3" | ".sqlite" | ".db":
            conn = create_connection(path)
            df = load_df_from_sqlite(TABLE_NAME, conn)
            conn.close()
            return df
        case _:
            raise ValueError(f"Unsupported file format: {path.suffix}")


def create_connection(db_file, mkfolder=True):
    """
    Create SQLite database connection.

    DEPRECATED: Use database.get_connection() context manager instead.
    This function is kept for backward compatibility but does not use
    context managers, so connections may leak if not explicitly closed.

    Args:
        db_file: Path to database file
        mkfolder: Create parent directories if they don't exist

    Returns:
        sqlite3.Connection (MUST be manually closed!)
    """
    import sqlite3

    if mkfolder:
        db_file.parent.mkdir(exist_ok=True, parents=True)

    conn = sqlite3.connect(str(db_file))

    # Apply basic optimizations
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")

    return conn


def load_df_from_sqlite(
    table_name,
    conn,
    comp_name=None,
    ind_name=None,
    start_date=None,
    end_date=None,
    validate_continuity=False,
):
    """
    Load data from SQLite database with filtering.

    Uses parameterized queries (SQL injection safe).

    Args:
        table_name: Name of table to query
        conn: Database connection
        comp_name: Filter by company ticker (optional)
        ind_name: Filter by industry (optional)
        start_date: Start date in ISO format (optional)
        end_date: End date in ISO format (optional)
        validate_continuity: If True, raises DiscontinuousDataError if significant gaps
                           (5+ consecutive trading days) exist in the requested date range.
                           This prevents training/analysis on incomplete data. (default: False)

    Returns:
        DataFrame or None if error/empty

    Raises:
        DiscontinuousDataError: If validate_continuity=True and significant gaps detected
    """
    import pandas as pd
    import sqlite3
    import warnings

    # Build parameterized query (SQL injection safe)
    query = f"SELECT * FROM {table_name}"  # Table name from constant
    params = []
    conditions = []

    # Company and Industry filtering
    # When both ticker and industry are provided, we want:
    # - The ticker's data (for the target)
    # - AND all other companies in that industry (for context)
    # This is the intended behavior for providing industry context
    if comp_name and ind_name:
        conditions.append("(Company = ? OR Industry = ?)")
        params.extend([comp_name, ind_name])
    elif comp_name:
        conditions.append("Company = ?")
        params.append(comp_name)
    elif ind_name:
        conditions.append("Industry = ?")
        params.append(ind_name)

    # Date range filtering
    # When both company and industry are provided with dates,
    # the dates should represent the intersection where both exist
    if start_date:
        conditions.append("Date >= ?")
        params.append(start_date)
    if end_date:
        conditions.append("Date <= ?")
        params.append(end_date)

    # Build WHERE clause if there are conditions
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    try:
        df = pd.read_sql_query(query, conn, params=params)

        # Validate data continuity BEFORE filtering (if requested)
        # This detects gaps in the RAW downloaded data, not gaps created by date overlap filtering
        # We check continuity before dropna() and date overlap filtering to avoid false positives
        if validate_continuity and start_date and end_date and not df.empty:
            # Check each company's data within its own date range (not the requested range)
            # This avoids false positives for companies with shorter trading histories (IPOs, etc.)
            has_gaps, gap_info = detect_date_gaps_per_company(
                df, start_date, end_date, gap_threshold_days=5
            )
            if has_gaps:
                raise DiscontinuousDataError(gap_info)

        # Additional filtering for multi-company datasets:
        # Ensure we only keep dates where ALL companies have data
        # This prevents NaN values during model training and distorted visualizations
        # Apply when: (1) both ticker+industry OR (2) industry-only with multiple companies
        should_filter_dates = False
        if df is not None and not df.empty and "Company" in df.columns:
            if comp_name and ind_name:
                # Case 1: Both ticker and industry specified
                should_filter_dates = True
            elif ind_name and not comp_name:
                # Case 2: Industry-only with multiple companies
                should_filter_dates = df["Company"].nunique() > 1

        if should_filter_dates:
            # Drop any rows with NaN values
            df = df.dropna()

            if not df.empty:
                # Get all unique companies in the result set (after dropping NaN rows)
                all_companies = df["Company"].unique()
                total_companies = len(all_companies)

                # For each date, count how many companies have complete data
                date_company_counts = df.groupby("Date")["Company"].nunique()

                # Only keep dates where ALL companies have observations
                complete_dates = date_company_counts[
                    date_company_counts == total_companies
                ].index

                if len(complete_dates) > 0:
                    df = df[df["Date"].isin(complete_dates)]
                else:
                    # No dates have complete data for all companies
                    return df.iloc[0:0]

        return df
    except (pd.errors.DatabaseError, sqlite3.Error, OSError) as e:
        # Comprehensive error handling:
        # - pd.errors.DatabaseError: Pandas database errors
        # - sqlite3.Error: All SQLite errors (IntegrityError, OperationalError, etc.)
        # - OSError: File system errors (permissions, disk space, etc.)
        warnings.warn(f"Database query failed: {e}")
        return None


def yfinance_interval_to_timedelta(interval):
    from dateutil.relativedelta import relativedelta

    if interval[-2:] == "mo":
        return relativedelta(months=int(interval[:-2]))
    elif interval[-1] == "y":
        return relativedelta(years=int(interval[:-1]))


def yfinance_date_ranger(period):
    import time

    end = int(time.time())
    start = datetime.date.fromtimestamp(end)
    start -= yfinance_interval_to_timedelta(period)
    start -= datetime.timedelta(days=4)
    return start.strftime("%Y-%m-%d")


def datadict_to_df(data_dict):
    import pandas as pd

    ind_name = data_dict["name"]
    for k, v in data_dict["data"].items():
        v["Industry"] = ind_name
        v["Company"] = k
    return pd.concat(list(data_dict.values()))


def df_to_datadict(df):
    gs = df.groupby("Company")
    return {g: d.drop(columns=["Company"]) for g, d in gs}


def gen_filter_df_smartcase(df, query, column):
    return df[column].apply(lambda s: s.lower()) == query.lower()


def gen_filter_company_smartcase(df, company):
    return gen_filter_df_smartcase(df, company, "Company")


def ind_under_name(industry):
    if industry is not None:
        return industry.replace(" ", "_")


def find_ticker(dir, ticker, history, date, datest=None):
    if datest:
        file_wc_fast = frozenset(dir.glob(f"data_*({ticker})_{datest}_{date}.*"))
        file_wc = frozenset(dir.glob(f"data_*_{datest}_{date}.*"))
    else:
        file_wc_fast = frozenset(dir.glob(f"data_*({ticker})_{history}_{date}.*"))
        file_wc = frozenset(dir.glob(f"data_*_{history}_{date}.*"))

    iter = file_wc.difference(file_wc_fast)

    stems = []
    for path in file_wc_fast.union(iter):
        if path.suffix[1:] not in ValidFormats:
            continue
        if path.stem in stems:
            continue
        df = read_df(path)
        rows = gen_filter_company_smartcase(df, ticker)
        if rows.any():
            return df[rows]
        stems.append(path.stem)
    return None


def find_ticker_industry(dir, ticker, history, date, datest=None):
    if datest:
        file_wc = f"data_*_{datest}_{date}.*"
    else:
        file_wc = f"data_*_{history}_{date}.*"
    # Remove the token "None" in case there is no industry
    stems = []
    for path in dir.glob(file_wc):

        if path.suffix[1:] not in ValidFormats:
            continue
        if path.stem in stems:
            continue
        if f"({ticker.upper()})" in path.name:
            continue
        df = read_df(path)
        rows = gen_filter_company_smartcase(df, ticker)
        if rows.any():
            return df[df["Industry"] == df[rows].iloc[0]["Industry"]]
        stems.append(path.stem)

    return None


def find_industry_df(dir, industry, history, date, datest=None):
    ind_fold_name = ind_under_name(industry)

    if datest:
        file_path = f"data_{ind_fold_name}_{datest}_{date}.*"
    else:
        file_path = f"data_{ind_fold_name}_{history}_{date}.*"
    for path in dir.glob(file_path):
        if path.exists() and path.suffix[1:] in ValidFormats:
            return read_df(path)

    file_wc = f"data_{ind_fold_name}(*)_{history}_{date}.*"
    for path in dir.glob(file_wc):
        df = read_df(path)
        return df[df["Industry"] == industry]

    return None


def gen_filename(
    industry: str,
    history: str,
    date: str,
    datest=None,
    kind=DataKind.DATA,
    ticker=None,
    format=None,
):
    """
    Generate a standardized filename for data files.

    Args:
        industry: Industry name
        history: History period (e.g., "3y", "10y")
        date: End date string
        datest: Optional start date string
        kind: Data kind (e.g., DataKind.DATA)
        ticker: Optional ticker symbol - included ONLY if file contains multiple industries
        format: File format extension (e.g., "feather", "sqlite")

    Returns:
        Formatted filename string

    Note:
        The ticker parameter should be None when the file contains only one industry,
        and should be set when the file contains multiple industries to indicate
        which ticker triggered the download.
    """
    ind_name = ind_under_name(industry)
    if ticker is not None:
        ind_name += f"({ticker.upper()})"
    if datest:
        file_name = f"{ind_under_name(ind_name)}_{datest}_{date}"
    else:
        file_name = f"{ind_under_name(ind_name)}_{history}_{date}"
    if kind:
        file_name = f"{kind}_" + file_name
    if format is not None:
        file_name += f".{format}"
    return file_name


def load(
    date,
    datest=None,
    ticker=None,
    industry=None,
    history=Periods.Y10,
    dir_path=None,
    ensure_combined_dataset: bool = False,
):
    # Construct file path
    dir_path = get_dirs(root=dir_path, create_dirs=False)

    df = None
    status = FinderSt.MISSING_INDUSTRY
    needs_save = False
    match (industry, ticker):
        case (str(), str()):
            df = find_industry_df(dir_path, industry, history, date, datest)
            if df is None:
                df_tic = find_ticker(dir_path, ticker, history, date, datest)
                if df_tic is None:
                    status = FinderSt.MISSING_ALL
                else:
                    df = df_tic
                    status = FinderSt.MISSING_INDUSTRY_TO_JOIN
            elif not gen_filter_company_smartcase(df, ticker).any():
                df_ind = df
                df_tic = find_ticker(dir_path, ticker, history, date, datest)
                if df_tic is not None:
                    import pandas as pd

                    df = pd.concat([df_ind, df_tic], axis=0)
                    status = FinderSt.SUCCESS
                    needs_save = True
                else:
                    status = FinderSt.MISSING_TICKER
            else:
                ticker = None
                status = FinderSt.SUCCESS
                needs_save = False
        case (str(), None):
            df = find_industry_df(dir_path, industry, history, date, datest)
            if df is not None:
                status = FinderSt.SUCCESS
        case (None, str()):
            df = find_ticker_industry(dir_path, ticker, history, date, datest)
            if df is not None:
                status = FinderSt.SUCCESS
        case (None, None):
            raise ValueError(
                """\
                 Please input a valid string for ticker and/or industry
            """
            )

    return df, status, needs_save


def analyze_sqlite_gaps(
    db_path,
    industry,
    ticker,
    datest,
    datend,
    table_name=TABLE_NAME,
):
    """
    Analyze what's missing in the SQLite database for incremental updates.

    DEPRECATED: This function is a wrapper around the new GapAnalyzer class.
    For new code, use GapAnalyzer directly for more comprehensive analysis.

    Returns:
        dict with keys:
            - 'existing_companies': list of companies already in DB
            - 'missing_companies': list of S&P 500 companies not in DB
            - 'sp500_companies': list of all S&P 500 companies for this industry
            - 'date_range_db': (min_date, max_date) actually in DB
            - 'date_range_requested': (datest, datend) user requested
            - 'missing_dates': list of trading days missing from DB
            - 'needs_company_download': bool
            - 'needs_date_download': bool
    """
    from datetime import date as date_type
    from automar.shared.services.gap_analyzer import GapAnalyzer
    import pandas as pd

    # Convert date strings to date objects
    start_date = pd.to_datetime(datest).date() if datest else date_type.today()
    end_date = pd.to_datetime(datend).date() if datend else date_type.today()

    # Use new GapAnalyzer
    analyzer = GapAnalyzer(db_path)
    result = analyzer.analyze_industry(
        industry=industry,
        start_date=start_date,
        end_date=end_date,
        table_name=table_name,
    )

    # Convert GapAnalysisResult to old dict format for backward compatibility
    # Calculate missing_dates (only dates AFTER current max, not backfill gaps)
    missing_dates = []
    if result.actual_end is not None and result.needs_date_extension:
        # Get trading days from actual_end+1 to requested_end
        missing_dates = analyzer._get_trading_days(
            result.actual_end, result.requested_end
        )
        # Remove the first date (actual_end itself)
        if missing_dates and missing_dates[0] == result.actual_end:
            missing_dates = missing_dates[1:]

    return {
        "existing_companies": sorted(result.actual_companies),
        "missing_companies": result.missing_companies,
        "sp500_companies": result.sp500_companies,
        "date_range_db": (result.actual_start, result.actual_end),
        "date_range_requested": (datest, datend),
        "missing_dates": missing_dates,
        "needs_company_download": result.needs_company_download,
        "needs_date_download": result.needs_date_extension,
    }


def load_sql(
    db_path,
    date,
    ticker=None,
    industry=None,
    dir_path=None,
    history=None,
    datest=None,
    datend=None,
    table_name=TABLE_NAME,
    ensure_combined_dataset: bool = False,
    skip=True,
):
    import pandas as pd
    import requests
    from io import StringIO

    status = FinderSt.MISSING_ALL

    conn = create_connection(db_path)

    # Force re-download mode: bypass all gap analysis and force download
    if not skip:
        # When ticker is specified (with auto-detected or explicit industry), re-download everything
        # When only industry is specified, re-download the entire industry
        if ticker:
            status = FinderSt.MISSING_ALL  # Re-download ticker + entire industry
        elif industry:
            status = FinderSt.MISSING_INDUSTRY  # Re-download entire industry
        else:
            status = FinderSt.MISSING_ALL

        # Return empty df to trigger download in extraction_service
        return None, status, False

    # STEP 1: Check company presence WITHOUT date filtering
    # Load all data for the industry to verify all S&P 500 companies are present
    # This check must happen before date overlap filtering which may remove companies
    df_unfiltered = load_df_from_sqlite(
        table_name,
        conn,
        comp_name=ticker,
        ind_name=industry,
        start_date=None,  # No date filtering for company check
        end_date=None,
    )

    if df_unfiltered is not None and df_unfiltered.empty:
        df_unfiltered = None

    if df_unfiltered is not None and ticker and not industry:
        industry = df_unfiltered[df_unfiltered["Company"] == ticker][
            "Industry"
        ].unique()[0]

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

    spsymbols = set(sp500_table.loc[sp500_table["GICS Sector"] == industry]["Symbol"])

    # Check if all required S&P 500 companies are present in the database
    if ticker and industry:
        if df_unfiltered is not None:
            found_industry = industry in df_unfiltered["Industry"].values
            found_company = ticker in df_unfiltered["Company"].values
            if found_industry and found_company:
                unique_companies = df_unfiltered[df_unfiltered["Industry"] == industry][
                    "Company"
                ].unique()
                missing_companies = sorted(list(spsymbols - set(unique_companies)))
                if not missing_companies:
                    status = FinderSt.SUCCESS
                else:
                    status = FinderSt.MISSING_INDUSTRY_TO_JOIN
            elif found_industry and not found_company:
                status = FinderSt.MISSING_TICKER
            elif not found_industry and found_company:
                status = FinderSt.MISSING_INDUSTRY_TO_JOIN
                # Will need to fetch all companies for this industry
                missing_companies = sorted(list(spsymbols))
        else:
            status = FinderSt.MISSING_ALL

    elif not ticker and industry:
        if df_unfiltered is not None:
            unique_companies = df_unfiltered[df_unfiltered["Industry"] == industry][
                "Company"
            ].unique()

            missing_companies = sorted(list(spsymbols - set(unique_companies)))
            if missing_companies:
                status = FinderSt.INCOMPLETE
            else:
                status = FinderSt.SUCCESS
        else:
            status = FinderSt.MISSING_INDUSTRY

    # STEP 2: Load WITH date filtering for actual use and freshness check
    # This applies date overlap filtering to ensure all companies have aligned dates
    df = load_df_from_sqlite(
        table_name,
        conn,
        comp_name=ticker,
        ind_name=industry,
        start_date=datest,
        end_date=datend,
    )

    if df is None:
        return None, status, False

    if df.empty:
        return None, FinderSt.MISSING_ALL, False

    if history is not None:
        datest = yfinance_date_ranger(history)

    import pandas_market_calendars as mcal

    nsq = mcal.get_calendar("NYSE")
    nsq_holidays = nsq.holidays().holidays
    today = pd.Timestamp.today().date()

    # Use the actual date range from the filtered dataframe
    # This is important because date overlap filtering may have reduced the date range
    # to only include dates where all companies have data
    df_date = pd.to_datetime(df["Date"].copy())
    actual_start_date = df_date.min()
    actual_end_date = df_date.max()

    # Guard against empty results caused by upstream filtering
    if pd.isna(actual_start_date) or pd.isna(actual_end_date):
        return None, FinderSt.MISSING_ALL, False

    # Check for missing dates within the ACTUAL date range (not requested range)
    # This prevents false positives when date overlap filtering reduces the range
    filtered_nsq__holidays = [
        hd
        for hd in nsq_holidays
        if actual_start_date <= pd.Timestamp(hd) <= pd.Timestamp(date)
    ]
    trading_days = pd.date_range(
        start=actual_start_date, end=pd.Timestamp(date), freq="B"
    ).drop(filtered_nsq__holidays)

    missing_dates = trading_days[~trading_days.isin(df_date)]
    if str(today) in missing_dates:
        missing_dates = missing_dates[missing_dates != pd.Timestamp(str(today))]
    recent_missing_dates = [d for d in missing_dates if d >= trading_days[-5]]
    older_missing_dates = [d for d in missing_dates if d < trading_days[-5]]
    if len(recent_missing_dates) < 2 and len(older_missing_dates) < 5:
        pass
    else:
        if industry and ticker:
            status = FinderSt.MISSING_ALL
        elif industry and not ticker:
            status = FinderSt.MISSING_INDUSTRY
        elif not industry and ticker:
            status = FinderSt.MISSING_TICKER

    # Store gap information in dataframe attributes for extraction_service to use
    if (
        status in (FinderSt.INCOMPLETE, FinderSt.MISSING_INDUSTRY_TO_JOIN)
        and "missing_companies" in locals()
    ):
        df.attrs["gap_info"] = {"missing_companies": missing_companies}

    return df, status, False


def convert_datetime(date):
    if date:
        match date:
            case datetime.date():
                return date
            case str():
                return datetime.datetime.strptime(date, "%Y-%m-%d").date()
            case _:
                raise ValueError("Incorrect date type.")


def check_dates(datest, datend):
    d0 = convert_datetime(datest)
    d1 = convert_datetime(datend)
    dd = (d1 - d0).days
    if dd < 300:
        raise ValueError(
            f"""The period is too short, please
                         choose a wider time frame."""
        )


def date_ender(date, end=False):
    if date:
        import pandas_market_calendars as mcal

        today = convert_datetime(datetime.datetime.now().strftime("%Y-%m-%d"))
        d1 = convert_datetime(date)
        nsq = mcal.get_calendar("NYSE")
        nsq_holidays = nsq.holidays().holidays

        if d1 == today:
            if datetime.datetime.now(datetime.timezone.utc).hour < 15:
                d1 -= datetime.timedelta(days=1)

        if d1.weekday() > 4:
            d1 -= datetime.timedelta(days=d1.weekday() - 4)

        while d1 in nsq_holidays:
            d1 -= datetime.timedelta(days=1)
            if d1.weekday() > 4:
                d1 -= datetime.timedelta(days=d1.weekday() - 4)

        if end:
            d2 = d1 + datetime.timedelta(days=1)
            return str(d1), str(d2)

        return str(d1)

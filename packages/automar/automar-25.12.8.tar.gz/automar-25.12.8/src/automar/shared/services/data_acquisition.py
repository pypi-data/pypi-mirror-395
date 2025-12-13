# -*- coding: utf-8 -*-
"""
Unified Data Acquisition System for Automar

This module provides a generalized interface for downloading financial data
from Yahoo Finance, based on the symbols_func pattern but extended with:
- Structured input/output (request/result dataclasses)
- Mode-based dispatch for different acquisition scenarios
- Comprehensive error handling and progress tracking
- Transaction-safe database writes

Phase 3 of SQL Data Management Improvement Plan.
"""

from dataclasses import dataclass
from datetime import date
from enum import Enum
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Callable, Set
import sqlite3

import pandas as pd
from tqdm import tqdm

from automar.core.preprocessing.extractor import (
    symbols_func,
    tick_func,
    GICStoYF,
)
from automar.core.preprocessing.stats import total_dic_func
from automar.shared.persistence.library import (
    convert_datetime,
    DATABASE_NAME,
    TABLE_NAME,
)
from automar.shared.persistence.database import write_df_safe


class AcquisitionMode(Enum):
    """Types of data acquisition operations."""

    FULL_INDUSTRY = "full_industry"  # Download entire industry
    MISSING_COMPANIES = "missing_companies"  # Download specific companies
    DATE_EXTENSION = "date_extension"  # Extend date range for all companies
    BACKFILL_GAPS = "backfill_gaps"  # Fill date gaps for specific companies
    SINGLE_TICKER = "single_ticker"  # Download single company


@dataclass
class DataAcquisitionRequest:
    """
    Structured request for data acquisition.

    Attributes:
        mode: Type of acquisition operation
        industry: Industry name (GICS format)
        companies: List of company tickers (optional, mode-dependent)
        start_date: Start date for data range
        end_date: End date for data range
        gap_info: Gap analysis result for backfill operations (optional)
        skip: Whether to skip companies with insufficient data
        history: History period (alternative to date range)
    """

    mode: AcquisitionMode
    industry: str
    companies: Optional[List[str]] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    gap_info: Optional[Dict] = None
    skip: bool = True
    history: Optional[str] = None

    def validate(self):
        """Ensure request parameters are valid for the specified mode."""
        if self.mode == AcquisitionMode.MISSING_COMPANIES:
            if not self.companies:
                raise ValueError("MISSING_COMPANIES mode requires company list")

        if self.mode in [
            AcquisitionMode.DATE_EXTENSION,
            AcquisitionMode.BACKFILL_GAPS,
        ]:
            if not (self.start_date and self.end_date):
                raise ValueError("Date range required for this mode")

        if self.mode == AcquisitionMode.BACKFILL_GAPS:
            if not self.gap_info:
                raise ValueError("BACKFILL_GAPS mode requires gap_info")

        if self.mode == AcquisitionMode.SINGLE_TICKER:
            if not self.companies or len(self.companies) != 1:
                raise ValueError("SINGLE_TICKER mode requires exactly one company")

        # Validate industry
        if self.industry and self.industry not in GICStoYF:
            raise ValueError(
                f"Invalid industry: {self.industry}. Must be one of: {', '.join(GICStoYF.keys())}"
            )


@dataclass
class AcquisitionResult:
    """
    Result from data acquisition operation.

    Attributes:
        success: Whether acquisition succeeded
        mode: Acquisition mode used
        companies_downloaded: List of successfully downloaded tickers
        companies_failed: List of failed tickers
        rows_added: Number of new rows written to database
        rows_skipped: Number of duplicate rows skipped
        date_range: Tuple of (start_date, end_date)
        error: Error message if success is False
    """

    success: bool
    mode: AcquisitionMode
    companies_downloaded: List[str]
    companies_failed: List[str]
    rows_added: int
    rows_skipped: int
    date_range: Tuple[Optional[date], Optional[date]]
    error: Optional[str] = None

    def summary(self) -> str:
        """Generate human-readable summary of acquisition result."""
        if not self.success:
            return f"❌ Acquisition failed: {self.error}"

        summary_parts = [
            f"✅ Downloaded {len(self.companies_downloaded)} companies",
            f"({self.rows_added} new rows, {self.rows_skipped} duplicates)",
        ]

        if self.date_range[0] and self.date_range[1]:
            summary_parts.append(
                f"for date range {self.date_range[0]} to {self.date_range[1]}"
            )

        if self.companies_failed:
            summary_parts.append(
                f"⚠️ {len(self.companies_failed)} companies failed: {', '.join(self.companies_failed[:5])}"
            )

        return " ".join(summary_parts)


class UnifiedDataAcquisition:
    """
    Generalized data acquisition system based on symbols_func.

    Provides a unified interface for all data download scenarios with:
    - Mode-based dispatch
    - Structured input/output
    - Progress tracking
    - Comprehensive error handling
    - Transaction-safe database writes

    Example:
        >>> request = DataAcquisitionRequest(
        ...     mode=AcquisitionMode.MISSING_COMPANIES,
        ...     industry="Information Technology",
        ...     companies=["AAPL", "MSFT"],
        ...     start_date=date(2020, 1, 1),
        ...     end_date=date(2025, 11, 19)
        ... )
        >>> acquisition = UnifiedDataAcquisition(db_file)
        >>> result = acquisition.acquire(request)
        >>> print(result.summary())
    """

    def __init__(
        self, db_file: Path, progress_callback: Optional[Callable[[str], None]] = None
    ):
        """
        Initialize acquisition system.

        Args:
            db_file: Path to SQLite database
            progress_callback: Optional callback for progress updates
        """
        self.db_file = Path(db_file)
        self.progress_callback = progress_callback or (lambda x: None)

    def acquire(self, request: DataAcquisitionRequest) -> AcquisitionResult:
        """
        Main entry point for data acquisition.

        Dispatches to appropriate handler based on mode.

        Args:
            request: Structured acquisition request

        Returns:
            AcquisitionResult with detailed status
        """
        request.validate()

        handlers = {
            AcquisitionMode.FULL_INDUSTRY: self._acquire_full_industry,
            AcquisitionMode.MISSING_COMPANIES: self._acquire_missing_companies,
            AcquisitionMode.DATE_EXTENSION: self._acquire_date_extension,
            AcquisitionMode.BACKFILL_GAPS: self._acquire_backfill_gaps,
            AcquisitionMode.SINGLE_TICKER: self._acquire_single_ticker,
        }

        handler = handlers[request.mode]
        return handler(request)

    def _acquire_full_industry(
        self, request: DataAcquisitionRequest
    ) -> AcquisitionResult:
        """
        Download all companies in an industry.

        Uses symbols_func to fetch all S&P 500 companies for the industry.
        """
        try:
            self.progress_callback(f"Fetching {request.industry} industry data...")

            # Prepare date parameters
            datest = request.start_date.isoformat() if request.start_date else None
            datend = request.end_date.isoformat() if request.end_date else None

            # Use symbols_func to download all companies
            result = symbols_func(
                tick_input=None,
                period=request.history,
                ind_input=request.industry,
                skip=request.skip,
                datest=datest,
                datend=datend,
            )

            # Process the raw data
            df = self._process_symbols_result(result)

            # Write to database (force overwrite if skip=False)
            write_result = write_df_safe(
                df,
                TABLE_NAME,
                self.db_file,
                validate=True,
                force_overwrite=not request.skip,
            )

            if not write_result.success:
                return AcquisitionResult(
                    success=False,
                    mode=request.mode,
                    companies_downloaded=[],
                    companies_failed=[],
                    rows_added=0,
                    rows_skipped=0,
                    date_range=(request.start_date, request.end_date),
                    error=write_result.error,
                )

            return AcquisitionResult(
                success=True,
                mode=request.mode,
                companies_downloaded=list(result["data"].keys()),
                companies_failed=[],
                rows_added=write_result.rows_written,
                rows_skipped=write_result.rows_skipped,
                date_range=(request.start_date, request.end_date),
            )

        except Exception as e:
            return AcquisitionResult(
                success=False,
                mode=request.mode,
                companies_downloaded=[],
                companies_failed=[],
                rows_added=0,
                rows_skipped=0,
                date_range=(request.start_date, request.end_date),
                error=str(e),
            )

    def _acquire_missing_companies(
        self, request: DataAcquisitionRequest
    ) -> AcquisitionResult:
        """
        Download specific companies only.

        Downloads each company individually with progress tracking.
        """
        companies_downloaded = []
        companies_failed = []
        all_data = []

        for i, company in enumerate(request.companies):
            try:
                self.progress_callback(
                    f"Downloading {company} ({i+1}/{len(request.companies)})..."
                )

                # Download single ticker
                df = self._download_single_ticker(
                    company,
                    request.industry,
                    request.start_date,
                    request.end_date,
                    request.history,
                )

                all_data.append(df)
                companies_downloaded.append(company)

            except Exception as e:
                self.progress_callback(f"Failed to download {company}: {e}")
                companies_failed.append(company)
                continue

        if not all_data:
            return AcquisitionResult(
                success=False,
                mode=request.mode,
                companies_downloaded=[],
                companies_failed=companies_failed,
                rows_added=0,
                rows_skipped=0,
                date_range=(request.start_date, request.end_date),
                error="No companies successfully downloaded",
            )

        # Combine and write (force overwrite if skip=False)
        combined_df = pd.concat(all_data, ignore_index=True)
        write_result = write_df_safe(
            combined_df,
            TABLE_NAME,
            self.db_file,
            validate=True,
            force_overwrite=not request.skip,
        )

        if not write_result.success:
            return AcquisitionResult(
                success=False,
                mode=request.mode,
                companies_downloaded=companies_downloaded,
                companies_failed=companies_failed,
                rows_added=0,
                rows_skipped=0,
                date_range=(request.start_date, request.end_date),
                error=write_result.error,
            )

        return AcquisitionResult(
            success=True,
            mode=request.mode,
            companies_downloaded=companies_downloaded,
            companies_failed=companies_failed,
            rows_added=write_result.rows_written,
            rows_skipped=write_result.rows_skipped,
            date_range=(request.start_date, request.end_date),
        )

    def _acquire_date_extension(
        self, request: DataAcquisitionRequest
    ) -> AcquisitionResult:
        """
        Extend date range for all companies in industry.

        Gets list of companies already in database and downloads
        them with the new date range.
        """
        try:
            # Get list of all companies in database for this industry
            conn = sqlite3.connect(str(self.db_file))
            query = """
                SELECT DISTINCT Company
                FROM data
                WHERE Industry = ?
            """
            existing = pd.read_sql(query, conn, params=(request.industry,))
            conn.close()

            if existing.empty:
                return AcquisitionResult(
                    success=False,
                    mode=request.mode,
                    companies_downloaded=[],
                    companies_failed=[],
                    rows_added=0,
                    rows_skipped=0,
                    date_range=(request.start_date, request.end_date),
                    error=f"No companies found in database for industry {request.industry}",
                )

            existing_companies = existing["Company"].tolist()

            # Create request for these companies with new date range
            extended_request = DataAcquisitionRequest(
                mode=AcquisitionMode.MISSING_COMPANIES,
                industry=request.industry,
                companies=existing_companies,
                start_date=request.start_date,
                end_date=request.end_date,
                skip=request.skip,
                history=request.history,
            )

            return self._acquire_missing_companies(extended_request)

        except Exception as e:
            return AcquisitionResult(
                success=False,
                mode=request.mode,
                companies_downloaded=[],
                companies_failed=[],
                rows_added=0,
                rows_skipped=0,
                date_range=(request.start_date, request.end_date),
                error=str(e),
            )

    def _acquire_backfill_gaps(
        self, request: DataAcquisitionRequest
    ) -> AcquisitionResult:
        """
        Fill date gaps for companies with incomplete data.

        Uses gap analysis result to determine which companies need backfilling.
        """
        if not request.gap_info:
            return AcquisitionResult(
                success=False,
                mode=request.mode,
                companies_downloaded=[],
                companies_failed=[],
                rows_added=0,
                rows_skipped=0,
                date_range=(request.start_date, request.end_date),
                error="BACKFILL_GAPS mode requires gap_info",
            )

        # Use gap analysis to determine which companies need backfilling
        incomplete = request.gap_info.get("incomplete_companies", [])

        if not incomplete:
            return AcquisitionResult(
                success=True,
                mode=request.mode,
                companies_downloaded=[],
                companies_failed=[],
                rows_added=0,
                rows_skipped=0,
                date_range=(request.start_date, request.end_date),
                error="No incomplete companies to backfill",
            )

        backfill_request = DataAcquisitionRequest(
            mode=AcquisitionMode.MISSING_COMPANIES,
            industry=request.industry,
            companies=incomplete,
            start_date=request.start_date,
            end_date=request.end_date,
            skip=request.skip,
            history=request.history,
            gap_info=request.gap_info,
        )

        return self._acquire_missing_companies(backfill_request)

    def _acquire_single_ticker(
        self, request: DataAcquisitionRequest
    ) -> AcquisitionResult:
        """Download a single company."""
        if not request.companies or len(request.companies) != 1:
            return AcquisitionResult(
                success=False,
                mode=request.mode,
                companies_downloaded=[],
                companies_failed=[],
                rows_added=0,
                rows_skipped=0,
                date_range=(request.start_date, request.end_date),
                error="SINGLE_TICKER mode requires exactly one company",
            )

        single_request = DataAcquisitionRequest(
            mode=AcquisitionMode.MISSING_COMPANIES,
            industry=request.industry,
            companies=request.companies,
            start_date=request.start_date,
            end_date=request.end_date,
            skip=request.skip,
            history=request.history,
        )

        return self._acquire_missing_companies(single_request)

    def _download_single_ticker(
        self,
        ticker: str,
        industry: str,
        start_date: Optional[date],
        end_date: Optional[date],
        history: Optional[str],
    ) -> pd.DataFrame:
        """
        Download and process data for a single ticker.

        Args:
            ticker: Company ticker symbol
            industry: Industry name (for metadata)
            start_date: Start date (optional)
            end_date: End date (optional)
            history: History period (alternative to dates)

        Returns:
            Processed DataFrame with technical indicators
        """
        # Download raw data
        # When history is provided, let Yahoo Finance calculate the date range
        # to ensure consistency with feather mode downloads
        if history and not (start_date and end_date):
            # Use period-based download (e.g., "4y")
            raw_df = tick_func(ticker, history, datest=None, datend=None)
        else:
            # Use explicit date range
            datest = start_date.isoformat() if start_date else None
            datend = end_date.isoformat() if end_date else None
            raw_df = tick_func(ticker, history, datest=datest, datend=datend)

        # Process with technical indicators
        processed = total_dic_func(raw_df, drop=False)
        processed["Date"] = processed.index.date
        processed["Company"] = ticker
        processed["Industry"] = industry

        return processed

    def _process_symbols_result(self, symbols_result: dict) -> pd.DataFrame:
        """
        Convert symbols_func result to database-ready DataFrame.

        Args:
            symbols_result: Dict with structure {'data': {ticker: df}, 'name': industry}

        Returns:
            Processed DataFrame ready for database insertion
        """
        industry = symbols_result["name"]
        data_dict = symbols_result["data"]

        company_list = []

        # Process each company's data
        for company_ticker, data in data_dict.items():
            processed_data = total_dic_func(data, drop=False)
            processed_data["Date"] = processed_data.index.date
            processed_data["Company"] = company_ticker
            processed_data["Industry"] = industry
            company_list.append(processed_data)

        # Combine all company data
        df = pd.concat(company_list, ignore_index=True)
        return df


# ============================================================================
# High-Level Convenience Functions
# ============================================================================


def download_missing_companies(
    db_file: Path,
    industry: str,
    start_date: date,
    end_date: date,
    no_confirm: bool = False,
) -> AcquisitionResult:
    """
    Automatically detect and download missing companies for an industry.

    This is the primary interface for most use cases.

    Args:
        db_file: Path to SQLite database
        industry: Industry name (GICS format)
        start_date: Start date for data range
        end_date: End date for data range
        no_confirm: Skip user confirmation prompt

    Returns:
        AcquisitionResult with download status
    """
    from automar.shared.services.gap_analyzer import GapAnalyzer
    from automar.shared.services.gap_reporter import GapReporter

    # Step 1: Analyze gaps
    analyzer = GapAnalyzer(db_file)
    gap_result = analyzer.analyze_industry(industry, start_date, end_date)

    # Step 2: Print summary
    GapReporter.print_summary(gap_result)

    # Step 3: Ask user for confirmation (unless no_confirm)
    if gap_result.missing_companies:
        if not no_confirm:
            print(
                f"\n📥 Download {len(gap_result.missing_companies)} missing companies?"
            )
            response = input("Continue? (y/n): ")
            if response.lower() != "y":
                return AcquisitionResult(
                    success=False,
                    mode=AcquisitionMode.MISSING_COMPANIES,
                    companies_downloaded=[],
                    companies_failed=[],
                    rows_added=0,
                    rows_skipped=0,
                    date_range=(start_date, end_date),
                    error="User cancelled",
                )

        # Step 4: Execute download
        request = DataAcquisitionRequest(
            mode=AcquisitionMode.MISSING_COMPANIES,
            industry=industry,
            companies=gap_result.missing_companies,
            start_date=start_date,
            end_date=end_date,
        )

        acquisition = UnifiedDataAcquisition(
            db_file, progress_callback=lambda msg: print(f"  {msg}")
        )
        return acquisition.acquire(request)
    else:
        print("✅ No missing companies - database is complete!")
        return AcquisitionResult(
            success=True,
            mode=AcquisitionMode.MISSING_COMPANIES,
            companies_downloaded=[],
            companies_failed=[],
            rows_added=0,
            rows_skipped=0,
            date_range=(start_date, end_date),
        )


def update_industry_to_date(
    db_file: Path,
    industry: str,
    target_date: Optional[date] = None,
) -> AcquisitionResult:
    """
    Update an industry's data to a target date (default: today).

    Handles both missing companies and date extensions.

    Args:
        db_file: Path to SQLite database
        industry: Industry name (GICS format)
        target_date: Target date (default: today)

    Returns:
        AcquisitionResult with download status
    """
    if target_date is None:
        target_date = date.today()

    # Get date range from database
    conn = sqlite3.connect(str(db_file))
    query = """
        SELECT MIN(Date) as min_date, MAX(Date) as max_date
        FROM data
        WHERE Industry = ?
    """
    result = pd.read_sql(query, conn, params=(industry,))
    conn.close()

    if result["min_date"].isna().all():
        # Industry not in database - full download needed
        print(f"⚠️ Industry {industry} not found in database.")
        print("Please use extraction service for initial download.")
        return AcquisitionResult(
            success=False,
            mode=AcquisitionMode.DATE_EXTENSION,
            companies_downloaded=[],
            companies_failed=[],
            rows_added=0,
            rows_skipped=0,
            date_range=(None, target_date),
            error=f"Industry {industry} not in database",
        )

    start_date = pd.to_datetime(result["min_date"].iloc[0]).date()
    end_date = target_date

    print(f"📅 Updating {industry} from {start_date} to {end_date}")

    # Download missing companies and extend dates
    return download_missing_companies(db_file, industry, start_date, end_date)


def backfill_all_gaps(
    db_file: Path,
    industry: str,
    start_date: date,
    end_date: date,
) -> AcquisitionResult:
    """
    Fill all date gaps for companies with incomplete data.

    Args:
        db_file: Path to SQLite database
        industry: Industry name (GICS format)
        start_date: Start date for backfill range
        end_date: End date for backfill range

    Returns:
        AcquisitionResult with backfill status
    """
    from automar.shared.services.gap_analyzer import GapAnalyzer
    from automar.shared.services.gap_reporter import GapReporter

    # Analyze gaps
    analyzer = GapAnalyzer(db_file)
    gap_result = analyzer.analyze_industry(industry, start_date, end_date)

    # Print summary
    GapReporter.print_summary(gap_result)

    if not gap_result.incomplete_companies:
        print("✅ No incomplete companies - all date ranges are complete!")
        return AcquisitionResult(
            success=True,
            mode=AcquisitionMode.BACKFILL_GAPS,
            companies_downloaded=[],
            companies_failed=[],
            rows_added=0,
            rows_skipped=0,
            date_range=(start_date, end_date),
        )

    # Ask for confirmation
    print(f"\n🔧 Backfill gaps for {len(gap_result.incomplete_companies)} companies?")
    response = input("Continue? (y/n): ")
    if response.lower() != "y":
        return AcquisitionResult(
            success=False,
            mode=AcquisitionMode.BACKFILL_GAPS,
            companies_downloaded=[],
            companies_failed=[],
            rows_added=0,
            rows_skipped=0,
            date_range=(start_date, end_date),
            error="User cancelled",
        )

    # Execute backfill
    request = DataAcquisitionRequest(
        mode=AcquisitionMode.BACKFILL_GAPS,
        industry=industry,
        start_date=start_date,
        end_date=end_date,
        gap_info=gap_result.to_dict(),
    )

    acquisition = UnifiedDataAcquisition(
        db_file, progress_callback=lambda msg: print(f"  {msg}")
    )
    return acquisition.acquire(request)

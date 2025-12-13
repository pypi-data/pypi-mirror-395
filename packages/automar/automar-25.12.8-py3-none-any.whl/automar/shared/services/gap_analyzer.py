# -*- coding: utf-8 -*-
"""
Gap Analysis Module for SQLite Database

Provides comprehensive analysis of missing data in SQLite databases,
comparing actual data against S&P 500 constituent lists and trading calendars.
"""

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
import sqlite3
import warnings

import pandas as pd
import pandas_market_calendars as mcal
import requests
from io import StringIO


@dataclass
class GapAnalysisResult:
    """
    Structured result from gap analysis.

    Contains comprehensive information about missing data at both
    company and date levels, with actionable recommendations.
    """

    # Company-level gaps
    missing_companies: List[str]  # Not in DB at all
    incomplete_companies: List[str]  # In DB but missing dates

    # Date-level gaps
    missing_date_ranges: List[Tuple[date, date]]  # Continuous gaps
    company_specific_gaps: Dict[str, List[date]]  # Per-company gaps

    # Industry-level status
    expected_companies: Set[str]  # From S&P 500
    actual_companies: Set[str]  # In database
    coverage_pct: float  # actual / expected

    # Date range status
    requested_start: date
    requested_end: date
    actual_start: Optional[date]
    actual_end: Optional[date]
    date_coverage_pct: float

    # Actionable recommendations
    needs_company_download: bool
    needs_date_extension: bool
    needs_backfill: bool
    estimated_api_calls: int

    # Additional metadata
    industry: str = ""
    sp500_companies: List[str] = field(default_factory=list)

    def to_dict(self):
        """Serialize for API response."""
        return {
            "industry": self.industry,
            "missing_companies": self.missing_companies,
            "incomplete_companies": self.incomplete_companies,
            "missing_date_ranges": [
                (start.isoformat(), end.isoformat())
                for start, end in self.missing_date_ranges
            ],
            "coverage": {
                "companies": f"{self.coverage_pct:.1%}",
                "companies_count": f"{len(self.actual_companies)}/{len(self.expected_companies)}",
                "dates": f"{self.date_coverage_pct:.1%}",
            },
            "date_range": {
                "requested": {
                    "start": self.requested_start.isoformat(),
                    "end": self.requested_end.isoformat(),
                },
                "actual": {
                    "start": (
                        self.actual_start.isoformat() if self.actual_start else None
                    ),
                    "end": self.actual_end.isoformat() if self.actual_end else None,
                },
            },
            "recommendations": {
                "download_companies": self.needs_company_download,
                "extend_dates": self.needs_date_extension,
                "backfill_gaps": self.needs_backfill,
            },
            "estimated_cost": self.estimated_api_calls,
        }


class GapAnalyzer:
    """
    Advanced gap detection with multi-dimensional analysis.

    Analyzes SQLite databases to identify:
    - Missing companies (compared to S&P 500)
    - Missing date ranges
    - Per-company date gaps
    - Coverage statistics
    """

    def __init__(
        self, db_file: Path, trading_calendar: Optional[mcal.MarketCalendar] = None
    ):
        """
        Initialize gap analyzer.

        Args:
            db_file: Path to SQLite database
            trading_calendar: NYSE calendar (created if not provided)
        """
        self.db_file = Path(db_file)
        self.calendar = trading_calendar or mcal.get_calendar("NYSE")

    def analyze_industry(
        self,
        industry: str,
        start_date: date,
        end_date: date,
        sp500_list: Optional[Set[str]] = None,
        table_name: str = "data",
    ) -> GapAnalysisResult:
        """
        Comprehensive gap analysis for an industry.

        Args:
            industry: GICS sector name
            start_date: Start of requested date range
            end_date: End of requested date range
            sp500_list: Set of S&P 500 tickers (fetched if not provided)
            table_name: Database table name

        Returns:
            GapAnalysisResult with detailed breakdown
        """
        # Fetch S&P 500 list if not provided
        if sp500_list is None:
            sp500_list = self._fetch_sp500_companies(industry)

        # Check if database/table exists
        if not self.db_file.exists():
            return self._empty_database_result(
                industry, start_date, end_date, sp500_list
            )

        conn = sqlite3.connect(str(self.db_file))

        # Check if table exists
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table_name,),
        )
        table_exists = cursor.fetchone() is not None

        if not table_exists:
            conn.close()
            return self._empty_database_result(
                industry, start_date, end_date, sp500_list
            )

        # Load all data for industry (no date filter)
        query = """
            SELECT DISTINCT Company, Date
            FROM data
            WHERE Industry = ?
            ORDER BY Company, Date
        """

        try:
            df = pd.read_sql(query, conn, params=(industry,))
        except (pd.errors.DatabaseError, sqlite3.Error) as e:
            warnings.warn(f"Database query failed: {e}")
            conn.close()
            return self._empty_database_result(
                industry, start_date, end_date, sp500_list
            )
        finally:
            conn.close()

        # Handle empty result
        if df.empty:
            return self._empty_database_result(
                industry, start_date, end_date, sp500_list
            )

        # Convert dates
        df["Date"] = pd.to_datetime(df["Date"])

        # Step 2: Identify missing companies
        actual_companies = set(df["Company"].unique())
        missing_companies = sorted(sp500_list - actual_companies)

        # Step 3: Generate expected trading days
        expected_dates = set(self._get_trading_days(start_date, end_date))

        # Step 4: Per-company gap analysis
        incomplete_companies = []
        company_specific_gaps = {}

        for company in actual_companies:
            company_dates = set(df[df["Company"] == company]["Date"].dt.date)
            missing_dates = expected_dates - company_dates

            if missing_dates:
                incomplete_companies.append(company)
                company_specific_gaps[company] = sorted(missing_dates)

        # Step 5: Find continuous date range gaps
        all_dates = sorted(df["Date"].dt.date.unique())
        missing_date_ranges = self._find_continuous_gaps(all_dates, expected_dates)

        # Step 6: Calculate coverage metrics
        coverage_pct = len(actual_companies) / len(sp500_list) if sp500_list else 0.0
        actual_start = min(all_dates) if all_dates else None
        actual_end = max(all_dates) if all_dates else None

        date_coverage = len(all_dates) / len(expected_dates) if expected_dates else 0.0

        # Step 7: Determine action flags
        needs_company_download = len(missing_companies) > 0
        needs_date_extension = (
            actual_end is not None
            and actual_end < end_date
            and (end_date - actual_end).days > 2
        )
        needs_backfill = len(company_specific_gaps) > 0

        # Step 8: Estimate API calls needed
        estimated_calls = len(missing_companies) + (  # New companies
            len(incomplete_companies) if needs_backfill else 0
        )

        return GapAnalysisResult(
            missing_companies=missing_companies,
            incomplete_companies=sorted(incomplete_companies),
            missing_date_ranges=missing_date_ranges,
            company_specific_gaps=company_specific_gaps,
            expected_companies=sp500_list,
            actual_companies=actual_companies,
            coverage_pct=coverage_pct,
            requested_start=start_date,
            requested_end=end_date,
            actual_start=actual_start,
            actual_end=actual_end,
            date_coverage_pct=date_coverage,
            needs_company_download=needs_company_download,
            needs_date_extension=needs_date_extension,
            needs_backfill=needs_backfill,
            estimated_api_calls=estimated_calls,
            industry=industry,
            sp500_companies=sorted(sp500_list),
        )

    def _find_continuous_gaps(
        self, actual_dates: List[date], expected_dates: Set[date]
    ) -> List[Tuple[date, date]]:
        """Find continuous ranges of missing dates."""
        missing = sorted(expected_dates - set(actual_dates))

        if not missing:
            return []

        ranges = []
        start = missing[0]
        prev = missing[0]

        for current in missing[1:]:
            # Check if there's a gap (accounting for weekends/holidays)
            if (current - prev).days > 1:
                # Verify it's not just a weekend/holiday
                intermediate_dates = self._get_trading_days(prev, current)
                if len(intermediate_dates) > 1:  # More than just prev
                    ranges.append((start, prev))
                    start = current
            prev = current

        ranges.append((start, prev))
        return ranges

    def _get_trading_days(self, start: date, end: date) -> List[date]:
        """Get valid trading days between start and end dates."""
        # Get NYSE holidays
        nsq_holidays = self.calendar.holidays().holidays

        # Filter holidays in our date range
        filtered_holidays = [
            hd
            for hd in nsq_holidays
            if pd.Timestamp(start) <= pd.Timestamp(hd) <= pd.Timestamp(end)
        ]

        # Generate business days and remove holidays
        trading_days = pd.date_range(start=start, end=end, freq="B").drop(
            filtered_holidays, errors="ignore"
        )

        # Exclude today if it's in the list (market might not be closed yet)
        today = pd.Timestamp.today().date()
        return [d.date() for d in trading_days if d.date() != today]

    def _fetch_sp500_companies(self, industry: str) -> Set[str]:
        """Fetch current S&P 500 constituents for an industry."""
        site = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

        try:
            response = requests.get(
                site,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                },
                timeout=10,
            )
            response.raise_for_status()

            sp500_tables = pd.read_html(StringIO(response.text))

            # Find the correct table
            sp500_table = None
            for table in sp500_tables:
                if "Symbol" in table.columns and "GICS Sector" in table.columns:
                    sp500_table = table
                    break

            if sp500_table is None:
                raise ValueError("Could not find S&P 500 constituents table")

            # Filter by industry
            companies = set(
                sp500_table.loc[sp500_table["GICS Sector"] == industry][
                    "Symbol"
                ].tolist()
            )

            return companies

        except Exception as e:
            warnings.warn(f"Failed to fetch S&P 500 list: {e}")
            return set()

    def _empty_database_result(
        self,
        industry: str,
        start_date: date,
        end_date: date,
        sp500_list: Set[str],
    ) -> GapAnalysisResult:
        """Create result for empty database."""
        expected_dates = self._get_trading_days(start_date, end_date)

        return GapAnalysisResult(
            missing_companies=sorted(sp500_list),
            incomplete_companies=[],
            missing_date_ranges=[(start_date, end_date)] if expected_dates else [],
            company_specific_gaps={},
            expected_companies=sp500_list,
            actual_companies=set(),
            coverage_pct=0.0,
            requested_start=start_date,
            requested_end=end_date,
            actual_start=None,
            actual_end=None,
            date_coverage_pct=0.0,
            needs_company_download=True,
            needs_date_extension=False,
            needs_backfill=False,
            estimated_api_calls=len(sp500_list),
            industry=industry,
            sp500_companies=sorted(sp500_list),
        )

    def analyze_all_industries(
        self,
        start_date: date,
        end_date: date,
        table_name: str = "data",
    ) -> Dict[str, GapAnalysisResult]:
        """
        Run gap analysis across all industries.

        Args:
            start_date: Start of requested date range
            end_date: End of requested date range
            table_name: Database table name

        Returns:
            Dict mapping industry name to GapAnalysisResult
        """
        from automar.core.preprocessing.extractor import GICStoYF

        results = {}
        for industry in GICStoYF.keys():
            try:
                results[industry] = self.analyze_industry(
                    industry,
                    start_date,
                    end_date,
                    table_name=table_name,
                )
            except Exception as e:
                warnings.warn(f"Failed to analyze {industry}: {e}")
                continue

        return results

    def check_staleness(self) -> Dict[str, any]:
        """
        Check if database is missing recent trading days.

        Returns:
            Dict with staleness information
        """
        if not self.db_file.exists():
            return {
                "stale": True,
                "reason": "Database does not exist",
                "days_behind": None,
            }

        conn = sqlite3.connect(str(self.db_file))

        try:
            # Get most recent date in database
            query = "SELECT MAX(Date) as max_date FROM data"
            result = pd.read_sql(query, conn)

            if result["max_date"].isna().all():
                return {
                    "stale": True,
                    "reason": "Database is empty",
                    "days_behind": None,
                }

            max_date = pd.to_datetime(result["max_date"].iloc[0]).date()
            today = date.today()

            # Calculate trading days between
            trading_days = self._get_trading_days(max_date, today)
            days_behind = len(trading_days)

            return {
                "stale": days_behind > 3,  # More than 3 trading days behind
                "max_date": max_date.isoformat(),
                "days_behind": days_behind,
                "last_trading_day": (
                    trading_days[-1].isoformat() if trading_days else None
                ),
            }

        except (pd.errors.DatabaseError, sqlite3.Error) as e:
            return {
                "stale": True,
                "reason": f"Database query failed: {e}",
                "days_behind": None,
            }
        finally:
            conn.close()

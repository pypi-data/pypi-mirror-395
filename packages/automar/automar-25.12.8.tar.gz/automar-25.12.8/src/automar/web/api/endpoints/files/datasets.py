# -*- coding: utf-8 -*-
"""Dataset file operations and metadata endpoints."""
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException

from automar.shared.persistence.job_store import get_job_store

router = APIRouter(tags=["files", "datasets"])


@router.get("/datasets")
async def list_datasets():
    """Get list of available datasets with job metadata enrichment"""
    try:
        from automar.shared.persistence.library import get_dirs
        import re

        # Get the datasets directory
        datasets_dir = get_dirs(create_dirs=False)

        if not datasets_dir.exists():
            return {"datasets": []}

        # Build a map of dataset paths -> job metadata for faster lookup
        job_store = get_job_store()
        all_jobs = job_store.get_all_jobs()
        dataset_to_job = {}

        for job_id, job in all_jobs.items():
            if (
                job.get("type") == "extract"
                and job.get("status") == "completed"
                and job.get("result")
            ):
                # Extract jobs have output_paths (list) not file_path
                output_paths = job["result"].get("output_paths", [])
                if not output_paths:
                    # Try legacy file_path for backwards compatibility
                    file_path = job["result"].get("file_path")
                    if file_path:
                        output_paths = [file_path]

                for file_path in output_paths:
                    # Normalize path for comparison
                    try:
                        normalized_path = str(Path(file_path).resolve())
                        dataset_to_job[normalized_path] = {
                            "job_id": job_id,
                            "industry": job["result"].get("industry"),
                            "ticker": job["result"].get("ticker"),
                        }
                    except Exception:
                        # Skip if path resolution fails
                        pass

        # Find all data files in the directory
        datasets = []
        supported_extensions = [".feather", ".parquet", ".csv", ".pickle", ".pkl"]

        for file_path in datasets_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
                # Try to find associated job
                normalized_file_path = str(file_path.resolve())
                job_metadata = dataset_to_job.get(normalized_file_path)

                # Build file info
                # Convert extension to ValidFormats enum or use as-is if not a valid format
                file_format = file_path.suffix.lstrip(".").lower()

                file_info = {
                    "name": file_path.name,
                    "path": str(file_path),
                    "size": file_path.stat().st_size,
                    "modified": file_path.stat().st_mtime,
                    "format": file_format,
                }

                # Enrich with job metadata if available
                if job_metadata:
                    file_info.update(
                        {
                            "industry": job_metadata["industry"],
                            "ticker": job_metadata["ticker"],
                            "job_id": job_metadata["job_id"],
                        }
                    )
                else:
                    # Fallback: infer from filename
                    # Typical format: "data_Materials_10y_2025-10-22.feather" or "Materials_AAPL_10y.parquet"
                    # Try to extract industry (may be after "data_" prefix or at start)
                    industry = None
                    ticker = None

                    # Remove common prefixes
                    name = file_path.stem  # Remove extension
                    if name.startswith("data_"):
                        name = name[5:]  # Remove "data_" prefix

                    # Extract industry - stop at date pattern or period indicator
                    # File format: IndustryName_PERIOD_DATE or IndustryName(TICKER)_PERIOD_DATE
                    # Industry names may have underscores (e.g., Consumer_Staples)
                    # Period indicators: 1y, 10y, etc. or date patterns: YYYY-MM-DD

                    # Remove ticker if present: "Consumer_Staples(COST)_10y_..." -> "Consumer_Staples_10y_..."
                    name_no_ticker = re.sub(r"\([A-Z]+\)", "", name)

                    # Match everything before period/date pattern
                    industry_match = re.match(
                        r"^([^_]+(?:_[^_]+)*?)_(?:\d+[ymwd]|[0-9]{4})", name_no_ticker
                    )
                    if industry_match:
                        industry = industry_match.group(1).replace("_", " ")
                    else:
                        # Fallback: take first part before underscore
                        parts = name.split("_")
                        industry = parts[0] if parts else None

                    # Extract ticker (uppercase 1-5 letter code, usually after industry)
                    ticker_match = re.search(r"_([A-Z]{1,5})_", file_path.name)
                    if ticker_match:
                        ticker = ticker_match.group(1)

                    file_info.update(
                        {"industry": industry, "ticker": ticker, "job_id": None}
                    )

                datasets.append(file_info)

        # Sort by modification time (newest first)
        datasets.sort(key=lambda x: x["modified"], reverse=True)

        return {"datasets": datasets}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing datasets: {str(e)}")


@router.get("/dataset/{dataset_path:path}/companies")
async def get_dataset_companies(dataset_path: str):
    """Get list of companies (tickers) available in a dataset file"""
    try:
        from pathlib import Path
        import re
        import pandas as pd
        from automar.shared.persistence.library import read_df

        # Convert dataset_path to Path object
        dataset_file = Path(dataset_path)

        if not dataset_file.exists():
            raise HTTPException(
                status_code=404, detail=f"Dataset file not found: {dataset_path}"
            )

        # Read the dataset
        df = read_df(dataset_file)

        # Extract unique companies from the dataset
        companies = []
        if "Company" in df.columns:
            from pandas import notna

            unique_companies = df["Company"].unique()
            companies = [str(company) for company in unique_companies if notna(company)]

        # Try to extract default ticker from filename (between parentheses)
        default_ticker = None
        filename = dataset_file.name
        ticker_match = re.search(r"\(([^)]+)\)", filename)
        if ticker_match:
            default_ticker = ticker_match.group(1)

        return {
            "companies": sorted(companies),
            "default_ticker": default_ticker,
            "total_companies": len(companies),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error reading dataset companies: {str(e)}"
        )


@router.get("/sqlite-files")
async def list_sqlite_files():
    """Get list of available SQLite database files"""
    try:
        from automar.shared.persistence.library import get_dirs

        # Get the datasets directory
        datasets_dir = get_dirs(create_dirs=False)

        if not datasets_dir.exists():
            return {"sqlite_files": []}

        # Find all SQLite files in the directory
        sqlite_files = []
        sqlite_extensions = [".sqlite", ".db"]

        for file_path in datasets_dir.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in sqlite_extensions:
                sqlite_files.append(
                    {
                        "name": file_path.name,
                        "path": str(file_path),
                        "size": file_path.stat().st_size,
                        "modified": file_path.stat().st_mtime,
                    }
                )

        # Sort by modification time (newest first)
        sqlite_files.sort(key=lambda x: x["modified"], reverse=True)

        return {"sqlite_files": sqlite_files}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error listing SQLite files: {str(e)}"
        )


@router.get("/sqlite/{sqlite_path:path}/industries")
async def get_sqlite_industries(sqlite_path: str):
    """Get list of all unique industries in a SQLite database file"""
    try:
        import sqlite3
        from pandas import notna

        # Convert sqlite_path to Path object
        sqlite_file = Path(sqlite_path)

        if not sqlite_file.exists():
            raise HTTPException(
                status_code=404, detail=f"SQLite file not found: {sqlite_path}"
            )

        # Connect to SQLite database
        conn = sqlite3.connect(str(sqlite_file))
        cursor = conn.cursor()

        # Query for distinct industries with company counts
        # The data table has columns: Date, Open, High, Low, Close, Volume, Company, Industry, Labels (optional)
        try:
            cursor.execute(
                """
                SELECT Industry, COUNT(DISTINCT Company) as company_count
                FROM data
                WHERE Industry IS NOT NULL AND Industry != ''
                GROUP BY Industry
                ORDER BY Industry
                """
            )
            results = cursor.fetchall()
            industries = [
                {"industry": industry, "company_count": count}
                for industry, count in results
                if industry and notna(industry)
            ]
        except sqlite3.OperationalError as e:
            # Fallback: If query fails, try to get industries without counts
            cursor.execute(
                "SELECT DISTINCT Industry FROM data WHERE Industry IS NOT NULL"
            )
            results = cursor.fetchall()
            industries = [
                {"industry": str(industry), "company_count": 0}
                for (industry,) in results
                if industry and notna(industry)
            ]
            industries.sort(key=lambda x: x["industry"])

        conn.close()

        return {
            "industries": industries,
            "total_industries": len(industries),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error reading SQLite industries: {str(e)}"
        )


@router.get("/sqlite/{sqlite_path:path}/companies")
async def get_sqlite_companies(sqlite_path: str):
    """Get list of all unique companies (tickers) in a SQLite database file"""
    try:
        import sqlite3
        from pandas import notna

        # Convert sqlite_path to Path object
        sqlite_file = Path(sqlite_path)

        if not sqlite_file.exists():
            raise HTTPException(
                status_code=404, detail=f"SQLite file not found: {sqlite_path}"
            )

        # Connect to SQLite database
        conn = sqlite3.connect(str(sqlite_file))
        cursor = conn.cursor()

        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Extract unique companies from all tables
        companies = set()
        for (table_name,) in tables:
            # Try to query for Company column if it exists
            try:
                cursor.execute(f"SELECT DISTINCT Company FROM '{table_name}'")
                table_companies = cursor.fetchall()
                for (company,) in table_companies:
                    if company and notna(company):
                        companies.add(str(company))
            except sqlite3.OperationalError:
                # Company column doesn't exist in this table, skip it
                pass

        conn.close()

        return {
            "companies": sorted(list(companies)),
            "total_companies": len(companies),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error reading SQLite companies: {str(e)}"
        )


@router.get("/sqlite/{sqlite_path:path}/date-range")
async def get_sqlite_date_range(
    sqlite_path: str, industry: str = None, ticker: str = None
):
    """Get available date range in SQLite database, optionally filtered by industry/ticker"""
    try:
        import sqlite3
        from pandas import notna

        # Convert sqlite_path to Path object
        sqlite_file = Path(sqlite_path)

        if not sqlite_file.exists():
            raise HTTPException(
                status_code=404, detail=f"SQLite file not found: {sqlite_path}"
            )

        # Connect to SQLite database
        conn = sqlite3.connect(str(sqlite_file))
        cursor = conn.cursor()

        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        min_date = None
        max_date = None
        total_records = 0

        # Query dates from all tables
        for (table_name,) in tables:
            try:
                # Build query with optional filters
                query = f"SELECT MIN(Date), MAX(Date), COUNT(*) FROM '{table_name}'"
                conditions = []

                if industry:
                    conditions.append(f"Industry = '{industry}'")
                if ticker:
                    conditions.append(f"Company = '{ticker}'")

                if conditions:
                    query += " WHERE " + " AND ".join(conditions)

                cursor.execute(query)
                result = cursor.fetchone()

                if result and result[0] and result[1]:
                    table_min, table_max, table_count = result

                    # Update global min/max
                    if min_date is None or table_min < min_date:
                        min_date = table_min
                    if max_date is None or table_max > max_date:
                        max_date = table_max

                    total_records += table_count

            except sqlite3.OperationalError:
                # Table doesn't have required columns, skip it
                pass

        conn.close()

        if min_date is None or max_date is None:
            return {
                "min_date": None,
                "max_date": None,
                "total_records": 0,
                "message": "No dates found with the specified filters",
            }

        return {
            "min_date": min_date,
            "max_date": max_date,
            "total_records": total_records,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error reading SQLite date range: {str(e)}"
        )

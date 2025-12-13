# -*- coding: utf-8 -*-
"""
Database schema definitions for Automar SQLite persistence layer.

This module provides:
- Complete DDL schema with PRIMARY KEY constraints
- Database initialization functions
- Schema validation utilities
- Migration support

CRITICAL: All dates must be stored in ISO 8601 format (YYYY-MM-DD)
"""

import sqlite3
from pathlib import Path
from typing import Optional
from dataclasses import dataclass
from enum import Enum


# Schema version for migration tracking
SCHEMA_VERSION = 1
TABLE_NAME = "data"


class SchemaValidationError(Exception):
    """Raised when schema validation fails."""

    pass


@dataclass
class SchemaInfo:
    """Information about database schema."""

    version: int
    table_exists: bool
    has_primary_key: bool
    has_indexes: bool
    row_count: int


def get_data_table_ddl() -> str:
    """
    Returns the complete DDL for the main data table.

    Key features:
    - PRIMARY KEY (Company, Date) - absolute guarantee against duplicates
    - WITHOUT ROWID - saves ~25% storage for compound primary keys
    - CHECK constraints - validate data integrity at database level
    - NOT NULL constraints - prevent missing critical fields

    Returns:
        SQL DDL string for creating the data table
    """
    return """
    CREATE TABLE IF NOT EXISTS data (
        -- IMPORTANT: Column order matches total_dic_func() output + Date/Company/Industry
        -- DO NOT reorder columns - this breaks pandas to_sql() and queries
        Open REAL CHECK(Open > 0),
        High REAL CHECK(High > 0),
        Low REAL CHECK(Low > 0),
        Close REAL CHECK(Close > 0),
        Volume REAL CHECK(Volume >= 0),

        -- Labels
        Labels INTEGER CHECK(Labels IN (0, 1)),

        -- Technical Indicators (Moving Averages)
        MA1 REAL,
        MA2 REAL,
        MA3 REAL,
        MA4 REAL,

        -- Stochastic Oscillator (KD)
        K REAL,
        D REAL,

        -- MACD Components
        DIFF REAL,
        DEA REAL,
        MACD REAL,

        -- Relative Strength Index
        RSI1 REAL,
        RSI2 REAL,

        -- Williams %R
        WR1 REAL,
        WR2 REAL,

        -- Commodity Channel Index
        CCI1 REAL,
        CCI2 REAL,

        -- Metadata columns (added by extraction_service.py)
        Date TEXT NOT NULL,  -- Format: YYYY-MM-DD (ISO 8601)
        Company TEXT NOT NULL,
        Industry TEXT NOT NULL,

        -- Primary key ensures no duplicate (Company, Date) pairs
        PRIMARY KEY (Company, Date)
    ) WITHOUT ROWID;
    """


def get_index_ddl() -> list[str]:
    """
    Returns DDL statements for all indexes.

    Indexes significantly improve query performance:
    - idx_industry: Filter by industry (common in gap analysis)
    - idx_date_range: Date range queries
    - idx_company_industry: Multi-column lookups

    Returns:
        List of CREATE INDEX SQL statements
    """
    return [
        "CREATE INDEX IF NOT EXISTS idx_industry ON data(Industry);",
        "CREATE INDEX IF NOT EXISTS idx_date_range ON data(Date);",
        "CREATE INDEX IF NOT EXISTS idx_company_industry ON data(Company, Industry);",
    ]


def get_schema_version_ddl() -> str:
    """
    Returns DDL for schema version tracking table.

    This enables migration detection and management.
    """
    return """
    CREATE TABLE IF NOT EXISTS schema_version (
        version INTEGER PRIMARY KEY,
        applied_date TEXT NOT NULL,
        description TEXT
    );
    """


def get_pragma_settings() -> list[str]:
    """
    Returns PRAGMA statements for optimal database configuration.

    - WAL mode: Better concurrency, crash recovery
    - NORMAL synchronous: Good balance of safety and performance
    - Larger cache: Improves query performance
    - MEMORY temp storage: Faster temporary operations

    Returns:
        List of PRAGMA SQL statements
    """
    return [
        "PRAGMA journal_mode=WAL;",
        "PRAGMA synchronous=NORMAL;",
        "PRAGMA cache_size=-64000;",  # 64 MB cache
        "PRAGMA temp_store=MEMORY;",
        "PRAGMA foreign_keys=ON;",
    ]


def initialize_database(db_path: Path) -> None:
    """
    Initialize a new database with complete schema.

    Creates:
    - Main data table with PRIMARY KEY
    - All indexes
    - Schema version table
    - Optimal PRAGMA settings

    Args:
        db_path: Path to database file

    Raises:
        sqlite3.Error: If database initialization fails
    """
    db_path = Path(db_path)
    db_path.parent.mkdir(exist_ok=True, parents=True)

    conn = None
    try:
        conn = sqlite3.connect(str(db_path))

        # Apply PRAGMA settings
        for pragma in get_pragma_settings():
            conn.execute(pragma)

        # Create schema version table
        conn.execute(get_schema_version_ddl())

        # Create main data table
        conn.execute(get_data_table_ddl())

        # Create indexes
        for index_ddl in get_index_ddl():
            conn.execute(index_ddl)

        # Record schema version
        conn.execute(
            """
            INSERT OR REPLACE INTO schema_version (version, applied_date, description)
            VALUES (?, datetime('now'), ?)
            """,
            (SCHEMA_VERSION, "Initial schema with PRIMARY KEY constraint"),
        )

        conn.commit()

    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        raise sqlite3.Error(f"Failed to initialize database: {e}") from e
    finally:
        if conn:
            conn.close()


def validate_schema(db_path: Path) -> SchemaInfo:
    """
    Validate database schema and return information.

    Checks:
    - Table existence
    - PRIMARY KEY constraint
    - Index existence
    - Row count

    Args:
        db_path: Path to database file

    Returns:
        SchemaInfo dataclass with validation results

    Raises:
        sqlite3.Error: If validation query fails
    """
    conn = None
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Check if data table exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (TABLE_NAME,),
        )
        table_exists = cursor.fetchone() is not None

        if not table_exists:
            return SchemaInfo(
                version=0,
                table_exists=False,
                has_primary_key=False,
                has_indexes=False,
                row_count=0,
            )

        # Check for PRIMARY KEY
        cursor.execute(f"PRAGMA table_info({TABLE_NAME})")
        columns = cursor.fetchall()
        has_primary_key = any(col[5] > 0 for col in columns)  # col[5] is pk field

        # Check for indexes
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='index' AND tbl_name=?",
            (TABLE_NAME,),
        )
        indexes = cursor.fetchall()
        has_indexes = len(indexes) >= 3  # We expect at least 3 indexes

        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
        row_count = cursor.fetchone()[0]

        # Get schema version
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='schema_version'"
        )
        version_table_exists = cursor.fetchone() is not None

        version = 0
        if version_table_exists:
            cursor.execute("SELECT MAX(version) FROM schema_version")
            result = cursor.fetchone()
            version = result[0] if result[0] is not None else 0

        return SchemaInfo(
            version=version,
            table_exists=table_exists,
            has_primary_key=has_primary_key,
            has_indexes=has_indexes,
            row_count=row_count,
        )

    except sqlite3.Error as e:
        raise sqlite3.Error(f"Schema validation failed: {e}") from e
    finally:
        if conn:
            conn.close()


def ensure_schema_up_to_date(db_path: Path) -> bool:
    """
    Ensure database schema is up to date.

    If database doesn't exist or schema is outdated, initializes/upgrades it.

    Args:
        db_path: Path to database file

    Returns:
        True if schema was created/updated, False if already up to date

    Raises:
        sqlite3.Error: If schema update fails
    """
    db_path = Path(db_path)

    if not db_path.exists():
        initialize_database(db_path)
        return True

    schema_info = validate_schema(db_path)

    if not schema_info.table_exists:
        initialize_database(db_path)
        return True

    if not schema_info.has_primary_key:
        # Schema needs migration - this will be handled by migration script
        raise SchemaValidationError(
            f"Database at {db_path} exists but lacks PRIMARY KEY constraint. "
            f"Run migration script to upgrade schema."
        )

    if schema_info.version < SCHEMA_VERSION:
        # Future migrations would go here
        pass

    return False


def check_data_integrity(db_path: Path) -> dict:
    """
    Perform integrity checks on the database.

    Checks:
    - SQLite integrity (PRAGMA integrity_check)
    - No duplicate (Company, Date) pairs
    - Date format validation
    - Price validation (positive values, High >= Low)

    Args:
        db_path: Path to database file

    Returns:
        Dictionary with check results and any violations found
    """
    import pandas as pd

    conn = None
    try:
        conn = sqlite3.connect(str(db_path))

        results = {
            "sqlite_integrity": None,
            "duplicate_rows": 0,
            "invalid_dates": 0,
            "invalid_prices": 0,
            "violations": [],
        }

        # SQLite integrity check
        cursor = conn.cursor()
        cursor.execute("PRAGMA integrity_check")
        integrity_result = cursor.fetchone()[0]
        results["sqlite_integrity"] = integrity_result

        if integrity_result != "ok":
            results["violations"].append(
                f"SQLite integrity check failed: {integrity_result}"
            )

        # Check for duplicates (shouldn't exist with PRIMARY KEY, but verify)
        cursor.execute(
            f"""
            SELECT Company, Date, COUNT(*) as cnt
            FROM {TABLE_NAME}
            GROUP BY Company, Date
            HAVING cnt > 1
        """
        )
        duplicates = cursor.fetchall()
        results["duplicate_rows"] = len(duplicates)

        if duplicates:
            results["violations"].append(
                f"Found {len(duplicates)} duplicate (Company, Date) pairs: {duplicates[:5]}"
            )

        # Check date format (ISO 8601: YYYY-MM-DD)
        cursor.execute(
            f"""
            SELECT COUNT(*) FROM {TABLE_NAME}
            WHERE Date NOT LIKE '____-__-__'
               OR length(Date) != 10
        """
        )
        invalid_dates = cursor.fetchone()[0]
        results["invalid_dates"] = invalid_dates

        if invalid_dates > 0:
            results["violations"].append(
                f"Found {invalid_dates} rows with invalid date format"
            )

        # Check price constraints (High >= Low, all positive)
        cursor.execute(
            f"""
            SELECT COUNT(*) FROM {TABLE_NAME}
            WHERE High < Low
               OR Open <= 0
               OR High <= 0
               OR Low <= 0
               OR Close <= 0
        """
        )
        invalid_prices = cursor.fetchone()[0]
        results["invalid_prices"] = invalid_prices

        if invalid_prices > 0:
            results["violations"].append(
                f"Found {invalid_prices} rows with invalid prices"
            )

        return results

    except sqlite3.Error as e:
        raise sqlite3.Error(f"Integrity check failed: {e}") from e
    finally:
        if conn:
            conn.close()


def get_table_stats(db_path: Path) -> dict:
    """
    Get statistics about the data table.

    Returns:
        Dictionary with:
        - total_rows: Total number of rows
        - companies: Number of unique companies
        - industries: List of unique industries
        - date_range: (min_date, max_date)
        - database_size: File size in bytes
    """
    import pandas as pd

    conn = None
    try:
        conn = sqlite3.connect(str(db_path))

        stats = {}

        # Total rows
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}")
        stats["total_rows"] = cursor.fetchone()[0]

        # Unique companies
        cursor.execute(f"SELECT COUNT(DISTINCT Company) FROM {TABLE_NAME}")
        stats["companies"] = cursor.fetchone()[0]

        # Industries
        cursor.execute(f"SELECT DISTINCT Industry FROM {TABLE_NAME} ORDER BY Industry")
        stats["industries"] = [row[0] for row in cursor.fetchall()]

        # Date range
        cursor.execute(f"SELECT MIN(Date), MAX(Date) FROM {TABLE_NAME}")
        result = cursor.fetchone()
        stats["date_range"] = (result[0], result[1]) if result[0] else (None, None)

        # Database file size
        db_path = Path(db_path)
        if db_path.exists():
            stats["database_size"] = db_path.stat().st_size
        else:
            stats["database_size"] = 0

        return stats

    except sqlite3.Error as e:
        raise sqlite3.Error(f"Failed to get table stats: {e}") from e
    finally:
        if conn:
            conn.close()

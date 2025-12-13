# -*- coding: utf-8 -*-
"""
Gap Analysis Reporting Module

Provides human-readable and machine-readable reporting utilities
for gap analysis results.
"""

import json
from pathlib import Path
from typing import Dict, List
import pandas as pd

from .gap_analyzer import GapAnalysisResult


class GapReporter:
    """Generate human-readable and exportable gap analysis reports."""

    @staticmethod
    def print_summary(result: GapAnalysisResult):
        """
        Print console-friendly summary.

        Args:
            result: Gap analysis result to report
        """
        print(f"\n{'='*70}")
        print(f"Gap Analysis Summary: {result.industry}")
        print(f"{'='*70}")

        # Date range
        print(
            f"\nRequested Date Range: {result.requested_start} to {result.requested_end}"
        )
        if result.actual_start:
            print(f"Actual Date Range:    {result.actual_start} to {result.actual_end}")
        else:
            print(f"Actual Date Range:    (no data)")

        # Coverage metrics
        print(f"\nCoverage Metrics:")
        print(
            f"  Company Coverage: {result.coverage_pct:>6.1%} "
            f"({len(result.actual_companies)}/{len(result.expected_companies)} companies)"
        )
        print(f"  Date Coverage:    {result.date_coverage_pct:>6.1%}")

        # Missing companies
        if result.missing_companies:
            print(f"\n  Missing Companies ({len(result.missing_companies)}):")
            # Show first 10
            for comp in result.missing_companies[:10]:
                print(f"    - {comp}")
            if len(result.missing_companies) > 10:
                remaining = len(result.missing_companies) - 10
                print(f"    ... and {remaining} more")

        # Incomplete companies
        if result.incomplete_companies:
            print(f"\n  Incomplete Companies ({len(result.incomplete_companies)}):")
            # Show first 5 with gap counts
            for comp in result.incomplete_companies[:5]:
                gaps = result.company_specific_gaps.get(comp, [])
                print(f"    - {comp}: {len(gaps)} missing days")
            if len(result.incomplete_companies) > 5:
                remaining = len(result.incomplete_companies) - 5
                print(f"    ... and {remaining} more")

        # Missing date ranges
        if result.missing_date_ranges:
            print(f"\n  Missing Date Ranges:")
            for i, (start, end) in enumerate(result.missing_date_ranges[:3]):
                days = (end - start).days + 1
                print(f"    - {start} to {end} ({days} days)")
            if len(result.missing_date_ranges) > 3:
                remaining = len(result.missing_date_ranges) - 3
                print(f"    ... and {remaining} more ranges")

        # Recommendations
        print(f"\n{'='*70}")
        print(f"Recommended Actions:")
        print(f"{'='*70}")

        actions = []
        if result.needs_company_download:
            actions.append(
                f"  [ ] Download {len(result.missing_companies)} missing companies"
            )
        if result.needs_date_extension:
            days_to_extend = (
                (result.requested_end - result.actual_end).days
                if result.actual_end
                else 0
            )
            actions.append(
                f"  [ ] Extend data to {result.requested_end} ({days_to_extend} days)"
            )
        if result.needs_backfill:
            actions.append(
                f"  [ ] Backfill gaps for {len(result.incomplete_companies)} companies"
            )

        if actions:
            for action in actions:
                print(action)
        else:
            print("  ✓ Database is complete - no action needed!")

        # Cost estimate
        print(f"\n  Estimated API Calls: {result.estimated_api_calls}")
        print(f"{'='*70}\n")

    @staticmethod
    def print_compact_summary(result: GapAnalysisResult):
        """
        Print a compact one-line summary.

        Args:
            result: Gap analysis result to report
        """
        status_parts = []

        if result.needs_company_download:
            status_parts.append(f"{len(result.missing_companies)} missing cos")

        if result.needs_backfill:
            status_parts.append(f"{len(result.incomplete_companies)} incomplete")

        if result.needs_date_extension:
            days = (
                (result.requested_end - result.actual_end).days
                if result.actual_end
                else 0
            )
            status_parts.append(f"{days} days behind")

        if status_parts:
            status = ", ".join(status_parts)
            print(f"{result.industry}: {status} ({result.coverage_pct:.1%} coverage)")
        else:
            print(f"{result.industry}: ✓ Complete ({result.coverage_pct:.1%} coverage)")

    @staticmethod
    def export_to_json(result: GapAnalysisResult, output_file: Path):
        """
        Export gap analysis as JSON for programmatic use.

        Args:
            result: Gap analysis result to export
            output_file: Path to JSON output file
        """
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w") as f:
            json.dump(result.to_dict(), f, indent=2)

    @staticmethod
    def export_to_csv(company_gaps: Dict[str, List], output_file: Path):
        """
        Export per-company gap details as CSV.

        Args:
            company_gaps: Dict mapping company to list of missing dates
            output_file: Path to CSV output file
        """
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        rows = []
        for company, dates in company_gaps.items():
            for missing_date in dates:
                rows.append(
                    {
                        "Company": company,
                        "Missing_Date": (
                            missing_date.isoformat()
                            if hasattr(missing_date, "isoformat")
                            else str(missing_date)
                        ),
                    }
                )

        # Ensure DataFrame has correct columns even when empty
        if not rows:
            df = pd.DataFrame(columns=["Company", "Missing_Date"])
        else:
            df = pd.DataFrame(rows)

        df.to_csv(output_file, index=False)

    @staticmethod
    def export_missing_companies_csv(missing_companies: List[str], output_file: Path):
        """
        Export list of missing companies as CSV.

        Args:
            missing_companies: List of company tickers
            output_file: Path to CSV output file
        """
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        df = pd.DataFrame({"Company": missing_companies})
        df.to_csv(output_file, index=False)

    @staticmethod
    def generate_markdown_report(result: GapAnalysisResult, output_file: Path):
        """
        Generate a detailed markdown report.

        Args:
            result: Gap analysis result to report
            output_file: Path to markdown output file
        """
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            f"# Gap Analysis Report: {result.industry}",
            "",
            f"**Generated**: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Summary",
            "",
            f"- **Requested Date Range**: {result.requested_start} to {result.requested_end}",
            f"- **Actual Date Range**: {result.actual_start or 'N/A'} to {result.actual_end or 'N/A'}",
            f"- **Company Coverage**: {result.coverage_pct:.1%} ({len(result.actual_companies)}/{len(result.expected_companies)})",
            f"- **Date Coverage**: {result.date_coverage_pct:.1%}",
            "",
            "## Missing Companies",
            "",
        ]

        if result.missing_companies:
            lines.append(f"Total: {len(result.missing_companies)} companies")
            lines.append("")
            for comp in result.missing_companies:
                lines.append(f"- {comp}")
        else:
            lines.append("✓ No missing companies")

        lines.extend(
            [
                "",
                "## Incomplete Companies",
                "",
            ]
        )

        if result.incomplete_companies:
            lines.append(f"Total: {len(result.incomplete_companies)} companies")
            lines.append("")
            lines.append("| Company | Missing Days |")
            lines.append("|---------|--------------|")
            for comp in result.incomplete_companies:
                gaps = result.company_specific_gaps.get(comp, [])
                lines.append(f"| {comp} | {len(gaps)} |")
        else:
            lines.append("✓ No incomplete companies")

        lines.extend(
            [
                "",
                "## Missing Date Ranges",
                "",
            ]
        )

        if result.missing_date_ranges:
            lines.append("| Start | End | Days |")
            lines.append("|-------|-----|------|")
            for start, end in result.missing_date_ranges:
                days = (end - start).days + 1
                lines.append(f"| {start} | {end} | {days} |")
        else:
            lines.append("✓ No missing date ranges")

        lines.extend(
            [
                "",
                "## Recommendations",
                "",
            ]
        )

        if result.needs_company_download:
            lines.append(
                f"- [ ] Download {len(result.missing_companies)} missing companies"
            )
        if result.needs_date_extension:
            days = (
                (result.requested_end - result.actual_end).days
                if result.actual_end
                else 0
            )
            lines.append(f"- [ ] Extend data to {result.requested_end} ({days} days)")
        if result.needs_backfill:
            lines.append(
                f"- [ ] Backfill gaps for {len(result.incomplete_companies)} companies"
            )

        if not (
            result.needs_company_download
            or result.needs_date_extension
            or result.needs_backfill
        ):
            lines.append("✓ Database is complete - no action needed!")

        lines.extend(
            [
                "",
                f"**Estimated API Calls**: {result.estimated_api_calls}",
                "",
            ]
        )

        with open(output_file, "w") as f:
            f.write("\n".join(lines))

    @staticmethod
    def print_multiple_industries(results: Dict[str, GapAnalysisResult]):
        """
        Print summary for multiple industries.

        Args:
            results: Dict mapping industry name to GapAnalysisResult
        """
        print(f"\n{'='*70}")
        print(f"Multi-Industry Gap Analysis")
        print(f"{'='*70}\n")

        for industry, result in results.items():
            GapReporter.print_compact_summary(result)

        # Overall statistics
        total_missing = sum(len(r.missing_companies) for r in results.values())
        total_incomplete = sum(len(r.incomplete_companies) for r in results.values())
        total_api_calls = sum(r.estimated_api_calls for r in results.values())

        print(f"\n{'='*70}")
        print(f"Overall Statistics:")
        print(f"  Total Missing Companies:    {total_missing}")
        print(f"  Total Incomplete Companies: {total_incomplete}")
        print(f"  Total Estimated API Calls:  {total_api_calls}")
        print(f"{'='*70}\n")

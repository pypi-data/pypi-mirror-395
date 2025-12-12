"""Utility functions for measurement analysis."""

from __future__ import annotations

import pathlib
from datetime import datetime
from functools import lru_cache
from typing import Any

from metsuperq.analysis.constants import MAX_PROJECT_ROOT_DEPTH, SECONDS_TO_MICROSECONDS
from metsuperq.utils import read_json, setup_logging, write_json

logger = setup_logging(__name__)


@lru_cache(maxsize=1)
def get_project_root() -> pathlib.Path:
    """Find project root directory.

    Searches upward from current location for project markers like:
    - pyproject.toml
    - setup.py
    - .git directory
    - metsuperq package directory

    Returns
    -------
    pathlib.Path
        Absolute path to project root
    """
    # Start from the module's location
    current_path = pathlib.Path(__file__).resolve().parent

    # Prefer explicit repository markers
    repo_markers = ["pyproject.toml", ".git", "setup.py"]

    # Traverse upwards with a sane max depth to avoid infinite loops under mocks
    for _ in range(MAX_PROJECT_ROOT_DEPTH):
        # Check for explicit repo markers first using any() for early exit
        try:
            found_marker = next((m for m in repo_markers if (current_path / m).exists()), None)
            if found_marker:
                logger.debug("Auto-detected project root via '%s': %s", found_marker, current_path)
                return current_path
        except OSError:
            logger.debug("Failed to check for repository markers at %s", current_path)

        # If we are at the package directory (e.g., 'metsuperq'), prefer its parent as project root
        try:
            if getattr(current_path, "name", None) == "metsuperq":
                parent = current_path.parent
                # If parent has typical repo markers, treat it as the project root
                if (parent / "pyproject.toml").exists() or (parent / ".git").exists():
                    logger.debug("Detected project root at package parent: %s", parent)
                    return parent
        except OSError:
            logger.debug("Failed to check for repository markers at %s", current_path)

        # Move up one directory
        try:
            current_path = current_path.parent
        except (OSError, AttributeError):
            logger.debug("Failed to move up one directory at %s", current_path)
            break

    # Fallback: use current working directory
    fallback_path = pathlib.Path.cwd()
    logger.warning("Could not find project root via markers, using fallback: %s", fallback_path)
    return fallback_path


# Type aliases
AnalysisResult = dict[str, Any]


def save_analysis_results(analysis_result: AnalysisResult, output_path: pathlib.Path) -> None:
    """Save analysis results to JSON file.

    Parameters
    ----------
    analysis_result : AnalysisResult
        Analysis results to save
    output_path : pathlib.Path
        Path for output JSON file
    """
    logger.debug("Saving analysis results to: %s", output_path)

    # Add analysis timestamp
    result_with_timestamp = analysis_result.copy()
    result_with_timestamp["analysis_timestamp"] = datetime.now().isoformat()

    try:
        write_json(result_with_timestamp, output_path)
        logger.info("Analysis results saved to: %s", output_path)
    except OSError as e:
        logger.error("Failed to save analysis results: %s", e, exc_info=True)
        raise


def load_analysis_results(input_path: pathlib.Path) -> AnalysisResult:
    """Load analysis results from JSON file.

    Parameters
    ----------
    input_path : pathlib.Path
        Path to JSON file containing analysis results

    Returns
    -------
    AnalysisResult
        Loaded analysis results

    Raises
    ------
    FileNotFoundError
        If the results file doesn't exist
    """
    logger.debug("Loading analysis results from: %s", input_path)

    try:
        results = read_json(input_path)
        logger.info("Analysis results loaded from: %s", input_path)
        return results
    except (OSError, ValueError) as e:
        logger.error("Failed to load analysis results: %s", e, exc_info=True)
        raise


def create_summary_report(analysis_result: AnalysisResult) -> str:  # noqa: C901, PLR0912, PLR0915
    """Create a text summary report of analysis results.

    Parameters
    ----------
    analysis_result : AnalysisResult
        Analysis results to summarize

    Returns
    -------
    str
        Formatted summary report
    """
    logger.debug("Creating summary report")

    report_lines = []
    report_lines.append("=== Measurement Analysis Report ===")
    report_lines.append("")

    # Basic info
    filepath = analysis_result.get("filepath", "Unknown")
    timestamp = analysis_result.get("analysis_timestamp", "Unknown")
    report_lines.append(f"Data file: {filepath}")
    report_lines.append(f"Analysis timestamp: {timestamp}")
    report_lines.append("")

    # Fit results
    fits = analysis_result.get("fits", {})
    if fits:
        report_lines.append("=== Fit Results ===")
        for meas_type, fit_result in fits.items():
            if fit_result.get("fit_success", False):
                decay_time = fit_result.get("decay_time", 0)
                decay_stderr = fit_result.get("decay_time_stderr", 0)
                amplitude = fit_result.get("amplitude", 0)
                r_squared = fit_result.get("r_squared", 0)

                report_lines.append(f"{meas_type.upper()}:")
                # Convert to microseconds for better readability
                decay_time_us = decay_time * SECONDS_TO_MICROSECONDS
                decay_stderr_us = decay_stderr * SECONDS_TO_MICROSECONDS
                report_lines.append(f"  Decay time: {decay_time_us:.1f} ± {decay_stderr_us:.1f} μs")
                report_lines.append(f"  Amplitude: {amplitude:.3f}")
                report_lines.append(f"  R²: {r_squared:.3f}")
            else:
                report_lines.append(f"{meas_type.upper()}: Fit failed")
            report_lines.append("")

    # Derived quantities
    derived = analysis_result.get("derived_quantities", {})
    if derived:
        report_lines.append("=== Derived Quantities ===")
        for key, value in derived.items():
            if not key.endswith("_stderr") and isinstance(value, (int, float)):
                stderr_key = f"{key}_stderr"
                stderr = derived.get(stderr_key, 0)
                clean_key = key.replace("_", " ").title()
                # Convert to microseconds for better readability
                value_us = value * SECONDS_TO_MICROSECONDS
                stderr_us = stderr * SECONDS_TO_MICROSECONDS
                report_lines.append(f"{clean_key}: {value_us:.1f} ± {stderr_us:.1f} μs")

    # Physics validation results
    physics_validation = analysis_result.get("physics_validation", {})
    if physics_validation:
        report_lines.append("")
        report_lines.append("=== Physics Validation ===")
        is_valid = physics_validation.get("is_valid", True)
        violations = physics_validation.get("violations", [])
        warnings = physics_validation.get("warnings", [])

        if is_valid:
            report_lines.append("Status: ✓ PASSED - All coherence times are physically valid")
        else:
            report_lines.append("Status: ✗ FAILED - Physics constraints violated!")

        if violations:
            report_lines.append("")
            report_lines.append("Violations:")
            for violation in violations:
                report_lines.append(f"  • {violation}")

        if warnings:
            report_lines.append("")
            report_lines.append("Warnings:")
            for warning in warnings:
                report_lines.append(f"  • {warning}")

    report = "\n".join(report_lines)
    logger.debug("Summary report created with %d lines", len(report_lines))
    return report


def save_summary_report(analysis_result: AnalysisResult, output_path: pathlib.Path) -> None:
    """Save a text summary report to file.

    Parameters
    ----------
    analysis_result : AnalysisResult
        Analysis results to summarize
    output_path : pathlib.Path
        Path for output text file
    """
    logger.debug("Saving summary report to: %s", output_path)

    report = create_summary_report(analysis_result)

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
        logger.info("Summary report saved to: %s", output_path)
    except OSError as e:
        logger.error("Failed to save summary report: %s", e, exc_info=True)
        raise

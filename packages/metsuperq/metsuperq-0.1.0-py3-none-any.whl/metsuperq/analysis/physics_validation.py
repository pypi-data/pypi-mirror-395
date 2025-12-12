"""Physics validation for quantum measurement analysis.

This module enforces fundamental quantum physics constraints on coherence times
and other measurement parameters.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from metsuperq.utils import setup_logging

logger = setup_logging(__name__)

# Type alias
AnalysisResult = dict[str, Any]

# Physics validation constants
MAX_COHERENCE_TIME_SECONDS = 3600  # 1 hour - catches unit conversion errors
MAX_RAMSEY_FREQUENCY_HZ = 10e6  # 10 MHz - typical upper limit
MIN_RAMSEY_FREQUENCY_HZ = 100  # 100 Hz - typical lower limit


class PhysicsViolationError(Exception):
    """Exception raised when measurement results violate fundamental physics laws.

    This indicates either:
    - Bad measurement data
    - Incorrect fitting
    - Hardware malfunction
    - Wrong measurement type assignment
    """

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        """Initialize physics violation error.

        Parameters
        ----------
        message : str
            Error description
        details : dict[str, Any] | None
            Additional context about the violation
        """
        super().__init__(message)
        self.details = details or {}


@dataclass
class CoherenceTimeValidation:
    """Results of coherence time physics validation."""

    is_valid: bool
    violations: list[str]
    warnings: list[str]
    t1: float | None = None
    t2_echo: float | None = None
    t2_ramsey: float | None = None


def validate_coherence_times(  # noqa: C901
    analysis_result: AnalysisResult, strict: bool = False
) -> CoherenceTimeValidation:
    """Validate coherence times against fundamental physics constraints.

    Enforces the quantum physics constraint: T2 ≤ 2×T1

    This is a fundamental law for qubits:
    - T1: Energy relaxation time (population decay)
    - T2: Phase coherence time (dephasing)
    - T2*: Ramsey dephasing time (includes inhomogeneous broadening)

    The relationship T2 ≤ 2×T1 comes from the fact that energy relaxation
    (T1 process) also causes dephasing. In the absence of pure dephasing,
    T2 = 2×T1. Any pure dephasing reduces T2 below this limit.

    Parameters
    ----------
    analysis_result : AnalysisResult
        Analysis results containing derived quantities
    strict : bool, optional
        If True, raise exception on violation. If False, only log warnings.
        Default: False

    Returns
    -------
    CoherenceTimeValidation
        Validation results with violations and warnings

    Raises
    ------
    PhysicsViolationError
        If strict=True and physics constraints are violated
    """
    derived = analysis_result.get("derived_quantities", {})

    t1 = derived.get("T1")
    t2_echo = derived.get("T2_echo")
    t2_ramsey = derived.get("T2_ramsey")

    violations: list[str] = []
    warnings: list[str] = []

    # Validate T2_echo ≤ 2×T1
    if t1 is not None and t2_echo is not None:
        if t2_echo > 2 * t1:
            violation_msg = (
                f"PHYSICS VIOLATION: T2_echo ({t2_echo:.3e} s) > 2×T1 ({2 * t1:.3e} s). "
                f"This violates fundamental quantum mechanics! "
                f"Ratio: T2/2T1 = {t2_echo / (2 * t1):.2f}"
            )
            violations.append(violation_msg)
            logger.error(violation_msg)

        # Warn if T2 is suspiciously close to 2×T1 (might indicate fitting issues)
        elif t2_echo > 1.9 * t1:
            warning_msg = (
                f"T2_echo ({t2_echo:.3e} s) is very close to 2×T1 ({2 * t1:.3e} s). "
                f"Ratio: {t2_echo / (2 * t1):.2f}. This is unusual - check fit quality."
            )
            warnings.append(warning_msg)
            logger.warning(warning_msg)

    # Validate T2* ≤ T2_echo (Ramsey should be shorter than echo)
    if t2_ramsey is not None and t2_echo is not None:
        if t2_ramsey > t2_echo:
            # This is unusual but not strictly forbidden (can happen with specific noise)
            warning_msg = (
                f"T2* ({t2_ramsey:.3e} s) > T2_echo ({t2_echo:.3e} s). "
                f"This is unusual but possible with certain noise characteristics. "
                f"Verify measurement setup."
            )
            warnings.append(warning_msg)
            logger.warning(warning_msg)

    # Validate T2* ≤ 2×T1
    if t1 is not None and t2_ramsey is not None:
        if t2_ramsey > 2 * t1:
            violation_msg = (
                f"PHYSICS VIOLATION: T2* ({t2_ramsey:.3e} s) > 2×T1 ({2 * t1:.3e} s). "
                f"This violates fundamental quantum mechanics! "
                f"Ratio: T2*/2T1 = {t2_ramsey / (2 * t1):.2f}"
            )
            violations.append(violation_msg)
            logger.error(violation_msg)

    # Check coherence time validity in a single pass
    coherence_times = [("T1", t1), ("T2_echo", t2_echo), ("T2_ramsey", t2_ramsey)]
    for name, value in coherence_times:
        if value is None:
            continue

        # Check for negative or zero coherence times
        if value <= 0:
            violation_msg = (
                f"PHYSICS VIOLATION: {name} = {value:.3e} s ≤ 0. Coherence times must be positive!"
            )
            violations.append(violation_msg)
            logger.error(violation_msg)
        # Check for unreasonably large coherence times (> 1 hour) - catches unit conversion errors
        elif value > MAX_COHERENCE_TIME_SECONDS:
            warning_msg = (
                f"{name} = {value:.3e} s (> 1 hour). "
                f"This is extremely long for a qubit. Check units!"
            )
            warnings.append(warning_msg)
            logger.warning(warning_msg)

    validation = CoherenceTimeValidation(
        is_valid=len(violations) == 0,
        violations=violations,
        warnings=warnings,
        t1=t1,
        t2_echo=t2_echo,
        t2_ramsey=t2_ramsey,
    )

    # Raise exception if strict mode and violations found
    if strict and not validation.is_valid:
        raise PhysicsViolationError(
            f"Physics validation failed with {len(violations)} violation(s)",
            details={
                "violations": violations,
                "warnings": warnings,
                "t1": t1,
                "t2_echo": t2_echo,
                "t2_ramsey": t2_ramsey,
            },
        )

    return validation


def validate_ramsey_parameters(
    frequency: float, phase: float, amplitude: float, baseline: float
) -> list[str]:
    """Validate Ramsey fit parameters for physical reasonableness.

    Parameters
    ----------
    frequency : float
        Detuning frequency in Hz
    phase : float
        Phase in radians
    amplitude : float
        Oscillation amplitude
    baseline : float
        Baseline offset

    Returns
    -------
    list[str]
        List of warning messages (empty if all valid)
    """
    warnings: list[str] = []

    # Check frequency range (typical: 1 kHz - 1 MHz for superconducting qubits)
    if abs(frequency) > MAX_RAMSEY_FREQUENCY_HZ:
        warnings.append(
            f"Ramsey frequency {frequency:.1e} Hz is very large (> 10 MHz). "
            f"Check if this is expected for your system."
        )
    elif abs(frequency) < MIN_RAMSEY_FREQUENCY_HZ:
        warnings.append(
            f"Ramsey frequency {frequency:.1f} Hz is very small (< 100 Hz). "
            f"May be difficult to resolve within T2*."
        )

    # Check phase wrapping
    if abs(phase) > np.pi:
        warnings.append(
            f"Phase {phase:.2f} rad is outside [-π, π]. Consider wrapping to principal value."
        )

    # Check amplitude
    if amplitude < 0:
        warnings.append(f"Negative amplitude {amplitude:.3f}. This is unusual.")

    # Check baseline
    if baseline < 0:
        warnings.append(
            f"Negative baseline {baseline:.3f}. This might indicate readout calibration issues."
        )

    return warnings

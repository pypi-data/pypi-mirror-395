"""Measurement analyzer."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

import h5py
import matplotlib.pyplot as plt
import numpy as np
from lmfit import Model, Parameters
from lmfit.models import ExponentialModel

from metsuperq.analysis.constants import (
    DEFAULT_DECAY_TIME_S,
    DEFAULT_FIT_POINTS,
    DEFAULT_FREQUENCY_HZ,
    DEFAULT_MEASUREMENT_TYPE,
    EXPECTED_DATASET_ROWS,
    HDF5_PATTERN,
    MAX_FREQUENCY_HZ,
    MAX_TIME_SCALE_ERROR,
    MAX_TIME_SCALE_WARNING,
    MEASUREMENT_TYPES,
    MIN_DECAY_TIME_S,
    MIN_OSCILLATIONS_FOR_FIT,
    MIN_POINTS_FOR_FFT,
    MIN_POINTS_PER_OSCILLATION,
    PLOT_CONFIG,
    SECONDS_TO_MICROSECONDS,
)
from metsuperq.analysis.physics_validation import (
    validate_coherence_times,
    validate_ramsey_parameters,
)
from metsuperq.analysis.utils import get_project_root, save_analysis_results, save_summary_report
from metsuperq.utils import setup_logging

logger = setup_logging(__name__)

# Type aliases
AnalysisResult = dict[str, Any]
FitResult = dict[str, Any]
DatasetDict = dict[str, np.ndarray]
MetadataDict = dict[str, Any]


@dataclass
class RamseyParams:
    """Parameters for Ramsey decay function."""

    amp: float
    tau: float
    freq: float
    phi: float
    base: float


class BaseAnalyzer:
    """Measurement analyzer.

    Provides a unified interface for:
    - Finding and loading HDF5 measurement files
    - Exponential decay fitting for T1, T2 echo, T2 Ramsey measurements
    - Visualization and results export
    - Complete analysis pipeline from TUID to results
    """

    def __init__(self, data_path: Path | str | None = None) -> None:
        """Initialize analyzer with data directory path.

        Parameters
        ----------
        data_path : Path | str | None, optional
            Path to directory containing HDF5 files.
            If None, automatically detects project root and uses 'data' subdirectory.

        Attributes
        ----------
        data_path : Path
            Path to directory containing HDF5 files
        """
        if data_path is not None:
            self.data_path = Path(data_path)
        else:
            self.data_path = get_project_root() / "data"

        logger.info("Initialized BaseAnalyzer with data path: %s", self.data_path)

    def find_hdf5_file(self, tuid: str) -> Path | None:
        """Find HDF5 file based on TUID."""
        logger.debug("Searching for HDF5 file with TUID: %s", tuid)
        logger.debug("Searching in data path: %s", self.data_path)

        # First, check if data_path itself is a TUID directory
        if self.data_path.name == tuid:
            logger.debug("Data path matches TUID, searching directly in: %s", self.data_path)
            for hdf5_file in self.data_path.glob("*.hdf5"):
                logger.info("Found HDF5 file in TUID directory: %s", hdf5_file)
                return hdf5_file

        # Search for files containing the TUID in filename
        for hdf5_file in self.data_path.glob(HDF5_PATTERN):
            if tuid in hdf5_file.stem:
                logger.info("Found HDF5 file: %s", hdf5_file)
                return hdf5_file

        # Search in subdirectories named with the TUID
        tuid_subdir = self.data_path / tuid
        if tuid_subdir.exists() and tuid_subdir.is_dir():
            logger.debug("Searching in TUID subdirectory: %s", tuid_subdir)
            for hdf5_file in tuid_subdir.glob("*.hdf5"):
                logger.info("Found HDF5 file in TUID subdirectory: %s", hdf5_file)
                return hdf5_file

        logger.error("No HDF5 file found for TUID: %s", tuid)
        logger.error("Searched in: %s and subdirectories", self.data_path)
        return None

    def _build_dataset_name_map(self, subgroup_keys: Iterable[str]) -> dict[str, dict[str, str]]:
        """Build a map of base dataset names from HDF5 subgroup keys."""
        bases: dict[str, dict[str, str]] = {}
        for ds_name in subgroup_keys:
            if ds_name.endswith("_time"):
                base = ds_name[: -len("_time")]
                bases.setdefault(base, {})["time"] = ds_name
            elif ds_name.endswith("_iq"):
                base = ds_name[: -len("_iq")]
                bases.setdefault(base, {})["iq"] = ds_name
            else:
                bases.setdefault(ds_name, {})["combined"] = ds_name
        return bases

    def _load_combined_dataset(self, subgroup: h5py.Group, dataset_name: str) -> np.ndarray | None:
        """Load a combined dataset from HDF5 subgroup."""
        ds = subgroup[dataset_name]
        if isinstance(ds, h5py.Dataset):
            return ds[:]
        return None

    def _load_time_iq_pair(
        self, subgroup: h5py.Group, time_name: str, iq_name: str
    ) -> np.ndarray | None:
        """Load and combine time/IQ pair datasets."""
        ds_time = subgroup[time_name]
        ds_iq = subgroup[iq_name]
        if isinstance(ds_time, h5py.Dataset) and isinstance(ds_iq, h5py.Dataset):
            time_arr = np.asarray(ds_time[:])
            iq_arr = np.asarray(ds_iq[:])
            # Reconstruct into 2xN array (complex dtype for compatibility)
            return np.vstack(
                [
                    time_arr.astype(np.complex128),
                    iq_arr.astype(np.complex128),
                ]
            )
        return None

    def _process_subgroup_datasets(
        self, subgroup: h5py.Group, subgroup_name: str
    ) -> dict[str, np.ndarray]:
        """Process all datasets in a single HDF5 subgroup."""
        datasets: dict[str, np.ndarray] = {}
        # subgroup.keys() returns a KeysViewHDF5 which is iterable - no need for list()
        bases = self._build_dataset_name_map(subgroup.keys())

        for base, parts in bases.items():
            try:
                result = None
                if "combined" in parts:
                    result = self._load_combined_dataset(subgroup, parts["combined"])
                elif "time" in parts and "iq" in parts:
                    result = self._load_time_iq_pair(subgroup, parts["time"], parts["iq"])

                if result is not None:
                    datasets[f"{subgroup_name}_{base}"] = result
            except (OSError, KeyError, ValueError) as e:
                logger.warning(
                    "Failed to load dataset '%s' in subgroup '%s': %s", base, subgroup_name, e
                )
        return datasets

    def load_measurement_data(
        self, filepath: Path, measurement_type: str = DEFAULT_MEASUREMENT_TYPE
    ) -> tuple[MetadataDict, DatasetDict]:
        """Load measurement data and metadata from HDF5 file."""
        logger.debug("Loading data from file: %s", filepath)

        try:
            with h5py.File(filepath, "r") as f:
                if measurement_type not in f:
                    raise KeyError(f"Measurement type '{measurement_type}' not found")

                group = cast(h5py.Group, f[measurement_type])
                metadata = dict(group.attrs)
                datasets: dict[str, np.ndarray] = {}

                # Load all datasets from measurement iterations
                for subgroup_name in group.keys():
                    subgroup_item = group[subgroup_name]
                    if isinstance(subgroup_item, h5py.Group):
                        subgroup_datasets = self._process_subgroup_datasets(
                            subgroup_item, subgroup_name
                        )
                        datasets.update(subgroup_datasets)

                logger.debug(
                    "Loaded %d datasets with %d metadata fields", len(datasets), len(metadata)
                )
                return metadata, datasets

        except Exception as e:
            logger.error("Error loading data from %s: %s", filepath, e, exc_info=True)
            raise

    def _extract_time_amplitude_data(self, dataset: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Extract time delays and amplitude data from complex dataset.

        Parameters
        ----------
        dataset : np.ndarray
            Complex dataset with shape (2, N) where first row is time delays
            and second row is complex I-Q measurements

        Returns
        -------
        tuple[np.ndarray, np.ndarray]
            Time delays and amplitude magnitudes
        """
        if dataset.shape[0] != EXPECTED_DATASET_ROWS:
            raise ValueError(
                f"Expected dataset with {EXPECTED_DATASET_ROWS} rows, got {dataset.shape[0]}"
            )

        # First row contains time delays (real part only)
        time_delays = np.real(dataset[0, :])

        # Second row contains complex I-Q measurements
        iq_data = dataset[1, :]
        amplitudes = np.abs(iq_data)

        logger.debug(
            "Extracted %d time points from %.2f to %.2f",
            len(time_delays),
            time_delays.min(),
            time_delays.max(),
        )

        return time_delays, amplitudes

    def _ramsey_decay_func(self, t: np.ndarray, params: RamseyParams) -> np.ndarray:
        """T2-Ramsey decaying sine function: A * exp(-t/T2*) * cos(2πft + φ) + B.

        Parameters
        ----------
        t : np.ndarray
            Time values
        params : RamseyParams
            Ramsey fit parameters (amp, tau, freq, phi, base)

        Returns
        -------
        np.ndarray
            Function values
        """
        return (
            params.amp * np.exp(-t / params.tau) * np.cos(2 * np.pi * params.freq * t + params.phi)
            + params.base
        )

    def _ramsey_decay_lmfit(self, t: np.ndarray, **kwargs: float) -> np.ndarray:
        """Provide fit wrapper for lmfit Model that uses individual parameters."""
        params = RamseyParams(
            amp=kwargs["amp"],
            tau=kwargs["tau"],
            freq=kwargs["freq"],
            phi=kwargs["phi"],
            base=kwargs["base"],
        )
        return self._ramsey_decay_func(t, params)

    def fit_exponential_decay(
        self, time_data: np.ndarray, amplitude_data: np.ndarray, measurement_type: str = "T1"
    ) -> FitResult:
        """Fit exponential decay model to measurement data.

        Parameters
        ----------
        time_data : np.ndarray
            Time delay values
        amplitude_data : np.ndarray
            Amplitude measurements
        measurement_type : str, optional
            Type of measurement for logging, by default "T1"

        Returns
        -------
        FitResult
            Dictionary containing fit parameters and uncertainties
        """
        logger.debug("Fitting exponential decay for %s measurement", measurement_type)

        # Create exponential decay model (model: y = amplitude * exp(-x/decay))
        model = ExponentialModel()

        # Set initial parameter guesses
        params = model.make_params()
        params["amplitude"].set(value=float(np.max(amplitude_data)), min=0)
        # lmfit ExponentialModel uses exp(-x/decay) where 'decay' is the time constant τ
        positive_times = time_data[time_data > 0]
        if positive_times.size > 0:
            # Use a reasonable fraction of the time range as initial guess
            init_tau = float(np.max(positive_times)) / 3  # Conservative estimate
        else:
            init_tau = DEFAULT_DECAY_TIME_S
        params["decay"].set(value=init_tau, min=MIN_DECAY_TIME_S)

        try:
            # Perform fit
            result = model.fit(amplitude_data, params, x=time_data)

            # Extract fit parameters and uncertainties. 'decay' is the time constant τ
            amp = float(result.params["amplitude"].value)
            amp_stderr = float(result.params["amplitude"].stderr or 0.0)
            decay_time = float(result.params["decay"].value)  # This is τ directly
            decay_time_stderr = float(result.params["decay"].stderr or 0.0)

            # Calculate decay rate for backward compatibility
            if decay_time > 0:
                decay_rate = 1.0 / decay_time
                # Error propagation: k = 1/τ => sigma_k = sigma_τ / τ^2
                decay_rate_stderr = (
                    decay_time_stderr / (decay_time**2) if decay_time_stderr else 0.0
                )
            else:
                decay_rate = float("inf")
                decay_rate_stderr = 0.0

            var_y = float(np.var(amplitude_data))
            if result.residual is not None and var_y > 0:
                r_squared = 1.0 - float(np.var(result.residual)) / var_y
            else:
                r_squared = 0.0

            fit_result = {
                "amplitude": amp,
                "amplitude_stderr": amp_stderr,
                # Keep backward-compatible keys while also storing rate
                "decay_time": decay_time,
                "decay_time_stderr": decay_time_stderr,
                "decay_rate": decay_rate,
                "decay_rate_stderr": decay_rate_stderr,
                "chi_squared": float(result.chisqr) if result.chisqr is not None else 0.0,
                "reduced_chi_squared": float(result.redchi) if result.redchi is not None else 0.0,
                "r_squared": r_squared,
                "fit_success": bool(result.success),
                "fit_type": "exponential",
            }

            logger.info(
                "%s fit: decay_time=%.1f±%.1f μs, amplitude=%.3f±%.3f",
                measurement_type,
                decay_time * SECONDS_TO_MICROSECONDS,
                decay_time_stderr * SECONDS_TO_MICROSECONDS,
                amp,
                amp_stderr,
            )

            return fit_result

        except Exception as e:
            logger.error("Fit failed for %s: %s", measurement_type, e, exc_info=True)
            raise

    def _validate_ramsey_data(self, time_data: np.ndarray) -> None:
        """Validate data for Ramsey fitting."""
        if len(time_data) < MIN_POINTS_FOR_FFT:
            raise ValueError(
                f"Insufficient data points for Ramsey fit: {len(time_data)} < {MIN_POINTS_FOR_FFT}"
            )

        max_time = np.max(time_data)
        if max_time > MAX_TIME_SCALE_WARNING:  # > 1 millisecond
            logger.warning(
                "Suspiciously large time scale for T2R: max_time=%.2e s. Expected µs scale.",
                max_time,
            )
        if max_time > MAX_TIME_SCALE_ERROR:
            raise ValueError(
                f"Time scale too large for qubit coherence: {max_time:.2e} s. Check units!"
            )

        if len(time_data) < MIN_POINTS_PER_OSCILLATION * MIN_OSCILLATIONS_FOR_FIT:
            logger.warning("Very few points for oscillating fit: %d points", len(time_data))

    def _estimate_ramsey_frequency(
        self, time_data: np.ndarray, amplitude_data: np.ndarray
    ) -> float:
        """Estimate detuning frequency using FFT."""
        if len(time_data) <= MIN_POINTS_FOR_FFT:
            return DEFAULT_FREQUENCY_HZ

        try:
            dt = np.mean(np.diff(time_data))
            freqs = np.fft.fftfreq(len(amplitude_data), dt)
            fft_vals = np.abs(np.fft.fft(amplitude_data - np.mean(amplitude_data)))
            # Find peak frequency (ignore DC component)
            peak_idx = np.argmax(fft_vals[1 : len(fft_vals) // 2]) + 1
            return abs(freqs[peak_idx])
        except (ValueError, FloatingPointError, ZeroDivisionError, IndexError):
            return DEFAULT_FREQUENCY_HZ

    def _setup_ramsey_parameters(
        self, time_data: np.ndarray, amplitude_data: np.ndarray
    ) -> Parameters:
        """Set up initial parameters for Ramsey fitting."""
        params = Parameters()

        # Amplitude: half the range of data (since it oscillates around baseline)
        amp_guess = (np.max(amplitude_data) - np.min(amplitude_data)) / 2
        params.add("amp", value=amp_guess, min=0)

        # T2* time: rough estimate from time range
        positive_times = time_data[time_data > 0]
        if positive_times.size > 0:
            tau_guess = float(np.max(positive_times)) / 3  # Conservative estimate
        else:
            tau_guess = DEFAULT_DECAY_TIME_S
        params.add("tau", value=tau_guess, min=MIN_DECAY_TIME_S)

        # Detuning frequency: estimate from oscillation period
        freq_guess = self._estimate_ramsey_frequency(time_data, amplitude_data)
        params.add("freq", value=freq_guess, min=-MAX_FREQUENCY_HZ, max=MAX_FREQUENCY_HZ)

        # Phase: start at 0
        params.add("phi", value=0.0, min=-np.pi, max=np.pi)

        # Baseline: mean of data
        base_guess = np.mean(amplitude_data)
        params.add("base", value=base_guess)

        return params

    def _extract_ramsey_fit_results(self, result, amplitude_data: np.ndarray) -> FitResult:
        """Extract fit results from lmfit result object."""
        # Extract fit parameters and uncertainties
        amp = float(result.params["amp"].value)
        amp_stderr = float(result.params["amp"].stderr or 0.0)
        tau = float(result.params["tau"].value)
        tau_stderr = float(result.params["tau"].stderr or 0.0)
        freq = float(result.params["freq"].value)
        freq_stderr = float(result.params["freq"].stderr or 0.0)
        phi = float(result.params["phi"].value)
        phi_stderr = float(result.params["phi"].stderr or 0.0)
        base = float(result.params["base"].value)
        base_stderr = float(result.params["base"].stderr or 0.0)

        var_y = float(np.var(amplitude_data))
        if result.residual is not None and var_y > 0:
            r_squared = 1.0 - float(np.var(result.residual)) / var_y
        else:
            r_squared = 0.0

        return {
            "amplitude": amp,
            "amplitude_stderr": amp_stderr,
            "decay_time": tau,  # T2* time
            "decay_time_stderr": tau_stderr,
            "frequency": freq,  # Detuning frequency
            "frequency_stderr": freq_stderr,
            "phase": phi,
            "phase_stderr": phi_stderr,
            "baseline": base,
            "baseline_stderr": base_stderr,
            "chi_squared": float(result.chisqr) if result.chisqr is not None else 0.0,
            "reduced_chi_squared": float(result.redchi) if result.redchi is not None else 0.0,
            "r_squared": r_squared,
            "fit_success": bool(result.success),
            "fit_type": "ramsey",
        }

    def fit_ramsey_decay(
        self, time_data: np.ndarray, amplitude_data: np.ndarray, measurement_type: str = "T2R"
    ) -> FitResult:
        """Fit T2-Ramsey decaying sine model to measurement data.

        Parameters
        ----------
        time_data : np.ndarray
            Time delay values
        amplitude_data : np.ndarray
            Amplitude measurements
        measurement_type : str, optional
            Type of measurement for logging, by default "T2R"

        Returns
        -------
        FitResult
            Dictionary containing fit parameters and uncertainties
        """
        logger.debug("Fitting T2-Ramsey decaying sine for %s measurement", measurement_type)

        # Validate data
        self._validate_ramsey_data(time_data)

        # Create custom Ramsey model
        model = Model(self._ramsey_decay_lmfit)

        # Set up parameters
        params = self._setup_ramsey_parameters(time_data, amplitude_data)

        try:
            # Perform fit
            result = model.fit(amplitude_data, params, t=time_data)

            # Extract fit parameters and uncertainties
            fit_result = self._extract_ramsey_fit_results(result, amplitude_data)

            # Validate Ramsey parameters for physical reasonableness
            param_warnings = validate_ramsey_parameters(
                frequency=fit_result["frequency"],
                phase=fit_result["phase"],
                amplitude=fit_result["amplitude"],
                baseline=fit_result["baseline"],
            )
            if param_warnings:
                fit_result["parameter_warnings"] = param_warnings
                for warning in param_warnings:
                    logger.warning("Ramsey parameter validation: %s", warning)

            logger.info(
                "%s fit: T2*=%.3f±%.3f μs, freq=%.1f±%.1f Hz, amp=%.3f±%.3f",
                measurement_type,
                fit_result["decay_time"] * 1e6,  # Convert to μs
                fit_result["decay_time_stderr"] * 1e6,
                fit_result["frequency"],
                fit_result["frequency_stderr"],
                fit_result["amplitude"],
                fit_result["amplitude_stderr"],
            )

            return fit_result

        except Exception as e:
            logger.error("Ramsey fit failed for %s: %s", measurement_type, e, exc_info=True)
            raise

    def analyze_coherence_data(self, filepath: Path) -> AnalysisResult:  # noqa: C901, PLR0912
        """Analyze coherence measurement data (T1, T2 echo, T2 Ramsey).

        Parameters
        ----------
        filepath : Path
            Path to HDF5 file containing coherence data

        Returns
        -------
        AnalysisResult
            Complete analysis results including fits and derived quantities
        """
        logger.info("Starting coherence analysis for file: %s", filepath)

        # Load data
        metadata, datasets = self.load_measurement_data(filepath)

        fits: dict[str, FitResult] = {}
        derived_quantities: dict[str, Any] = {}
        analysis_result: AnalysisResult = {
            "filepath": str(filepath),
            "metadata": metadata,
            "fits": fits,
            "derived_quantities": derived_quantities,
        }

        # Analyze each measurement type
        measurement_types = MEASUREMENT_TYPES

        for meas_type in measurement_types:
            # Find datasets for this measurement type
            matching_datasets = [k for k in datasets.keys() if meas_type in k.lower()]

            if not matching_datasets:
                logger.warning("No datasets found for measurement type: %s", meas_type)
                continue

            # Combine data from all measurement iterations
            all_times = []
            all_amplitudes = []

            for dataset_name in matching_datasets:
                dataset = datasets[dataset_name]
                times, amplitudes = self._extract_time_amplitude_data(dataset)
                all_times.extend(times)
                all_amplitudes.extend(amplitudes)

            if len(all_times) == 0:
                continue

            # Sort by time
            sorted_indices = np.argsort(all_times)
            sorted_times = np.array(all_times)[sorted_indices]
            sorted_amplitudes = np.array(all_amplitudes)[sorted_indices]

            # Choose appropriate fit based on measurement type
            try:
                if meas_type == "t2r":  # T2-Ramsey needs decaying sine fit
                    fit_result = self.fit_ramsey_decay(
                        sorted_times, sorted_amplitudes, meas_type.upper()
                    )
                else:  # T1 and T2E use exponential decay fit
                    fit_result = self.fit_exponential_decay(
                        sorted_times, sorted_amplitudes, meas_type.upper()
                    )
                fits[meas_type] = fit_result

                # Store derived quantities
                if meas_type == "t1":
                    derived_quantities["T1"] = fit_result["decay_time"]
                    derived_quantities["T1_stderr"] = fit_result["decay_time_stderr"]
                elif meas_type == "t2e":
                    derived_quantities["T2_echo"] = fit_result["decay_time"]
                    derived_quantities["T2_echo_stderr"] = fit_result["decay_time_stderr"]
                elif meas_type == "t2r":
                    derived_quantities["T2_ramsey"] = fit_result["decay_time"]
                    derived_quantities["T2_ramsey_stderr"] = fit_result["decay_time_stderr"]

            except (ValueError, RuntimeError) as e:
                logger.error("Failed to analyze %s data: %s", meas_type, e)
                continue

        logger.info("Coherence analysis completed with %d successful fits", len(fits))

        # Validate physics constraints (T2 ≤ 2×T1)
        validation = validate_coherence_times(analysis_result, strict=False)
        analysis_result["physics_validation"] = {
            "is_valid": validation.is_valid,
            "violations": validation.violations,
            "warnings": validation.warnings,
        }

        if not validation.is_valid:
            logger.error(
                "Physics validation FAILED with %d violation(s). Results may be unreliable!",
                len(validation.violations),
            )
            for violation in validation.violations:
                logger.error("  - %s", violation)
        elif validation.warnings:
            logger.warning("Physics validation passed with %d warning(s)", len(validation.warnings))
            for warning in validation.warnings:
                logger.warning("  - %s", warning)
        else:
            logger.info("Physics validation PASSED - all coherence times are physically valid")

        return analysis_result

    def _generate_fit_curve(
        self,
        fit_result: FitResult,
        time_range: tuple[float, float],
        num_points: int = DEFAULT_FIT_POINTS,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Generate fitted curve data for plotting.

        Parameters
        ----------
        fit_result : FitResult
            Fit results from fit_exponential_decay or fit_ramsey_decay
        time_range : tuple[float, float]
            Min and max time values for curve
        num_points : int, optional
            Number of points in curve, by default 100

        Returns
        -------
        tuple[np.ndarray, np.ndarray]
            Time points and fitted amplitude values
        """
        if not fit_result["fit_success"]:
            raise ValueError("Cannot generate curve from unsuccessful fit")

        x_fit = np.linspace(time_range[0], time_range[1], num_points)

        # Generate curve based on fit type
        if fit_result.get("fit_type") == "ramsey":
            # T2-Ramsey: A * exp(-t/T2*) * cos(2πft + φ) + B
            ramsey_params = RamseyParams(
                amp=fit_result["amplitude"],
                tau=fit_result["decay_time"],
                freq=fit_result["frequency"],
                phi=fit_result["phase"],
                base=fit_result["baseline"],
            )
            y_fit = self._ramsey_decay_func(x_fit, ramsey_params)
        else:
            # Exponential: A * exp(-t/τ)
            y_fit = fit_result["amplitude"] * np.exp(-x_fit / fit_result["decay_time"])

        return x_fit, y_fit

    def _create_empty_plot_if_needed(self, save_path: Path | None) -> bool:
        """Create empty plot if needed and return True if handled."""
        if save_path:
            _fig, ax = plt.subplots(
                1, 1, figsize=(PLOT_CONFIG["figsize_per_plot"], PLOT_CONFIG["height"])
            )
            ax.set_title("No fits available")
            ax.axis("off")
            plt.tight_layout()
            plt.savefig(save_path, dpi=PLOT_CONFIG["dpi"], bbox_inches="tight")
            plt.close()
        return True

    def _collect_measurement_data(
        self, datasets: DatasetDict, meas_type: str
    ) -> tuple[np.ndarray, np.ndarray]:
        """Collect and sort time/amplitude data for a measurement type."""
        matching_datasets = [k for k in datasets.keys() if meas_type in k.lower()]

        all_times = []
        all_amplitudes = []

        for dataset_name in matching_datasets:
            dataset = datasets[dataset_name]
            times, amplitudes = self._extract_time_amplitude_data(dataset)
            all_times.extend(times)
            all_amplitudes.extend(amplitudes)

        # Sort data
        sorted_indices = np.argsort(all_times)
        sorted_times = np.array(all_times)[sorted_indices]
        sorted_amplitudes = np.array(all_amplitudes)[sorted_indices]

        return sorted_times, sorted_amplitudes

    def _create_fit_label(self, fit_result: FitResult) -> str:
        """Create appropriate label based on fit type."""
        if fit_result.get("fit_type") == "ramsey":
            decay_time_us = fit_result["decay_time"] * 1e6
            decay_stderr_us = fit_result["decay_time_stderr"] * 1e6
            freq = fit_result["frequency"]
            freq_stderr = fit_result["frequency_stderr"]
            return (
                f"Fit: T₂*={decay_time_us:.1f}±{decay_stderr_us:.1f} μs, "
                f"f={freq:.0f}±{freq_stderr:.0f} Hz"
            )
        else:
            # Convert to microseconds for better readability
            decay_us = fit_result["decay_time"] * 1e6
            decay_stderr_us = fit_result["decay_time_stderr"] * 1e6
            return f"Fit: τ={decay_us:.1f}±{decay_stderr_us:.1f} μs"

    def plot_analysis(self, analysis_result: AnalysisResult, save_path: Path | None = None) -> None:
        """Plot analysis results with fits.

        Parameters
        ----------
        analysis_result : AnalysisResult
            Analysis results from analyze_coherence_data
        save_path : Path | None, optional
            Path to save plot PNG file, by default None
        """
        logger.debug("Creating analysis plots")

        # Load original data for plotting
        filepath = Path(analysis_result["filepath"])
        _, datasets = self.load_measurement_data(filepath)

        fits = analysis_result.get("fits", {})
        n_plots = len([mt for mt in MEASUREMENT_TYPES if mt in fits])

        if n_plots == 0:
            logger.warning("No successful fits to plot")
            self._create_empty_plot_if_needed(save_path)
            return

        _fig, axes = plt.subplots(
            1, n_plots, figsize=(PLOT_CONFIG["figsize_per_plot"] * n_plots, PLOT_CONFIG["height"])
        )
        if n_plots == 1:
            axes = [axes]

        plot_idx = 0

        for meas_type in MEASUREMENT_TYPES:
            if meas_type not in fits:
                continue

            ax = axes[plot_idx]
            sorted_times, sorted_amplitudes = self._collect_measurement_data(datasets, meas_type)

            # Plot data points
            ax.scatter(sorted_times, sorted_amplitudes, alpha=PLOT_CONFIG["alpha"], label="Data")

            # Plot fit if successful
            fit_result = fits[meas_type]
            if fit_result["fit_success"]:
                time_range = (sorted_times.min(), sorted_times.max())
                x_fit, y_fit = self._generate_fit_curve(fit_result, time_range)
                label = self._create_fit_label(fit_result)
                ax.plot(x_fit, y_fit, "r-", label=label)

            ax.set_xlabel("Time")
            ax.set_ylabel("Amplitude")
            ax.set_title(f"{meas_type.upper()} Measurement")
            ax.legend()
            ax.grid(True, alpha=PLOT_CONFIG["grid_alpha"])

            plot_idx += 1

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=PLOT_CONFIG["dpi"], bbox_inches="tight")
            logger.info("Plot saved to: %s", save_path)
        else:
            plt.show()

        plt.close()

    def save_analysis_results(self, analysis_result: AnalysisResult, output_path: Path) -> None:
        """Save analysis results to JSON file.

        Parameters
        ----------
        analysis_result : AnalysisResult
            Analysis results to save
        output_path : Path
            Path for output JSON file
        """
        save_analysis_results(analysis_result, output_path)

    def save_summary_report(self, analysis_result: AnalysisResult, output_path: Path) -> None:
        """Save a text summary report to file.

        Parameters
        ----------
        analysis_result : AnalysisResult
            Analysis results to summarize
        output_path : Path
            Path for output text file
        """
        save_summary_report(analysis_result, output_path)

    def run_full_analysis(self, tuid: str, output_dir: Path | None = None) -> AnalysisResult:
        """Run complete analysis pipeline for a given TUID.

        Parameters
        ----------
        tuid : str
            Timestamp-based unique identifier for the measurement
            (format: YYYYmmDD-HHMMSS-sss-******)
        output_dir : Path | None, optional
            Directory for output files, by default None (uses data_path)

        Returns
        -------
        AnalysisResult
            Complete analysis results
        """
        logger.info("Starting full analysis for TUID: %s", tuid)

        # Find HDF5 file
        hdf5_file = self.find_hdf5_file(tuid)
        if hdf5_file is None:
            raise FileNotFoundError(f"No HDF5 file found for TUID: {tuid}")

        # Run analysis
        analysis_result = self.analyze_coherence_data(hdf5_file)

        # Set up output directory
        if output_dir is None:
            output_dir = self.data_path / tuid  # Save to TUID-specific folder
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)

        # Save results
        json_path = output_dir / f"{tuid}_analysis_results.json"
        self.save_analysis_results(analysis_result, json_path)

        # Create and save plot
        plot_path = output_dir / f"{tuid}_analysis_plot.png"
        self.plot_analysis(analysis_result, plot_path)

        # Save summary report
        report_path = output_dir / f"{tuid}_summary_report.txt"
        self.save_summary_report(analysis_result, report_path)

        logger.info("Full analysis completed for TUID: %s", tuid)
        return analysis_result

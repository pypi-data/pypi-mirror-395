"""Processor for transforming analysis results to database format."""

from __future__ import annotations

import json
from collections.abc import Mapping
from datetime import datetime
from numbers import Number
from pathlib import Path
from typing import Any

import numpy as np

from metsuperq.data_handling.hdf5_data_manager import DEFAULT_METADATA_REQUIREMENTS
from metsuperq.database.schema import (
    FitQuality,
    InfluxPoint,
    MeasurementPoint,
    MeasurementTags,
    MeasurementType,
    T1MeasurementFields,
    T2EchoMeasurementFields,
    T2RamseyMeasurementFields,
)
from metsuperq.utils import setup_logging

logger = setup_logging(__name__)

# Type alias for analysis results from BaseAnalyzer
AnalysisResult = dict[str, Any]

# Constants for fit quality thresholds
EXCELLENT_R_SQUARED_THRESHOLD = 0.95
EXCELLENT_CHI_SQUARED_THRESHOLD = 2.0
GOOD_R_SQUARED_THRESHOLD = 0.90
GOOD_CHI_SQUARED_THRESHOLD = 5.0
FAIR_R_SQUARED_THRESHOLD = 0.80
FAIR_CHI_SQUARED_THRESHOLD = 10.0
POOR_R_SQUARED_THRESHOLD = 0.50

# Constants for TUID parsing
TUID_TIMESTAMP_LENGTH = 15
TUID_FIRST_DASH_POS = 8
TUID_SECOND_DASH_POS = 15


class MeasurementProcessor:
    """Transforms analysis results to InfluxDB measurement points."""

    def __init__(self) -> None:
        """Initialize measurement processor."""
        self._metadata_requirements = DEFAULT_METADATA_REQUIREMENTS.copy()
        logger.debug("Initialized MeasurementProcessor")

    def process_analysis_result(
        self,
        analysis_result: AnalysisResult,
        experiment_id: str,
        device_name: str,
        qubit_name: str,
    ) -> list[InfluxPoint]:
        """Transform analysis result to measurement points.

        Parameters
        ----------
        analysis_result : AnalysisResult
            Analysis result from BaseAnalyzer.run_full_analysis()
        experiment_id : str
            Experiment unique identifier
        device_name : str
            Name of the quantum device
        qubit_name : str
            Name of the measured qubit

        Returns
        -------
        list[InfluxPoint]
            List of measurement points with denormalized metadata
        """
        logger.info("Processing analysis result for qubit %s", qubit_name)

        # Check physics validation results
        physics_validation = analysis_result.get("physics_validation", {})
        if not physics_validation.get("is_valid", True):
            violations = physics_validation.get("violations", [])
            logger.error(
                "Physics validation FAILED for qubit %s. Recording anyway but flagging issues.",
                qubit_name,
            )
            for violation in violations:
                logger.error("  Physics violation: %s", violation)

        # Extract and validate metadata once (used for all measurements)
        metadata = analysis_result.get("metadata")
        if metadata is None:
            raise ValueError("Analysis result missing metadata; cannot create measurement points")

        validated_metadata = self._validate_and_normalize_metadata(metadata)

        points: list[InfluxPoint] = []
        fits = analysis_result.get("fits", {})
        timestamp = self._extract_timestamp(analysis_result)
        tuid = analysis_result.get("tuid")

        for measurement_type_str, fit_result in fits.items():
            if not fit_result.get("fit_success", False):
                logger.warning("Skipping failed fit for %s", measurement_type_str)
                continue

            try:
                point = self._create_measurement_point(
                    measurement_type_str=measurement_type_str,
                    fit_result=fit_result,
                    metadata=validated_metadata,
                    experiment_id=experiment_id,
                    device_name=device_name,
                    qubit_name=qubit_name,
                    timestamp=timestamp,
                    tuid=tuid,
                )
                points.append(point)
                logger.debug("Created measurement point for %s", measurement_type_str)

            except (ValueError, KeyError, TypeError) as e:
                logger.error(
                    "Failed to process %s measurement: %s", measurement_type_str, e, exc_info=True
                )
                continue

        logger.info("Processed %d measurement points with denormalized metadata", len(points))
        return points

    def _extract_timestamp(self, analysis_result: AnalysisResult) -> datetime:
        """Extract measurement timestamp from analysis result."""
        # Try to get timestamp from analysis result
        if "timestamp" in analysis_result:
            timestamp = analysis_result["timestamp"]
            if isinstance(timestamp, datetime):
                return timestamp
            elif isinstance(timestamp, str):
                return datetime.fromisoformat(timestamp.replace("Z", "+00:00"))

        # Try to extract from TUID (format: YYYYmmDD-HHMMSS-sss-******)
        tuid = analysis_result.get("tuid")
        if tuid:
            try:
                # Extract timestamp part (first 15 characters)
                timestamp_str = tuid[:15]  # YYYYmmDD-HHMMSS
                return datetime.strptime(timestamp_str, "%Y%m%d-%H%M%S")
            except ValueError:
                logger.warning("Could not parse timestamp from TUID: %s", tuid)

        # Try to extract from filepath
        filepath = analysis_result.get("filepath")
        if filepath:
            try:
                path = Path(filepath)
                # Look for TUID pattern in path components
                for part in path.parts:
                    if (
                        len(part) >= TUID_TIMESTAMP_LENGTH
                        and part[TUID_FIRST_DASH_POS] == "-"
                        and part[TUID_SECOND_DASH_POS] == "-"
                    ):
                        timestamp_str = part[:TUID_TIMESTAMP_LENGTH]
                        return datetime.strptime(timestamp_str, "%Y%m%d-%H%M%S")
            except (ValueError, IndexError, KeyError):
                pass  # Expected failures when parsing timestamp from filepath

        # Fallback to current time
        logger.warning("Could not extract timestamp, using current time")
        return datetime.now()

    def _create_measurement_point(  # noqa: PLR0913
        self,
        measurement_type_str: str,
        fit_result: dict[str, Any],
        metadata: dict[str, Any],
        experiment_id: str,
        device_name: str,
        qubit_name: str,
        timestamp: datetime,
        tuid: str | None,
    ) -> MeasurementPoint:
        """Create a measurement point with denormalized metadata."""
        # Map measurement type
        measurement_type = self._map_measurement_type(measurement_type_str)

        # Assess and log fit quality
        quality = self._assess_fit_quality(fit_result)
        if quality in [FitQuality.POOR, FitQuality.FAILED]:
            logger.warning(
                "Poor fit quality (%s) for %s: R²=%.3f, χ²=%.2f",
                quality.value,
                measurement_type_str,
                fit_result.get("r_squared", 0.0),
                fit_result.get("chi_squared", float("inf")),
            )
        else:
            logger.debug(
                "Fit quality (%s) for %s: R²=%.3f",
                quality.value,
                measurement_type_str,
                fit_result.get("r_squared", 0.0),
            )

        # Create tags with metadata identifiers
        tags = MeasurementTags(
            measurement_type=measurement_type,
            experiment_id=experiment_id,
            device_name=device_name,
            qubit_name=qubit_name,
            sample_identifier=metadata["sample_identifier"],
            qubit_type=metadata["qubit_type"],
            measurement_institute=metadata["measurement_institute"],
            measurement_fridge=metadata["measurement_fridge"],
        )

        # Create fields with denormalized metadata
        fields = self._create_measurement_fields(measurement_type, fit_result, metadata)

        # Create measurement name
        measurement_name = f"{measurement_type.value}"

        return MeasurementPoint(
            measurement=measurement_name,
            tags=tags,
            fields=fields,
            timestamp=timestamp,
            tuid=tuid,
        )

    def _validate_and_normalize_metadata(self, metadata: Mapping[str, Any]) -> dict[str, Any]:
        """Validate and normalize metadata for use in measurements.

        Returns
        -------
        dict[str, Any]
            Normalized metadata dictionary with all required fields

        Raises
        ------
        ValueError
            If mandatory metadata fields are missing
        """
        for required_key, is_mandatory in self._metadata_requirements.items():
            if is_mandatory and required_key not in metadata:
                raise ValueError(f"Missing mandatory metadata field '{required_key}'")

        normalized_fields: dict[str, Any] = {}
        for key, value in metadata.items():
            normalized_fields[key] = self._normalize_metadata_value(value)

        return normalized_fields

    @staticmethod
    def _normalize_metadata_value(value: Any) -> str | int | float | bool:
        """Normalize metadata values to Influx-friendly scalars."""
        # Handle numpy types first
        normalized = MeasurementProcessor._convert_numpy_types(value)

        # Handle collections (recursive)
        if isinstance(normalized, Mapping):
            return MeasurementProcessor._normalize_mapping(normalized)
        if isinstance(normalized, (list, tuple, set)):
            return MeasurementProcessor._normalize_sequence(normalized)

        # Convert special types to strings
        if isinstance(normalized, (datetime, Path)):
            normalized = (
                normalized.isoformat() if isinstance(normalized, datetime) else str(normalized)
            )

        # Handle primitives and numeric types
        if isinstance(normalized, (str, bool, int, float)):
            return normalized
        if isinstance(normalized, Number):
            return MeasurementProcessor._convert_to_int_or_float(normalized)

        return str(normalized)

    @staticmethod
    def _convert_numpy_types(value: Any) -> Any:
        """Convert numpy types to Python primitives."""
        if isinstance(value, np.generic):
            return value.item()
        if isinstance(value, np.ndarray):
            return value.tolist()
        return value

    @staticmethod
    def _normalize_mapping(mapping: Mapping[Any, Any]) -> str:
        """Normalize a mapping to JSON string."""
        normalized = {
            str(k): MeasurementProcessor._normalize_metadata_value(v) for k, v in mapping.items()
        }
        return json.dumps(normalized)

    @staticmethod
    def _normalize_sequence(sequence: list | tuple | set) -> str:
        """Normalize a sequence to JSON string."""
        items = [MeasurementProcessor._normalize_metadata_value(item) for item in sequence]
        return json.dumps(items)

    @staticmethod
    def _convert_to_int_or_float(value: Number) -> int | float:
        """Convert abstract Number type to concrete int or float.

        Prefers int if the value can be represented exactly as an integer.
        """
        try:
            return int(value)  # type: ignore[arg-type]
        except (ValueError, TypeError):
            return float(value)  # type: ignore[arg-type]

    @staticmethod
    def _parse_metadata_timestamp(value: str) -> datetime:
        """Parse timestamp from metadata, fallback to current time on failure."""
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            logger.warning("Invalid metadata timestamp '%s', using current time", value)
            return datetime.now()

    def _map_measurement_type(self, measurement_type_str: str) -> MeasurementType:
        """Map string measurement type to enum."""
        type_mapping = {
            "t1": MeasurementType.T1,
            "t2e": MeasurementType.T2_ECHO,
            "t2r": MeasurementType.T2_RAMSEY,
        }

        normalized = measurement_type_str.lower()
        if normalized not in type_mapping:
            raise ValueError(f"Unknown measurement type: {measurement_type_str}")

        return type_mapping[normalized]

    def _assess_fit_quality(self, fit_result: dict[str, Any]) -> FitQuality:
        """Assess fit quality based on fit statistics."""
        r_squared = fit_result.get("r_squared", 0.0)
        chi_squared = fit_result.get("chi_squared", float("inf"))

        # Simple quality assessment
        if (
            r_squared >= EXCELLENT_R_SQUARED_THRESHOLD
            and chi_squared < EXCELLENT_CHI_SQUARED_THRESHOLD
        ):
            return FitQuality.EXCELLENT
        elif r_squared >= GOOD_R_SQUARED_THRESHOLD and chi_squared < GOOD_CHI_SQUARED_THRESHOLD:
            return FitQuality.GOOD
        elif r_squared >= FAIR_R_SQUARED_THRESHOLD and chi_squared < FAIR_CHI_SQUARED_THRESHOLD:
            return FitQuality.FAIR
        elif r_squared >= POOR_R_SQUARED_THRESHOLD:
            return FitQuality.POOR
        else:
            return FitQuality.FAILED

    def _create_measurement_fields(
        self,
        measurement_type: MeasurementType,
        fit_result: dict[str, Any],
        metadata: dict[str, Any],
    ) -> T1MeasurementFields | T2EchoMeasurementFields | T2RamseyMeasurementFields:
        """Create measurement fields with denormalized metadata."""
        # Common physics results
        common_fields = {
            "decay_time": fit_result["decay_time"],
            "decay_time_stderr": fit_result["decay_time_stderr"],
            "amplitude": fit_result["amplitude"],
            "amplitude_stderr": fit_result["amplitude_stderr"],
            "r_squared": fit_result["r_squared"],
            "chi_squared": fit_result["chi_squared"],
        }

        # Add baseline if present
        if "baseline" in fit_result:
            common_fields["baseline"] = fit_result["baseline"]
        if "baseline_stderr" in fit_result:
            common_fields["baseline_stderr"] = fit_result["baseline_stderr"]

        # Common metadata fields (ALL fields denormalized for team visibility)
        # Note: metadata values are already normalized by _validate_and_normalize_metadata,
        # Explicit type conversions ensure pyright can verify types match Pydantic models

        # Helper to safely get optional string values
        def _opt_str(key: str) -> str | None:
            v = metadata.get(key)
            return str(v) if v is not None else None

        # Helper to safely get optional float values
        def _opt_float(key: str) -> float | None:
            v = metadata.get(key)
            return float(v) if v is not None else None

        # Helper to safely get optional bool values
        def _opt_bool(key: str) -> bool | None:
            v = metadata.get(key)
            return bool(v) if v is not None else None

        if measurement_type == MeasurementType.T1:
            return T1MeasurementFields(
                **common_fields,
                # Experimental conditions
                cooldown_days=int(metadata["time_since_cooldown_start_days"]),
                t1_averages=int(metadata["t1_averages"]),
                # Pulse parameters
                ctrlpulse_pi_duration_ns=int(metadata["ctrlpulse_pi_duration_ns"]),
                ctrlpulse_shape=str(metadata["ctrlpulse_shape"]),
                ctrlpulse_pi_amplitude=_opt_float("ctrlpulse_pi_amplitude"),
                readpulse_duration_ns=int(metadata["readpulse_duration_ns"]),
                readpulse_shape=str(metadata["readpulse_shape"]),
                readpulse_amplitude=float(metadata["readpulse_amplitude"]),
                reset_time_us=float(metadata["reset_time_us"]),
                # Qubit and resonator properties
                qubit_frequency=float(metadata["qubit_frequency"]),
                resonator_frequency=float(metadata["resonator_frequency"]),
                resonator_qtotal=float(metadata["resonator_qtotal"]),
                qubit_ej_ghz=_opt_float("qubit_ej_ghz"),
                qubit_ec_ghz=_opt_float("qubit_ec_ghz"),
                qubit_el_ghz=_opt_float("qubit_el_ghz"),
                anharmonicity_mhz=_opt_float("anharmonicity_mhz"),
                # Material properties
                sample_origin_cleanroom=str(metadata["sample_origin_cleanroom"]),
                material_substrate=str(metadata["material_substrate"]),
                material_superconductor=str(metadata["material_superconductor"]),
                material_jj=str(metadata["material_jj"]),
                fabrication_date=_opt_str("fabrication_date"),
                # Amplifier and temperature
                parametric_amplifier_used=str(metadata["parametric_amplifier_used"]),
                parametric_amplifier_gain_db=_opt_float("parametric_amplifier_gain_db"),
                base_temperature_mk=_opt_float("base_temperature_mk"),
                chip_package=_opt_str("chip_package"),
                # Wiring configuration
                control_line_number=str(metadata["control_line_number"]),
                control_line_config=str(metadata["control_line_config"]),
                readout_in_line_number=str(metadata["readout_in_line_number"]),
                readout_in_line_config=str(metadata["readout_in_line_config"]),
                readout_out_line_number=str(metadata["readout_out_line_number"]),
                readout_out_line_config=str(metadata["readout_out_line_config"]),
                fridge_wiring_reference=str(metadata["fridge_wiring_reference"]),
                # References and history
                data_reference=str(metadata["data_reference"]),
                tuneup_measurement_reference=str(metadata["tuneup_measurement_reference"]),
                sample_history_reference=_opt_str("sample_history_reference"),
                # Sweep parameters (optional)
                part_of_sweep=_opt_bool("part_of_sweep"),
                sweep_variable=_opt_str("sweep_variable"),
                sweep_variable_value=_opt_float("sweep_variable_value"),
                sweep_variable_unit=_opt_str("sweep_variable_unit"),
                sweep_variable_list=_opt_str("sweep_variable_list"),
                sweep_reference_next=_opt_str("sweep_reference_next"),
                sweep_reference_previous=_opt_str("sweep_reference_previous"),
            )

        if measurement_type == MeasurementType.T2_ECHO:
            return T2EchoMeasurementFields(
                **common_fields,
                # Experimental conditions
                cooldown_days=int(metadata["time_since_cooldown_start_days"]),
                t2e_averages=int(metadata["t2e_averages"]),
                # Pulse parameters
                ctrlpulse_pi_duration_ns=int(metadata["ctrlpulse_pi_duration_ns"]),
                ctrlpulse_shape=str(metadata["ctrlpulse_shape"]),
                ctrlpulse_pi_amplitude=_opt_float("ctrlpulse_pi_amplitude"),
                readpulse_duration_ns=int(metadata["readpulse_duration_ns"]),
                readpulse_shape=str(metadata["readpulse_shape"]),
                readpulse_amplitude=float(metadata["readpulse_amplitude"]),
                reset_time_us=float(metadata["reset_time_us"]),
                # Qubit and resonator properties
                qubit_frequency=float(metadata["qubit_frequency"]),
                resonator_frequency=float(metadata["resonator_frequency"]),
                resonator_qtotal=float(metadata["resonator_qtotal"]),
                qubit_ej_ghz=_opt_float("qubit_ej_ghz"),
                qubit_ec_ghz=_opt_float("qubit_ec_ghz"),
                qubit_el_ghz=_opt_float("qubit_el_ghz"),
                anharmonicity_mhz=_opt_float("anharmonicity_mhz"),
                # Material properties
                sample_origin_cleanroom=str(metadata["sample_origin_cleanroom"]),
                material_substrate=str(metadata["material_substrate"]),
                material_superconductor=str(metadata["material_superconductor"]),
                material_jj=str(metadata["material_jj"]),
                fabrication_date=_opt_str("fabrication_date"),
                # Amplifier and temperature
                parametric_amplifier_used=str(metadata["parametric_amplifier_used"]),
                parametric_amplifier_gain_db=_opt_float("parametric_amplifier_gain_db"),
                base_temperature_mk=_opt_float("base_temperature_mk"),
                chip_package=_opt_str("chip_package"),
                # Wiring configuration
                control_line_number=str(metadata["control_line_number"]),
                control_line_config=str(metadata["control_line_config"]),
                readout_in_line_number=str(metadata["readout_in_line_number"]),
                readout_in_line_config=str(metadata["readout_in_line_config"]),
                readout_out_line_number=str(metadata["readout_out_line_number"]),
                readout_out_line_config=str(metadata["readout_out_line_config"]),
                fridge_wiring_reference=str(metadata["fridge_wiring_reference"]),
                # References and history
                data_reference=str(metadata["data_reference"]),
                tuneup_measurement_reference=str(metadata["tuneup_measurement_reference"]),
                sample_history_reference=_opt_str("sample_history_reference"),
                # Sweep parameters (optional)
                part_of_sweep=_opt_bool("part_of_sweep"),
                sweep_variable=_opt_str("sweep_variable"),
                sweep_variable_value=_opt_float("sweep_variable_value"),
                sweep_variable_unit=_opt_str("sweep_variable_unit"),
                sweep_variable_list=_opt_str("sweep_variable_list"),
                sweep_reference_next=_opt_str("sweep_reference_next"),
                sweep_reference_previous=_opt_str("sweep_reference_previous"),
            )

        if measurement_type == MeasurementType.T2_RAMSEY:
            return T2RamseyMeasurementFields(
                **common_fields,
                # T2 Ramsey specific fields
                frequency=float(fit_result["frequency"]),
                frequency_stderr=float(fit_result["frequency_stderr"]),
                phase=float(fit_result["phase"]),
                phase_stderr=float(fit_result["phase_stderr"]),
                # Experimental conditions
                cooldown_days=int(metadata["time_since_cooldown_start_days"]),
                t2r_averages=int(metadata["t2r_averages"]),
                ramsey_detuning_hz=_opt_float("ramsey_detuning_hz"),
                # Pulse parameters
                ctrlpulse_pi_duration_ns=int(metadata["ctrlpulse_pi_duration_ns"]),
                ctrlpulse_shape=str(metadata["ctrlpulse_shape"]),
                ctrlpulse_pi_amplitude=_opt_float("ctrlpulse_pi_amplitude"),
                readpulse_duration_ns=int(metadata["readpulse_duration_ns"]),
                readpulse_shape=str(metadata["readpulse_shape"]),
                readpulse_amplitude=float(metadata["readpulse_amplitude"]),
                reset_time_us=float(metadata["reset_time_us"]),
                # Qubit and resonator properties
                qubit_frequency=float(metadata["qubit_frequency"]),
                resonator_frequency=float(metadata["resonator_frequency"]),
                resonator_qtotal=float(metadata["resonator_qtotal"]),
                qubit_ej_ghz=_opt_float("qubit_ej_ghz"),
                qubit_ec_ghz=_opt_float("qubit_ec_ghz"),
                qubit_el_ghz=_opt_float("qubit_el_ghz"),
                anharmonicity_mhz=_opt_float("anharmonicity_mhz"),
                # Material properties
                sample_origin_cleanroom=str(metadata["sample_origin_cleanroom"]),
                material_substrate=str(metadata["material_substrate"]),
                material_superconductor=str(metadata["material_superconductor"]),
                material_jj=str(metadata["material_jj"]),
                fabrication_date=_opt_str("fabrication_date"),
                # Amplifier and temperature
                parametric_amplifier_used=str(metadata["parametric_amplifier_used"]),
                parametric_amplifier_gain_db=_opt_float("parametric_amplifier_gain_db"),
                base_temperature_mk=_opt_float("base_temperature_mk"),
                chip_package=_opt_str("chip_package"),
                # Wiring configuration
                control_line_number=str(metadata["control_line_number"]),
                control_line_config=str(metadata["control_line_config"]),
                readout_in_line_number=str(metadata["readout_in_line_number"]),
                readout_in_line_config=str(metadata["readout_in_line_config"]),
                readout_out_line_number=str(metadata["readout_out_line_number"]),
                readout_out_line_config=str(metadata["readout_out_line_config"]),
                fridge_wiring_reference=str(metadata["fridge_wiring_reference"]),
                # References and history
                data_reference=str(metadata["data_reference"]),
                tuneup_measurement_reference=str(metadata["tuneup_measurement_reference"]),
                sample_history_reference=_opt_str("sample_history_reference"),
                # Sweep parameters (optional)
                part_of_sweep=_opt_bool("part_of_sweep"),
                sweep_variable=_opt_str("sweep_variable"),
                sweep_variable_value=_opt_float("sweep_variable_value"),
                sweep_variable_unit=_opt_str("sweep_variable_unit"),
                sweep_variable_list=_opt_str("sweep_variable_list"),
                sweep_reference_next=_opt_str("sweep_reference_next"),
                sweep_reference_previous=_opt_str("sweep_reference_previous"),
            )

        raise ValueError(f"Unsupported measurement type: {measurement_type}")

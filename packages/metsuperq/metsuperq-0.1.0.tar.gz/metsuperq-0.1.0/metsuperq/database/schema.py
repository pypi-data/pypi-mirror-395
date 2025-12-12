"""Pydantic models for quantum measurement data schema."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Protocol

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from metsuperq.utils import setup_logging

logger = setup_logging(__name__)


class MeasurementType(str, Enum):
    """Supported quantum measurement types."""

    T1 = "t1"
    T2_ECHO = "t2e"
    T2_RAMSEY = "t2r"


class FitQuality(str, Enum):
    """Fit quality assessment."""

    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    FAILED = "failed"


class InfluxPoint(Protocol):
    """Protocol for models that can be written to InfluxDB."""

    measurement: str

    def to_influx_dict(self) -> dict[str, Any]:
        """Convert point to InfluxDB-compatible dictionary."""
        ...

    def model_dump(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Dump model representation."""
        ...


class MeasurementTags(BaseModel):
    """Tags for categorizing measurements (indexed in InfluxDB).

    Tags are indexed and used for filtering/grouping. Keep cardinality low.
    Use tags for: identifiers, categorical metadata, discrete values.
    """

    measurement_type: MeasurementType = Field(description="Type of measurement")
    experiment_id: str = Field(description="Experiment unique identifier")
    device_name: str = Field(description="Quantum device name")
    qubit_name: str = Field(description="Qubit name")

    # Core experimental context (low cardinality, used for filtering)
    sample_identifier: str = Field(description="Sample/chip identifier")
    qubit_type: str = Field(description="Qubit type (e.g., transmon, fluxonium)")
    measurement_institute: str = Field(description="Institution performing measurement")
    measurement_fridge: str = Field(description="Dilution fridge identifier")

    @field_validator("experiment_id", "device_name", "qubit_name", "sample_identifier")
    @classmethod
    def validate_identifiers(cls, v: str) -> str:
        """Validate identifier format (no spaces, special chars)."""
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError("Identifiers must be alphanumeric with _ or - only")
        return v


class T1MeasurementFields(BaseModel):
    """Fields for T1 relaxation measurements.

    Fields store measured values and high-cardinality context.
    Not indexed, but queryable and used for calculations.
    """

    # Physics results
    decay_time: float = Field(description="T1 decay time in seconds", gt=0, allow_inf_nan=False)
    decay_time_stderr: float = Field(
        description="Standard error of decay time", ge=0, allow_inf_nan=False
    )
    amplitude: float = Field(description="Fit amplitude", ge=0, allow_inf_nan=False)
    amplitude_stderr: float = Field(
        description="Standard error of amplitude", ge=0, allow_inf_nan=False
    )
    baseline: float | None = Field(default=None, description="Baseline offset", allow_inf_nan=False)
    baseline_stderr: float | None = Field(
        default=None, description="Baseline stderr", ge=0, allow_inf_nan=False
    )
    r_squared: float = Field(description="Fit R-squared", ge=0, le=1, allow_inf_nan=False)
    chi_squared: float = Field(description="Chi-squared statistic", ge=0, allow_inf_nan=False)

    # Experimental conditions (denormalized from metadata)
    cooldown_days: int = Field(description="Days since cooldown start")
    t1_averages: int = Field(description="Number of averages for T1 measurement", gt=0)

    # Pulse parameters
    ctrlpulse_pi_duration_ns: int = Field(description="Control pulse pi duration in ns", gt=0)
    ctrlpulse_shape: str = Field(description="Control pulse shape")
    ctrlpulse_pi_amplitude: float | None = Field(
        default=None, description="Control pulse pi amplitude"
    )
    readpulse_duration_ns: int = Field(description="Readout pulse duration in ns", gt=0)
    readpulse_shape: str = Field(description="Readout pulse shape")
    readpulse_amplitude: float = Field(description="Readout pulse amplitude")
    reset_time_us: float = Field(description="Reset time in microseconds")

    # Qubit and resonator properties
    qubit_frequency: float = Field(description="Qubit frequency in Hz", gt=0)
    resonator_frequency: float = Field(description="Resonator frequency in Hz", gt=0)
    resonator_qtotal: float = Field(description="Resonator total Q factor")
    qubit_ej_ghz: float | None = Field(default=None, description="Qubit EJ in GHz")
    qubit_ec_ghz: float | None = Field(default=None, description="Qubit EC in GHz")
    qubit_el_ghz: float | None = Field(default=None, description="Qubit EL in GHz")
    anharmonicity_mhz: float | None = Field(default=None, description="Anharmonicity in MHz")

    # Material properties
    sample_origin_cleanroom: str = Field(description="Sample origin cleanroom")
    material_substrate: str = Field(description="Substrate material")
    material_superconductor: str = Field(description="Superconductor material")
    material_jj: str = Field(description="Josephson junction material")
    fabrication_date: str | None = Field(default=None, description="Fabrication date")

    # Amplifier and temperature
    parametric_amplifier_used: str = Field(description="Parametric amplifier identifier")
    parametric_amplifier_gain_db: float | None = Field(
        default=None, description="Amplifier gain in dB"
    )
    base_temperature_mk: float | None = Field(default=None, description="Base temperature in mK")
    chip_package: str | None = Field(default=None, description="Chip package type")

    # Wiring configuration
    control_line_number: str = Field(description="Control line number")
    control_line_config: str = Field(description="Control line configuration")
    readout_in_line_number: str = Field(description="Readout input line number")
    readout_in_line_config: str = Field(description="Readout input line configuration")
    readout_out_line_number: str = Field(description="Readout output line number")
    readout_out_line_config: str = Field(description="Readout output line configuration")
    fridge_wiring_reference: str = Field(description="Fridge wiring reference")

    # References and history
    data_reference: str = Field(description="Data reference")
    tuneup_measurement_reference: str = Field(description="Tuneup measurement reference")
    sample_history_reference: str | None = Field(
        default=None, description="Sample history reference"
    )

    # Sweep parameters (optional)
    part_of_sweep: bool | None = Field(default=None, description="Whether part of a sweep")
    sweep_variable: str | None = Field(default=None, description="Sweep variable name")
    sweep_variable_value: float | None = Field(default=None, description="Sweep variable value")
    sweep_variable_unit: str | None = Field(default=None, description="Sweep variable unit")
    sweep_variable_list: str | None = Field(default=None, description="Sweep variable list (JSON)")
    sweep_reference_next: str | None = Field(default=None, description="Next sweep reference")
    sweep_reference_previous: str | None = Field(
        default=None, description="Previous sweep reference"
    )

    @model_validator(mode="after")
    def validate_errors(self) -> T1MeasurementFields:
        """Validate error values make sense."""
        if self.decay_time_stderr > self.decay_time:
            logger.warning("Decay time error larger than value itself")
        return self


class T2EchoMeasurementFields(BaseModel):
    """Fields for T2 echo measurements."""

    # Physics results
    decay_time: float = Field(description="T2 echo time in seconds", gt=0, allow_inf_nan=False)
    decay_time_stderr: float = Field(
        description="Standard error of decay time", ge=0, allow_inf_nan=False
    )
    amplitude: float = Field(description="Fit amplitude", ge=0, allow_inf_nan=False)
    amplitude_stderr: float = Field(
        description="Standard error of amplitude", ge=0, allow_inf_nan=False
    )
    baseline: float | None = Field(default=None, description="Baseline offset", allow_inf_nan=False)
    baseline_stderr: float | None = Field(
        default=None, description="Baseline stderr", ge=0, allow_inf_nan=False
    )
    r_squared: float = Field(description="Fit R-squared", ge=0, le=1, allow_inf_nan=False)
    chi_squared: float = Field(description="Chi-squared statistic", ge=0, allow_inf_nan=False)

    # Experimental conditions (denormalized from metadata)
    cooldown_days: int = Field(description="Days since cooldown start")
    t2e_averages: int = Field(description="Number of averages for T2 echo measurement", gt=0)

    # Pulse parameters
    ctrlpulse_pi_duration_ns: int = Field(description="Control pulse pi duration in ns", gt=0)
    ctrlpulse_shape: str = Field(description="Control pulse shape")
    ctrlpulse_pi_amplitude: float | None = Field(
        default=None, description="Control pulse pi amplitude"
    )
    readpulse_duration_ns: int = Field(description="Readout pulse duration in ns", gt=0)
    readpulse_shape: str = Field(description="Readout pulse shape")
    readpulse_amplitude: float = Field(description="Readout pulse amplitude")
    reset_time_us: float = Field(description="Reset time in microseconds")

    # Qubit and resonator properties
    qubit_frequency: float = Field(description="Qubit frequency in Hz", gt=0)
    resonator_frequency: float = Field(description="Resonator frequency in Hz", gt=0)
    resonator_qtotal: float = Field(description="Resonator total Q factor")
    qubit_ej_ghz: float | None = Field(default=None, description="Qubit EJ in GHz")
    qubit_ec_ghz: float | None = Field(default=None, description="Qubit EC in GHz")
    qubit_el_ghz: float | None = Field(default=None, description="Qubit EL in GHz")
    anharmonicity_mhz: float | None = Field(default=None, description="Anharmonicity in MHz")

    # Material properties
    sample_origin_cleanroom: str = Field(description="Sample origin cleanroom")
    material_substrate: str = Field(description="Substrate material")
    material_superconductor: str = Field(description="Superconductor material")
    material_jj: str = Field(description="Josephson junction material")
    fabrication_date: str | None = Field(default=None, description="Fabrication date")

    # Amplifier and temperature
    parametric_amplifier_used: str = Field(description="Parametric amplifier identifier")
    parametric_amplifier_gain_db: float | None = Field(
        default=None, description="Amplifier gain in dB"
    )
    base_temperature_mk: float | None = Field(default=None, description="Base temperature in mK")
    chip_package: str | None = Field(default=None, description="Chip package type")

    # Wiring configuration
    control_line_number: str = Field(description="Control line number")
    control_line_config: str = Field(description="Control line configuration")
    readout_in_line_number: str = Field(description="Readout input line number")
    readout_in_line_config: str = Field(description="Readout input line configuration")
    readout_out_line_number: str = Field(description="Readout output line number")
    readout_out_line_config: str = Field(description="Readout output line configuration")
    fridge_wiring_reference: str = Field(description="Fridge wiring reference")

    # References and history
    data_reference: str = Field(description="Data reference")
    tuneup_measurement_reference: str = Field(description="Tuneup measurement reference")
    sample_history_reference: str | None = Field(
        default=None, description="Sample history reference"
    )

    # Sweep parameters (optional)
    part_of_sweep: bool | None = Field(default=None, description="Whether part of a sweep")
    sweep_variable: str | None = Field(default=None, description="Sweep variable name")
    sweep_variable_value: float | None = Field(default=None, description="Sweep variable value")
    sweep_variable_unit: str | None = Field(default=None, description="Sweep variable unit")
    sweep_variable_list: str | None = Field(default=None, description="Sweep variable list (JSON)")
    sweep_reference_next: str | None = Field(default=None, description="Next sweep reference")
    sweep_reference_previous: str | None = Field(
        default=None, description="Previous sweep reference"
    )


class T2RamseyMeasurementFields(BaseModel):
    """Fields for T2 Ramsey measurements."""

    # Physics results
    decay_time: float = Field(description="T2* decay time in seconds", gt=0, allow_inf_nan=False)
    decay_time_stderr: float = Field(
        description="Standard error of decay time", ge=0, allow_inf_nan=False
    )
    amplitude: float = Field(description="Fit amplitude", ge=0, allow_inf_nan=False)
    amplitude_stderr: float = Field(
        description="Standard error of amplitude", ge=0, allow_inf_nan=False
    )
    frequency: float = Field(description="Ramsey oscillation frequency in Hz", allow_inf_nan=False)
    frequency_stderr: float = Field(
        description="Standard error of frequency", ge=0, allow_inf_nan=False
    )
    phase: float = Field(description="Phase in radians", allow_inf_nan=False)
    phase_stderr: float = Field(description="Standard error of phase", ge=0, allow_inf_nan=False)
    baseline: float | None = Field(default=None, description="Baseline offset", allow_inf_nan=False)
    baseline_stderr: float | None = Field(
        default=None, description="Baseline stderr", ge=0, allow_inf_nan=False
    )
    r_squared: float = Field(description="Fit R-squared", ge=0, le=1, allow_inf_nan=False)
    chi_squared: float = Field(description="Chi-squared statistic", ge=0, allow_inf_nan=False)

    # Experimental conditions (denormalized from metadata)
    cooldown_days: int = Field(description="Days since cooldown start")
    t2r_averages: int = Field(description="Number of averages for T2 Ramsey measurement", gt=0)
    ramsey_detuning_hz: float | None = Field(default=None, description="Ramsey detuning in Hz")

    # Pulse parameters
    ctrlpulse_pi_duration_ns: int = Field(description="Control pulse pi duration in ns", gt=0)
    ctrlpulse_shape: str = Field(description="Control pulse shape")
    ctrlpulse_pi_amplitude: float | None = Field(
        default=None, description="Control pulse pi amplitude"
    )
    readpulse_duration_ns: int = Field(description="Readout pulse duration in ns", gt=0)
    readpulse_shape: str = Field(description="Readout pulse shape")
    readpulse_amplitude: float = Field(description="Readout pulse amplitude")
    reset_time_us: float = Field(description="Reset time in microseconds")

    # Qubit and resonator properties
    qubit_frequency: float = Field(description="Qubit frequency in Hz", gt=0)
    resonator_frequency: float = Field(description="Resonator frequency in Hz", gt=0)
    resonator_qtotal: float = Field(description="Resonator total Q factor")
    qubit_ej_ghz: float | None = Field(default=None, description="Qubit EJ in GHz")
    qubit_ec_ghz: float | None = Field(default=None, description="Qubit EC in GHz")
    qubit_el_ghz: float | None = Field(default=None, description="Qubit EL in GHz")
    anharmonicity_mhz: float | None = Field(default=None, description="Anharmonicity in MHz")

    # Material properties
    sample_origin_cleanroom: str = Field(description="Sample origin cleanroom")
    material_substrate: str = Field(description="Substrate material")
    material_superconductor: str = Field(description="Superconductor material")
    material_jj: str = Field(description="Josephson junction material")
    fabrication_date: str | None = Field(default=None, description="Fabrication date")

    # Amplifier and temperature
    parametric_amplifier_used: str = Field(description="Parametric amplifier identifier")
    parametric_amplifier_gain_db: float | None = Field(
        default=None, description="Amplifier gain in dB"
    )
    base_temperature_mk: float | None = Field(default=None, description="Base temperature in mK")
    chip_package: str | None = Field(default=None, description="Chip package type")

    # Wiring configuration
    control_line_number: str = Field(description="Control line number")
    control_line_config: str = Field(description="Control line configuration")
    readout_in_line_number: str = Field(description="Readout input line number")
    readout_in_line_config: str = Field(description="Readout input line configuration")
    readout_out_line_number: str = Field(description="Readout output line number")
    readout_out_line_config: str = Field(description="Readout output line configuration")
    fridge_wiring_reference: str = Field(description="Fridge wiring reference")

    # References and history
    data_reference: str = Field(description="Data reference")
    tuneup_measurement_reference: str = Field(description="Tuneup measurement reference")
    sample_history_reference: str | None = Field(
        default=None, description="Sample history reference"
    )

    # Sweep parameters (optional)
    part_of_sweep: bool | None = Field(default=None, description="Whether part of a sweep")
    sweep_variable: str | None = Field(default=None, description="Sweep variable name")
    sweep_variable_value: float | None = Field(default=None, description="Sweep variable value")
    sweep_variable_unit: str | None = Field(default=None, description="Sweep variable unit")
    sweep_variable_list: str | None = Field(default=None, description="Sweep variable list (JSON)")
    sweep_reference_next: str | None = Field(default=None, description="Next sweep reference")
    sweep_reference_previous: str | None = Field(
        default=None, description="Previous sweep reference"
    )


class MeasurementPoint(BaseModel):
    """A single quantum measurement data point for InfluxDB."""

    measurement: str = Field(description="InfluxDB measurement name")
    tags: MeasurementTags = Field(description="Measurement tags")
    fields: T1MeasurementFields | T2EchoMeasurementFields | T2RamseyMeasurementFields = Field(
        description="Measurement fields"
    )
    timestamp: datetime = Field(description="Measurement timestamp")
    tuid: str | None = Field(default=None, description="Original TUID from analysis")

    @field_validator("measurement")
    @classmethod
    def validate_measurement_name(cls, v: str) -> str:
        """Validate InfluxDB measurement name format."""
        if not v.replace("_", "").isalnum():
            raise ValueError("Measurement name must be alphanumeric with underscores")
        return v

    @model_validator(mode="after")
    def validate_measurement_type_matches_fields(self) -> MeasurementPoint:
        """Validate that measurement type tag matches the fields model type."""
        measurement_type = self.tags.measurement_type
        actual_fields_type = type(self.fields).__name__

        expected_fields_type_mapping = {
            MeasurementType.T1: "T1MeasurementFields",
            MeasurementType.T2_ECHO: "T2EchoMeasurementFields",
            MeasurementType.T2_RAMSEY: "T2RamseyMeasurementFields",
        }

        expected_fields_type = expected_fields_type_mapping.get(measurement_type)
        if expected_fields_type != actual_fields_type:
            raise ValueError(
                f"Measurement type mismatch: {measurement_type} requires "
                f"{expected_fields_type}, got {actual_fields_type}"
            )

        return self

    def to_influx_dict(self) -> dict[str, Any]:
        """Convert to InfluxDB line protocol dictionary."""
        return {
            "measurement": self.measurement,
            "tags": self.tags.model_dump(exclude_none=True),
            "fields": self.fields.model_dump(exclude_none=True),
            "time": self.timestamp,
        }


class AnalysisMetadataTags(BaseModel):
    """Tags associated with analysis metadata points."""

    measurement_type: str = Field(description="Measurement grouping from metadata")
    experiment_id: str = Field(description="Experiment unique identifier")
    device_name: str = Field(description="Quantum device name")
    qubit_name: str = Field(description="Qubit name")

    @field_validator("experiment_id", "device_name", "qubit_name")
    @classmethod
    def validate_identifiers(cls, v: str) -> str:
        """Validate identifier format (no spaces, special chars)."""
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError("Identifiers must be alphanumeric with _ or - only")
        return v


class AnalysisMetadataFields(BaseModel):
    """Flexible metadata fields for analysis points."""

    model_config = ConfigDict(extra="allow")

    measurement_time: str = Field(description="Timestamp recorded in metadata (ISO string)")


class AnalysisMetadataPoint(BaseModel):
    """Metadata snapshot associated with an analysis run."""

    measurement: str = Field(description="InfluxDB measurement name")
    tags: AnalysisMetadataTags = Field(description="Metadata tags")
    fields: AnalysisMetadataFields = Field(description="Metadata fields")
    timestamp: datetime = Field(description="Metadata timestamp")
    tuid: str | None = Field(default=None, description="Original TUID from analysis")

    def to_influx_dict(self) -> dict[str, Any]:
        """Convert to InfluxDB line protocol dictionary."""
        return {
            "measurement": self.measurement,
            "tags": self.tags.model_dump(exclude_none=True),
            "fields": self.fields.model_dump(exclude_none=True),
            "time": self.timestamp,
        }

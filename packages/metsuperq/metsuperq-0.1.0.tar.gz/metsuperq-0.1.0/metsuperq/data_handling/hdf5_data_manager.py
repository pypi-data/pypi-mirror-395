"""
Provide the HDF5DataManager class for managing HDF5 file operations.

Includes metadata validation and logging for measurement data handling.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator, Mapping, Sequence
from contextlib import AbstractContextManager, contextmanager
from pathlib import Path
from typing import Any

import h5py
import numpy as np

from metsuperq.analysis.constants import EXPECTED_DATASET_ROWS
from metsuperq.utils import setup_logging

logger = setup_logging(__name__)

# Type aliases for better type safety
DatasetDict = dict[str, Any]
MetadataValue = str | int | float | bool | Sequence[str | int | float]
MetadataDict = dict[str, MetadataValue]

DEFAULT_METADATA_REQUIREMENTS: dict[str, bool] = {
    "measurement_type": True,
    "data_reference": True,
    "tuneup_measurement_reference": True,
    "measurement_time": True,
    "time_since_cooldown_start_days": True,
    "t1_averages": True,
    "t2r_averages": True,
    "t2e_averages": True,
    "ctrlpulse_pi_duration_ns": True,
    "ctrlpulse_shape": True,
    "ctrlpulse_pi_amplitude": False,
    "ctrlpulse_sequence": False,
    "readpulse_duration_ns": True,
    "readpulse_shape": True,
    "readpulse_amplitude": True,
    "reset_time_us": True,
    "part_of_sweep": False,
    "sweep_variable": False,
    "sweep_variable_value": False,
    "sweep_variable_unit": False,
    "sweep_variable_list": False,
    "sweep_reference_next": False,
    "sweep_reference_previous": False,
    "ramsey_detuning_hz": False,
    "sample_identifier": True,
    "sample_origin_cleanroom": True,
    "material_substrate": True,
    "material_superconductor": True,
    "material_jj": True,
    "fabrication_date": False,
    "qubit_identifier": True,
    "qubit_type": True,
    "qubit_frequency": True,
    "resonator_frequency": True,
    "resonator_qtotal": True,
    "qubit_ej_ghz": False,
    "qubit_ec_ghz": False,
    "qubit_el_ghz": False,
    "anharmonicity_mhz": False,
    "measurement_institute": True,
    "measurement_fridge": True,
    "parametric_amplifier_used": True,
    "parametric_amplifier_gain_db": False,
    "base_temperature_mk": False,
    "chip_package": False,
    "fridge_wiring_reference": True,
    "sample_history_reference": False,
    "control_line_number": True,
    "control_line_config": True,
    "readout_in_line_number": True,
    "readout_in_line_config": True,
    "readout_out_line_number": True,
    "readout_out_line_config": True,
}


class HDF5DataManager:
    """
    A class to manage HDF5 file operations.

    Attributes
    ----------
    file : str
        The name of the HDF5 file (without extension).
    """

    def __init__(
        self,
        filename: str,
        *,
        metadata_requirements: Mapping[str, bool] | None = None,
        base_dir: str | Path | None = None,
    ) -> None:
        """
        Initialize the data manager.

        Parameters
        ----------
        filename : str
            The path to the HDF5 file (with or without .hdf5 extension).
            Relative paths are resolved against base_dir (or project root if base_dir is None).
        metadata_requirements : Mapping[str, bool] | None, optional
            Custom metadata requirement overrides where ``True`` marks a
            field as mandatory and ``False`` marks it optional. Missing
            keys fall back to the default requirements.
        base_dir : str | Path | None, optional
            Base directory for resolving relative paths. If None, uses project root
            (directory containing pyproject.toml). Absolute paths ignore this parameter.
        """
        self.file = self._normalize_filename(filename, base_dir)
        self.metadata_requirements: dict[str, bool] = DEFAULT_METADATA_REQUIREMENTS.copy()
        if metadata_requirements is not None:
            for key, required in metadata_requirements.items():
                if not isinstance(required, bool):
                    raise TypeError("metadata_requirements values must be boolean flags")
                self.metadata_requirements[key] = required
        self._metadata_allowed_keys = set(self.metadata_requirements)
        # Ensure parent directory exists
        self._ensure_directory_exists()
        # Ensure file exists by opening in append mode
        with self._open_file("a"):
            pass
        logger.info("HDF5 file created/opened: %s", self.file)

    def _normalize_filename(self, filename: str, base_dir: str | Path | None = None) -> str:
        """
        Normalize filename to ensure proper .hdf5 extension and resolve path.

        Parameters
        ----------
        filename : str
            Input filename with or without .hdf5 extension
        base_dir : str | Path | None, optional
            Base directory for resolving relative paths. If None, uses project root.

        Returns
        -------
        str
            Absolute path with exactly one .hdf5 extension
        """
        p = Path(filename)

        # Resolve relative paths against base_dir or project root
        if not p.is_absolute():
            if base_dir is not None:
                p = Path(base_dir) / p
            else:
                # Find project root (directory containing pyproject.toml)
                p = self._find_project_root() / p

        # Ensure exactly one .hdf5 extension
        if p.suffix != ".hdf5":
            p = p.with_suffix(".hdf5")

        return str(p.resolve())

    @staticmethod
    def _find_project_root() -> Path:
        """
        Find the project root by locating pyproject.toml.

        Returns
        -------
        Path
            Absolute path to project root

        Raises
        ------
        FileNotFoundError
            If project root cannot be determined
        """
        # Start from this file's location
        current = Path(__file__).resolve().parent

        # Walk up the directory tree looking for pyproject.toml
        for parent in [current, *current.parents]:
            if (parent / "pyproject.toml").exists():
                return parent

        # Fallback to current working directory if pyproject.toml not found
        return Path.cwd()

    def _ensure_directory_exists(self) -> None:
        """Create parent directories if they don't exist."""
        parent_dir = Path(self.file).parent
        if parent_dir != Path("."):
            parent_dir.mkdir(parents=True, exist_ok=True)
            logger.debug("Created directory: %s", parent_dir)

    @contextmanager
    def _open_file(self, mode: str = "r") -> Iterator[h5py.File]:
        """
        Context manager for safe HDF5 file operations.

        Parameters
        ----------
        mode : str, optional
            File access mode, by default "r"

        Yields
        ------
        h5py.File
            The opened HDF5 file object.
        """
        file_handle = None
        try:
            file_handle = h5py.File(self.file, mode)
            logger.debug("Opened HDF5 file in mode '%s': %s", mode, self.file)
            yield file_handle
        except OSError as e:
            logger.error("Failed to open HDF5 file %s: %s", self.file, e)
            raise
        finally:
            if file_handle is not None:
                file_handle.close()
                logger.debug("Closed HDF5 file: %s", self.file)

    def open_file(self, mode: str = "r") -> AbstractContextManager[h5py.File]:
        """
        Public context manager for HDF5 file operations.

        Parameters
        ----------
        mode : str, optional
            File access mode ('r', 'r+', 'w', 'a'), by default "r"

        Yields
        ------
        h5py.File
            The opened HDF5 file object.

        Examples
        --------
        >>> manager = HDF5DataManager("myfile")
        >>> with manager.open_file("r") as f:
        ...     data = f["dataset"][:]
        """
        return self._open_file(mode)

    def read_attributes(self, measurement_type: str) -> list[tuple[str, MetadataValue]]:
        """
        Read the attributes for a given experiment.

        Parameters
        ----------
        measurement_type : str
            The type of measurement to retrieve attributes for.

        Returns
        -------
        list[tuple[str, MetadataValue]]
            A list of attribute name-value pairs.

        Raises
        ------
        KeyError
            If the measurement_type group does not exist.
        """
        logger.debug("Reading attributes for measurement type: %s", measurement_type)
        try:
            with self._open_file("r") as file:
                if measurement_type not in file:
                    raise KeyError(f"Measurement type '{measurement_type}' not found in file")
                attributes = list(file[measurement_type].attrs.items())
            return attributes
        except KeyError:
            logger.error(
                "Measurement type '%s' not found in file %s.hdf5", measurement_type, self.file
            )
            raise

    def _validate_long_dataset(self, dataset: DatasetDict) -> None:
        """
        Validate long dataset format.

        Parameters
        ----------
        dataset : DatasetDict
            The dataset to validate.

        Raises
        ------
        ValueError
            If the dataset format is invalid.
        """
        for measurement_iter in dataset:
            for t_data in dataset[measurement_iter]:
                try:
                    time_data = dataset[measurement_iter][t_data][1][0][0]
                    if not isinstance(time_data, (float, int, np.floating, np.integer)):
                        raise ValueError(
                            f"Time delay data for {measurement_iter}/{t_data} should be float, "
                            f"got {type(time_data).__name__}"
                        )

                    iq_data = dataset[measurement_iter][t_data][1][1][0]
                    if not isinstance(iq_data, (complex, np.complexfloating)):
                        raise ValueError(
                            f"I-Q pair data for {measurement_iter}/{t_data} should be complex "
                            f"(e.g., 4-6j), got {type(iq_data).__name__}"
                        )
                except (IndexError, KeyError, TypeError) as e:
                    raise ValueError(
                        f"Invalid dataset structure for {measurement_iter}/{t_data}: {e}"
                    ) from e

    def _validate_fidelity_dataset(self, dataset: DatasetDict) -> None:
        """
        Validate fidelity dataset format.

        Parameters
        ----------
        dataset : DatasetDict
            The dataset to validate.

        Raises
        ------
        ValueError
            If the dataset format is invalid.
        """
        for measurement_iter in dataset:
            for f_data in dataset[measurement_iter]:
                try:
                    iq_data = dataset[measurement_iter][f_data][1][0]
                    if not isinstance(iq_data, (complex, np.complexfloating)):
                        raise ValueError(
                            f"I-Q pair data for {measurement_iter}/{f_data} should be complex "
                            f"(e.g., 4-6j), got {type(iq_data).__name__}"
                        )
                except (IndexError, KeyError, TypeError) as e:
                    raise ValueError(
                        f"Invalid dataset structure for {measurement_iter}/{f_data}: {e}"
                    ) from e

    def _process_dataset_data(
        self, dataset_data: Any
    ) -> tuple[Any, np.ndarray | None, np.ndarray | None]:
        """Process and normalize dataset data, extracting time/IQ components if applicable."""
        separate_time: np.ndarray | None = None
        separate_iq: np.ndarray | None = None

        if isinstance(dataset_data, np.ndarray):
            if (
                dataset_data.ndim == EXPECTED_DATASET_ROWS
                and dataset_data.shape[0] == EXPECTED_DATASET_ROWS
            ):
                # row 0: time, row 1: complex IQ
                separate_time = np.asarray(dataset_data[0], dtype=np.float64)
                separate_iq = np.asarray(dataset_data[1], dtype=np.complex128)
        elif isinstance(dataset_data, (list, tuple)) and len(dataset_data) == EXPECTED_DATASET_ROWS:
            # list-like [time_list, iq_list]
            separate_time = np.asarray(dataset_data[0], dtype=np.float64)
            separate_iq = np.asarray(dataset_data[1], dtype=np.complex128)
            # Build a 2xN complex array for backward compatibility
            dataset_data = np.vstack([separate_time, separate_iq])

        return dataset_data, separate_time, separate_iq

    def _determine_maxshape(self, dataset_data: Any) -> tuple[int | None, ...] | None:
        """Determine maxshape for HDF5 dataset based on data dimensions."""
        if isinstance(dataset_data, np.ndarray):
            if dataset_data.ndim == 1:
                return (None,)
            elif dataset_data.ndim == EXPECTED_DATASET_ROWS:
                return (None, None)
        return None

    def _save_measurement_data(self, subgroup: h5py.Group, data_key: str, data_value: Any) -> None:
        """Save individual measurement data to HDF5 subgroup."""
        # Set timestamp attribute
        timestamp = data_value[0]
        subgroup.attrs[f"{data_key} time_stamp"] = timestamp

        # Process dataset data
        dataset_data, separate_time, separate_iq = self._process_dataset_data(data_value[1])
        maxshape = self._determine_maxshape(dataset_data)

        # Create main dataset
        subgroup.create_dataset(
            data_key,
            data=dataset_data,
            maxshape=maxshape,
            compression="gzip",
            compression_opts=9,
        )

        # Create separate time and iq datasets if available
        if separate_time is not None and separate_iq is not None:
            subgroup.create_dataset(
                f"{data_key}_time",
                data=separate_time,
                compression="gzip",
                compression_opts=9,
            )
            subgroup.create_dataset(
                f"{data_key}_iq",
                data=separate_iq,
                compression="gzip",
                compression_opts=9,
            )

    def _save_measurement_iteration(
        self, group: h5py.Group, measurement_iter: str, measurement_data: dict
    ) -> None:
        """Save data for a single measurement iteration."""
        subgroup_name = str(measurement_iter)
        if subgroup_name in group:
            logger.warning("Subgroup '%s' already exists, overwriting", subgroup_name)
            del group[subgroup_name]

        subgroup = group.create_group(subgroup_name, track_order=True)

        for data_key, data_value in measurement_data.items():
            try:
                self._save_measurement_data(subgroup, data_key, data_value)
            except (IndexError, TypeError, ValueError) as e:
                raise ValueError(
                    f"Invalid data format for {measurement_iter}/{data_key}: {e}"
                ) from e
            except Exception as e:
                logger.error(
                    "Unexpected error saving %s/%s: %s",
                    measurement_iter,
                    data_key,
                    e,
                    exc_info=True,
                )
                raise

    def _save_dataset_common(
        self, dataset: DatasetDict, metadata: MetadataDict, validator: Callable[[DatasetDict], None]
    ) -> None:
        """Save dataset and associated metadata to the HDF5 file."""
        logger.debug("Saving dataset with metadata: %s", metadata)

        # Validate metadata and dataset
        self.metadata_check(metadata)
        validator(dataset)

        measurement_type = metadata["measurement_type"]
        if not isinstance(measurement_type, str):
            raise ValueError(
                f"measurement_type must be string, got {type(measurement_type).__name__}"
            )

        try:
            with self._open_file("a") as file:
                # Create or get group
                if measurement_type in file:
                    logger.warning(
                        "Group '%s' already exists, data may be overwritten", measurement_type
                    )
                    group = file[measurement_type]
                else:
                    group = file.create_group(measurement_type)

                # Set metadata attributes
                for metadata_key, metadata_value in metadata.items():
                    group.attrs[metadata_key] = metadata_value

                # Save datasets
                for measurement_iter, measurement_data in dataset.items():
                    if isinstance(group, h5py.Group):
                        self._save_measurement_iteration(group, measurement_iter, measurement_data)

        except OSError as e:
            logger.error("File I/O error while saving dataset: %s", e, exc_info=True)
            raise

        logger.info("Dataset successfully saved to HDF5 file: %s", self.file)

    def save_long_dataset(self, dataset: DatasetDict, metadata: MetadataDict) -> None:
        """
        Save a long dataset to the HDF5 file.

        Parameters
        ----------
        dataset : DatasetDict
            The dataset to save, structured as a dictionary.
        metadata : MetadataDict
            Metadata associated with the dataset.

        Notes
        -----
        - Qubit data should be as I-Q pairs, and time data should be floats.
        - Metadata timestamps should be in datetime format.
        - Data is compressed using gzip for space efficiency.

        Raises
        ------
        ValueError
            If the dataset or metadata is improperly formatted.
        KeyError
            If required metadata fields are missing.
        """
        self._save_dataset_common(dataset, metadata, self._validate_long_dataset)

    def save_fidelity_data(self, dataset: DatasetDict, metadata: MetadataDict) -> None:
        """
        Save state separation data to the HDF5 file.

        Parameters
        ----------
        dataset : DatasetDict
            The dataset to save, structured as a dictionary.
        metadata : MetadataDict
            Metadata associated with the dataset.

        Notes
        -----
        - The dataset should include state separation data with timestamps.
        - Metadata is validated before saving.
        - Data is compressed using gzip for space efficiency.

        Raises
        ------
        ValueError
            If the dataset or metadata is improperly formatted.
        KeyError
            If required metadata fields are missing.
        """
        self._save_dataset_common(dataset, metadata, self._validate_fidelity_dataset)

    def metadata_check(self, metadata: MetadataDict) -> None:
        """
        Check metadata values against the mandatory metadata list.

        Parameters
        ----------
        metadata : MetadataDict
            A dictionary of metadata keys and corresponding values.

        Raises
        ------
        ValueError
            If mandatory metadata fields are missing or have invalid types.
        """
        missing_list: list[str] = []

        # True for mandatory fields, False for optional fields
        check_dict = self.metadata_requirements

        for key in metadata:
            if key not in self._metadata_allowed_keys:
                logger.warning(
                    "Metadata piece does not match existing schema: %s, "
                    "will pass into the HDF5 file anyway.",
                    key,
                )

        for check_key, is_mandatory in check_dict.items():
            if check_key not in metadata and is_mandatory:
                missing_list.append(check_key)

        if missing_list:
            missing_fields = ", ".join(missing_list)
            raise ValueError(
                f"Missing mandatory metadata fields: {missing_fields}. "
                f"Please add missing data and re-check."
            )

        logger.info("All mandatory metadata fields present, validation complete.")

    def read_file(self) -> h5py.File:
        """
        Open a database file and return the file handle.

        Returns
        -------
        h5py.File
            The opened HDF5 file handle.

        Notes
        -----
        This method returns a raw h5py.File object that must be manually closed by the user.
        """
        f = h5py.File(self.file, "r")
        return f

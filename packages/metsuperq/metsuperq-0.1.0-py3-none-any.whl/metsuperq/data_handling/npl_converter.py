"""NPL data converter module for QCoDeS database operations and data processing."""

import os
from typing import Any

import numpy as np
import qcodes.dataset as qd

from metsuperq.analysis.constants import MEASUREMENTS_PER_ITERATION
from metsuperq.utils import setup_logging

logger = setup_logging(__name__)

# Time conversion constants for NPL instrument data
# Instrument samples are in units that need conversion to physical time
SAMPLE_TO_MICROSECONDS = 40e-3  # Convert instrument samples to microseconds
SAMPLE_TO_SECONDS = 40e-9  # Convert instrument samples to seconds


# Known measurement type identifiers in NPL database
KNOWN_MEASUREMENT_TYPES = ["t1_data", "T2_Echo_data", "ramsey_data"]


def _extract_measurement_type_from_table(cursor: Any, table_name: str) -> str:
    """Extract measurement type identifier from database table parameters."""
    result_id = cursor.execute(
        "SELECT result_table_name,parameters FROM runs WHERE result_table_name=?", (table_name,)
    ).fetchall()

    try:
        parameters = result_id[0][1].split(",")  # split() already returns a list
    except (IndexError, AttributeError) as e:
        logger.warning(f"Failed to parse parameters for table {table_name}: {e}", exc_info=True)
        return "unknown_measurement"

    for item in parameters:
        if item in KNOWN_MEASUREMENT_TYPES:
            return item

    return "unknown_measurement"


def _fetch_iq_data(cursor: Any, table_name: str) -> list[complex]:
    """Fetch I and Q data from database and combine into complex numbers."""
    # Fetch I data
    cursor.execute("SELECT I FROM ?", (table_name,))
    i_data = [row[0] for row in cursor.fetchall() if isinstance(row[0], float)]

    # Fetch Q data
    cursor.execute("SELECT Q FROM ?", (table_name,))
    q_data = [row[0] for row in cursor.fetchall() if isinstance(row[0], float)]

    # Combine into complex numbers
    return [complex(i_val, q_val) for i_val, q_val in zip(i_data, q_data, strict=False)]


def _fetch_delay_data(cursor: Any, table_name: str) -> list[float]:
    """Fetch pulse delay data from database and convert to microseconds."""
    cursor.execute("SELECT pulse_delay FROM ?", (table_name,))
    delays = []

    for row in cursor.fetchall():
        if isinstance(row[0], (float, int, np.floating, np.integer)):
            # Convert from instrument sample to microseconds
            delays.append(float(np.round(row[0] * SAMPLE_TO_MICROSECONDS, 3)))

    return delays


def read_measurement_data_from_db(cursor: Any, table_entries: list[str]) -> dict[str, Any]:
    """Read quantum measurement data from database tables.

    Args:
        cursor: Database cursor object for executing SQL queries
        table_entries: List of table name entries to read data from

    Returns
    -------
        Dictionary containing organized measurement data with delays and complex IQ values
    """
    output_dict: dict[str, Any] = {}
    measurement_index = 0
    iteration_count = 0

    for table_entry in table_entries:
        table_name = table_entry[0]

        # Extract measurement type
        measurement_type = _extract_measurement_type_from_table(cursor, table_name)
        if measurement_type == "unknown_measurement":
            continue

        # Fetch data
        iq_data = _fetch_iq_data(cursor, table_name)
        delay_data = _fetch_delay_data(cursor, table_name)

        # Update output dictionary
        measurement_key = f"measurement_{measurement_index}"
        if measurement_key not in output_dict:
            logger.info("Added measurement index: %s", measurement_index)
            output_dict[measurement_key] = {}

        data_key = f"{measurement_type}_{measurement_index}"
        output_dict[measurement_key][data_key] = [delay_data, iq_data]
        iteration_count += 1

        if iteration_count == MEASUREMENTS_PER_ITERATION:
            measurement_index += 1
            iteration_count = 0

    return output_dict


# Backward compatibility alias
data_reader_from_db = read_measurement_data_from_db


def _add_datasets_to_output_dict(
    datasets: list, output_dict: dict[str, Any], measurement_type_prefix: str
) -> None:
    """Convert QCoDeS datasets to measurement dictionary format.

    Args:
        datasets: List of QCoDeS datasets to process
        output_dict: Dictionary to update with processed data
        measurement_type_prefix: Prefix for measurement type (e.g., "T1", "T2E", "T2R")
    """
    for index, dataset in enumerate(datasets):
        dataframe = dataset.to_pandas_dataframe()
        # Use .tolist() directly on numpy result - avoids intermediate array copy
        delay_times_s = (dataframe.pulse_delay.values * SAMPLE_TO_SECONDS).tolist()
        iq_values = (dataframe.I.values + 1j * dataframe.Q.values).tolist()
        timestamps = dataframe.time_stamp

        measurement_key = f"measurement_{index:04}"
        if measurement_key not in output_dict:
            output_dict[measurement_key] = {}

        data_key = f"{measurement_type_prefix}_{index:04}"
        output_dict[measurement_key][data_key] = {timestamps[0]: [delay_times_s, iq_values]}


def _load_experiment_datasets(experiment, experiment_name: str, start_offset: int, conn) -> list:
    """Load datasets for an experiment with interleaved run IDs.

    Args:
        experiment: Loaded QCoDeS experiment
        experiment_name: Name of the experiment for loading
        start_offset: Starting offset for run IDs (1 for T1, 2 for T2E, 3 for T2R)
        conn: Database connection

    Returns
    -------
        List of loaded datasets
    """
    datasets = []
    interleave_step = 3  # Experiments are interleaved with step of 3
    for i in range(start_offset, len(experiment) * interleave_step + 1, interleave_step):
        res_dataset = qd.load_by_run_spec(
            captured_run_id=i, experiment_name=experiment_name, conn=conn
        )
        datasets.append(res_dataset)
    return datasets


def read_from_qcodes_db(db_name: str) -> dict[str, Any]:
    """Read quantum measurement data from QCoDeS database.

    Args:
        db_name: Name of the database file

    Returns
    -------
        Dictionary containing organized measurement data from T1, T2Echo, and Ramsey experiments

    Note
    ----
        All database operations are performed within the connection scope.
        Data is extracted to Python objects before the connection is closed.
    """
    source_path = os.path.join(os.getcwd(), db_name)
    source_conn = qd.connect(source_path)

    try:
        # Load experiments and their datasets
        experiments = [
            ("T1", "T1", 1),
            ("T2Echo", "T2Echo", 2),
            ("ramsey_calibration", "ramsey_calibration", 3),
        ]
        prefixes = ["T1", "T2E", "T2R"]

        output_dict: dict[str, Any] = {}

        # All database access happens within this try block while connection is active
        for (exp_name, load_name, start_offset), prefix in zip(experiments, prefixes, strict=True):
            experiment = qd.load_experiment_by_name(name=exp_name, conn=source_conn)
            datasets = _load_experiment_datasets(experiment, load_name, start_offset, source_conn)
            # Data is converted to Python dicts/lists here, safe to use after connection closes
            _add_datasets_to_output_dict(datasets, output_dict, prefix)

        return output_dict
    finally:
        # Ensure connection is closed even if an exception occurs
        source_conn.close()
        logger.debug("Closed QCoDeS database connection: %s", source_path)


def convert_npl_to_hdf5_format(npl_data: dict[str, Any]) -> dict[str, Any]:
    """
    Convert NPL data format to HDF5DataManager expected format.

    Transforms:
        {measurement: {t_data: {timestamp: [delays, iq_vals]}}}
    To:
        {measurement: {t_data: [metadata, [[delays], [iq_vals]]]}}

    Parameters
    ----------
    npl_data : dict
        Data from read_from_qcodes_db()

    Returns
    -------
    dict
        Data in HDF5DataManager compatible format
    """
    logger.debug("Converting NPL data format to HDF5 format")
    converted = {}

    for measurement_iter, measurement_data in npl_data.items():
        converted[measurement_iter] = {}

        for t_data, time_data_dict in measurement_data.items():
            # Extract first (and typically only) timestamp entry using next()
            timestamp, data_arrays = next(iter(time_data_dict.items()))
            delays, iq_vals = data_arrays

            # Convert to expected HDF5 format: [metadata, [delays_array, iq_array]]
            converted[measurement_iter][t_data] = [
                timestamp,  # metadata (timestamp)
                [delays, iq_vals],  # [delays_array, iq_array]
            ]

    logger.debug("Converted %d measurements to HDF5 format", len(converted))
    return converted


def convert_from_dataset(long_interleaved_dataset: dict[str, Any]) -> dict[str, Any]:
    """Convert dataset format to organized measurement dictionary.

    Args:
        long_interleaved_dataset: Input dataset in interleaved format

    Returns
    -------
        Dictionary with converted measurement data structure
    """
    result_dict = {}

    for _measurement_iter, measurement_data in long_interleaved_dataset.items():
        iteration_dict = {}
        for measurement_type, type_data in measurement_data.items():
            timestamp = type_data[0]
            dataset = type_data[1].to_pandas_dataframe()
            delay_us = (dataset.pulse_delay.values * SAMPLE_TO_MICROSECONDS).tolist()
            # Vectorized complex number creation - much faster than loop
            iq_values = (dataset.I.values + 1j * dataset.Q.values).tolist()
            iteration_dict[measurement_type] = {timestamp: [delay_us, iq_values]}
        result_dict.update(iteration_dict)
    return result_dict

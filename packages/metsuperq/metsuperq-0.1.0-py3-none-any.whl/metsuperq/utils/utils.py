"""Utility functions."""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any

import numpy as np


def setup_logging(name: str, level: str | None = None) -> logging.Logger:
    """Set up logging with enhanced configuration for quantum measurements.

    Parameters
    ----------
    name : str
        Name of the logger (typically __name__)
    level : str | None, optional
        Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        If None, uses LOG_LEVEL environment variable or defaults to DEBUG.

    Returns
    -------
    logging.Logger
        Configured logger instance with enhanced formatting
    """
    logger = logging.getLogger(name)

    # Only configure if not already configured to avoid duplicate handlers
    if not logger.handlers:
        # Determine log level from parameter or environment
        if level is None:
            level = os.getenv("LOG_LEVEL", "DEBUG").upper()

        # Convert string level to logging level constant
        level_constant = getattr(logging, level.upper(), logging.INFO)
        logger.setLevel(level_constant)

        # Create handler with enhanced formatting
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s | %(name)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        handler.setLevel(level_constant)
        logger.addHandler(handler)

        # Prevent propagation to avoid duplicate logs
        logger.propagate = False

    return logger


def ensure_directory_exists(directory: Path | str) -> None:
    """Ensure a directory exists, creating it and parents if necessary.

    Parameters
    ----------
    directory : Path | str
        Directory path to ensure exists
    """
    Path(directory).mkdir(parents=True, exist_ok=True)


# Backward compatibility alias
check_and_create_dir = ensure_directory_exists


def serialize_for_json(obj: Any) -> Any:
    """Convert numpy types and other objects for JSON serialization.

    Parameters
    ----------
    obj : Any
        Object to convert for JSON serialization

    Returns
    -------
    Any
        JSON-serializable object

    Raises
    ------
    TypeError
        If the object cannot be serialized to JSON
    """
    try:
        # Handle different types with consolidated logic
        conversion_map = {
            np.integer: int,
            np.floating: float,
        }

        for obj_type, converter in conversion_map.items():
            if isinstance(obj, obj_type):
                return converter(obj)

        # Handle special cases
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: serialize_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [serialize_for_json(item) for item in obj]
        elif isinstance(obj, (str, int, float, bool, type(None))):
            return obj
        else:
            # Try to serialize the object to JSON to see if it's serializable
            json.dumps(obj)
            return obj
    except (TypeError, OverflowError) as e:
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable") from e


def read_json(file_path: Path | str) -> Any:
    """Read a JSON file and return its contents.

    Parameters
    ----------
    file_path : Path | str
        Path to JSON file

    Returns
    -------
    Any
        Parsed JSON data

    Raises
    ------
    FileNotFoundError
        If file doesn't exist
    json.JSONDecodeError
        If file contains invalid JSON
    """
    try:
        with open(file_path) as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"JSON file not found: {file_path}") from e
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in file: {file_path}", e.doc, e.pos) from e


def write_json(data: Any, file_path: Path | str, indent: int = 2) -> None:
    """Write data to a JSON file with proper serialization.

    Parameters
    ----------
    data : Any
        Data to write to JSON
    file_path : Path | str
        Output file path
    indent : int, optional
        JSON indentation, by default 2

    Raises
    ------
    TypeError
        If data cannot be serialized to JSON
    """
    # Ensure directory exists
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    # Serialize data
    serialized_data = serialize_for_json(data)

    try:
        with open(file_path, "w") as f:
            json.dump(serialized_data, f, indent=indent)
    except TypeError as e:
        raise TypeError(f"Cannot serialize data to JSON: {e}") from e

"""Constants for the base measurement analyzer."""

from __future__ import annotations

# Measurement types
MEASUREMENT_TYPES = ["t1", "t2e", "t2r"]

# Plot configuration
PLOT_CONFIG = {
    "figsize_per_plot": 5,
    "height": 4,
    "dpi": 300,
    "alpha": 0.7,
    "grid_alpha": 0.3,
}

# File patterns
HDF5_PATTERN = "**/*.hdf5"
DEFAULT_MEASUREMENT_TYPE = "coherence_dataset"

# Fit parameters
DEFAULT_FIT_POINTS = 100

# Data structure constants
EXPECTED_DATASET_ROWS = 2  # Expected number of rows in dataset (time, IQ data)
MIN_POINTS_FOR_FFT = 3  # Minimum points needed for FFT frequency estimation

# Function complexity limits
MAX_RETURN_STATEMENTS = 6  # Maximum return statements allowed in functions
MAX_FUNCTION_ARGUMENTS = 5  # Maximum arguments allowed in function definition
MAX_FUNCTION_STATEMENTS = 50  # Maximum statements allowed in functions
MAX_FUNCTION_BRANCHES = 12  # Maximum branches allowed in functions
MAX_FUNCTION_COMPLEXITY = 10  # Maximum cyclomatic complexity

# Data processing constants
IQ_PAIR_SIZE = 2  # Size of I-Q measurement pair
MEASUREMENTS_PER_ITERATION = 2  # Number of measurements per iteration in converter

# Measurement validation thresholds
MAX_TIME_SCALE_WARNING = 1e-3  # Time scale above 1 ms triggers warning for qubit measurements
MAX_TIME_SCALE_ERROR = 1.0  # Time scale above 1 s is invalid for qubit coherence

# Time unit defaults for fitting
DEFAULT_DECAY_TIME_S = 1e-6  # Default decay time: 1 μs
MIN_DECAY_TIME_S = 1e-9  # Minimum decay time: 1 ns
DEFAULT_FREQUENCY_HZ = 1e3  # Default detuning frequency: 1 kHz
MAX_FREQUENCY_HZ = 1e6  # Maximum detuning frequency: ±1 MHz

# Oscillation fitting
MIN_POINTS_PER_OSCILLATION = 4  # Minimum data points per oscillation period
MIN_OSCILLATIONS_FOR_FIT = 2  # Minimum oscillations needed for reliable fit

# Unit conversions
SECONDS_TO_MICROSECONDS = 1e6  # Multiply seconds by this to get microseconds

# Project root search
MAX_PROJECT_ROOT_DEPTH = 50  # Maximum directory levels to search for project root

# Test constants
TEST_DECAY_TIME = 10.0  # Test decay time value in seconds
TEST_PLOT_SIZE = 5  # Test plot size
TEST_PLOT_HEIGHT = 4  # Test plot height
TEST_DPI = 300  # Test DPI value
TEST_ALPHA = 0.7  # Test alpha value
TEST_GRID_ALPHA = 0.3  # Test grid alpha value
TEST_FIT_POINTS = 100  # Test fit points value
TEST_DATA_LENGTH = 3  # Test data length for validation

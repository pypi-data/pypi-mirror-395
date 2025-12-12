# MetSuperQ

[![PyPI version](https://img.shields.io/pypi/v/metsuperq.svg)](https://pypi.org/project/metsuperq/)
[![Python versions](https://img.shields.io/pypi/pyversions/metsuperq.svg)](https://pypi.org/project/metsuperq/)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](LICENSE)

Quantum measurement analysis with integrated InfluxDB time-series storage.

## Features

- **Quantum Measurement Analysis**: T1, T2 echo, and T2 Ramsey measurement analysis
- **InfluxDB Integration**: Modern time-series database storage
- **User-Friendly API**: Simple interface for users to record measurements
- **Comprehensive Validation**: Pydantic-based data validation at all boundaries
- **Performance Monitoring**: Built-in logging and performance tracking

## Quick Start

### Prerequisites

- Python 3.12+
- InfluxDB v2.x (optional)

### Installation

**For users** (install from PyPI or source):

```bash
# From PyPI (when published)
pip install metsuperq

# Or from source
git clone https://code.orangeqs.com/opensource/metsuperq.git
```

**For developers** (using [uv](https://docs.astral.sh/uv/)):

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and install in development mode
git clone https://code.orangeqs.com/opensource/metsuperq.git
cd metsuperq
uv sync  # Installs all dev dependencies
```

See [Installation Guide](docs/tutorials/installation.md) for detailed setup.

### Basic Usage

```python
from metsuperq.analysis import BaseAnalyzer
from metsuperq.integrations import record_measurement

# Run analysis
analyzer = BaseAnalyzer()
result = analyzer.run_full_analysis("20241008-143022-123-abcdef")

# Record to database
record_measurement(
    analysis_result=result,
    experiment_id="experiment_1",
    device_name="device_1",
    qubit_name="Q1",
)
```

## Development

This project uses [uv](https://docs.astral.sh/uv/) for fast, reproducible dependency management.

```bash
# Install dependencies and set up environment
uv sync

# Run pre-commit hooks
uv run pre-commit install
uv run pre-commit run --all-files

# Run tests
uv run pytest

# Run type checking
uv run pyright
```

See [Contributing Guide](docs/how-to/contributing.md) for details.

## Documentation

- [Installation Guide](docs/tutorials/installation.md)
- [API Reference](docs/reference/)
- [Architecture Overview](docs/explanation/architecture.md)

## Contributing

Fork, create a feature branch, add tests, and submit a PR. See [Contributing Guide](docs/how-to/contributing.md).

## License

BSD 3-Clause License. See [LICENSE](LICENSE) for details.

## Support

- **Documentation**: [Project Docs](https://opensource.orangeqs.info/metsuperq)
- **Issues** and **Discussions**: [GitLab Issues](https://code.orangeqs.com/opensource/metsuperq/-/issues)
- **Merge Requests**: [GitLab Merge Requests](https://code.orangeqs.com/opensource/metsuperq/-/merge_requests)

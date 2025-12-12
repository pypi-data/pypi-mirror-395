<div align="center">

# Reminder Aggregator

**A simple Python tool that scans files for common reminder tags like TODO and FIXME to generate a report from them.**

[![PyPI - Version](https://img.shields.io/pypi/v/reminder-aggregator)](https://pypi.org/project/reminder-aggregator/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/reminder-aggregator)](https://pypi.org/project/reminder-aggregator/)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)

</div>

## Requirements

- Python 3.10+

## Installation

From PyPI (recommended):

```bash
pip install reminder-aggregator
```

From source with [uv](https://docs.astral.sh/uv/getting-started/installation/):

```bash
git clone https://github.com/NocDerEchte/reminder-aggregator.git
cd reminder-aggregator

uv sync
uv run reminder-aggregator --help
```

## Usage

Scan current directory:

```bash
reminder-aggregator
```

Scan specific directory:

```bash
reminder-aggregator /path/to/directory
```

Specify output file:

```bash
reminder-aggregator --out-file /path/to/report.json
```

Show all available options:

```bash
reminder-aggregator --help
```

## Docker Usage

Run the containerized version by mounting your project directory:

```bash
docker run --rm -v "$(pwd):/work" nocderechte/reminder-aggregator:latest
```

## Roadmap

- [x] Filter to check whether a reminder-tag is inside a comment (currently causes false positives)
- [ ] Support for multiple output formats
  - [x] junitxml
  - [ ] raw/stdout
  - [x] codeclimate

## License

GNU General Public License v3.0 or later

See [LICENSE](./LICENSE) to see the full text.

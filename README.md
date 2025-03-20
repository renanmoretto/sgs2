# SGS2

A lightweight Python library for fetching historical economic data from the Brazilian Central Bank's SGS system.

## Installation

```bash
pip install sgs2
```

## Usage

### Quick Start

```python
import sgs2 as sgs

# Get a time series as a pandas DataFrame
sgs.dataframe(12)  # CDI (Brazilian Interbank Deposit Rate)

# Get data with a custom date range
sgs.dataframe(12, start='2020-01-01', end='2021-01-01')

# Get multiple series with custom column names
sgs.dataframe({433: 'ipca', 189: 'igpm'})

# Get a single series as a pandas Series
sgs.series(12)
sgs.series({12: 'cdi'})  # With custom name
```

#### `json()`

Fetch the raw JSON data from the API (to be implemented).

#### `metadata()`

Fetch metadata about a series (to be implemented).

#### `search()`

Fetch metadata about a series (to be implemented).

## Data Codes

Some common series codes:

- `12`: CDI (Brazilian Interbank Deposit Rate)
- `433`: IPCA
- `189`: IGP-M (General Market Price Index)

## License

MIT

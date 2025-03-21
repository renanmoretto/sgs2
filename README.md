# SGS2

A lightweight Python library for fetching historical economic data from the Brazilian Central Bank's SGS system.

## Installation

```bash
pip install sgs2
```

## Usage

### `dataframe()`

Fetch time series data as a pandas DataFrame.

```python
import sgs2 as sgs

# Get a single time series as a DataFrame
df = sgs.dataframe(12)  # CDI (Brazilian Interbank Deposit Rate)
# Returns a DataFrame with date as index and code as column name

# Get data with a custom date range
df = sgs.dataframe(12, start='2020-01-01', end='2021-01-01')

# Get multiple series at once
df = sgs.dataframe([12, 433, 189])
# Returns a DataFrame with date as index and codes as column names

# Get multiple series with custom column names
df = sgs.dataframe({433: 'ipca', 189: 'igpm', 12: 'cdi'})
# Returns a DataFrame with date as index and custom names as column names
```

### `series()`

Fetch a single time series as a pandas Series.

```python
import sgs2 as sgs

# Get a single time series as a Series
s = sgs.series(12)  # CDI (Brazilian Interbank Deposit Rate)
# Returns a Series with date as index and values as data

# Get data with a custom date range
s = sgs.series(12, start='2020-01-01', end='2021-01-01')

# Get a series with a custom name
s = sgs.series({12: 'cdi'})
# Returns a Series with date as index and 'cdi' as name
```

### `json()`

Fetch the raw JSON data from the API.

```python
# Get JSON data for a single series
sgs.json(12)

# Get JSON data with a custom date range
sgs.json(12, start='2020-01-01', end='2021-01-01')

# Get JSON data for multiple series as a list
sgs.json([12, 433, 189])

# Get JSON data for multiple series with custom names
sgs.json({12: 'cdi', 433: 'ipca', 189: 'igpm'})

# All parameters work the same as with dataframe()
sgs.json([12, 433], start='2020-01-01', end='2021-01-01')
```

### `metadata()`

Fetch metadata about a series.

```python
sgs.metadata(12)
```

Example output:
```python
{
  'code': '12',
  'name': 'Taxa de juros - CDI',
  'unit': '% a.d.',
  'frequency': 'D',
  'start_date': '06/03/1986',
  'end_date': '19/03/2025',
  'source_name': 'Cetip',
  'special': 'N'
}
```

### `search()`

Search for series by keyword.

```python
sgs.search('cdi')
```

Example output:
```python
[
  {
    'code': '12',
    'name': 'Taxa de juros - CDI',
    'unit': '% a.d.',
    'frequency': 'D',
    'start_date': '06/03/1986',
    'end_date': '19/03/2025',
    'source_name': 'Cetip',
    'special': 'N'
  },
  {
    'code': '4389',
    'name': 'Taxa de juros - CDI anualizada base 252',
    'unit': '% a.a.',
    'frequency': 'D',
    'start_date': '06/03/1986',
    'end_date': '19/03/2025',
    'source_name': 'BCB-Demab',
    'special': 'N'
  },
  {
    'code': '4391',
    'name': 'Taxa de juros - CDI acumulada no mês',
    'unit': '% a.m.',
    'frequency': 'M',
    'start_date': '31/07/1986',
    'end_date': 'mar/2025',
    'source_name': 'BCB-Demab',
    'special': 'N'
  },
  {
    'code': '4392',
    'name': 'Taxa de juros - CDI acumulada no mês anualizada base 252',
    'unit': '% a.a.',
    'frequency': 'M',
    'start_date': '31/07/1986',
    'end_date': 'mar/2025',
    'source_name': 'BCB-Demab',
    'special': 'N'
  }
]
```

## Data Codes

Some common series codes:

- `12`: CDI (Brazilian Interbank Deposit Rate)
- `433`: IPCA
- `189`: IGP-M (General Market Price Index)

## License

MIT

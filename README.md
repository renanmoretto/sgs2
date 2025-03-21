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

#### `metadata()`

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

#### `search()`

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

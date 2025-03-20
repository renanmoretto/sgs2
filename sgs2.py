import datetime
from typing import Optional, Union, Dict, List

import requests
import pandas as pd


URL = "https://api.bcb.gov.br"


def _get_url(
    code: int,
    start: Optional[datetime.date] = None,
    end: Optional[datetime.date] = None,
) -> str:
    start = start.strftime("%d/%m/%Y") if start else ""
    end = end.strftime("%d/%m/%Y") if end else ""
    return f"{URL}/dados/serie/bcdata.sgs.{code}/dados?formato=json&dataInicial={start}&dataFinal={end}"


def _get_data_json(
    code: int,
    start: Optional[datetime.date] = None,
    end: Optional[datetime.date] = None,
) -> List[dict]:
    url = _get_url(code, start, end)
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def _get_data(
    code: int,
    start: Optional[datetime.date] = None,
    end: Optional[datetime.date] = None,
    rename_to: Optional[str] = None,
) -> pd.Series:
    data = _get_data_json(code, start, end)
    values = [v["valor"] for v in data]
    s = pd.Series(
        pd.to_numeric(values), index=pd.to_datetime([v["data"] for v in data])
    )
    s.index.name = "data"
    s.name = rename_to or "valor"
    return s


def series(
    code: Union[int, Dict[int, str]],
    start: Optional[Union[datetime.date, str]] = None,
    end: Optional[Union[datetime.date, str]] = None,
) -> pd.Series:
    """Fetch a single time series from the Brazilian Central Bank's SGS.

    Parameters
    ----------
    code : int or dict
        If int, the code of the series to fetch.
        If dict, a single key-value pair where key is the series code and value is the desired name.
    start : datetime.date or str, optional
        Start date for the series data. If string, must be in 'YYYY-MM-DD' format.
        If None, fetches from the earliest available date.
    end : datetime.date or str, optional
        End date for the series data. If string, must be in 'YYYY-MM-DD' format.
        If None, fetches until the latest available date.

    Returns
    -------
    pandas.Series
        A time series with dates as index and values as data.
        The series name will be 'valor' for integer codes or the specified name for dict input.

    Examples
    --------
    >>> sgs.series(12)  # Get CDI series with default name
    >>> sgs.series({12: 'cdi'})  # Get CDI series with custom name
    >>> sgs.series(12, start='2020-01-01')  # Get CDI from specific start date
    >>> sgs.series(12, start='2015-01-01', end='2020-01-01')  # Get date range
    """
    if isinstance(start, str):
        start = datetime.datetime.strptime(start, "%Y-%m-%d").date()
    if isinstance(end, str):
        end = datetime.datetime.strptime(end, "%Y-%m-%d").date()

    if isinstance(code, int):
        return _get_data(code, start, end)

    elif isinstance(code, dict):
        if len(code) > 1:
            raise ValueError(
                "Only one code is allowed when using a 'series' function. For multiple codes use 'dataframe' function."
            )

        _code = list(code.keys())[0]
        _name = code[_code]
        return _get_data(_code, start, end, rename_to=_name)


def dataframe(
    code: Union[int, List[int], Dict[int, str]],
    start: Optional[Union[datetime.date, str]] = None,
    end: Optional[Union[datetime.date, str]] = None,
) -> pd.DataFrame:
    """Fetch one or multiple time series from the Brazilian Central Bank's SGS as a DataFrame.

    Parameters
    ----------
    code : int or list or dict
        If int, fetches a single series.
        If list, fetches multiple series using the codes in the list.
        If dict, fetches series using codes as keys and uses the values as column names.
    start : datetime.date or str, optional
        Start date for the series data. If string, must be in 'YYYY-MM-DD' format.
        If None, fetches from the earliest available date.
    end : datetime.date or str, optional
        End date for the series data. If string, must be in 'YYYY-MM-DD' format.
        If None, fetches until the latest available date.

    Returns
    -------
    pandas.DataFrame
        A DataFrame with dates as index and series values as columns.
        Column names will be 'valor' for integer codes or the specified names for dict input.

    Examples
    --------
    >>> sgs.dataframe(12)  # Single series
    >>> sgs.dataframe([12, 433])  # Multiple series
    >>> sgs.dataframe({12: 'cdi', 433: 'poupanca'})  # Multiple series with custom names
    >>> sgs.dataframe(12, start='2020-01-01')  # From specific start date
    >>> sgs.dataframe(12, start='2015-01-01', end='2020-01-01')  # Date range
    """
    if isinstance(start, str):
        start = datetime.datetime.strptime(start, "%Y-%m-%d").date()
    if isinstance(end, str):
        end = datetime.datetime.strptime(end, "%Y-%m-%d").date()

    if isinstance(code, int):
        data = _get_data(code, start, end)

    elif isinstance(code, list):
        data = pd.DataFrame()
        for c in code:
            single_data = _get_data(c, start, end)
            data = pd.concat([data, single_data], axis=1)

    elif isinstance(code, dict):
        data = pd.DataFrame()
        for c, name in code.items():
            single_data = _get_data(c, start, end, rename_to=name)
            data = pd.concat([data, single_data], axis=1)

    return data

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
    start: Optional[datetime.date] = None,
    end: Optional[datetime.date] = None,
) -> pd.Series:
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
    start: Optional[datetime.date] = None,
    end: Optional[datetime.date] = None,
) -> pd.DataFrame:
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

import io
import json
import logging
from functools import wraps
from typing import Dict, Optional

import numpy as np
import pandas as pd
import pandas.io.json as pj
import requests

from datafarmclient.schemas import DateTime


def ensure_auth(func):
    """Reauthenticate if access token is expired / not set"""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except requests.HTTPError as e:
            if e.response.status_code == 401 and self._client.connected:
                logging.info("Session expired. You need to reconnect")
            else:
                raise e

    return wrapper


def json_to_pandas(json_input: str) -> pd.DataFrame:
    """Converts a json string to a pandas dataframe."""
    columns = []
    data = json.loads(json_input)

    if "schema" not in data:
        raise ValueError("No schema in data")

    for f in data["schema"]["fields"]:
        columns.append(f["name"])
    if "data" not in data:
        return pd.DataFrame(columns=columns)

    df = pd.read_json(
        io.StringIO(json.dumps(data["data"])), orient="values"
    )  # Create the dataframe from values - index is being created automatically, that should be ignored!
    df.columns = columns

    dict_fields = data["schema"]["fields"]
    df_fields = pj.build_table_schema(df, index=False)["fields"]
    for dict_field, df_field in zip(dict_fields, df_fields):
        if dict_field["type"] != df_field["type"]:
            if dict_field["type"] == "datetime":
                dt_col = pd.to_datetime(df.loc[:, dict_field["name"]], unit="ms")
                df = df.astype({dict_field["name"]: "datetime64[ns]"})
                df.loc[:, dict_field["name"]] = dt_col
            if dict_field["type"] == "number":
                df.loc[:, dict_field["name"]] = df.loc[:, dict_field["name"]].astype(
                    float
                )
    df.set_index(
        data["schema"]["primaryKey"][0], inplace=True
    )  # Setting index in actual dataframe, Assume index name from PK
    return df


def format_datetime(dt: DateTime) -> str:
    """Returns an ISO8601 formated datetime string.
    E.g. 2015-03-24T10:16:45.034Z
    """
    datetime_obj = pd.to_datetime(dt)
    return datetime_obj.isoformat(timespec="milliseconds") + "Z"


def format_float(x: Optional[float]) -> Dict[str, float]:
    """Format a float for JSON serialization."""
    if x is None or np.isnan(x):
        return {"N": 1, "V": 0.0}
    return {"N": 0, "V": float(x)}

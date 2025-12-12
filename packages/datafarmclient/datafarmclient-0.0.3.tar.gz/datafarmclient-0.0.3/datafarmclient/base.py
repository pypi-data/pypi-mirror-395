from __future__ import annotations

import json
import logging
from functools import cached_property, partial
from typing import Any, Dict, Optional

import pandas as pd
import requests

import datafarmclient
from datafarmclient.schemas import EntityType
from datafarmclient.utils import ensure_auth, json_to_pandas


class DatafarmClient:
    """Base `DatafarmClient` class, the main entrypoint to use the client.

    Attributes:
        api_url: The instantiated api url.
        timeseries: The timeseries subclass
        variables: The variables subclass
        entities: The entities subclass that you instantiate with an Entitytype

    Examples:
        >>> from datafarmclient import DatafarmClient
        >>> client = DatafarmClient(api_url=api_url)
        >>> client.login(api_key=api_key)
        True

    """

    def __init__(self, api_url: str):
        """Base-class initializer.

        Args:
            api_url: The URL for which api server to use.
        """
        self.api_url = self.validate_api_url(api_url)
        self.session = requests.Session()
        self.connected = False
        self.timeseries = datafarmclient.timeseries.TimeSeries(client=self)
        self.variables = datafarmclient.variables.Variables(client=self)
        self.entities = partial(datafarmclient.entities.Entities, client=self)

    @staticmethod
    def validate_api_url(host_address: str):
        response = requests.get(f"{host_address}/api/System/ServerTime")
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.error("No datafarm api found at that url")
        return f"{host_address}/api"

    def login(self, api_key: str) -> bool:
        """Connect to the Datafarm API.

        Args:
            api_key: A valid API key for the class api url.

        Returns:
            Whether or not you succesfully logged in.
        """
        url = self.api_url + "/Login/Login"
        data = {"Token": api_key}
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            reason = err.response.json()["error"]
            raise Exception(f"Connection attempt failed due to {reason}")
        else:
            try:
                access_token = response.headers["Access-Token"]
            except KeyError:
                logging.error("No Access-Token in response from server")
                return False
            else:
                self.session.headers.update({"Access-Token": access_token})
                self.connected = True
                logging.info("Succesfully logged in")
                return True

    def logoff(self) -> None:
        """Close the connection to the Datafarm API."""
        url = self.api_url + "/Login/Logoff"
        response = self.session.post(url)
        response.raise_for_status()
        self.session.headers.update({"Access-Token": ""})
        self.connected = False
        logging.info("Logged off")

    @ensure_auth
    def list(self, class_id: EntityType):
        return self.entities(class_id=class_id).list()

    @cached_property
    @ensure_auth
    def time_series_source_descriptions(self) -> pd.DataFrame:
        endpoint = "/List/TimeSeriesSourceDescriptions"
        return self._get_pandas_df(endpoint)

    @cached_property
    @ensure_auth
    def units(self) -> pd.DataFrame:
        endpoint = "/List/Units"
        return self._get_pandas_df(endpoint)

    @cached_property
    @ensure_auth
    def time_series_types(self) -> pd.DataFrame:
        endpoint = "/List/TimeSeriesTypes"
        return self._get_pandas_df(endpoint)

    @cached_property
    @ensure_auth
    def time_series_status(self) -> pd.DataFrame:
        endpoint = "/List/TimeSeriesStatus"
        return self._get_pandas_df(endpoint)

    @cached_property
    @ensure_auth
    def qualities(self) -> pd.DataFrame:
        endpoint = "/List/Qualities"
        return self._get_pandas_df(endpoint)

    @cached_property
    @ensure_auth
    def parameters(self) -> pd.DataFrame:
        endpoint = "/List/Parameters"
        return self._get_pandas_df(endpoint)

    @cached_property
    @ensure_auth
    def medias(self) -> pd.DataFrame:
        endpoint = "/List/Medias"
        return self._get_pandas_df(endpoint)

    @cached_property
    @ensure_auth
    def locations(self) -> pd.DataFrame:
        endpoint = "/List/Locations"
        return self._get_pandas_df(endpoint)

    @cached_property
    @ensure_auth
    def quality_level_to_name(self) -> Dict[int, str]:
        df = self.qualities
        return {df["Level"].iloc[i]: df["IDName"].iloc[i] for i in range(len(df))}

    @cached_property
    @ensure_auth
    def quality_name_to_level(self) -> Dict[str, int]:
        df = self.qualities
        return {df["IDName"].iloc[i]: df["Level"].iloc[i] for i in range(len(df))}

    def _get_pandas_df(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> pd.DataFrame:
        url = self.api_url + endpoint
        r = self.session.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        return json_to_pandas(json.dumps(data))

    def __enter__(self) -> DatafarmClient:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.logoff()

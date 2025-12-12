import base64
import datetime
import json
import logging
import os
from typing import Any, Dict, List, Literal, Optional, Union

import pandas as pd
import pandera.pandas as pa
import requests

from datafarmclient.base import DatafarmClient
from datafarmclient.exceptions import EntityNotFoundError, QualityError
from datafarmclient.schemas import (
    DateTime,
    Fields,
    TAggregation,
    TAggregationMethod,
    TAggregationPeriod,
    TGapFill,
    TimeSeriesInsertSchema,
    TPeriodDirection,
)
from datafarmclient.utils import (
    ensure_auth,
    format_datetime,
    format_float,
    json_to_pandas,
)


class TimeSeries:
    """A TimeSeries subclass for the base class."""

    def __init__(self, client: DatafarmClient):
        """
        Args:
            client: The base client allowing the subclass to use
                the shared session and client methods.
        """
        self._client = client

    @ensure_auth
    def get_data(
        self,
        time_series_id: Union[str, List[str]],
        start: DateTime = datetime.datetime(1900, 1, 1, 0, 0, 0, 0),
        end: DateTime = datetime.datetime(2100, 1, 1, 0, 0, 0, 0),
        fields: Optional[List[Fields]] = None,
        qualities: Optional[List[str]] = None,
        aggregation: Optional[TAggregation] = None,
        limit: int = 0,
        ascending: bool = True,
    ) -> List[pd.DataFrame]:
        """Get data from Datafarm.

        Args:
            time_series_id: The time series to get data from.
            start: The start of the range to get data from.
            end: The end of the range to get data from.
            fields: fields/columns to return
            qualities: Filter the data by qualities.
            aggregation: Complex data structure that gets constructed with
                create_aggregation() or create_resample().
            limit: The maximum number of rows to return.
            ascending: Whether to sort the data in ascending order.

        Returns:
            List of dataframes.

        Raises:
            EntityNotFoundError: An error occurs if no timeseries are found.
        """
        start = format_datetime(start)
        end = format_datetime(end)
        qualities = qualities or []
        fields = fields or []
        aggregation = aggregation.model_dump(mode="json") if aggregation else {}
        sort_order = "soAscending" if ascending else "soDescending"
        if isinstance(time_series_id, str):
            time_series_id = [time_series_id]

        url = self._client.api_url + "/TimeSeries/ExtractData"
        body = {
            "TimeSeries": time_series_id,
            "ISO8601_TimeStamp": False,
            "LimitRowCount": limit,
            "Qualities": qualities,
            "RangeEnd": end,
            "RangeStart": start,
            "SortOrder": sort_order,
            "Fields": fields,
            "Aggregation": aggregation,
        }
        response = self._client.session.post(url, json=body)
        response.raise_for_status()
        
        if "error" in response.json():
            raise SystemError(response.json()["error"])    
        else:
            datasets = response.json()["datasets"]
            if datasets:
                resp = []
                for dataset in datasets:
                    resp.append(json_to_pandas(json.dumps(dataset)))
                return resp
            else:
                raise EntityNotFoundError("No timeseries found for that request")

    @ensure_auth
    def delete_data(
        self,
        time_series_id: str,
        timestamps: Optional[List[DateTime]] = None,
        start: Optional[DateTime] = None,
        end: Optional[DateTime] = None,
    ) -> requests.Response:
        """
        Delete data from a time series.
        Either timestamps or start and end must be provided.

        Args:
            time_series_id: The time series to delete data from.
            timestamps: The timestamps to delete.
            start: The start of the range to delete data from.
            end: The end of the range to delete data from.
                Note that this is NOT inclusive.

        Returns:
            Response from the API.

        Raises:
            HttpError: Requests threw an exception
        """
        if timestamps is None and (start is None or end is None):
            raise ValueError("Either timestamps or start and end must be provided.")
        if timestamps is not None and (start is not None or end is not None):
            raise ValueError("Either timestamps or start and end must be provided.")
        if timestamps is not None:
            return self._delete_data_timestamps(time_series_id, timestamps)

        return self._delete_data_range(time_series_id, start, end)

    @ensure_auth
    def update_data_quality(
        self,
        time_series_id: str,
        qualities: pd.Series,
    ) -> requests.Response:
        """Update the quality of data in a time series.

        Args:
            time_series_id: The time series to update.
            qualities: The qualities to set.

        Returns:
            Response from the API.

        Raises:
            HttpError: Requests threw an exception
        """
        try:
            new_qualities = [
                int(self._client.quality_name_to_level[q])
                if isinstance(q, str)
                else int(q)
                for q in qualities
            ]
        except KeyError:
            raise QualityError(
                "Quality must be one of: {}".format(
                    ", ".join(self._client.quality_name_to_level.keys())
                )
            )

        endpoint = "/TimeSeries/UpdateDataQuality"
        url = self._client.api_url + endpoint
        body = {
            "TimeSeriesName": time_series_id,
            "TimeStamp": [format_datetime(ts) for ts in list(qualities.index)],
            "QualityLevel": new_qualities,
        }
        response = self._client.session.post(url, json=body)
        response.raise_for_status()
        return response

    @ensure_auth
    def update_data_quality_range(
        self,
        time_series_id: str,
        quality: Union[int, str],
        start: DateTime,
        end: DateTime,
    ) -> requests.Response:
        """Update the quality of data in a range in a time series.

        Args:
            time_series_id: The time series to update.
            start: The start of the range to update data quality from.
            end: The end of the range to update data quality from.
                Note that this is NOT inclusive.
            quality: The quality to set.

        Returns:
            Response from the API.

        Raises:
            HttpError: Requests threw an exception
        """
        if isinstance(quality, str):
            try:
                new_quality = int(self._client.quality_name_to_level[quality])
            except KeyError:
                raise QualityError(
                    "Quality must be one of: {}".format(
                        ", ".join(self._client.quality_name_to_level.keys())
                    )
                )
        else:
            new_quality = quality

        endpoint = "/TimeSeries/UpdateDataQualityRange"
        url = self._client.api_url + endpoint
        body = {
            "TimeSeriesName": time_series_id,
            "RangeStart": format_datetime(start),
            "RangeFinish": format_datetime(end),
            "QualityLevel": new_quality,
        }
        response = self._client.session.post(url, json=body)
        response.raise_for_status()
        return response

    @ensure_auth
    def insert_data(
        self,
        time_series_id: str,
        data: pd.DataFrame,
        bulk_insert: bool = False,
        values_col: str = "Data",
        qualities_col: str = "QualityTxt",
        confidence_col: str = "Confidence",
        duration_col: str = "Duration",
        filepath_col: str = "FilePath",
    ) -> requests.Response:
        """Insert data into a time series.

        It is assumed that the dataframe has a DateTimeIndex
        and not a TimeStamp column

        Args:
            time_series_id: The time series to update.
            data: The dataframe containing the data to insert.
            bulk_insert: bool = False,
            values_col: str = "Data",
            qualities_col: str = "QualityTxt",
            confidence_col: str = "Confidence",
            duration_col: str = "Duration",
            filepath_col: str = "FilePath",

        Returns:
            Response from the API

        Raises:
            HttpError: Requests threw an exception
        """
        if not isinstance(data.index, pd.DatetimeIndex):
            raise Exception("Dataframe missing datetimeindex")
        data = self._format_dataframe(
            data,
            values_col=values_col,
            qualities_col=qualities_col,
            confidence_col=confidence_col,
            duration_col=duration_col,
            filepath_col=filepath_col,
        )
        body = self._get_insert_data_body(
            time_series_id,
            data,
            bulk_insert,
        )
        endpoint = "/TimeSeries/InsertData"
        url = self._client.api_url + endpoint
        try:
            response = self._client.session.post(url, json=body)
            response.raise_for_status()
        except requests.HTTPError as e:
            raise Exception(e.response.text)
        return response

    @ensure_auth
    def statistics(self, time_series_id: Union[str, List[str]]) -> pd.DataFrame:
        """Get statistics for a time series or a list of time series.

        Args:
            time_series_id: The time series to get statistics for.

        Returns:
            Pandas dataframe with statistics about the timeseries dataset.

        Raises:
            HttpError: Requests threw an exception
        """
        url = self._client.api_url + "/TimeSeries/Statistics"
        if isinstance(time_series_id, str):
            time_series_id = [time_series_id]
        body = {"TimeSeries": list(time_series_id), "ISO8601_Timestamp": True}
        response = self._client.session.post(url, json=body)
        response.raise_for_status()
        data = response.json()

        return json_to_pandas(json.dumps(data))

    @ensure_auth
    def list(self) -> pd.DataFrame:
        return self._client.entities("enTimeSeries").list()

    @ensure_auth
    def latest_values(
        self,
        time_series_id: Union[str, List[str]],
        before: Optional[DateTime] = None,
    ) -> List[pd.DataFrame]:
        """Get data from Datafarm.

        Args:
            time_series_id: The time series to get data from.
            before: Get values from before this timestamp.

        Returns
            List of dataframes

        Raises:
            HttpError: Requests threw an exception
        """
        if not before:
            before = datetime.datetime.now()
        before = format_datetime(before)
        if isinstance(time_series_id, str):
            time_series_id = [time_series_id]

        url = self._client.api_url + "/TimeSeries/LatestValues"
        body = {
            "TimeSeries": time_series_id,
            "ISO8601_TimeStamp": False,
            "Before": before,
        }
        response = self._client.session.post(url, json=body)
        response.raise_for_status()
        data = response.json()

        return json_to_pandas(json.dumps(data))

    @staticmethod
    def create_resample(
        *,
        method: Literal["interpolation", "repetition"],
        repetition_type: Literal["stairs", "inverted_stairs"],
        period: TAggregationPeriod = "apHour",
        period_offset: float = 0,
        user_def_period: int = 0,
        user_def_time_ref: DateTime = datetime.datetime.now(),
    ) -> TAggregation:
        """Helper function for creating a timeseries resampling object.

        Args:
            method: Choose from 2 different resampling methods.
            repetition_type: Stairs or inverted stairs.
            period: Aggregation period to use.
            period_offset: An optional offset to use for the period.
                This is ignored for period=apUserDefinedSeconds
            user_def_period: If period=apUserDefinedSeconds then this parameter is used
            user_def_time_ref: If period=apUserDefinedSeconds then this parameter is used

        Returns
            TAggregation
        """
        method = "fmInterpolation" if method == "interpolation" else "fmRepetition"
        rep_type = "rtStairs" if repetition_type == "stairs" else "rtInvertedStairs"
        resampling = TGapFill(Enabled=True, Method=method, RepetitionType=rep_type)
        agg = TAggregation(
            Method="amResample",
            MethodConstant=0,
            Period=period,
            PeriodOffset=period_offset,
            Resampling=resampling,
            UserDefPeriod=user_def_period,
            UserDefTimeRef=user_def_time_ref,
        )
        return agg

    @staticmethod
    def create_aggregation(
        *,
        method: TAggregationMethod,
        period: TAggregationPeriod,
        method_constant: float = 0,
        direction: TPeriodDirection = "pdStraight",
        period_offset: float = 0,
        user_def_period: int = 0,
        user_def_time_ref: DateTime = datetime.datetime.now(),
    ) -> TAggregation:
        """Helper function for creating a timeseries aggregation object.

        Args:
            method: Choose from 10 different aggregation methods.
            period: Aggregation period to use.
            period_offset: An optional offset to use for the period.
                This is ignored for period=apUserDefinedSeconds
            direction: How to do the aggregation.
            user_def_period: If period=apUserDefinedSeconds then this parameter is used.
            user_def_time_ref: If period=apUserDefinedSeconds then this parameter is used.

         Returns
             TAggregation
        """
        resampling = TGapFill(
            Enabled=False, Method="fmInterpolation", RepetitionType="rtStairs"
        )
        agg = TAggregation(
            Direction=direction,
            Method=method,
            MethodConstant=method_constant,
            Period=period,
            PeriodOffset=period_offset,
            Resampling=resampling,
            UserDefPeriod=user_def_period,
            UserDefTimeRef=user_def_time_ref,
        )
        return agg

    def _get_insert_data_body(
        self,
        time_series_id: str,
        data: pd.DataFrame,
        bulk_insert: bool = False,
    ) -> Dict[str, Any]:
        """Insert data into a time series.

        Args:

        time_series_id : str
            The time series to insert data into.
        data : pd.DataFrame
            The data to insert.
        bulk_insert : bool, optional
            Whether to use bulk insert.
            Defaults to False.
        """

        insert_data = self._prepare_insert_data(data)

        insert_data_dict = {col: list(insert_data[col]) for col in insert_data.columns}
        body = {
            "BulkInsert": bulk_insert,
            "TimeSeriesName": time_series_id,
            **insert_data_dict,
        }
        return body

    @staticmethod
    def _format_dataframe(
        data: pd.DataFrame,
        values_col: str = "Data",
        qualities_col: str = "QualityTxt",
        confidence_col: str = "Confidence",
        duration_col: str = "Duration",
        filepath_col: str = "FilePath",
    ):
        data.rename(
            columns={
                values_col: "Data",
                qualities_col: "QualityLevel",
                confidence_col: "Confidence",
                duration_col: "Duration",
                filepath_col: "FilePath",
            },
            inplace=True,
        )
        data["TimeStamp"] = data.index
        return data

    def _prepare_insert_data(
        self,
        data: pd.DataFrame,
    ) -> pd.DataFrame:
        """Prepare data for insertion. This includes converting the timestamp to ISO8601 format,
        converting the quality level to an integer, and checking that the data is valid.
        """
        insert_data = data.copy()

        if data.empty:
            raise ValueError("No data to insert")

        if insert_data["QualityLevel"].dtype in ("object", "string", "str"):
            logging.info("Converting quality names to quality level")
            try:
                insert_data["QualityLevel"] = insert_data["QualityLevel"].apply(
                    lambda x: self._client.quality_name_to_level[x]
                )
            except KeyError:
                raise QualityError(
                    f"Invalid quality string values. Must be in {self._client.quality_name_to_level.keys()} or an integer."
                )
        else:
            insert_data["QualityLevel"] = insert_data["QualityLevel"].astype(int)

        insert_data["Data"] = insert_data["Data"].astype(float)

        try:
            logging.info("Ensuring timestamps are in ISO8601 format")
            insert_data["TimeStamp"] = insert_data["TimeStamp"].apply(format_datetime)
        except KeyError:
            raise KeyError("No 'TimeStamp' column in data")
        except ValueError:
            raise ValueError("Invalid 'TimeStamp' column in data")

        try:
            TimeSeriesInsertSchema.validate(insert_data)
        except pa.errors.SchemaError as err:
            raise (err)
        # Convert file to base64
        if "FilePath" in insert_data.columns:
            logging.info("Converting file to base64")
            insert_data["ObjectFileName"] = insert_data["FilePath"].apply(
                lambda p: os.path.basename(p)
            )
            try:
                insert_data["ObjectBase64"] = insert_data["FilePath"].apply(
                    lambda p: base64.b64encode(open(p, "rb").read()).decode("utf-8")
                )
            except FileNotFoundError as err:
                raise FileNotFoundError(
                    f"File {err.filename} not found. Please check the path."
                )
            del insert_data["FilePath"]

        # Format floats
        for col in ("Data", "Confidence", "Duration"):
            if col in insert_data.columns:
                insert_data[col] = insert_data[col].apply(format_float)

        return insert_data

    def _delete_data_timestamps(
        self, time_series_id: str, timestamps: List[DateTime]
    ) -> requests.Response:
        """Delete data from a time series by timestamps.

        Args:
        ----------
        time_series_id : str
            The time series to delete data from.
        timestamps : list of DateTime objects
            The timestamps to delete.
        """
        endpoint = "/TimeSeries/DeleteData"
        url = self._client.api_url + endpoint
        body = {
            "TimeSeriesName": time_series_id,
            "TimeStamp": [format_datetime(ts) for ts in timestamps],
        }
        response = self._client.session.post(url, json=body)
        response.raise_for_status()
        return response

    def _delete_data_range(
        self, time_series_id: str, start: DateTime, end: DateTime
    ) -> requests.Response:
        """Delete data from a time series by range [start, end).

        Args:
        ----------
        time_series_id : str
            The time series to delete data from.
        start : DateTime
            The start of the range to delete data from.
        end : DateTime
            The end of the range to delete data from.
            Note that this is NOT inclusive.
        """
        endpoint = "/TimeSeries/DeleteDataRange"
        url = self._client.api_url + endpoint
        body = {
            "TimeSeriesName": time_series_id,
            "RangeStart": format_datetime(start),
            "RangeFinish": format_datetime(end),
        }
        response = self._client.session.post(url, json=body)
        response.raise_for_status()
        return response
